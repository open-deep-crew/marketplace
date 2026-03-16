#!/usr/bin/env bash
# Git 工作空间初始化脚本
# 用法: init_workspace.sh <repo_url> [workspace_dir] [branch_name]
#   repo_url:       Git 仓库 SSH/HTTPS 地址
#   workspace_dir:  本地目录名，默认 "repo"
#   branch_name:    完整分支名，如 feat/add-feishu-bot-config-2026-03-15

set -euo pipefail

REPO_URL="${1:?用法: init_workspace.sh <repo_url> [workspace_dir] [branch_name]}"
WORKSPACE="${2:-repo}"
BRANCH="${3:-}"

# ── 1. Clone 或 Fetch ──
if [ -d "$WORKSPACE/.git" ]; then
  EXISTING_REMOTE=$(git -C "$WORKSPACE" remote get-url origin 2>/dev/null || echo "")
  if [ "$EXISTING_REMOTE" = "$REPO_URL" ]; then
    echo "📂 仓库已存在，执行 fetch..."
    git -C "$WORKSPACE" fetch origin
  else
    echo "❌ 目录 $WORKSPACE 已存在但 remote 不匹配"
    echo "   期望: $REPO_URL"
    echo "   实际: $EXISTING_REMOTE"
    exit 1
  fi
else
  echo "📥 Cloning $REPO_URL → $WORKSPACE ..."
  mkdir -p "$WORKSPACE"
  git clone "$REPO_URL" "$WORKSPACE"
fi

# ── 2. 创建分支 ──
cd "$WORKSPACE"

if [ -z "$BRANCH" ]; then
  echo "❌ 未指定分支名，请由 AI 根据分支命名规范生成分支名并传入"
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "🔀 分支 $BRANCH 已存在，切换..."
  git checkout "$BRANCH"
else
  echo "🌿 创建分支 $BRANCH ..."
  git checkout -b "$BRANCH"
fi

# ── 3. 输出环境信息 ──
REMOTE=$(git remote get-url origin)
CURRENT_BRANCH=$(git branch --show-current)
STATUS=$(git status --short)
if [ -z "$STATUS" ]; then
  STATUS_DISPLAY="clean"
else
  STATUS_DISPLAY="$STATUS"
fi

# 生成目录树（仅顶层）
TREE=$(ls -1 | while read -r item; do
  if [ -d "$item" ]; then
    echo "├── ${item}/"
  else
    echo "├── ${item}"
  fi
done | sed '$ s/├/└/')

LOCAL_PATH=$(pwd)

cat <<EOF

📦 仓库就绪

本地路径:   $LOCAL_PATH
Remote:     $REMOTE
当前分支:   $CURRENT_BRANCH
分支状态:   $STATUS_DISPLAY

目录结构:
$TREE
EOF
