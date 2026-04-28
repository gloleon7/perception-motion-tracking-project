import cv2
import numpy as np
from pathlib import Path


def generate_synthetic_video(
    output_path: str,
    width: int = 640,
    height: int = 360,
    fps: int = 30,
    duration_seconds: int = 6,
) -> None:
    """
    Generate a simple synthetic video with a moving circle.
    This video will be used to test the motion detection pipeline.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    total_frames = fps * duration_seconds

    for frame_idx in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Moving circle position
        x = 60 + int((width - 120) * frame_idx / total_frames)
        y = height // 2 + int(60 * np.sin(frame_idx * 0.08))

        cv2.circle(frame, (x, y), 25, (255, 255, 255), -1)

        writer.write(frame)

    writer.release()
    print(f"Synthetic video saved at: {output_path}")


if __name__ == "__main__":
    generate_synthetic_video(
        output_path="data/synthetic_videos/synthetic_circle.mp4"
    )