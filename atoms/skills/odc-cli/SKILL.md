---
name: odc-cli
description: 使用 odc CLI 管理 marketplace 的 atoms/plugins、订阅源、工作空间、服务器和配置。当用户提到列出技能、添加 atom、创建插件、合并插件、管理工作空间等 odc 操作时使用此技能——即使用户没有明确说"odc"。
---

# odc CLI

`odc` 是一个用于编排 AI 编码 agent 团队的 CLI 工具。它管理一个本地 marketplace，包含可复用组件（atoms：commands、skills、hooks、agents、MCP servers）和插件（plugins：一组 atoms 的集合），以及 agent 运行的工作空间（workspaces）。

本文档聚焦高频场景及其最优调用链。完整命令参考请按需读取对应文件：

- `references/global.md` — 输出模式、全局选项、错误码、`--force` 行为
- `references/atom.md` — atom show / files / add / update / delete / set-inject
- `references/plugin.md` — plugin list / add / update / merge / delete
- `references/marketplace.md` — marketplace show / sync / history / rollback / regenerate
- `references/subscription.md` — subscription list / add / remove / enable / disable / refresh
- `references/workspace.md` — workspace list / show / open / init / reinit / update / add-plugin / remove-plugin
- `references/server-config.md` — 服务器启动、配置管理

## 核心约束

以下约束不可违反，影响所有场景：

1. **没有 `atom list` 命令。** 要枚举 atoms，使用 `plugin list --json`（按插件查看）或 `marketplace show`（完整注册表）。
2. **本地插件只能引用本地 atoms。** 订阅源的 atoms 必须先通过 `plugin merge` 合并到本地，本地插件才能引用它们。
3. **`plugin list --json` 返回所有插件**（本地 + 所有订阅源）。同名插件可能出现多次但 `source.type` 不同。始终通过 **name + source** 共同匹配。
4. **获取当前工作空间信息优先读 `.aiworkspace.json`**，它包含 workspace name、plugins、agent type、permission mode。只有在需要其他工作空间信息时才用 `workspace show`。要获取 plugin 的 atom 详情，仍需 `plugin list --json`。
5. **非 TTY 环境自动输出 JSON。** 通过 Bash 工具调用 odc 时，输出默认为 JSON。第一行可能是 dotenv 注入信息——解析时需处理。
6. **非 TTY 环境下破坏性操作需要 `--force`。** `atom add`（覆盖）、`atom delete`、`plugin delete`、`marketplace rollback` 都需要 `--force` 跳过确认。

## 高频场景 Playbook

### Playbook 1：查询当前工作空间的 Atoms

**用户意图：** "当前空间有哪些技能/agent/命令"

```
步骤 1：读取当前工作空间目录下的 .aiworkspace.json
        → 包含 workspace name、plugins 数组（每项有 name + source）
        → 直接读本地文件，无需 CLI 调用

步骤 2：odc plugin list --json
        → 通过 name 和 source.type/source.name 共同匹配每个插件
        → 提取匹配插件的 skills/agents/commands/mcpServers

步骤 3：去重后展示给用户
        → 标注每个 atom 来自哪个插件
```

**如何获取工作空间上下文：** 每个 odc 工作空间目录下都有一个 `.aiworkspace.json` 文件，包含工作空间名称、挂载的插件、agent 类型和权限模式。直接读取此文件，比调用 `workspace show` 更快且省一次 CLI 调用。

### Playbook 2：将工作空间转为单个本地插件

**用户意图：** "把当前工作空间打包成一个本地 plugin，方便下次直接用"

一个工作空间可能挂载多个插件（本地 + 订阅源）。此 playbook 创建一个包含所有 atoms 的本地插件。

```
步骤 1：读取当前工作空间目录下的 .aiworkspace.json
        → 获取工作空间名称、所有挂载的插件及其来源

步骤 2：odc plugin list --json
        → 按 name + source 匹配每个挂载的插件
        → 收集所有插件的 atoms（skills、agents、commands、mcpServers）

步骤 3：对列表中的每个订阅源插件执行：
        odc plugin merge <订阅源插件名> --source <订阅源名称>
        → 将订阅源 atoms 复制到本地 marketplace
        → 必须执行：本地插件无法引用订阅源 atoms

步骤 4：odc plugin add <新插件名> \
          --description "<描述>" \
          --category <分类> \
          --skills "<去重后的逗号分隔技能名>" \
          --agents "<agent 名>" \
          --commands "<命令名>" \
          --mcps '<mcpServers JSON>'
        → 创建合并后的本地插件

步骤 5：odc plugin list --json
        → 校验：按新插件名 + source.type=local 过滤
        → 确认 atom 数量符合预期
```

**要点：**
- 创建前先对所有插件的 atom 名称去重。
- MCP servers 需要以 JSON 字符串传给 `--mcps`。
- 创建前询问用户新插件的名称。

