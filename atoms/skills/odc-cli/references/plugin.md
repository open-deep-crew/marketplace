# plugin — Manage Plugins

Manage plugins (bundles of atoms).

## plugin list

```bash
odc plugin list --json
```

Returns ALL plugins (local + subscription). Each plugin has `source.type` ("local" or "subscription") and optionally `source.name`.

## plugin create (interactive, TTY only)

```bash
odc plugin create
```

Non-TTY throws E0001 with guidance to use `plugin add`.

## plugin add (non-interactive)

```bash
odc plugin add my-plugin \
  --description "My plugin" \
  --category development \
  --skills "skill-a,skill-b" \
  --commands "cmd-a" \
  --agents "agent-a" \
  --mcps '{"server-a":{"command":"npx","args":["my-mcp"]}}'
```

## plugin update (non-interactive, incremental)

```bash
odc plugin update my-plugin --add-skills "new-skill-a,new-skill-b"
odc plugin update my-plugin --remove-agents "old-agent"
odc plugin update my-plugin --description "Updated" --category "tools"
odc plugin update my-plugin --add-skills "foo" --remove-mcps "bar"
```

Options:
- `--description <desc>` / `--category <cat>`: Update metadata
- `--add-skills` / `--remove-skills`: Add/remove skills (comma-separated)
- `--add-commands` / `--remove-commands`: Add/remove commands
- `--add-agents` / `--remove-agents`: Add/remove agents
- `--add-mcps` / `--remove-mcps`: Add/remove MCP servers

## plugin edit (interactive, TTY only)

```bash
odc plugin edit my-plugin
```

Non-TTY throws E0001 with guidance to use `plugin update`.

## plugin merge

```bash
odc plugin merge <local-plugin-name> --source <subscription-name>
```

Batch-copy atoms from a subscription plugin into the local marketplace. Existing atoms with same name are force-overwritten. Hooks are not copied. Auto-runs regenerateRegistry + git commit.

## plugin delete

```bash
odc plugin delete my-plugin --force
```
