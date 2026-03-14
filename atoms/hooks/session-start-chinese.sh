#!/bin/bash
# SessionStart Hook: 设置会话默认使用中文
# 此脚本在每次 Claude Code 会话启动或恢复时执行

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "本会话默认使用简体中文进行交流和回复。会话中生成的文档也使用简体中文。"
  }
}
EOF

exit 0