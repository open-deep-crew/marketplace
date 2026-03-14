---
name: git-workspace-init
description: Git 仓库工作空间初始化流程。当会话启动时需要 clone 仓库、创建修复分支并输出环境信息时使用此 Skill。适用于 bug 修复、功能开发等需要在本地初始化 Git 工作空间的场景。触发词包括：初始化仓库、clone 项目、准备工作空间、开始修复。
---

# Git 工作空间初始化

在当前工作空间下初始化 Git 仓库，创建日期分支，输出格式化的环境信息。

## 工作流程

### 1. 运行初始化脚本

```bash
bash <skill-path>/scripts/init_workspace.sh <repo_url> [workspace_dir] [branch_prefix]
```

参数：
- `repo_url`：Git 仓库地址（SSH 或 HTTPS）
- `workspace_dir`：本地目录名，默认 `repo`
- `branch_prefix`：分支前缀，如 `fix`、`feat`、`chore`，默认 `feat`

脚本自动处理：
- 目录不存在 → clone
- 目录已存在且 remote 匹配 → fetch
- 目录已存在但 remote 不匹配 → 报错退出
- 创建 `<prefix>/<workspace-name>-<date>` 分支（已存在则切换）
- 输出格式化的环境信息

### 2. 告知用户仓库信息

将脚本结果输出给用户确认。

## 分支命名规则

格式：`<prefix>/<workspace-name>-<YYYY-MM-DD>`

- `prefix` 由调用方指定，默认 `feat`，常见值：`fix`（修 bug）、`feat`（新功能）、`chore`（杂项）
- `workspace-name` 取自工作空间上级目录名，去掉 `ws-` 前缀
- 日期为当天日期
