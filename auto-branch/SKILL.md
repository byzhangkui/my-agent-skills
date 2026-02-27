---
name: Generate and Switch Branch
description: Analyze uncommitted changes in the current repo, generate a semantic branch name, and switch to it.
---

# Generate and Switch Branch (自动生成分支名并切换)

## 技能说明
当前技能允许智能分析用户工作区中尚未提交的代码更改（staged 或 unstaged），根据更改的上下文语义（如功能开发、修复缺陷等），按照 Git Flow 规范自动生成一个简短且具有描述性的分支名，并切换到该新分支中。

## 执行步骤

1. **状态检查，确认是否有改动**:
   - 运行 `git status` 检查当前是否在 Git 仓库中。
   - 检查当前所在分支：如果已经在一个非 main/master 的功能分支上，提示用户确认是否要从当前分支创建新分支，避免分支嵌套。
   - 确认是否存在未提交的修改（若无改动，则向用户说明无法根据改动生成分支名，并询问是否需要手动指定）。

2. **分析代码变更细节**:
   - 优先运行 `git diff --stat` 获取变更概览（涉及哪些文件、增删行数）。
   - 如需了解具体改动，再对关键文件执行 `git diff HEAD -- <file>` 查看详情，避免大量 diff 撑爆上下文。
   - 若仓库尚无任何 commit（全新仓库），改用 `git diff --cached` 或 `git status --short` 分析 staged 文件。
   - 总结改动的核心意图。

3. **生成标准化分支名**:
   - 根据改动语义，推断对应的分支前缀（Conventional types）：
     - `feat/`: 新功能
     - `fix/`: 修复 bug
     - `refactor/`: 重构代码
     - `docs/`: 更新文档
     - `chore/`: 构建过程或辅助工具变动
     - `perf/`: 性能优化
     - `test/`: 添加或修改测试
     - `style/`: 代码格式调整（不影响逻辑）
     - `ci/`: CI/CD 配置变更
   - 在前缀之后拼接简短、全小写、破折号连字符分隔的英文简述。例如：`feat/user-login-form`, `fix/header-padding`。

4. **执行切换动作**:
   - 使用 `git switch -c <生成的标准分支名>` 创建并切换到新分支。若环境不支持 `git switch`，回退使用 `git checkout -b`。
   - 如果同名分支已存在，依次尝试：加递增数字后缀（如 `feat/user-login-form-2`）→ 加日期时间后缀（如 `feat/user-login-form-0227-1430`）。

## 约束 & 最佳实践
- 分支名**必须全部小写**，使用连字符 `-` 连接单词。
- 保证生成的描述简明扼要，且能够准确概括当前已写代码的核心点。
- 操作仅限创建、切换分支，**不要**随意在此过程中替用户提交（Commit）代码。提交应通过其他技能或指令来完成。
