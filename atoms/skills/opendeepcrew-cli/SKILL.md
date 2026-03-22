---
name: opendeepcrew-cli
description: Use opendeepcrew CLI to manage marketplace atoms/plugins, workspaces, server, and configuration. Covers all commands, output modes, error codes, and AI-agent integration patterns.
---

# opendeepcrew CLI

## When to use this skill

Use this skill when you need to:

- Manage marketplace content (atoms, plugins, registry)
- List, open, or update workspaces
- Start or configure the opendeepcrew server
- Read or modify opendeepcrew configuration
- Integrate opendeepcrew operations into automation scripts or AI agent workflows

## What opendeepcrew CLI is

`opendeepcrew` is a CLI for orchestrating AI coding agent teams. It manages a local marketplace of reusable components (atoms: commands, skills, hooks, agents, MCP servers) and plugins (bundles of atoms), plus workspaces where agents operate.

Core capabilities:

- Marketplace atom CRUD with git version tracking
- Plugin assembly from atoms (interactive and non-interactive)
- Workspace listing, opening in IDE, and configuration
- Server lifecycle with auto-restart
- Configuration management (env-based, `~/.opendeepcrew/.env`)
- AI-first design: auto-detects TTY vs non-TTY, outputs JSON for automation
- Structured error codes for programmatic error handling
- `--force` flag on destructive operations for non-interactive use

## Install

```bash
npm install -g @opendeepcrew/opendeepcrew
```

## Output modes

The CLI auto-detects the output mode:

| Environment | Default output | Override |
|---|---|---|
| TTY (terminal) | Human-readable (tables, colors) | `--json` forces JSON |
| Non-TTY (pipe, AI agent) | JSON | `--pretty` forces human-readable |

This means AI agents calling the CLI via `exec`/`spawn` automatically get JSON without needing `--json`.

## Command model

```
opendeepcrew [global_options] <command> [subcommand] [options] [arguments]
```

## Global options

| Option | Description |
|---|---|
| `-V, --version` | Output version number |
| `--json` | Force JSON output |
| `--pretty` | Force human-readable output |
| `--no-color` | Disable colored output |
| `--verbose` | Enable debug logging |
| `-h, --help` | Display help |

## Commands

### server

Start the opendeepcrew server.

```bash
opendeepcrew server
opendeepcrew server --port 8080
```

Behavior:
- On first run, auto-detects missing config and runs interactive setup (TTY) or generates defaults (non-TTY)
- Spawns server as a child process with auto-restart on exit code 120
- Forwards SIGINT/SIGTERM to child process for graceful shutdown
- Port priority: `--port` flag > `PORT` env var > config file > default 4000

### config

Manage configuration stored in `~/.opendeepcrew/.env`.

```bash
opendeepcrew config show              # Display all config
opendeepcrew config get <key>         # Get single value
opendeepcrew config set <key> <value> # Set single value
```

Examples:

```bash
# Human-readable
opendeepcrew config show

# JSON output (non-TTY auto or explicit)
opendeepcrew config show --json

# Get port
opendeepcrew config get PORT

# Set marketplace source
opendeepcrew config set MARKETPLACE_SOURCE https://github.com/org/marketplace.git
```

### atom

Manage marketplace atoms (commands, skills, hooks, agents, MCP servers).

```bash
opendeepcrew atom list [--type <type>]
opendeepcrew atom show <type> <name> [--file <path>]
opendeepcrew atom files <type> <name>
opendeepcrew atom add <source> --type <type> [options] [-f|--force]
opendeepcrew atom update <name> [options]
opendeepcrew atom delete <type> <name> [-f|--force]
```

#### atom list

```bash
opendeepcrew atom list                 # All types
opendeepcrew atom list --type skill    # Filter by type
opendeepcrew atom list --type mcp      # List MCP servers
opendeepcrew atom list --json          # JSON output
```

Valid types: `command`, `agent`, `skill`, `hook`, `mcp`

#### atom show

