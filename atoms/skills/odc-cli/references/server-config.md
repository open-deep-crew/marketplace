# server & config

## server

Start the odc server.

```bash
odc server
odc server --port 8080
```

- On first run, auto-detects missing config and runs interactive setup (TTY) or generates defaults (non-TTY)
- Spawns server as a child process with auto-restart on exit code 120
- Port priority: `--port` flag > `PORT` env var > config file > default 4000

## config

Manage configuration stored in `~/.odc/.env`.

```bash
odc config show              # Display all config
odc config get <key>         # Get single value
odc config set <key> <value> # Set single value
```

Config keys:
- `PORT`: Server port (default: 4000)
- `MARKETPLACE_SOURCE`: Git URL to marketplace repository
- `ENABLED_AGENTS`: Comma-separated list of enabled agents

Config priority: CLI flags > environment variables > config file > defaults
