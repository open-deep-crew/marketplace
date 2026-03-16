---
name: nano-banana-pro
description: 使用谷歌的 Nano Banana Pro（Gemini 3 Pro 图片）API 生成和编辑图片。当用户请求生成、创建、编辑、修改、修改、修改或更新图像时使用。当用户引用已有的图片文件并请求以任何方式修改时，也要使用（例如，“修改此图像”、“更改背景”、“用 Y 替换 X”）。支持文本生成和图像对图像编辑，分辨率可配置（默认 1K，高分辨率为 2K 或 4K）。千万不要先读图片文件——直接用这个技能配合 --input-image 参数。
---

# Nano Banana Pro 图像生成与编辑

使用谷歌的 Nano Banana Pro API（Gemini 3 Pro 图片）生成新图片或编辑现有图片。

## Usage

**生成新图像:**
```bash
uv run <skill-path>/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**编辑现有图片:**
```bash
uv run <skill-path>/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**重要提示:** 始终从用户当前的工作目录运行，这样图片保存在用户正在工作的地方，而不是技能目录。

## 分辨率选项

Gemini 3 Pro 图像 API 支持三种分辨率（需要大写 K）：


- **1K** (默认) - ~1024px 分辨率
- **2K** - ~2048px 分辨率
- **4K** - ~4096px 分辨率

将用户请求映射到 API 参数：
- 没有提到 1K→分辨率
- “低分辨率”、“1080”、“1080p”、“1K”→1K
- “2K”、“2048”、“普通”、“中分辨率”→2K
- “高分辨率”、“高分辨率”、“高分辨率”、“4K”、“超高分辨率”→4K

## API 密钥

脚本按以下顺序检查 API 密钥：
1. `--api-key` 参数（在聊天中使用用户提供密钥）
2. `GEMINI_API_KEY` 环境变量

如果两者都不可用，脚本会以错误信息退出。

## 文件名生成

生成带有模式的文件名: `yyyy-mm-dd-hh-mm-ss-name.png`

**形式:** `{timestamp}-{descriptive-name}.png`
- 时间戳：当前日期/时间，格式 `yyyy-mm-dd-hh-mm-ss` (24 小时格式)
- 名称：带连字符的描述性小写文本
- 描述部分保持简洁（通常1-5个单词）
- 利用用户提示或对话中的上下文
- 如果不清楚，使用随机标识符（例如 x9k2，a7b3）

示例:
- 提示词“宁静的日本庭园” → `2025-11-23-14-23-05-japanese-garden.png`
- 提示词“山上的日落” → `2025-11-23-15-30-12-sunset-mountains.png`
- 提示词“创建一个机器人图像” → `2025-11-23-16-45-33-robot.png`
- 背景不明 → `2025-11-23-17-12-48-x9k2.png`

## 图像编辑

当用户想要修改已有的图片时：
1. 检查他们是否提供图片路径或当前目录中的图片引用。
2. 使用与图像路径相符的 `--input-image` 参数
3. 提示应包含编辑指令（例如，“让天空更具戏剧性”，“移除人物”，“切换为卡通风格”）
4. 常见的编辑任务：添加/移除元素、更改样式、调整颜色、模糊背景等。

## 及时处理

**关于生成:** 直接把用户的图片描述直接传递给 `--prompt`. 只有在明显不够时才重做.

**编辑方面:** 在 `--prompt` 词中传递编辑指令（例如，“在天空中添加彩虹”、“让它看起来像水彩画”）

在这两种情况下都要保留用户的创作意图。


## 输出

- 将 PNG 保存到当前目录（或如果文件名包含目录，则指定路径）
- 脚本输出生成图像的完整路径
- **不要回读图片** ——只需告知用户已保存的路径

## 示例

**生成新图像：**
```bash
uv run <skill-path>/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**编辑现有图片：**
```bash
uv run <skill-path>/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```
