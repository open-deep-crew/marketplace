# OpenDeepCrew Marketplace CLI 文档

## 核心命令

| 命令 | 说明 |
|------|------|
| `marketplace show` | 显示完整的 registry 数据 |
| `marketplace regenerate` | 重新生成 registry |
| `marketplace repodir` | 输出本地仓库路径 |
| `marketplace sync` | 与远程仓库同步 |

## `marketplace history [options]`

查看变更历史。

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-n, --limit <count>` | 显示条数 | 20 |

```bash
opendeepcrew marketplace history -n 10
```

## `marketplace rollback <commit>`

回滚指定变更。

| 参数 | 说明 |
|------|------|
| `<commit>` | commit hash（从 `marketplace history` 获取） |

```bash
opendeepcrew marketplace rollback abc1234
```

## `marketplace add <source> [options]`

从外部源拉取 atom 到本地 marketplace。

| 参数/选项 | 说明 | 必填 |
|-----------|------|------|
| `<source>` | Git URL 或本地路径 | 是 |
| `--type <type>` | atom 类型：`skill` \| `command` \| `hook` \| `agent` \| `mcp` | 是 |
| `--transport <transport>` | MCP 传输类型：`stdio` \| `http` \| `sse` | 否（默认 stdio） |
| `--command <command>` | MCP 服务启动命令 | 否 |
| `--args <args...>` | MCP 命令参数 | 否 |
| `--url <url>` | MCP 服务 URL（http/sse） | 否 |
| `--env <pairs...>` | 环境变量（KEY=VALUE 格式） | 否 |

```bash
opendeepcrew marketplace add /path/to/skill --type skill
opendeepcrew marketplace add https://github.com/org/repo --type mcp --transport stdio --command npx --args ts-node server.ts
```

## Atom 子命令

| 命令 | 说明 |
|------|------|
| `marketplace atom list [--type <type>]` | 列出全部 atom（可按类型过滤） |
| `marketplace atom show <type> <name>` | 查看 atom 内容 |
| `marketplace atom delete <type> <name>` | 删除 atom |

## `marketplace plugin add <name> [options]`

创建插件。

| 选项 | 说明 |
|------|------|
| `--description <desc>` | 插件描述 |
| `--category <cat>` | 分类 |
| `--skills <list>` | 逗号分隔的 skill 列表 |
| `--commands <list>` | 逗号分隔的 command 列表 |
| `--agents <list>` | 逗号分隔的 agent 列表 |
| `--mcps <json>` | MCP 配置（JSON 字符串） |

```bash
opendeepcrew marketplace plugin add my-plugin --description "My plugin" --skills "skill-a,skill-b"
```

## 枚举值参考

| 类别 | 可选值 |
|------|--------|
| Atom 类型 | `skill`, `command`, `hook`, `agent`, `mcp` |
| MCP 传输类型 | `stdio`, `http`, `sse` |
