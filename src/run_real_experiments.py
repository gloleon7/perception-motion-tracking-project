import cv2
import numpy as np
import pandas as pd
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_DIR / "data" / "input_videos"
OUTPUT_VIDEO_DIR = PROJECT_DIR / "outputs" / "processed_videos" / "real"
OUTPUT_PLOTS_DIR = PROJECT_DIR / "outputs" / "plots" / "real"

OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PLOTS_DIR.mkdir(parents=True, exist_ok=True)


TARGET_LONG_SIDE = 1280


def resize_frame(frame: np.ndarray, target_long_side: int | None = TARGET_LONG_SIDE) -> np.ndarray:
    """
    Resize a frame keeping the aspect ratio.

    This is useful because some real videos may be 4K or vertical.
    Using a common long side makes processing faster and outputs easier to compare.
    """

    if target_long_side is None:
        return frame

    height, width = frame.shape[:2]
    current_long_side = max(width, height)

    if current_long_side == target_long_side:
        return frame

    scale = target_long_side / current_long_side
    new_width = int(round(width * scale))
    new_height = int(round(height * scale))

    
    if new_width % 2 != 0:
        new_width -= 1

    if new_height % 2 != 0:
        new_height -= 1

    new_width = max(new_width, 2)
    new_height = max(new_height, 2)

    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)


def get_valid_fps(cap: cv2.VideoCapture, default_fps: float = 25.0) -> float:
    """
    Get FPS from a video. If the value is invalid, return a default value.
    """

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps is None or fps <= 0 or np.isnan(fps):
        return default_fps

    return fps


def clear_previous_outputs() -> None:
    """
    Delete previous real video outputs before running the experiments again.
    This avoids mixing old CSV files, plots or processed videos with new results.
    """

    for file in OUTPUT_VIDEO_DIR.glob("*.mp4"):
        file.unlink()

    for file in OUTPUT_PLOTS_DIR.glob("*.csv"):
        file.unlink()

    for file in OUTPUT_PLOTS_DIR.glob("*.png"):
        file.unlink()



VIDEO_IDS = [1, 2, 3, 4]

CONDITIONS = [
    "normal",
    "noisy",
    "light_change",
    "fast",
]

SCENARIOS = {
    f"real_{condition}_{video_id}": INPUT_DIR / f"real_{condition}_{video_id}.mp4"
    for condition in CONDITIONS
    for video_id in VIDEO_IDS
}


