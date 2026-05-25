import cv2
import numpy as np
from pathlib import Path


OUTPUT_DIR = Path("data/synthetic_videos")


def delete_previous_synthetic_videos(output_dir: Path) -> None:
    """
    Delete previous synthetic videos before generating the new dataset.
    Only .mp4 files inside data/synthetic_videos are removed.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for video_file in output_dir.glob("*.mp4"):
        video_file.unlink()
        print(f"Deleted previous video: {video_file}")


def create_writer(output_path: Path, fps: int, width: int, height: int):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))


def create_background(width: int, height: int, object_id: int) -> np.ndarray:
    """
    Object 1: dark background.
    Object 2: blue background.
    """
    if object_id == 1:
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Subtle floor/reference lines
        for y in range(60, height, 60):
            cv2.line(frame, (0, y), (width, y), (25, 25, 25), 1)

        return frame

    if object_id == 2:
        # Blue background
        frame = np.full((height, width, 3), (120, 70, 20), dtype=np.uint8)

        # Slight grid to make the background different but stable
        for x in range(0, width, 50):
            cv2.line(frame, (x, 0), (x, height), (140, 90, 35), 1)
        for y in range(0, height, 50):
            cv2.line(frame, (0, y), (width, y), (140, 90, 35), 1)

        return frame

    return np.zeros((height, width, 3), dtype=np.uint8)


def draw_moving_object(frame: np.ndarray, center: tuple[int, int], object_id: int) -> None:
    x, y = center

    if object_id == 1:
        # White circle with internal black details
        radius = 26

        cv2.circle(frame, (x, y), radius, (255, 255, 255), -1)
        cv2.circle(frame, (x, y), radius, (0, 0, 0), 2)

        # Internal texture for Lucas-Kanade
        cv2.line(frame, (x - radius, y), (x + radius, y), (0, 0, 0), 2)
        cv2.line(frame, (x, y - radius), (x, y + radius), (0, 0, 0), 2)
        cv2.circle(frame, (x, y), 6, (0, 0, 0), -1)

    elif object_id == 2:
        # White square with black pattern
        size = 28

        cv2.rectangle(
            frame,
            (x - size, y - size),
            (x + size, y + size),
            (255, 255, 255),
            -1,
        )

        cv2.rectangle(
            frame,
            (x - size, y - size),
            (x + size, y + size),
            (0, 0, 0),
            2,
        )

        # Internal texture for Lucas-Kanade
        cv2.line(frame, (x - size, y - size), (x + size, y + size), (0, 0, 0), 2)
        cv2.line(frame, (x + size, y - size), (x - size, y + size), (0, 0, 0), 2)

        cv2.putText(
            frame,
            "A",
            (x - 10, y + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 0),
            2,
        )


def get_position(
    frame_idx: int,
    total_frames: int,
    width: int,
    height: int,
    object_id: int,
    speed_factor: float = 1.0,
) -> tuple[int, int]:
    """
    Object 1: circle moving in zigzag.
    Object 2: square moving on blue background with a different trajectory.
    """
    progress = min(frame_idx * speed_factor / max(total_frames - 1, 1), 1.0)

    if object_id == 1:
        # Circle: left to right with zigzag movement
        x = 60 + int((width - 120) * progress)
        y = height // 2 + int(70 * np.sin(frame_idx * 0.13 * speed_factor))

    else:
        # Square: right to left with smoother vertical oscillation
        x = width - 60 - int((width - 120) * progress)
        y = height // 2 + int(45 * np.cos(frame_idx * 0.10 * speed_factor))

    x = max(45, min(x, width - 45))
    y = max(45, min(y, height - 45))

    return x, y


def apply_global_light_change(frame: np.ndarray, frame_idx: int, total_frames: int) -> np.ndarray:
    """
    Simulates switching the light off and on again.
    This is a global brightness change, without artificial stripes or spotlights.
    """
    t = frame_idx / max(total_frames - 1, 1)

    if t < 0.30:
        factor = 1.00
    elif t < 0.45:
        alpha = (t - 0.30) / 0.15
        factor = 1.00 * (1 - alpha) + 0.45 * alpha
    elif t < 0.65:
        factor = 0.45
    elif t < 0.80:
        alpha = (t - 0.65) / 0.15
        factor = 0.45 * (1 - alpha) + 1.35 * alpha
    else:
        factor = 1.35

    output = frame.astype(np.float32) * factor
    return np.clip(output, 0, 255).astype(np.uint8)


def generate_video(
    output_path: Path,
    object_id: int,
    scenario: str,
    width: int = 640,
    height: int = 360,
    fps: int = 30,
    duration_seconds: int = 6,
) -> None:
    writer = create_writer(output_path, fps, width, height)
    total_frames = fps * duration_seconds

    rng = np.random.default_rng(seed=object_id * 100)

    if scenario == "fast":
        speed_factor = 1.8
    else:
        speed_factor = 1.0

    for frame_idx in range(total_frames):
        frame = create_background(width, height, object_id)

        x, y = get_position(
            frame_idx=frame_idx,
            total_frames=total_frames,
            width=width,
            height=height,
            object_id=object_id,
            speed_factor=speed_factor,
        )

        draw_moving_object(frame, (x, y), object_id)

        if scenario == "light_change":
            frame = apply_global_light_change(frame, frame_idx, total_frames)

        if scenario == "noisy":
            noise_sigma = 25 if object_id == 1 else 30
            noise = rng.normal(0, noise_sigma, frame.shape).astype(np.int16)
            frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        writer.write(frame)

    writer.release()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    delete_previous_synthetic_videos(OUTPUT_DIR)

    # Object 1: circle on dark background
    generate_video(
        output_path=OUTPUT_DIR / "synthetic_clean_1.mp4",
        object_id=1,
        scenario="clean",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_noisy_1.mp4",
        object_id=1,
        scenario="noisy",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_light_change_1.mp4",
        object_id=1,
        scenario="light_change",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_fast_1.mp4",
        object_id=1,
        scenario="fast",
    )

    # Object 2: square on blue background
    generate_video(
        output_path=OUTPUT_DIR / "synthetic_clean_2.mp4",
        object_id=2,
        scenario="clean",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_noisy_2.mp4",
        object_id=2,
        scenario="noisy",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_light_change_2.mp4",
        object_id=2,
        scenario="light_change",
    )

    generate_video(
        output_path=OUTPUT_DIR / "synthetic_fast_2.mp4",
        object_id=2,
        scenario="fast",
    )