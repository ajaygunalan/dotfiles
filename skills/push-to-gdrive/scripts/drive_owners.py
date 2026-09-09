#!/usr/bin/env python3
"""Google Drive ownership tools, authenticated with rclone's saved OAuth token.

    drive_owners.py list [FOLDER_ID]                 tree of files with their owners (default: root)
    drive_owners.py transfer EMAIL FILE_ID...        send an ownership-transfer request per file
    drive_owners.py bulk EMAIL FILE_ID...            same, batched (100 per API call), grants writer first if needed

Ownership transfer between personal @gmail.com accounts works by setting
pendingOwner=true; the recipient gets an email and must accept.

Dependencies:  uv run --with google-api-python-client --with google-auth drive_owners.py ...
Used once in April 2026 to consolidate Drive accounts.
"""

import configparser
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

RCLONE_CONF = Path.home() / ".config/rclone/rclone.conf"


def service(remote="gdrive"):
    config = configparser.ConfigParser()
    config.read(RCLONE_CONF)
    token = json.loads(config[remote]["token"])
    creds = Credentials(
        token=token.get("access_token"),
        refresh_token=token["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config[remote]["client_id"],
        client_secret=config[remote]["client_secret"],
    )
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds)


def name_of(svc, file_id):
    return svc.files().get(fileId=file_id, fields="name").execute().get("name", file_id)


def cmd_list(svc, folder_id="root", indent=0):
    fields = "nextPageToken,files(id,name,mimeType,owners(displayName,emailAddress))"
    page_token = None
    while True:
        resp = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields=fields, pageSize=100, pageToken=page_token,
            includeItemsFromAllDrives=True, supportsAllDrives=True,
        ).execute()
        for f in resp.get("files", []):
            owners = ", ".join(f"{o['displayName']} <{o['emailAddress']}>" for o in f.get("owners", [])) or "unknown"
            is_folder = f["mimeType"] == "application/vnd.google-apps.folder"
            print("  " * indent + ("[dir]  " if is_folder else "[file] ") + f"{f['name']}  [{owners}]")
            if is_folder:
                cmd_list(svc, f["id"], indent + 1)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def cmd_transfer(svc, email, file_ids):
    ok = fail = 0
    for fid in file_ids:
        try:
            svc.permissions().create(
                fileId=fid,
                body={"type": "user", "role": "writer", "emailAddress": email, "pendingOwner": True},
                sendNotificationEmail=True, transferOwnership=False, fields="id",
            ).execute()
            print(f"sent      {name_of(svc, fid)}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAILED    {name_of(svc, fid)}: {e}")
            fail += 1
    print(f"\n{ok} sent, {fail} failed")


def cmd_bulk(svc, email, file_ids):
    def permission_id(fid):
        perms = svc.permissions().list(fileId=fid, fields="permissions(id,emailAddress)").execute()
        for p in perms.get("permissions", []):
            if p.get("emailAddress", "").lower() == email.lower():
                return p["id"]
        return None

    todo = []
    for fid in file_ids:
        name = name_of(svc, fid)
        pid = permission_id(fid)
        if pid is None:
            pid = svc.permissions().create(
                fileId=fid, body={"type": "user", "role": "writer", "emailAddress": email},
                sendNotificationEmail=False, fields="id",
            ).execute()["id"]
            print(f"granted writer   {name}")
        todo.append((fid, name, pid))

    names = {}

    def done(request_id, response, exception):
        n = names[request_id]
        print(f"FAILED    {n}: {exception}" if exception else f"pending   {n}")

    for start in range(0, len(todo), 100):
        batch = svc.new_batch_http_request(callback=done)
        for i, (fid, name, pid) in enumerate(todo[start:start + 100]):
            rid = str(start + i)
            names[rid] = name
            batch.add(
                svc.permissions().update(
                    fileId=fid, permissionId=pid, body={"pendingOwner": True, "role": "writer"},
                    transferOwnership=False, fields="id",
                ),
                request_id=rid,
            )
        batch.execute()
    print(f"\n{len(todo)} requests sent")


def main(argv):
    if len(argv) < 2 or argv[1] not in {"list", "transfer", "bulk"}:
        print(__doc__)
        sys.exit(1)
    svc = service()
    if argv[1] == "list":
        cmd_list(svc, argv[2] if len(argv) > 2 else "root")
    else:
        if len(argv) < 4:
            print(__doc__)
            sys.exit(1)
        (cmd_transfer if argv[1] == "transfer" else cmd_bulk)(svc, argv[2], argv[3:])


if __name__ == "__main__":
    main(sys.argv)