### Playbook 3：给插件添加 Atom

**用户意图：** "把 xxx skill 加到 xxx plugin 里"

atom 来源可以是：本地路径、GitHub URL、订阅源、或已在本地 marketplace 中。

```
步骤 1：将 atom 添加到本地 marketplace（如果还不在的话）

        来自 GitHub URL：
        odc atom add <github-url> --type <type> --force

        来自本地路径：
        odc atom add <本地路径> --type <type> --force

        来自订阅源（必须先合并）：
        odc plugin merge <订阅源插件名> --source <订阅源名称>

        已在本地：跳过此步骤。

步骤 2：检查目标插件是否已包含此 atom
        odc plugin list --json
        → 按 name + source 匹配目标插件
        → 检查 atom 名称是否已存在于对应数组（skills/agents/commands）中

步骤 3：如果已包含：
        → 询问用户："该插件已包含 <atom-name>，是否要覆盖？"
        → 用户确认：继续执行步骤 4
        → 用户拒绝：停止

步骤 4：将 atom 添加到插件
        odc plugin update <插件名> --add-skills "<atom-name>"
        （或 --add-agents / --add-commands，取决于 atom 类型）

步骤 5：校验
        odc plugin list --json → 确认 atom 出现在插件中
```

**说明：** `--add-skills` 即使名称已存在也会添加（会重新指向引用）。对于 atom 内容更新（如用 GitHub 版本覆盖），步骤 1 的 `--force` 处理内容更新；步骤 4 确保插件引用是最新的。

### Playbook 4：将插件合并到本地插件

**用户意图：** "将某个插件合并到本地的某个插件中"

两种情况：来源是订阅源插件，或来源是另一个本地插件。

**情况 A：来源是订阅源插件**

```
步骤 1：odc plugin merge <目标本地插件> --source <订阅源名称>
        → 将订阅源插件的所有 atoms 批量复制到本地 marketplace
        → 同名 atoms 会被强制覆盖
        → 自动重建注册表

步骤 2：odc plugin list --json
        → 校验目标插件是否已包含合并的 atoms
```

**说明：** `plugin merge` 一条命令同时完成 atom 复制和目标插件装配更新，是最高效的路径。

**情况 B：来源是另一个本地插件**

```
步骤 1：odc plugin list --json
        → 获取源插件和目标插件的 atom 列表

步骤 2：对每种 atom 类型（skills、agents、commands、mcps）：
        → 识别源插件有但目标插件没有的 atoms
        → 识别两者都有的 atoms（潜在冲突）

步骤 3：如果有重名 atoms，询问用户冲突解决策略

步骤 4：odc plugin update <目标插件> \
          --add-skills "<要添加的技能>" \
          --add-agents "<要添加的 agents>" \
          --add-commands "<要添加的命令>" \
          --add-mcps '<要添加的 mcps JSON>'

步骤 5：odc plugin list --json → 校验结果
```

### Playbook 5：注册表故障排查

**用户意图：** "atom 找不到" / "注册表不对" / E2002 错误

```
步骤 1：odc marketplace regenerate
        → 从磁盘重建注册表，修复过期索引

步骤 2：odc marketplace show
        → 检查完整注册表，确认 atom 是否存在

步骤 3：如果 atom 仍然缺失：
        → 检查是否被删除或从未添加
        → 如需要，用 odc atom add 重新添加
```

## 命令速查表

| 操作 | 命令 |
|---|---|
| 列出所有插件 | `odc plugin list --json` |
| 查看工作空间详情 | `odc workspace show <name> --json` |
| 查看 atom 内容 | `odc atom show <type> <name>` |
| 列出 atom 文件 | `odc atom files <type> <name>` |
| 从路径/URL 添加 atom | `odc atom add <source> --type <type> --force` |
| 删除 atom | `odc atom delete <type> <name> --force` |
| 创建插件 | `odc plugin add <name> --description "..." --skills "a,b"` |
| 更新插件 atoms | `odc plugin update <name> --add-skills "x" --remove-agents "y"` |
| 合并订阅源到本地 | `odc plugin merge <plugin> --source <subscription>` |
| 重建注册表 | `odc marketplace regenerate` |
| 完整注册表导出 | `odc marketplace show` |
| 列出订阅源 | `odc subscription list --json` |
| 刷新订阅源 | `odc subscription refresh [name]` |
| 列出工作空间 | `odc workspace list --json` |
| 初始化工作空间 | `odc workspace init <plugin> [--source <source>]` |
| 重新初始化工作空间 | `odc workspace reinit <name>` |
| 为工作空间添加插件 | `odc workspace add-plugin <ws> <plugin> [--subscription-name <name>]` |
| 从工作空间移除插件 | `odc workspace remove-plugin <ws> <plugin> [--subscription-name <name>]` |

完整命令参数请读取本文档顶部列出的对应参考文件。
