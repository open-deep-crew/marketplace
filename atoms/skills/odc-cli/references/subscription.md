# subscription — Manage Git Subscriptions

Manage named git subscriptions for marketplace sources (clone, pull, enable/disable).

## subscription list

```bash
odc subscription list --json
```

Columns: NAME, REPO, BRANCH, ENABLED, LAST_SYNC

## subscription add

```bash
odc subscription add --name <name> --repo <git-url> [--branch <branch>]
```

After persisting, runs an initial clone (refresh).

## subscription remove

```bash
odc subscription remove <name>
```

## subscription enable / disable

```bash
odc subscription enable <name>
odc subscription disable <name>
```

## subscription refresh

```bash
odc subscription refresh           # All subscriptions
odc subscription refresh <name>    # Specific one
```

Pulls latest code for the subscription(s).
