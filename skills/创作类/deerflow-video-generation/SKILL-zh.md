---
name: video-generation
description: 当用户请求生成、创建或想象视频时使用此技能。支持结构化提示词和参考图像以进行引导式生成。
---

# 视频生成技能

## 概述

此技能使用结构化提示词和 Python 脚本生成高质量视频。工作流程包括创建 JSON 格式的提示词，并通过可选的参考图像执行视频生成。

## 核心能力

- 为 AIGC 视频生成创建结构化 JSON 提示词
- 支持参考图像作为引导或视频的第一帧/最后一帧
- 通过自动化 Python 脚本执行生成视频

## 工作流程

### 步骤 1：理解需求

当用户请求生成视频时，识别以下信息：

- 主题/内容：图像中应该包含什么
- 风格偏好：艺术风格、氛围、色彩方案
- 技术规格：宽高比、构图、光照
- 参考图像：任何用于引导生成的图像
- 你不需要检查 `/mnt/user-data` 下的文件夹

### 步骤 2：创建结构化提示词

在 `/mnt/user-data/workspace/` 中生成结构化 JSON 文件，命名格式为：`{描述性名称}.json`

### 步骤 3：创建参考图像（当 image-generation 技能可用时为可选项）

为视频生成创建参考图像。

- 如果只提供了 1 张图像，将其用作视频的引导帧

### 步骤 3：执行生成

调用 Python 脚本：
```bash
python /mnt/skills/public/video-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/prompt-file.json \
  --reference-images /path/to/ref1.jpg \
  --output-file /mnt/user-data/outputs/generated-video.mp4 \
  --aspect-ratio 16:9
```

参数说明：

- `--prompt-file`：JSON 提示词文件的绝对路径（必需）
- `--reference-images`：参考图像的绝对路径（可选）
- `--output-file`：输出图像文件的绝对路径（必需）
- `--aspect-ratio`：生成图像的宽高比（可选，默认：16:9）

[!NOTE]
不要读取 python 文件，直接使用参数调用它。

## 视频生成示例

用户请求："生成一个描述《纳尼亚传奇：狮子、女巫和魔衣橱》开场场景的短视频片段"

步骤 1：在网上搜索《纳尼亚传奇：狮子、女巫和魔衣橱》的开场场景

步骤 2：创建包含以下内容的 JSON 提示词文件：

```json
{
  "title": "The Chronicles of Narnia - Train Station Farewell",
  "background": {
    "description": "World War II evacuation scene at a crowded London train station. Steam and smoke fill the air as children are being sent to the countryside to escape the Blitz.",
    "era": "1940s wartime Britain",
    "location": "London railway station platform"
  },
  "characters": ["Mrs. Pevensie", "Lucy Pevensie"],
  "camera": {
    "type": "Close-up two-shot",
    "movement": "Static with subtle handheld movement",
    "angle": "Profile view, intimate framing",
    "focus": "Both faces in focus, background soft bokeh"
  },
  "dialogue": [
    {
      "character": "Mrs. Pevensie",
      "text": "You must be brave for me, darling. I'll come for you... I promise."
    },
    {
      "character": "Lucy Pevensie",
      "text": "I will be, mother. I promise."
    }
  ],
  "audio": [
    {
      "type": "Train whistle blows (signaling departure)",
      "volume": 1
    },
    {
      "type": "Strings swell emotionally, then fade",
      "volume": 0.5
    },
    {
      "type": "Ambient sound of the train station",
      "volume": 0.5
    }
  ]
}
```

步骤 3：使用 image-generation 技能生成参考图像

加载 image-generation 技能，按照该技能说明生成单张参考图像 `narnia-farewell-scene-01.jpg`。

步骤 4：使用 generate.py 脚本生成视频
```bash
python /mnt/skills/public/video-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/narnia-farewell-scene.json \
  --reference-images /mnt/user-data/outputs/narnia-farewell-scene-01.jpg \
  --output-file /mnt/user-data/outputs/narnia-farewell-scene-01.mp4 \
  --aspect-ratio 16:9
```
> 不要读取 python 文件，直接使用参数调用它。

## 输出处理

生成完成后：

- 视频通常保存在 `/mnt/user-data/outputs/`
- 使用 `present_files` 工具将生成的视频（优先）以及生成的图像（如适用）分享给用户
- 提供生成结果的简要描述
- 如需调整，提供迭代选项

## 注意事项

- 无论用户使用什么语言，提示词始终使用英文
- JSON 格式确保结构化、可解析的提示词
- 参考图像可以显著提升生成质量
- 迭代优化是获得最佳结果的常规流程
