---
name: gmail
description: Fetch and process Gmail emails into Obsidian notes. Use when the user wants to check email, process new messages, review fetched emails, or configure Gmail integration. Supports subcommands: fetch, process, config, setup.
---

# Gmail 邮件处理技能

## Overview

从 Gmail 拉取特定发件人的邮件，原样保存为 Obsidian 笔记（含图片和附件），然后进行 AI 摘要、标签分配和知识扩展。

邮件存储目录：`80_Resources/邮件/{发件人名}/`
配置文件：`scripts/gmail_config.json`
拉取脚本：`scripts/gmail_fetcher.py`

## 子命令

### `/gmail` 或 `/gmail fetch`

拉取新邮件并保存为 Obsidian 笔记。

**执行步骤：**
1. 运行脚本：
```bash
cd "/Users/zhangkui/Obsidian Vault" && python3 scripts/gmail_fetcher.py --once
```
2. 向用户报告拉取结果（几封新邮件、来自哪些发件人）
3. 如果有新邮件，自动进入 process 流程

### `/gmail process`

对 `80_Resources/邮件/` 中 `status: seed` 的笔记进行 AI 处理。

**处理步骤：**

1. 用 Glob 查找 `80_Resources/邮件/**/*.md` 中 `status: seed` 的笔记
2. 逐个读取并处理，对每封邮件：

   a. **生成摘要**：在正文前（`---` 分隔线之后）插入 `## 摘要` 区块，包含 2-3 句关键信息概述

   b. **分配标签**：根据邮件内容，从现有标签体系中选择合适的标签更新 frontmatter 的 `tags` 字段：
      - 投资相关 → `#invest/macro`, `#invest/research`, `#invest/strategy/options` 等
      - 技术相关 → `#tech/ai`, `#tech/dev` 等
      - 成长/学习 → `#growth/mindset`, `#growth/system` 等
      - 生活相关 → `#life/health`, `#life/interest` 等
      - 参考标签体系：读取 `99_Meta/System/Obsidian 标签管理.md`

   c. **识别行动项**：如果邮件中包含待办事项、截止日期或需要回复的内容，在笔记末尾追加 `## 行动项` 区块

   d. **关联笔记**：搜索 vault 中相关主题的笔记，在末尾追加 `## 相关笔记` 区块，使用 `[[wikilinks]]`

3. 将 `status` 从 `seed` 更新为 `growing`
4. 向用户汇报处理结果

### `/gmail config`

查看或修改 Gmail 配置。

**执行步骤：**
1. 读取 `scripts/gmail_config.json`
2. 向用户展示当前配置（发件人白名单等）
3. 如果用户要修改，编辑配置文件

### `/gmail setup`

引导用户完成首次 OAuth 设置。

**引导步骤：**

1. 检查 `~/.config/gmail-obsidian/credentials.json` 是否存在

2. 如果不存在，引导用户：
   - 访问 Google Cloud Console (console.cloud.google.com)
   - 创建新项目（或选择已有项目）
   - 左侧菜单 → APIs & Services → Library → 搜索 "Gmail API" → Enable
   - 左侧菜单 → APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
   - Application type 选择 "Desktop app"
   - 下载 JSON 文件，重命名为 `credentials.json`
   - 放到 `~/.config/gmail-obsidian/` 目录下

3. 如果 credentials.json 已存在：
```bash
cd "/Users/zhangkui/Obsidian Vault" && python3 scripts/gmail_fetcher.py --setup
```
   这会打开浏览器完成 OAuth 授权

4. 认证成功后，引导用户配置发件人白名单：
```bash
cat scripts/gmail_config.json
```
   提示用户将 `sender_whitelist` 修改为实际要监控的邮箱地址

5. 安装 Python 依赖（如果尚未安装）：
```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib markdownify beautifulsoup4
```

## 注意事项

- 凭证文件 (`credentials.json`, `token.json`) 存放在 `~/.config/gmail-obsidian/`，不在 git 仓库中
- 首次运行需要浏览器授权，后续自动刷新 token
- 邮件的 `gmail_id` 用于去重，不会重复拉取同一封邮件
- 图片和附件保存在 `80_Resources/邮件/{发件人}/attachments/` 目录
- 笔记格式遵循 Obsidian 知识管理实践：`type: summary`, `status: seed`
