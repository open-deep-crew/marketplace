# odc CLI Global Reference

## Install

```bash
npm install -g @odc/odc
```

## Output Modes

| Environment | Default output | Override |
|---|---|---|
| TTY (terminal) | Human-readable (tables, colors) | `--json` forces JSON |
| Non-TTY (pipe, AI agent) | JSON | `--pretty` forces human-readable |

## Command Model

```
odc [global_options] <command> [subcommand] [options] [arguments]
```

## Global Options

| Option | Description |
|---|---|
| `-V, --version` | Output version number |
| `--json` | Force JSON output |
| `--pretty` | Force human-readable output |
| `--no-color` | Disable colored output |
| `--verbose` | Enable debug logging |
| `-h, --help` | Display help |

## Error Codes

| Code | Meaning | Fix |
|---|---|---|
| E0001 | Requires interactive terminal | Use `--force` or `--json` |
| E1001 | Config key not found | Check with `config show` |
| E2001 | MARKETPLACE_SOURCE not configured | `config set MARKETPLACE_SOURCE <url>` |
| E2002 | Atom not found | Check registry or verify type/name |
| E2003 | Invalid atom type | Use: command, agent, skill, hook, mcp |
| E3001 | Workspace not found | Check with `workspace list --json` |

## `--force` Behavior

| Command | `--force` effect |
|---|---|
| `atom add` (exists) | Overwrite without asking |
| `atom delete` | Delete without asking |
| `plugin delete` | Delete without asking |
| `marketplace rollback` | Revert without asking |

## Filesystem Layout

```
~/.odc/
  .env                    # Configuration
  workspaces/             # Workspace directories
    <workspace-name>/

~/.opendeepcrew/
  workspaces/             # Workspace directories (alternative path)
```

Marketplace is a separate git repository cloned from `MARKETPLACE_SOURCE`.

## Notes

- All marketplace CUD operations are automatically git-committed
- `workspace create` and `workspace delete` are NOT in CLI — use Web UI
- `marketplace repodir` is NOT provided — use `marketplace open`
