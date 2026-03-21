# 🤖 My AI Skills

A curated collection of custom AI Agent skills designed to automate complex workflows and enhance productivity. Each skill is self-contained and ready to be integrated into your AI-assisted development environment.

## 🚀 Key Features

- **Modular Design**: Each skill resides in its own directory with comprehensive documentation.
- **Easy Integration**: Simple `SKILL.md` format for quick understanding and deployment.
- **Proven Workflows**: Optimized for real-world automation tasks.

## 🛠️ Available Skills

| Skill Name | Description | Link |
| :--- | :--- | :--- |
| **Imagen** | 使用 Google AI 生成图片（Gemini 3 Pro Image / Imagen 4.0） | [View Skill](imagen/SKILL.md) |
| **Gmail** | 抓取和处理 Gmail 邮件到 Obsidian 笔记 | [View Skill](gmail/SKILL.md) |
| **Bilibili Downloader** | 使用 yt-dlp 下载 Bilibili 视频、合集和课程 | [View Skill](bilibili-downloader/SKILL.md) |
| **Auto Branch** | 分析未提交变更，自动生成语义化分支名 | [View Skill](auto-branch/SKILL.md) |
| **PDF to PNG** | 将 PDF 页面转换为高清 PNG 图片 | [View Skill](pdf-to-png/SKILL.md) |

## 📦 Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:byzhangkui/my-agent-skills.git ~/.claude/skills
   ```

2. **Set up the environment:**
   We recommend using a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## ➕ Creating a New Skill

Follow these steps to contribute a new skill:

1. **Create a directory**: Name it according to the skill (e.g., `my-new-skill`).
2. **Add `SKILL.md`**: Describe the purpose, dependencies, and usage.
3. **Include Scripts**: Place your implementation scripts within the skill folder.
4. **Update README**: Add your skill to the "Available Skills" table above.

---

*Built with ❤️ for AI-native developers.*