```bash
opendeepcrew atom show skill my-skill
opendeepcrew atom show mcp my-server
opendeepcrew atom show skill my-skill --file references/best-practices.md
```

Returns atom content. For MCP, returns the server configuration JSON.

Use `--file <path>` to read a specific sub-file within a directory-type atom. Use `atom files` first to discover available files.

#### atom files

```bash
opendeepcrew atom files skill my-skill
opendeepcrew atom files skill my-skill --json
```

Lists all files in a directory-type atom. Returns `null`/E2002 for single-file atoms. Useful for discovering reference files, scripts, or other resources bundled with an atom.

Example workflow for AI agents:
```bash
# 1. List files to discover structure
opendeepcrew atom files skill nodejs-cli-best-practices
# ["SKILL.md", "references/best-practices.md"]

# 2. Read the main skill
opendeepcrew atom show skill nodejs-cli-best-practices

# 3. Read a referenced file
opendeepcrew atom show skill nodejs-cli-best-practices --file references/best-practices.md
```

#### atom add

From local path:

```bash
opendeepcrew atom add ./my-skill.md --type skill
opendeepcrew atom add ./my-agent/ --type agent
```

From git URL:

```bash
opendeepcrew atom add https://github.com/org/repo/tree/main/skills/foo --type skill
```

Add MCP server:

```bash
opendeepcrew atom add my-mcp --type mcp \
  --command npx \
  --args my-mcp-server \
  --env API_KEY=xxx
```

MCP-specific options:
- `--transport <type>`: stdio (default), http, sse
- `--command <cmd>`: Server start command
- `--args <args...>`: Command arguments
- `--url <url>`: Server URL (http/sse)
- `--env <KEY=VALUE...>`: Environment variables

If target already exists:
- TTY without `--force`: prompts for confirmation
- Non-TTY without `--force`: errors with E0001
- `--force`: overwrites silently

All add operations auto-commit to marketplace git and regenerate registry.

#### atom update (MCP only)

Update an existing MCP server's configuration. Merges with existing config (does not replace).

```bash
opendeepcrew atom update my-mcp --command new-cmd
opendeepcrew atom update my-mcp --args arg1 arg2
opendeepcrew atom update my-mcp --env NEW_KEY=value
opendeepcrew atom update my-mcp --transport http --url https://example.com/mcp
```

Options are the same as `atom add --type mcp`. Only specified fields are updated; unspecified fields keep their current values.

#### atom delete

```bash
opendeepcrew atom delete skill my-skill           # TTY: prompts confirmation
opendeepcrew atom delete skill my-skill --force    # Skip confirmation
```

### plugin

Manage plugins (bundles of atoms).

```bash
opendeepcrew plugin list
opendeepcrew plugin create
opendeepcrew plugin add <name> [options]
opendeepcrew plugin update <name> [options]
opendeepcrew plugin edit [name]
opendeepcrew plugin delete [name] [-f|--force]
```

#### plugin list

```bash
opendeepcrew plugin list          # Table: NAME, DESCRIPTION, ATOMS, MCPS
opendeepcrew plugin list --json   # JSON array
```

#### plugin create (interactive, TTY only)

```bash
opendeepcrew plugin create
```

Step-by-step prompts: name → description → category → select commands → select skills → select agents → select MCPs → confirm.

Non-TTY throws E0001 with guidance to use `plugin add`.

#### plugin add (non-interactive)

```bash
opendeepcrew plugin add my-plugin \
  --description "My plugin" \
  --category development \
  --skills "skill-a,skill-b" \
  --commands "cmd-a" \
  --agents "agent-a" \
  --mcps '{"server-a":{"command":"npx","args":["my-mcp"]}}'
```

Options:
- `--description <desc>`: Plugin description
- `--category <cat>`: Category
- `--skills <list>`: Comma-separated skill names
- `--commands <list>`: Comma-separated command names
- `--agents <list>`: Comma-separated agent names
- `--mcps <json>`: MCP servers as JSON string

#### plugin update (non-interactive, incremental)

Add or remove individual components from an existing plugin without replacing it entirely.

