---
name: odc-cli
description: Use odc CLI to manage marketplace atoms/plugins, subscriptions, workspaces, server, and configuration. Covers all commands, output modes, error codes, and AI-agent integration patterns.
---

# odc CLI

## When to use this skill

Use this skill when you need to:

- Manage marketplace content (atoms, plugins, registry, subscriptions)
- List, open, or update workspaces
- Start or configure the odc server
- Read or modify odc configuration
- Integrate odc operations into automation scripts or AI agent workflows

## What odc CLI is

`odc` is a CLI for orchestrating AI coding agent teams. It manages a local marketplace of reusable components (atoms: commands, skills, hooks, agents, MCP servers) and plugins (bundles of atoms), plus workspaces where agents operate.

Core capabilities:

- Marketplace atom CRUD with git version tracking
- Multiple marketplace subscriptions (clone, refresh, enable/disable)
- Plugin assembly from atoms (interactive and non-interactive)
- Workspace listing, detail view, opening in IDE, initialization, reinitialization, and configuration
- Server lifecycle with auto-restart
- Configuration management (env-based, `~/.odc/.env`)
- AI-first design: auto-detects TTY vs non-TTY, outputs JSON for automation
- Structured error codes for programmatic error handling
- `--force` flag on destructive operations for non-interactive use

## Install

```bash
npm install -g @odc/odc
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
odc [global_options] <command> [subcommand] [options] [arguments]
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

Start the odc server.

```bash
odc server
odc server --port 8080
```

Behavior:
- On first run, auto-detects missing config and runs interactive setup (TTY) or generates defaults (non-TTY)
- Spawns server as a child process with auto-restart on exit code 120
- Forwards SIGINT/SIGTERM to child process for graceful shutdown
- Port priority: `--port` flag > `PORT` env var > config file > default 4000

### config

Manage configuration stored in `~/.odc/.env`.

```bash
odc config show              # Display all config
odc config get <key>         # Get single value
odc config set <key> <value> # Set single value
```

Examples:

```bash
# Human-readable
odc config show

# JSON output (non-TTY auto or explicit)
odc config show --json

# Get port
odc config get PORT

# Set marketplace source
odc config set MARKETPLACE_SOURCE https://github.com/org/marketplace.git
```

### atom

Manage marketplace atoms (commands, skills, hooks, agents, MCP servers).

```bash
odc atom show <type> <name> [--file <path>]
odc atom files <type> <name>
odc atom add <source> --type <type> [options] [-f|--force]
odc atom update <name> [options]
odc atom delete <type> <name> [-f|--force]
odc atom set-inject <name> [value] [--remove]
```

To enumerate atoms, use `marketplace show` (full registry JSON) or inspect the marketplace repo; there is no `atom list` subcommand.

Valid types: `command`, `agent`, `skill`, `hook`, `mcp`

#### atom show

```bash
odc atom show skill my-skill
odc atom show mcp my-server
odc atom show skill my-skill --file references/best-practices.md
```

Returns atom content. For MCP, returns the server configuration JSON.

Use `--file <path>` to read a specific sub-file within a directory-type atom. Use `atom files` first to discover available files.

#### atom files

```bash
odc atom files skill my-skill
odc atom files skill my-skill --json
```

Lists all files in a directory-type atom. Returns `null`/E2002 for single-file atoms. Useful for discovering reference files, scripts, or other resources bundled with an atom.

Example workflow for AI agents:
```bash
# 1. List files to discover structure
odc atom files skill nodejs-cli-best-practices
# ["SKILL.md", "references/best-practices.md"]

# 2. Read the main skill
odc atom show skill nodejs-cli-best-practices

