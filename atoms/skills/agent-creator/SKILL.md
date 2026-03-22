---
name: agent-creator
description: 创建和修改 Agent 的指南。当用户想要创建新的 Agent 或修改现有 Agent 时使用此 Skill。Agent 是定义 AI 角色、行为准则和工作流程的 Markdown 文件，存放在 marketplace 的 atoms/agents 目录下。
---

# Agent Creator

创建和修改 Agent 文件。Agent 格式详见 [references/agent-format.md](references/agent-format.md)。

## 创建流程

### 1. 理解需求

向用户确认：
- Agent 的角色定位是什么？
- 需要哪些核心能力？
- 工作流程是怎样的？有哪些阶段？
- 需要引用哪些已有的 Skill？

从最关键的问题开始，避免一次问太多。

### 2. 初始化 Agent

运行初始化脚本创建模板文件：

```bash
python3 <skill-path>/scripts/init_agent.py <agent-name>
```

文件将创建在当前工作目录下：`./<agent-name>.md`。

### 3. 编写 Agent

编辑生成的模板文件，填充以下内容：

**Frontmatter：**
- `name`：人类可读的显示名称
- `description`：完整描述角色、能力和使用场景

**正文结构：**
- **Role 标题**：`# Role: <名称> — <副标题>`
- **行为准则**：交流语言、流程控制规则、范围限定
- **工作流程**：分阶段定义，每阶段结束用 `**⏸ 停下，等待用户确认。**`

引用 Skill 时使用 `/<skill-name>` 格式，如 `/bugfix`、`/git-workspace-init`。

### 4. 注册 Agent

```bash
opendeepcrew atom add ./<agent-name>.md --type agent --force
```

该命令会自动完成 git commit 和 marketplace 注册。

## 修改流程

1. `opendeepcrew atom show agent <name>` — 读取目标 Agent 内容，保存到本地文件
2. 根据用户需求修改内容
3. `opendeepcrew atom add ./<agent-name>.md --type agent --force` — 覆盖更新到 marketplace
