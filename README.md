# marketplace

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> OpenDeepCrew 的 atom 市场模板仓库。Fork 后即可创建自己团队的插件市场。

Atom 市场是 [OpenDeepCrew](https://github.com/open-deep-clew/opendeepcrew) 的插件源。将 commands、agents、skills、hooks 作为**原子（atoms）**管理，通过 plugins 自由组合成工作流。

- **原子复用**：同一个 atom 可被多个 plugin 引用，改一处全部生效
- **自由组合**：不同 plugin 按需组合 atoms，定义特定工作流
- **标签涌现**：atom 的标签从 plugin 的 keywords 自动聚合，频率越高说明越核心
- **零依赖**：纯文件结构，不需要构建工具就能用

## 目录结构

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 核心配置：定义 plugins 和 atom 引用关系
├── atoms/                        # 原子库
│   ├── commands/                 # Slash commands（.md）
│   ├── agents/                   # AI agents（.md，带 frontmatter）
│   ├── skills/                   # Skills（目录，含 SKILL.md）
│   └── hooks/                    # Event hooks（.sh）
├── scripts/
│   └── generate-registry.js      # 生成 registry.json（供前端/API 消费）
└── package.json
```

## 快速开始

### 1. 从模板创建自己的市场

在 GitHub 上 Fork 本仓库，或者：

```bash
git clone https://github.com/open-deep-clew/marketplace.git my-marketplace
cd my-marketplace
rm -rf .git && git init
```

### 2. 添加 atoms

**添加 Command：**

```bash
cat > atoms/commands/smart-commit.md << 'EOF'
---
name: smart-commit
description: 自动生成 conventional commit 消息
---

# /smart-commit

分析 staged changes，生成符合 conventional commits 规范的提交消息。
EOF
```

**添加 Agent：**

```bash
cat > atoms/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: 代码审查专家
tools: Read, Grep, Glob
model: sonnet
---

你是一个资深代码审查专家。审查代码时关注：
1. 逻辑正确性
2. 安全漏洞
3. 性能问题
4. 代码风格
EOF
```

**添加 Skill：**

```bash
mkdir -p atoms/skills/tdd-workflow
cat > atoms/skills/tdd-workflow/SKILL.md << 'EOF'
---
name: tdd-workflow
description: 测试驱动开发工作流
---

# TDD Workflow

## 触发条件
当用户要求实现新功能或修复 bug 时激活。

## 行为
1. 先写测试
2. 运行测试确认失败
3. 写最小实现让测试通过
4. 重构
EOF
```

**添加 Hook：**

```bash
cat > atoms/hooks/session-start-chinese.sh << 'EOF'
#!/usr/bin/env bash
echo "请使用中文回复。" >&2
EOF
chmod +x atoms/hooks/session-start-chinese.sh
```

### 3. 组合成 Plugin

编辑 `.claude-plugin/marketplace.json`，在 `plugins` 数组中添加：

```json
{
  "name": "my-dev-workflow",
  "description": "我的开发工作流",
  "version": "1.0.0",
  "source": "./",
  "strict": false,
  "category": "development",
  "keywords": ["dev", "git", "tdd"],
  "author": { "name": "My Team" },
  "commands": [
    "./atoms/commands/smart-commit.md"
  ],
  "agents": [
    "./atoms/agents/code-reviewer.md"
  ],
  "skills": [
    "./atoms/skills/tdd-workflow"
  ],
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/atoms/hooks/session-start-chinese.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

同一个 atom 可以出现在多个 plugin 中 — 这就是原子复用。

### 4. 验证

```bash
npm run generate-registry
```

输出 `public/generated/registry.json`，包含所有 atoms 的元数据和引用关系。

### 5. 配合 OpenDeepCrew 使用

在 OpenDeepCrew 的 `.env` 中指向你的市场：

```bash
# 本地路径
MARKETPLACE_SOURCE=./path/to/my-marketplace

# 或 git 仓库
MARKETPLACE_SOURCE=https://github.com/your-org/my-marketplace.git
```

创建工作区时，OpenDeepCrew 会从市场拉取 atoms 并初始化 agent 配置。

## marketplace.json 配置说明

```json
{
  "name": "市场名称",
  "owner": { "name": "团队名", "email": "team@example.com" },
  "plugins": [
    {
      "name": "plugin 名称（唯一）",
      "description": "plugin 描述",
      "version": "1.0.0",
      "source": "./",
      "strict": false,
      "category": "分类标签",
      "keywords": ["标签会聚合到被引用的 atoms 上"],
      "commands": ["./atoms/commands/xxx.md"],
      "agents": ["./atoms/agents/xxx.md"],
      "skills": ["./atoms/skills/xxx"],
      "hooks": { "SessionStart": [...] },
      "mcpServers": {
        "server-name": {
          "type": "stdio",
          "command": "npx",
          "args": ["-y", "@some/mcp-server"]
        }
      }
    }
  ]
}
```

**关键点：**
- `source: "./"` — 所有 plugin 共享同一个根目录
- `strict: false` — 无需 plugin 内部的 plugin.json
- `keywords` — 会聚合到被引用 atoms 的元数据中
- `mcpServers` — 创建工作区时写入 agent 的 MCP 配置
- `hooks` — 中的 `${CLAUDE_PLUGIN_ROOT}` 会被替换为实际路径

## 相关项目

| 项目 | 说明 |
|------|------|
| [opendeepcrew](https://github.com/open-deep-clew/opendeepcrew) | AI agent 团队编排服务器，消费本市场 |
| [acpx](https://github.com/open-deep-clew/acpx) | Agent Client Protocol 的 headless CLI 客户端 |
| [acpx-teams](https://github.com/open-deep-clew/acpx-teams-mcp) | agent 团队协调的 MCP server |

## License

MIT
