---
name: imagen
description: "使用 Google AI 生成图片（支持 Gemini 3 Pro Image / Imagen 4.0）。当用户要求生成图片、创建图像、画图时使用此技能。"
argument-hint: "[图片描述]"
allowed-tools: Bash(python3 *), Read
---

# AI 图片生成

使用 Google Gemini / Imagen 模型生成高质量图片。

## 使用方式

根据用户的描述，构建英文 prompt（英文 prompt 效果更好），然后执行：

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py "<prompt>" -o "<output_dir>" -m <model> -f <filename> -r <ratio> -n <count>
```

## 参数说明

- `prompt`: 图片描述（英文，尽量详细）
- `-o`: 输出目录，默认为当前目录。对于 Obsidian 知识库，保存到同级 `attachments/` 目录
- `-m`: 模型名称，默认 `gemini-3-pro-image-preview`（推荐，效果最好）
- `-f`: 自定义输出文件名（如 `my-image.png`），不指定则自动生成时间戳文件名
- `-r`: 宽高比，可选 `1:1`、`3:4`、`4:3`、`9:16`、`16:9`，默认 `1:1`（仅 Imagen 模型支持）
- `-n`: 生成数量，1-4 张，默认 1 张

## 可用模型

| 模型 | 类型 | 推荐场景 |
|------|------|----------|
| `gemini-3-pro-image-preview` | generateContent | **默认推荐**，理解复杂 prompt 能力强，画质优秀 |
| `gemini-3.1-flash-image-preview` | generateContent | 速度快，画质好 |
| `gemini-2.5-flash-image` | generateContent | 速度最快，画质一般 |
| `imagen-4.0-ultra-generate-001` | predict | 最高画质，需付费计划 |
| `imagen-4.0-generate-001` | predict | 画质与速度平衡，需付费计划 |
| `imagen-4.0-fast-generate-001` | predict | 速度快，需付费计划 |

## 执行流程

1. 将用户的中文描述翻译为详细的英文 prompt（加入风格、光照、细节等描述词以提升质量）
2. 执行生成脚本，使用 `-f` 参数指定有意义的文件名
3. 用 Read 工具展示生成的图片给用户
4. 如果生成失败，尝试换一个模型重试

## 环境要求

需要设置环境变量 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY`。
获取地址：https://aistudio.google.com/apikey

设置方式（在 Claude Code settings 中添加）：
```json
{
  "env": {
    "GEMINI_API_KEY": "your-api-key-here"
  }
}
```

## Prompt 优化技巧

- 添加画面风格：photorealistic, digital art, watercolor, oil painting, anime style, children's book illustration 等
- 添加光照描述：soft lighting, golden hour, dramatic shadows 等
- 添加相机参数：35mm lens, shallow depth of field, macro shot 等
- 添加情绪氛围：cozy, mysterious, vibrant, serene 等