```bash
# Add skills to existing plugin
opendeepcrew plugin update my-plugin --add-skills "new-skill-a,new-skill-b"

# Remove agents
opendeepcrew plugin update my-plugin --remove-agents "old-agent"

# Update metadata
opendeepcrew plugin update my-plugin --description "Updated description" --category "tools"

# Combine operations
opendeepcrew plugin update my-plugin --add-skills "foo" --remove-mcps "bar"
```

Options:
- `--description <desc>`: Update description
- `--category <cat>`: Update category
- `--add-skills <list>`: Add skills (comma-separated)
- `--remove-skills <list>`: Remove skills (comma-separated)
- `--add-commands <list>`: Add commands (comma-separated)
- `--remove-commands <list>`: Remove commands (comma-separated)
- `--add-agents <list>`: Add agents (comma-separated)
- `--remove-agents <list>`: Remove agents (comma-separated)
- `--add-mcps <json>`: Add MCP servers (JSON string)
- `--remove-mcps <list>`: Remove MCP servers (comma-separated)

#### plugin edit (interactive, TTY only)

Interactive editor for existing plugins. Shows current components pre-selected for modification.

```bash
opendeepcrew plugin edit my-plugin    # Edit specific plugin
opendeepcrew plugin edit              # TTY: interactive selection
```

Step-by-step prompts with pre-filled values: description → category → re-select commands/skills/agents/MCPs → confirm.

Non-TTY throws E0001 with guidance to use `plugin update`.

#### plugin delete

```bash
opendeepcrew plugin delete my-plugin           # TTY: confirms
opendeepcrew plugin delete my-plugin --force   # Skip confirmation
opendeepcrew plugin delete                     # TTY: interactive selection
```

### marketplace

Marketplace repository-level operations.

```bash
opendeepcrew marketplace show
opendeepcrew marketplace open
opendeepcrew marketplace sync
opendeepcrew marketplace history [-n <count>]
opendeepcrew marketplace rollback <commit> [-f|--force]
opendeepcrew marketplace regenerate
```

#### marketplace show

Outputs the full registry JSON.

#### marketplace open

Opens the marketplace repository in a detected IDE (Cursor, VS Code, Windsurf, Kiro, WebStorm, IDEA). If multiple IDEs are detected, prompts for selection (TTY).

#### marketplace sync

Pulls from and pushes to the remote marketplace repository (`git pull --rebase && git push`).

#### marketplace history

```bash
opendeepcrew marketplace history          # Last 20 entries
opendeepcrew marketplace history -n 5     # Last 5
opendeepcrew marketplace history --json   # JSON array
```

Returns: hash, message, date for each commit.

#### marketplace rollback

```bash
opendeepcrew marketplace rollback abc123f           # TTY: confirms
opendeepcrew marketplace rollback abc123f --force   # Skip confirmation
```

Performs `git revert`, regenerates registry, and commits.

#### marketplace regenerate

Rebuilds the registry index from current marketplace content and commits.

### workspace

Manage workspaces where AI agents work.

```bash
opendeepcrew workspace list [--no-open]
opendeepcrew workspace open <name>
opendeepcrew workspace update <name> [--permission-mode <mode>] [--agent <agent>]
```

#### workspace list

```bash
opendeepcrew workspace list              # TTY: table + interactive select to open
opendeepcrew workspace list --no-open    # TTY: table only, no interaction
opendeepcrew workspace list --json       # JSON array
```

Columns: NAME, PLUGIN, AGENT, CREATED

#### workspace open

```bash
opendeepcrew workspace open my-workspace
```

Opens workspace directory in detected IDE.

#### workspace update

```bash
opendeepcrew workspace update my-workspace --permission-mode approve-all
opendeepcrew workspace update my-workspace --agent cursor
opendeepcrew workspace update my-workspace --permission-mode approve-reads --agent claude-code
```

Options:
- `--permission-mode <mode>`: Agent permission mode (`approve-all`, `approve-reads`)
- `--agent <agent>`: Agent type (`claude-code`, `cursor`, `kiro`)