# 3. Read a referenced file
odc atom show skill nodejs-cli-best-practices --file references/best-practices.md
```

#### atom add

From local path:

```bash
odc atom add ./my-skill.md --type skill
odc atom add ./my-agent/ --type agent
```

From git URL:

```bash
odc atom add https://github.com/org/repo/tree/main/skills/foo --type skill
```

Add MCP server:

```bash
odc atom add my-mcp --type mcp \
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
odc atom update my-mcp --command new-cmd
odc atom update my-mcp --args arg1 arg2
odc atom update my-mcp --env NEW_KEY=value
odc atom update my-mcp --transport http --url https://example.com/mcp
```

Options are the same as `atom add --type mcp`. Only specified fields are updated; unspecified fields keep their current values.

#### atom delete

```bash
odc atom delete skill my-skill           # TTY: prompts confirmation
odc atom delete skill my-skill --force    # Skip confirmation
```

#### atom set-inject

Set or remove an agent’s inject marker (e.g. `init` for injection behavior). Regenerates the registry and commits to marketplace git.

```bash
odc atom set-inject my-agent init        # set inject to init
odc atom set-inject my-agent --remove    # remove inject marker
```

- `<name>`: agent name
- `[value]`: inject value (e.g. `init`); must supply either this or `--remove`, otherwise E0001

### plugin

Manage plugins (bundles of atoms).

```bash
odc plugin list
odc plugin create
odc plugin add <name> [options]
odc plugin update <name> [options]
odc plugin edit [name]
odc plugin delete [name] [-f|--force]
```

#### plugin list

```bash
odc plugin list          # Table: NAME, DESCRIPTION, ATOMS, MCPS
odc plugin list --json   # JSON array
```

#### plugin create (interactive, TTY only)

```bash
odc plugin create
```

Step-by-step prompts: name → description → category → select commands → select skills → select agents → select MCPs → confirm.

Non-TTY throws E0001 with guidance to use `plugin add`.

#### plugin add (non-interactive)

```bash
odc plugin add my-plugin \
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
odc plugin update my-plugin --add-skills "new-skill-a,new-skill-b"

# Remove agents
odc plugin update my-plugin --remove-agents "old-agent"

# Update metadata
odc plugin update my-plugin --description "Updated description" --category "tools"

# Combine operations
odc plugin update my-plugin --add-skills "foo" --remove-mcps "bar"
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
odc plugin edit my-plugin    # Edit specific plugin
odc plugin edit              # TTY: interactive selection
```

Step-by-step prompts with pre-filled values: description → category → re-select commands/skills/agents/MCPs → confirm.

Non-TTY throws E0001 with guidance to use `plugin update`.

#### plugin delete

```bash
odc plugin delete my-plugin           # TTY: confirms
odc plugin delete my-plugin --force   # Skip confirmation
odc plugin delete                     # TTY: interactive selection
```

### marketplace

Marketplace repository-level operations.

```bash
odc marketplace show
odc marketplace open
odc marketplace sync
odc marketplace history [-n <count>]
odc marketplace rollback <commit> [-f|--force]
odc marketplace regenerate
```

#### marketplace show

Outputs the full registry JSON.

#### marketplace open

Opens the marketplace repository in a detected IDE (Cursor, VS Code, Windsurf, Kiro, WebStorm, IDEA). If multiple IDEs are detected, prompts for selection (TTY).

#### marketplace sync

Pulls from and pushes to the remote marketplace repository (`git pull --rebase && git push`).

#### marketplace history

```bash
odc marketplace history          # Last 20 entries
odc marketplace history -n 5     # Last 5
odc marketplace history --json   # JSON array
```

Returns: hash, message, date for each commit.

#### marketplace rollback

```bash
odc marketplace rollback abc123f           # TTY: confirms
odc marketplace rollback abc123f --force   # Skip confirmation
```

Performs `git revert`, regenerates registry, and commits.

#### marketplace regenerate

Rebuilds the registry index from current marketplace content and commits.

### subscription

Manage named git subscriptions for marketplace sources (clone, pull, enable/disable). Uses the same global output flags as other commands (`--json`, `--pretty`, `--no-color`).

```bash
odc subscription list
odc subscription add --name <name> --repo <repo> [--branch <branch>]
odc subscription remove <name>
odc subscription enable <name>
odc subscription disable <name>
odc subscription refresh [name]
```

#### subscription list

```bash
odc subscription list
odc subscription list --json
```

Human-readable: table columns **NAME**, **REPO**, **BRANCH**, **ENABLED** (`yes` / `no`), **LAST_SYNC** (registry last sync time, or `-` if not cloned yet). If there are no subscriptions, prints a short hint to use `subscription add`.

#### subscription add

```bash
odc subscription add --name my-feed --repo https://github.com/org/marketplace.git
odc subscription add --name my-feed --repo https://github.com/org/marketplace.git --branch main
```

- **Required:** `--name <name>`, `--repo <repo>` (Git remote URL).
- **Optional:** `--branch <branch>` — branch to track (if omitted, list view shows `main` when branch is unset).

After persisting the subscription, the CLI runs an initial **clone** (`refresh`). On success: single success line including “首次 clone” wording. If clone fails: still reports that the subscription was added, then prints a separate **clone failed** error with the message (non-JSON path).

#### subscription remove

```bash
odc subscription remove my-feed
```

Removes the subscription by name.

#### subscription enable / disable

```bash
odc subscription enable my-feed
odc subscription disable my-feed
```

Toggles whether the subscription is enabled.

#### subscription refresh

```bash
odc subscription refresh           # Refresh all subscriptions
odc subscription refresh my-feed # Refresh one by name
```

Pulls latest code for the subscription(s). On error, prints the error message and exits with code **1**.

### workspace

Manage workspaces where AI agents work.

```bash
odc workspace list [--no-open]
odc workspace show <name>
odc workspace open <name>
odc workspace reinit <name>
odc workspace update <name> [--permission-mode <mode>] [--agent <agent>]
```

#### workspace list

```bash
odc workspace list              # TTY: table + interactive select to open
odc workspace list --no-open    # TTY: table only, no interaction
odc workspace list --json       # JSON array
```

Columns: NAME, PLUGIN, AGENT, CREATED

#### workspace show

```bash
odc workspace show my-workspace
odc workspace show my-workspace --json
```

Displays workspace details in a key-value table: Name, Plugin, Agent, Permission Mode, Init Agents, Source, Directory, Created, Updated.

#### workspace open

```bash
odc workspace open my-workspace
```

Opens workspace directory in detected IDE.

#### workspace reinit

```bash
odc workspace reinit my-workspace
```

Re-generates agent configuration files for the workspace. Useful after plugin updates or manual config changes.

#### workspace update

```bash
odc workspace update my-workspace --permission-mode approve-all
odc workspace update my-workspace --agent cursor
odc workspace update my-workspace --permission-mode approve-reads --agent claude-code
```

Options:
- `--permission-mode <mode>`: Agent permission mode (`approve-all`, `approve-reads`)
- `--agent <agent>`: Agent type (`claude-code`, `cursor`, `kiro`)

At least one option is required.

## Error codes

All errors follow the format: `odc v{version} — Error ({code}): {message}`

| Code | Meaning | Typical fix |
|---|---|---|
| E0001 | Requires interactive terminal | Use `--force` for destructive ops, or `--json` for read ops |
| E1001 | Config key not found | Check key name with `config show` |
| E2001 | MARKETPLACE_SOURCE not configured | Run `odc config set MARKETPLACE_SOURCE <url>` |
| E2002 | Atom not found | Inspect registry with `marketplace show --json` or verify type/name |
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
odc marketplace show
odc plugin list
odc workspace list
odc workspace show my-workspace
odc config show
odc marketplace history
odc subscription list
```