def track_with_frame_difference(
    input_video_path: Path,
    output_video_path: Path,
    threshold_value: int = 25,
    min_area: int = 800,
    kernel_size: int = 7,
) -> pd.DataFrame:
    cap = cv2.VideoCapture(str(input_video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {input_video_path}")

    fps = get_valid_fps(cap)

    ret, previous_frame = cap.read()

    if not ret:
        raise RuntimeError(f"Could not read first frame: {input_video_path}")

    previous_frame = resize_frame(previous_frame)
    height, width = previous_frame.shape[:2]

    writer = cv2.VideoWriter(
        str(output_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.GaussianBlur(previous_gray, (5, 5), 0)

    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    trajectory = []
    frame_index = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = resize_frame(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        frame_difference = cv2.absdiff(previous_gray, gray)

        _, motion_mask = cv2.threshold(
            frame_difference,
            threshold_value,
            255,
            cv2.THRESH_BINARY,
        )

        motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel)
        motion_mask = cv2.dilate(motion_mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            motion_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        detected = False
        cx, cy, area = None, None, 0

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            if area > min_area:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cx = x + w // 2
                cy = y + h // 2
                detected = True

                trajectory.append({
                    "frame": frame_index,
                    "x": cx,
                    "y": cy,
                    "area": area,
                })

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1,
                )

        status_text = "Detected" if detected else "Not detected"

        cv2.putText(
            frame,
            f"Frame: {frame_index} | Motion: {status_text}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        if detected:
            cv2.putText(
                frame,
                f"Centroid: ({cx}, {cy})",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

        writer.write(frame)

        previous_gray = gray.copy()
        frame_index += 1

    cap.release()
    writer.release()

    df = pd.DataFrame(trajectory)

    if not df.empty:
        df = df.sort_values("frame").reset_index(drop=True)
        df["dx"] = df["x"].diff()
        df["dy"] = df["y"].diff()
        df["displacement"] = np.sqrt(df["dx"] ** 2 + df["dy"] ** 2)

    return df


def track_with_lucas_kanade(
    input_video_path: Path,
    output_video_path: Path,
) -> pd.DataFrame:
    cap = cv2.VideoCapture(str(input_video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {input_video_path}")

    fps = get_valid_fps(cap)

    ret, old_frame = cap.read()

    if not ret:
        raise RuntimeError(f"Could not read first frame: {input_video_path}")

    old_frame = resize_frame(old_frame)
    height, width = old_frame.shape[:2]

    writer = cv2.VideoWriter(
        str(output_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    feature_params = dict(
        maxCorners=50,
        qualityLevel=0.05,
        minDistance=15,
        blockSize=7,
    )

    lk_params = dict(
        winSize=(21, 21),
        maxLevel=3,
        criteria=(
            cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
            20,
            0.03,
        ),
    )

    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    tracked_data = []
    frame_index = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = resize_frame(frame)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        output_frame = frame.copy()

        if p0 is None or len(p0) < 5:
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=None, **feature_params)

            cv2.putText(
                output_frame,
                f"Frame: {frame_index} | LK points: 0",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                output_frame,
                "Re-detecting feature points",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            writer.write(output_frame)

            old_gray = frame_gray.copy()
            frame_index += 1
            continue

        p1, status, error = cv2.calcOpticalFlowPyrLK(
            old_gray,
            frame_gray,
            p0,
            None,
            **lk_params,
        )

        if p1 is None or status is None:
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=None, **feature_params)

            cv2.putText(
                output_frame,
                f"Frame: {frame_index} | LK points: 0",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                output_frame,
                "Optical flow lost - reinitializing",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            writer.write(output_frame)

            old_gray = frame_gray.copy()
            frame_index += 1
            continue

        good_new = p1[status == 1]
        good_old = p0[status == 1]

        displacements = []

        for new_point, old_point in zip(good_new, good_old):
            x_new, y_new = new_point.ravel()
            x_old, y_old = old_point.ravel()

            dx = x_new - x_old
            dy = y_new - y_old
            displacement = np.sqrt(dx**2 + dy**2)

            displacements.append(displacement)

            tracked_data.append({
                "frame": frame_index,
                "x_old": x_old,
                "y_old": y_old,
                "x_new": x_new,
                "y_new": y_new,
                "dx": dx,
                "dy": dy,
                "displacement": displacement,
            })

            x_new_i, y_new_i = int(x_new), int(y_new)
            x_old_i, y_old_i = int(x_old), int(y_old)

            cv2.line(
                output_frame,
                (x_old_i, y_old_i),
                (x_new_i, y_new_i),
                (255, 0, 0),
                2,
            )

            cv2.circle(
                output_frame,
                (x_new_i, y_new_i),
                4,
                (0, 0, 255),
                -1,
            )

        mean_displacement = np.mean(displacements) if len(displacements) > 0 else 0

        cv2.putText(
            output_frame,
            f"Frame: {frame_index} | LK points: {len(good_new)}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            output_frame,
            f"Mean displacement: {mean_displacement:.2f} px/frame",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        writer.write(output_frame)

        old_gray = frame_gray.copy()

        if len(good_new) < 5:
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
        else:
            p0 = good_new.reshape(-1, 1, 2)

        frame_index += 1

    cap.release()
    writer.release()

    return pd.DataFrame(tracked_data)


def summarize_frame_difference(df: pd.DataFrame, scenario_name: str) -> dict:
    if df.empty or "displacement" not in df.columns:
        return {
            "scenario": scenario_name,
            "method": "frame_difference",
            "detections": 0,
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_area": 0,
            "mean_points_per_frame": np.nan,
        }

    displacement = df["displacement"].dropna()

    if displacement.empty:
        return {
            "scenario": scenario_name,
            "method": "frame_difference",
            "detections": len(df),
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_area": df["area"].mean() if "area" in df.columns else 0,
            "mean_points_per_frame": np.nan,
        }

    return {
        "scenario": scenario_name,
        "method": "frame_difference",
        "detections": len(df),
        "mean_displacement": displacement.mean(),
        "median_displacement": displacement.median(),
        "p95_displacement": displacement.quantile(0.95),
        "max_displacement": displacement.max(),
        "mean_area": df["area"].mean() if "area" in df.columns else 0,
        "mean_points_per_frame": np.nan,
    }


def summarize_lucas_kanade(df: pd.DataFrame, scenario_name: str) -> dict:
    if df.empty or "displacement" not in df.columns:
        return {
            "scenario": scenario_name,
            "method": "lucas_kanade",
            "detections": 0,
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_area": np.nan,
            "mean_points_per_frame": 0,
        }

    displacement = df["displacement"].dropna()

    if displacement.empty:
        return {
            "scenario": scenario_name,
            "method": "lucas_kanade",
            "detections": 0,
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_area": np.nan,
            "mean_points_per_frame": 0,
        }

    points_per_frame = df.groupby("frame")["displacement"].count()

    return {
        "scenario": scenario_name,
        "method": "lucas_kanade",
        "detections": df["frame"].nunique(),
        "mean_displacement": displacement.mean(),
        "median_displacement": displacement.median(),
        "p95_displacement": displacement.quantile(0.95),
        "max_displacement": displacement.max(),
        "mean_area": np.nan,
        "mean_points_per_frame": points_per_frame.mean(),
    }


def main():
    clear_previous_outputs()
    all_summaries = []

    print("Real scenarios to process:")
    for scenario_name in SCENARIOS:
        print(f"- {scenario_name}")

    for scenario_name, video_path in SCENARIOS.items():
        print(f"\nProcessing scenario: {scenario_name}")
        print(f"Input video: {video_path}")

        if not video_path.exists():
            print(f"Skipping. Video not found: {video_path}")
            continue

        frame_diff_video = OUTPUT_VIDEO_DIR / f"frame_difference_{scenario_name}.mp4"
        lk_video = OUTPUT_VIDEO_DIR / f"lucas_kanade_{scenario_name}.mp4"

        frame_diff_csv = OUTPUT_PLOTS_DIR / f"frame_difference_{scenario_name}.csv"
        lk_csv = OUTPUT_PLOTS_DIR / f"lucas_kanade_{scenario_name}.csv"

        frame_df = track_with_frame_difference(
            input_video_path=video_path,
            output_video_path=frame_diff_video,
            threshold_value=25,
            min_area=800,
            kernel_size=7,
        )

        lk_df = track_with_lucas_kanade(
            input_video_path=video_path,
            output_video_path=lk_video,
        )

        frame_columns = ["frame", "x", "y", "area", "dx", "dy", "displacement"]
        lk_columns = ["frame", "x_old", "y_old", "x_new", "y_new", "dx", "dy", "displacement"]

        if frame_df.empty:
            frame_df = pd.DataFrame(columns=frame_columns)

        if lk_df.empty:
            lk_df = pd.DataFrame(columns=lk_columns)

        frame_df.to_csv(frame_diff_csv, index=False)
        lk_df.to_csv(lk_csv, index=False)

        all_summaries.append(summarize_frame_difference(frame_df, scenario_name))
        all_summaries.append(summarize_lucas_kanade(lk_df, scenario_name))

        print(f"Saved frame difference video: {frame_diff_video}")
        print(f"Saved Lucas-Kanade video: {lk_video}")
        print(f"Saved frame difference CSV: {frame_diff_csv}")
        print(f"Saved Lucas-Kanade CSV: {lk_csv}")

    summary_df = pd.DataFrame(all_summaries)

    summary_columns = [
        "scenario",
        "method",
        "detections",
        "mean_displacement",
        "median_displacement",
        "p95_displacement",
        "max_displacement",
        "mean_area",
        "mean_points_per_frame",
    ]

    if summary_df.empty:
        summary_df = pd.DataFrame(columns=summary_columns)
    else:
        summary_df = summary_df[summary_columns]

    summary_path = OUTPUT_PLOTS_DIR / "real_experiments_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print("\nFinal summary:")
    print(summary_df)
    print(f"\nSummary saved at: {summary_path}")


if __name__ == "__main__":
    main()