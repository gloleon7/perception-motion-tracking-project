import cv2
import numpy as np
import pandas as pd
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_DIR / "data" / "synthetic_videos"
OUTPUT_VIDEO_DIR = PROJECT_DIR / "outputs" / "processed_videos" / "synthetic"
OUTPUT_PLOTS_DIR = PROJECT_DIR / "outputs" / "plots" / "synthetic"

OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PLOTS_DIR.mkdir(parents=True, exist_ok=True)


SCENARIOS = {
    "clean": INPUT_DIR / "synthetic_clean_circle.mp4",
    "noisy": INPUT_DIR / "synthetic_noisy_circle.mp4",
    "light_change": INPUT_DIR / "synthetic_light_circle.mp4",
    "fast_motion": INPUT_DIR / "synthetic_fast_circle.mp4",
}


def track_with_frame_difference(
    input_video_path: Path,
    output_video_path: Path,
    threshold_value: int = 25,
    min_area: int = 300,
    kernel_size: int = 5,
) -> pd.DataFrame:
    cap = cv2.VideoCapture(str(input_video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {input_video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        str(output_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    ret, previous_frame = cap.read()

    if not ret:
        raise RuntimeError(f"Could not read first frame: {input_video_path}")

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.GaussianBlur(previous_gray, (5, 5), 0)

    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    trajectory = []
    frame_index = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

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

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        trajectory_points = [(point["x"], point["y"]) for point in trajectory]

        for i in range(1, len(trajectory_points)):
            cv2.line(
                frame,
                trajectory_points[i - 1],
                trajectory_points[i],
                (255, 0, 0),
                2,
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

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        str(output_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    ret, old_frame = cap.read()

    if not ret:
        raise RuntimeError(f"Could not read first frame: {input_video_path}")

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

    if p0 is None:
        raise RuntimeError(f"No feature points found in: {input_video_path}")

    tracked_data = []
    frame_index = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        p1, status, error = cv2.calcOpticalFlowPyrLK(
            old_gray,
            frame_gray,
            p0,
            None,
            **lk_params,
        )

        if p1 is None or status is None:
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
            old_gray = frame_gray.copy()

            if p0 is None:
                break

            continue

        good_new = p1[status == 1]
        good_old = p0[status == 1]

        displacements = []

        output_frame = frame.copy()

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

            # Draw only the current optical flow vector.
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

            if p0 is None:
                break
        else:
            p0 = good_new.reshape(-1, 1, 2)

        frame_index += 1

    cap.release()
    writer.release()

    return pd.DataFrame(tracked_data)

def summarize_frame_difference(df: pd.DataFrame, scenario_name: str) -> dict:
    if df.empty:
        return {
            "scenario": scenario_name,
            "method": "frame_difference",
            "detections": 0,
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_area": 0,
        }

    displacement = df["displacement"].dropna()

    return {
        "scenario": scenario_name,
        "method": "frame_difference",
        "detections": len(df),
        "mean_displacement": displacement.mean(),
        "median_displacement": displacement.median(),
        "p95_displacement": displacement.quantile(0.95),
        "max_displacement": displacement.max(),
        "mean_area": df["area"].mean(),
    }

def summarize_lucas_kanade(df: pd.DataFrame, scenario_name: str) -> dict:
    if df.empty:
        return {
            "scenario": scenario_name,
            "method": "lucas_kanade",
            "detections": 0,
            "mean_displacement": 0,
            "median_displacement": 0,
            "p95_displacement": 0,
            "max_displacement": 0,
            "mean_points_per_frame": 0,
        }

    displacement = df["displacement"].dropna()
    points_per_frame = df.groupby("frame")["displacement"].count()

    return {
        "scenario": scenario_name,
        "method": "lucas_kanade",
        "detections": df["frame"].nunique(),
        "mean_displacement": displacement.mean(),
        "median_displacement": displacement.median(),
        "p95_displacement": displacement.quantile(0.95),
        "max_displacement": displacement.max(),
        "mean_points_per_frame": points_per_frame.mean(),
    }

def main():
    all_summaries = []

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
        )

        lk_df = track_with_lucas_kanade(
            input_video_path=video_path,
            output_video_path=lk_video,
        )

        frame_df.to_csv(frame_diff_csv, index=False)
        lk_df.to_csv(lk_csv, index=False)

        all_summaries.append(summarize_frame_difference(frame_df, scenario_name))
        all_summaries.append(summarize_lucas_kanade(lk_df, scenario_name))

        print(f"Saved frame difference video: {frame_diff_video}")
        print(f"Saved Lucas-Kanade video: {lk_video}")

    summary_df = pd.DataFrame(all_summaries)
    summary_path = OUTPUT_PLOTS_DIR / "synthetic_experiments_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print("\nFinal summary:")
    print(summary_df)
    print(f"\nSummary saved at: {summary_path}")


if __name__ == "__main__":
    main()