### Write operations (use `--force` for destructive)

```bash
odc atom add ./path --type skill --force
odc atom delete skill old-skill --force
odc plugin add my-plugin --description "desc" --skills "a,b"
odc plugin delete my-plugin --force
odc marketplace rollback abc123f --force
odc subscription add --name feed --repo https://github.com/org/repo.git
odc subscription refresh feed
```

### Incremental update operations (no `--force` needed)

```bash
# Update MCP server config
odc atom update my-mcp --command new-cmd --args arg1 arg2

# Set or clear agent inject marker
odc atom set-inject my-agent init
odc atom set-inject my-agent --remove

# Add skills to existing plugin
odc plugin update my-plugin --add-skills "new-skill"

# Remove agent from plugin
odc plugin update my-plugin --remove-agents "old-agent"

# Switch workspace agent
odc workspace update my-ws --agent cursor
```

### Chaining operations

```bash
# Add atom, then verify
odc atom add ./new-skill.md --type skill --force
odc atom show skill new-skill

# Create plugin from atoms, then verify
odc plugin add dev-tools --description "Dev tools" --skills "lint,format"
odc plugin list
```

### Error handling in scripts

```bash
output=$(odc atom show skill my-skill 2>&1)
exit_code=$?
if [ $exit_code -ne 0 ]; then
  # Parse error code from stderr
  echo "$output" | grep -o 'E[0-9]*'
fi
```

## Configuration

Config is stored in `~/.odc/.env` with these keys:

- `PORT`: Server port (default: 4000)
- `MARKETPLACE_SOURCE`: Git URL to marketplace repository
- `ENABLED_AGENTS`: Comma-separated list of enabled agents

Config priority: CLI flags > environment variables > config file > defaults

## Filesystem layout

```
~/.odc/
  .env                    # Configuration
  workspaces/             # Workspace directories
    <workspace-name>/     # Individual workspace
```

Marketplace is a separate git repository cloned from `MARKETPLACE_SOURCE`.

## Notes

- All marketplace CUD operations (atom add/delete/set-inject, plugin add/delete, MCP add) are automatically git-committed with descriptive messages
- `marketplace regenerate` rebuilds the registry index from disk; use when registry is corrupted or after manual edits
- `marketplace sync` does `git pull --rebase && git push` — ensure your remote is configured
- `workspace create` and `workspace delete` are intentionally NOT provided in CLI for safety — use Web UI instead
- `marketplace repodir` is intentionally NOT provided — use `marketplace open` to access via IDE