At least one option is required.

## Error codes

All errors follow the format: `opendeepcrew v{version} — Error ({code}): {message}`

| Code | Meaning | Typical fix |
|---|---|---|
| E0001 | Requires interactive terminal | Use `--force` for destructive ops, or `--json` for read ops |
| E1001 | Config key not found | Check key name with `config show` |
| E2001 | MARKETPLACE_SOURCE not configured | Run `opendeepcrew config set MARKETPLACE_SOURCE <url>` |
| E2002 | Atom not found | Check name with `atom list --type <type>` |
| E2003 | Invalid atom type | Use: command, agent, skill, hook, mcp |
| E3001 | Workspace not found | Check name with `workspace list --json` |

## `--force` behavior

Destructive operations require confirmation. `--force` (`-f`) skips it.

| Command | Trigger | `--force` behavior |
|---|---|---|
| `atom add` | Target already exists | Overwrite without asking |
| `atom delete` | Before deletion | Delete without asking |
| `plugin delete` | Before deletion | Delete without asking |
| `marketplace rollback` | Before revert | Revert without asking |

In non-TTY without `--force`, these commands throw E0001.

## AI agent integration

The CLI is designed primarily for AI agent use. Key patterns:

### Read operations (no `--force` needed)

```bash
# All of these auto-output JSON in non-TTY
opendeepcrew atom list
opendeepcrew plugin list
opendeepcrew workspace list
opendeepcrew config show
opendeepcrew marketplace history
```

### Write operations (use `--force` for destructive)

```bash
opendeepcrew atom add ./path --type skill --force
opendeepcrew atom delete skill old-skill --force
opendeepcrew plugin add my-plugin --description "desc" --skills "a,b"
opendeepcrew plugin delete my-plugin --force
opendeepcrew marketplace rollback abc123f --force
```

### Incremental update operations (no `--force` needed)

```bash
# Update MCP server config
opendeepcrew atom update my-mcp --command new-cmd --args arg1 arg2

# Add skills to existing plugin
opendeepcrew plugin update my-plugin --add-skills "new-skill"

# Remove agent from plugin
opendeepcrew plugin update my-plugin --remove-agents "old-agent"

# Switch workspace agent
opendeepcrew workspace update my-ws --agent cursor
```

### Chaining operations

```bash
# Add atom, then verify
opendeepcrew atom add ./new-skill.md --type skill --force
opendeepcrew atom show skill new-skill

# Create plugin from atoms, then verify
opendeepcrew plugin add dev-tools --description "Dev tools" --skills "lint,format"
opendeepcrew plugin list
```

### Error handling in scripts

```bash
output=$(opendeepcrew atom show skill my-skill 2>&1)
exit_code=$?
if [ $exit_code -ne 0 ]; then
  # Parse error code from stderr
  echo "$output" | grep -o 'E[0-9]*'
fi
```

## Configuration

Config is stored in `~/.opendeepcrew/.env` with these keys:

- `PORT`: Server port (default: 4000)
- `MARKETPLACE_SOURCE`: Git URL to marketplace repository
- `ENABLED_AGENTS`: Comma-separated list of enabled agents

Config priority: CLI flags > environment variables > config file > defaults

## Filesystem layout

```
~/.opendeepcrew/
  .env                    # Configuration
  workspaces/             # Workspace directories
    <workspace-name>/     # Individual workspace
```

Marketplace is a separate git repository cloned from `MARKETPLACE_SOURCE`.

## Notes

- All marketplace CUD operations (atom add/delete, plugin add/delete, MCP add) are automatically git-committed with descriptive messages
- `marketplace regenerate` rebuilds the registry index from disk; use when registry is corrupted or after manual edits
- `marketplace sync` does `git pull --rebase && git push` — ensure your remote is configured
- `workspace create` and `workspace delete` are intentionally NOT provided in CLI for safety — use Web UI instead
- `marketplace repodir` is intentionally NOT provided — use `marketplace open` to access via IDE
