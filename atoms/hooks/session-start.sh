#!/usr/bin/env bash
# 示例 hook：会话启动时执行
# 输出到 stderr 会显示在 agent 上下文中

echo "Session started at $(date '+%Y-%m-%d %H:%M:%S')" >&2
