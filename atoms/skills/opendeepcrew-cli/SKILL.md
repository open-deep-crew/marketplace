---
name: opendeepcrew-cli
description: 智能 marketplace 助手。当用户描述任何工作需求时，自动从 opendeepcrew marketplace 中匹配合适的 plugin 或 atom（skill/agent/mcp），推荐给用户使用。找不到合适资源时，协同用户创建新的 skill/agent/plugin。当用户反馈现有 plugin 使用问题时，自动诊断问题根因并给出优化方案。触发场景：(1) 用户描述工作需求（如"我要修 bug"、"帮我做需求开发"），(2) 用户问"有什么 plugin 可以用"，(3) 用户说"这个 plugin 不好用"或反馈 plugin 问题，(4) 用户想添加/创建新的 skill/agent/plugin。
---

# OpenDeepCrew Marketplace 智能助手

根据用户需求，从 marketplace 中匹配、推荐、组装或创建合适的 plugin。

## 场景 A：用户描述工作需求

### 流程

1. **理解需求** — 提炼用户核心诉求（修 bug？做新需求？代码问答？）
2. **查询资源** — 运行 `opendeepcrew marketplace show` 获取所有可用 plugin 和 atom
3. **匹配推荐**：
   - 找到完全匹配的 plugin → 直接推荐，说明它包含哪些能力
   - 找到部分匹配 → 推荐最接近的 plugin，说明差距
   - 完全没有匹配 → 进入"协同创建"流程
4. **确认使用** — 用户确认后，告知如何在 workspace 中选择该 plugin

### 匹配策略

从 `marketplace show` 输出中分析每个 plugin 的：
- description（描述与用户需求的语义匹配度）
- 包含的 skills（提供哪些工作流能力）
- 包含的 agents（提供哪些角色专长）
- 包含的 mcps（提供哪些外部工具集成）

优先推荐匹配度最高的 plugin；当多个 plugin 部分匹配时，列出对比让用户选择。

### 协同创建

当 marketplace 中没有合适的 plugin 时：

1. 告知用户当前缺少的能力
2. 询问是否需要创建新资源
3. 根据需要创建的资源类型引导：
   - 需要新 skill → 引导使用 `/skill-creator`
   - 需要新 agent → 引导使用 `/agent-creator`
   - 需要新 MCP → 参见 [references/cli-commands.md](references/cli-commands.md) 中的 MCP 添加命令
4. 创建完成后，组装为新 plugin 或添加到现有 plugin
5. 运行 `opendeepcrew marketplace regenerate` 注册变更

## 场景 B：诊断现有 Plugin 问题

### 流程

1. **收集症状** — 明确用户遇到的问题（输出质量差？流程不对？缺少能力？）
2. **定位根因** — 查看 plugin 包含的 atom，逐层排查：

   | 症状 | 可能根因 | 排查方向 |
   |------|----------|----------|
   | AI 输出质量差、不符合预期 | Agent 提示词不够好 | 检查 agent .md 文件内容 |
   | 工作流程缺步骤、流程不对 | Skill 流程不完善 | 检查 skill 的 SKILL.md |
   | 缺少外部工具能力 | 缺少 MCP 集成 | 查看是否需要添加 MCP |
   | 多个能力冲突或冗余 | Plugin 组装不合理 | 重新调整 plugin 的 atom 组合 |

3. **提出方案** — 给出具体修改建议，经用户确认后执行
4. **执行修复** — 修改对应资源，运行 `opendeepcrew marketplace regenerate`

### 排查方法

- 查看 plugin 详情：`opendeepcrew marketplace show` 找到目标 plugin，分析其 atom 列表
- 查看 skill 内容：读取对应 skill 的 SKILL.md 和 references
- 查看 agent 内容：读取对应 agent 的 .md 文件
- 定位 marketplace 仓库：`opendeepcrew marketplace repodir`

## CLI 命令参考

执行具体 CLI 操作时，参见 [references/cli-commands.md](references/cli-commands.md) 获取完整命令文档。
