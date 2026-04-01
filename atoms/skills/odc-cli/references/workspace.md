# workspace — 工作空间管理

管理 AI agent 运行的工作空间。

## workspace list

```bash
odc workspace list --json
```

列：NAME, PLUGIN, AGENT, CREATED

## workspace show

```bash
odc workspace show <name> --json
```

返回：Name、Plugin(s)、Agent、Permission Mode、Init Agents、Source、Directory、Created、Updated。

## workspace open

```bash
odc workspace open <name>
```

在检测到的 IDE 中打开工作空间目录。

## workspace init

```bash
odc workspace init <plugin>
odc workspace init <plugin> --source <source>
```

在当前目录初始化 plugin 并绑定 workspace。

参数：
- `<plugin>`：plugin 名称

选项：
- `--source <source>`：来源，`local` 或订阅源名称。不指定则为 local。

## workspace reinit

```bash
odc workspace reinit <name>
```

重新初始化工作空间（重新生成 agent 配置文件）。适用于插件更新后或手动修改配置后。

## workspace update

```bash
odc workspace update <name> --permission-mode approve-all --agent cursor
```

选项：
- `--permission-mode <mode>`：`approve-all`、`approve-reads`
- `--agent <agent>`：`claude-code`、`cursor`、`kiro`

至少需要一个选项。

## workspace add-plugin

```bash
odc workspace add-plugin <workspace-name> <plugin-name>
odc workspace add-plugin <workspace-name> <plugin-name> --subscription-name <name>
```

为工作空间添加 plugin。

参数：
- `<workspace-name>`：工作空间名称
- `<plugin-name>`：plugin 名称

选项：
- `--subscription-name <name>`：订阅源名称。不指定则为 local。

## workspace remove-plugin

```bash
odc workspace remove-plugin <workspace-name> <plugin-name>
odc workspace remove-plugin <workspace-name> <plugin-name> --subscription-name <name>
```

从工作空间移除 plugin。

参数：
- `<workspace-name>`：工作空间名称
- `<plugin-name>`：plugin 名称

选项：
- `--subscription-name <name>`：订阅源名称。不指定则匹配 local。

## 备注

- `workspace create` 和 `workspace delete` 不在 CLI 中提供——请使用 Web UI
