---
name: git-workspace-init
description: Git 仓库工作空间初始化流程。当会话启动时需要 clone 仓库、创建修复分支并输出环境信息时使用此 Skill。适用于 bug 修复、功能开发等需要在本地初始化 Git 工作空间的场景。触发词包括：初始化仓库、clone 项目、准备工作空间、开始修复。
---

# Git 工作空间初始化

在当前工作空间下初始化 Git 仓库，创建日期分支，输出格式化的环境信息。

## 工作流程

### 1. 运行初始化脚本

```bash
bash <skill-path>/scripts/init_workspace.sh <repo_url> [workspace_dir] [branch_name]
```

参数：
- `repo_url`：Git 仓库地址（SSH 或 HTTPS）
- `workspace_dir`：本地目录名，默认 `repo`
- `branch_name`：完整分支名，由 AI 根据下方命名规范生成

脚本自动处理：
- 目录不存在 → clone
- 目录已存在且 remote 匹配 → fetch
- 目录已存在但 remote 不匹配 → 报错退出
- 创建指定分支（已存在则切换）
- 输出格式化的环境信息

### 2. 告知用户仓库信息

将脚本结果输出给用户确认。

## 分支命名规范

AI 在调用脚本前，必须根据任务上下文生成符合以下规范的分支名。

### 格式

```
<prefix>/<short-description>-<YYYY-MM-DD>
```

### 规则

1. **仅允许 ASCII 字符**：小写字母 `a-z`、数字 `0-9`、连字符 `-`、斜杠 `/`（仅用于 prefix 分隔）
2. **禁止中文及其他非 ASCII 字符**：如果 workspace 名称含中文，必须翻译为简短英文描述
3. **short-description**：用 kebab-case，简洁概括任务内容，不超过 5 个单词
4. **prefix**：`feat`（新功能）、`fix`（修 bug）、`chore`（杂项）、`refactor`（重构）
5. **日期**：当天日期，格式 `YYYY-MM-DD`

### 示例

| workspace 名称 | ✅ 正确分支名 | ❌ 错误分支名 |
|---|---|---|
| 添加主飞书bot的agent配置 | `feat/add-feishu-bot-config-2026-03-15` | `feat/添加主飞书bot的agent配置-2026-03-15` |
| 修复登录页面样式问题 | `fix/login-page-style-2026-03-15` | `fix/修复登录页面样式问题-2026-03-15` |
| ws-update-ci-pipeline | `chore/update-ci-pipeline-2026-03-15` | — |
