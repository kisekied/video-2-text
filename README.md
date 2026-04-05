English | [中文](README_CN.md)

# video-2-text

Convert a video into ASCII art text frames, suitable for terminal character animation playback.

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/kisekied/video-2-text.git
cd video-2-text
uv sync
```

Or install globally as a CLI command:

```bash
uv tool install git+https://github.com/kisekied/video-2-text.git
```

## Usage

```bash
uv run video2text.py input.mp4
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `input` | (required) | Path to input video file |
| `--fps` | `24` | Target frame rate |
| `--width` | `120` | Output character width |
| `--height` | — | Output character height |
| `--output` | `output.txt` | Output file name |
| `--delimiter` | `---FRAME---` | Frame delimiter string |
| `--mode` | `binary` | Rendering mode: `grayscale` (multi-level chars) or `binary` (`@` and `.` only) |

**Width/height rules:**
- Only `--width` → height scaled proportionally
- Only `--height` → width scaled proportionally
- Both specified → exact values, no aspect ratio preservation
- Neither specified → width 120, height proportional

### Examples

```bash
# Default settings
uv run video2text.py input.mp4

# Custom width and frame rate
uv run video2text.py input.mp4 --width 80 --fps 10

# Fixed width and height
uv run video2text.py input.mp4 --width 160 --height 50

# Custom output file and delimiter
uv run video2text.py input.mp4 --output frames.txt --delimiter "=FRAME="

# Grayscale mode (multi-level ASCII characters)
uv run video2text.py input.mp4 --mode grayscale
```

### Output Format

Each frame is an ASCII art block separated by the delimiter:

```
@@@...@@@
@@.....@@
...
---FRAME---
@@@...@@@
...
```

## Development

```bash
uv run pytest tests/
```
