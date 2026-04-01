# atom — Manage Marketplace Atoms

Manage marketplace atoms (commands, skills, hooks, agents, MCP servers).

Valid types: `command`, `agent`, `skill`, `hook`, `mcp`

## atom show

```bash
odc atom show <type> <name>
odc atom show skill my-skill --file references/best-practices.md
```

Returns atom content. Use `--file <path>` to read a specific sub-file within a directory-type atom.

## atom files

```bash
odc atom files <type> <name>
```

Lists all files in a directory-type atom. Returns `null`/E2002 for single-file atoms.

## atom add

```bash
# From local path
odc atom add ./my-skill.md --type skill
odc atom add ./my-agent/ --type agent

# From git URL
odc atom add https://github.com/org/repo/tree/main/skills/foo --type skill

# Add MCP server
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
- `--force`: overwrites silently
- Without `--force` in non-TTY: errors with E0001

All add operations auto-commit to marketplace git and regenerate registry.

## atom update (MCP only)

```bash
odc atom update my-mcp --command new-cmd
odc atom update my-mcp --args arg1 arg2
odc atom update my-mcp --env NEW_KEY=value
```

Merges with existing config (does not replace). Only specified fields are updated.

## atom delete

```bash
odc atom delete <type> <name> --force
```

## atom set-inject

```bash
odc atom set-inject <agent-name> init        # set inject to init
odc atom set-inject <agent-name> --remove    # remove inject marker
```

Regenerates registry and commits to marketplace git.
