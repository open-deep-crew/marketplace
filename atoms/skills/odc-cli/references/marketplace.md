# marketplace — Repository-Level Operations

## marketplace show

Outputs the full registry JSON.

## marketplace open

Opens marketplace repository in detected IDE (Cursor, VS Code, Windsurf, Kiro, WebStorm, IDEA).

## marketplace sync

`git pull --rebase && git push` on marketplace repository.

## marketplace history

```bash
odc marketplace history          # Last 20 entries
odc marketplace history -n 5     # Last 5
odc marketplace history --json
```

Returns: hash, message, date for each commit.

## marketplace rollback

```bash
odc marketplace rollback <commit> --force
```

Performs `git revert`, regenerates registry, and commits.

## marketplace regenerate

Rebuilds registry index from current marketplace content and commits. Use when registry is corrupted or after manual edits.
