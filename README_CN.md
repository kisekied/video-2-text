[English](README.md) | 中文

# video-2-text

将视频转换为 ASCII 字符画文本文件，可用于终端字符动画播放。

## 安装

需要 [uv](https://docs.astral.sh/uv/)。

```bash
git clone https://github.com/kisekied/video-2-text.git
cd video-2-text
uv sync
```

或者全局安装为 CLI 命令：

```bash
uv tool install git+https://github.com/kisekied/video-2-text.git
```

## 使用

```bash
uv run video2text.py input.mp4
```

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | (必填) | 视频文件路径 |
| `--fps` | `24` | 截取帧率 |
| `--width` | `120` | 输出字符宽度 |
| `--height` | — | 输出字符高度 |
| `--output` | `output.txt` | 输出文件名 |
| `--delimiter` | `---FRAME---` | 帧分隔符 |
| `--mode` | `binary` | 渲染模式：`grayscale`（多级字符）或 `binary`（仅 `@` 和 `.`）|

**宽高规则：**
- 只指定 `--width` → 高度按视频比例等比缩放
- 只指定 `--height` → 宽度按视频比例等比缩放
- 两者都指定 → 按指定值，不等比缩放
- 都不指定 → 宽度 120，高度等比缩放

### 示例

```bash
# 默认参数
uv run video2text.py input.mp4

# 指定宽度和帧率
uv run video2text.py input.mp4 --width 80 --fps 10

# 固定宽高
uv run video2text.py input.mp4 --width 160 --height 50

# 自定义输出和分隔符
uv run video2text.py input.mp4 --output frames.txt --delimiter "=FRAME="

# 黑白模式（仅 @ 和 .）
uv run video2text.py input.mp4 --mode binary
```

### 输出格式

每帧为一段 ASCII 字符画，帧之间用分隔符隔开：

```
@@@%%%###
@@%%##**+
...
---FRAME---
@@@%%%###
...
```

## 开发

```bash
uv run pytest tests/
```
