import cv2
import numpy as np
from pathlib import Path


def create_writer(output_path: Path, fps: int, width: int, height: int):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))


def get_circle_position(frame_idx: int, total_frames: int, width: int, height: int, speed_factor: float = 1.0):
    progress = min(frame_idx * speed_factor / total_frames, 1.0)
    x = 60 + int((width - 120) * progress)
    y = height // 2 + int(60 * np.sin(frame_idx * 0.08 * speed_factor))
    return x, y


def generate_clean_video(output_path: Path, width=640, height=360, fps=30, duration_seconds=6):
    writer = create_writer(output_path, fps, width, height)
    total_frames = fps * duration_seconds

    for frame_idx in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        x, y = get_circle_position(frame_idx, total_frames, width, height)
        cv2.circle(frame, (x, y), 25, (255, 255, 255), -1)

        writer.write(frame)

    writer.release()
    print(f"Saved: {output_path}")


def generate_noisy_video(output_path: Path, width=640, height=360, fps=30, duration_seconds=6):
    writer = create_writer(output_path, fps, width, height)
    total_frames = fps * duration_seconds

    for frame_idx in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        x, y = get_circle_position(frame_idx, total_frames, width, height)
        cv2.circle(frame, (x, y), 25, (255, 255, 255), -1)

        noise = np.random.normal(0, 25, frame.shape).astype(np.int16)
        noisy_frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        writer.write(noisy_frame)

    writer.release()
    print(f"Saved: {output_path}")


def generate_light_change_video(output_path: Path, width=640, height=360, fps=30, duration_seconds=6):
    writer = create_writer(output_path, fps, width, height)
    total_frames = fps * duration_seconds

    for frame_idx in range(total_frames):
        # Brightness always between 20 and 100
        brightness = int(60 + 40 * np.sin(frame_idx * 0.06))
        brightness = np.clip(brightness, 0, 255)

        frame = np.full((height, width, 3), brightness, dtype=np.uint8)

        # Moving shadow
        shadow_x = int((width + 100) * frame_idx / total_frames) - 100
        cv2.rectangle(frame, (shadow_x, 0), (shadow_x + 120, height), (10, 10, 10), -1)

        x, y = get_circle_position(frame_idx, total_frames, width, height)
        cv2.circle(frame, (x, y), 25, (255, 255, 255), -1)

        writer.write(frame)

    writer.release()
    print(f"Saved: {output_path}")


def generate_fast_motion_video(output_path: Path, width=640, height=360, fps=30, duration_seconds=6):
    writer = create_writer(output_path, fps, width, height)
    total_frames = fps * duration_seconds

    for frame_idx in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        x, y = get_circle_position(frame_idx, total_frames, width, height, speed_factor=2.0)

        # When progress reaches the end, keep it inside the frame
        x = min(x, width - 40)

        cv2.circle(frame, (x, y), 25, (255, 255, 255), -1)

        writer.write(frame)

    writer.release()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    output_dir = Path("data/synthetic_videos")

    generate_clean_video(output_dir / "synthetic_clean_circle.mp4")
    generate_noisy_video(output_dir / "synthetic_noisy_circle.mp4")
    generate_light_change_video(output_dir / "synthetic_light_circle.mp4")
    generate_fast_motion_video(output_dir / "synthetic_fast_circle.mp4")