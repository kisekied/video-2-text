import argparse
import sys
import cv2
import numpy as np
from tqdm import tqdm

ASCII_CHARS = "@%#*+=-:. "
BW_CHARS = "@."


def pixel_to_char(gray_value: int, chars: str = ASCII_CHARS) -> str:
    index = round(gray_value * (len(chars) - 1) / 255)
    return chars[index]


def calculate_dimensions(
    video_width: int,
    video_height: int,
    target_width: int | None,
    target_height: int | None,
) -> tuple[int, int]:
    # Character cells are roughly twice as tall as wide, so divide height by 2
    CHAR_ASPECT = 2.0
    video_ratio = video_height / video_width

    if target_width is not None and target_height is not None:
        return target_width, target_height

    if target_width is not None:
        h = max(1, round(target_width * video_ratio / CHAR_ASPECT))
        return target_width, h

    if target_height is not None:
        w = max(1, round(target_height * CHAR_ASPECT / video_ratio))
        return w, target_height

    # Default: width 120, height proportional
    default_width = 120
    h = max(1, round(default_width * video_ratio / CHAR_ASPECT))
    return default_width, h


def frame_to_ascii(
    frame: np.ndarray, width: int, height: int, chars: str = ASCII_CHARS
) -> str:
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    rows = []
    for row in gray:
        rows.append("".join(pixel_to_char(int(px), chars) for px in row))
    return "\n".join(rows)


def video_to_text(
    path: str,
    fps: float,
    target_width: int | None,
    target_height: int | None,
    output: str,
    delimiter: str,
    mode: str = "binary",
) -> None:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: cannot open video file '{path}'", file=sys.stderr)
        sys.exit(1)

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    char_width, char_height = calculate_dimensions(
        video_width, video_height, target_width, target_height
    )

    chars = BW_CHARS if mode == "binary" else ASCII_CHARS
    frame_interval = original_fps / fps if fps < original_fps else 1.0
    expected_output_frames = max(1, round(total_frames / frame_interval))

    print(
        f"Video: {video_width}x{video_height} @ {original_fps:.1f}fps  |  "
        f"Output: {char_width}x{char_height} chars @ {fps}fps  |  "
        f"~{expected_output_frames} frames"
    )

    ascii_frames = []
    current_frame_idx = 0
    next_capture = 0.0

    with tqdm(total=expected_output_frames, unit="frame") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if current_frame_idx >= round(next_capture):
                ascii_frames.append(frame_to_ascii(frame, char_width, char_height, chars))
                next_capture += frame_interval
                pbar.update(1)

            current_frame_idx += 1

    cap.release()

    with open(output, "w", encoding="utf-8") as f:
        f.write(f"\n{delimiter}\n".join(ascii_frames))
        f.write("\n")

    print(f"Written {len(ascii_frames)} frames to '{output}'")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a video to ASCII text art frames."
    )
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument(
        "--fps", type=float, default=24.0, help="Target frame rate (default: 24)"
    )
    parser.add_argument(
        "--width", type=int, default=None, help="Output character width"
    )
    parser.add_argument(
        "--height", type=int, default=None, help="Output character height"
    )
    parser.add_argument(
        "--output", default="output.txt", help="Output file name (default: output.txt)"
    )
    parser.add_argument(
        "--delimiter",
        default="---FRAME---",
        help="Frame delimiter string (default: ---FRAME---)",
    )
    parser.add_argument(
        "--mode",
        choices=["grayscale", "binary"],
        default="binary",
        help="Rendering mode: grayscale uses ASCII_CHARS, binary uses @ and . only (default: binary)",
    )
    args = parser.parse_args()

    video_to_text(
        path=args.input,
        fps=args.fps,
        target_width=args.width,
        target_height=args.height,
        output=args.output,
        delimiter=args.delimiter,
        mode=args.mode,
    )


if __name__ == "__main__":
    main()
