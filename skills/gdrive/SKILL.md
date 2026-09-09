---
name: gdrive
description: Google Drive operations for the local gdrive folder — push to Drive with rclone (scope decided by the current directory), and Drive account admin (list file owners, transfer ownership to another account). Use for "push to gdrive", "back up gdrive", "who owns these Drive files", "transfer Drive ownership".
allowed-tools:
  - Bash
  - AskUserQuestion
---

## Push to Drive

The local gdrive folder is `~/gdrive` (a symlink to the real location). Scope comes from the current directory:

1. `pwd`.
2. If cwd is the gdrive root: source = the root, dest = `gdrive:`.
3. If cwd is under the root: source = that subfolder, dest = `gdrive:<relative path>`.
4. If cwd is outside gdrive: ask whether to push the whole drive or a named folder.

Say what will be pushed before running:

```bash
rclone copy <source> <dest> \
  --exclude-from ~/gdrive/.rcloneignore \
  --transfers 3 --verbose --stats-one-line --stats 10s
```

`copy`, never `sync`: uploads new and changed files, never deletes on Drive. Report files transferred, size, and time.

## Drive ownership admin

`scripts/drive_owners.py` authenticates with rclone's saved token. Run with uv so the Google client libraries are pulled on demand:

```bash
uv run --with google-api-python-client --with google-auth scripts/drive_owners.py list            # tree with owners
uv run --with google-api-python-client --with google-auth scripts/drive_owners.py transfer EMAIL ID...
uv run --with google-api-python-client --with google-auth scripts/drive_owners.py bulk EMAIL ID...  # batched
```

Transfers between personal Gmail accounts set `pendingOwner`; the recipient must accept from their email. Used in April 2026 to consolidate accounts.
