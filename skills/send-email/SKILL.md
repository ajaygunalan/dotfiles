---
name: send-email
description: >
  REQUIRED whenever sending, drafting, replying to, or forwarding email on Ajay's
  behalf, from any account. Covers the never-send-without-approval rule, which
  account to send from, the signature, and how to attach local files (the only
  working route is the local google-workspace MCP). Triggers: send an email, reply
  to, forward, draft a mail, attach my CV/resume, follow up with, write to
  <person>, Gmail, inbox, application follow-up.
---

# Sending email as Ajay

## The hard rule

**Never send without explicit approval.** Show the complete draft — From, To/Cc,
Subject, body, attachment filenames — as text in the terminal, then wait. "Send it"
means send it; anything else is another revision round. Replies and forwards count.

Always show the **Subject**, and call it out when Ajay dictated the body without
naming one — he reviews body wording closely and can skim past a subject you
invented on his behalf.

## Which account

| Kind of mail | Send as | Mailbox (`user_google_email`) |
|---|---|---|
| Professional, new outreach, job applications | ajay@ajaygunalan.com | ajay.gunalan.work@gmail.com |
| Replies on an application already running through Proton | ajay.gunalan@pm.me | forwards to ajay@ajaygunalan.com |
| Personal | ajaygunalan1995@gmail.com | ajaygunalan1995@gmail.com |

`ajay@ajaygunalan.com` is a Gmail "Send mail as" alias on the work mailbox — pass it
as `from_email` with `user_google_email` set to the work address.

If Ajay names an account that conflicts with this table, **follow his instruction**
and flag the mismatch once in the final summary. Don't re-ask every revision round.

## Signature

Close every email with exactly:

```
Warm regards,
Ajay Gunalan
ajaygunalan.com
```

Pass `include_signature: false` — the Gmail-side signature differs, and leaving it
on produces a double sign-off.

## Attachments — only the local MCP works

The claude.ai Gmail connector (`mcp__claude_ai_Gmail__*`) takes attachments **only**
as inline base64. A 79 KB PDF is ~105 KB encoded, which cannot be carried into a
tool call reliably — one wrong character silently corrupts the file the recipient
opens. **Never attach that way.**

Use the local `google-workspace` MCP, which attaches by file path:

```
mcp__google-workspace__send_gmail_message(
  user_google_email = "<sending mailbox>",
  to = "...", subject = "...", body = "...",
  include_signature = false,
  attachments = [{"path": "/home/ajay/Downloads/file.pdf", "mime_type": "application/pdf"}],
)
```

Constraints, each learned by hitting it:

- The path must sit under a directory listed in `ALLOWED_FILE_DIRS` in
  `~/.config/google-workspace-mcp/env` — currently `~/Downloads` and `~/Documents`.
  Anywhere else is refused, including `~` itself and the MCP's own data directory.
- Adding a directory there requires **restarting Claude Code** to take effect.
- `localhost` / `127.0.0.1` URLs are rejected, so serving the file locally is not a
  workaround.
- Both accounts are authorized in the local MCP; credentials sit in
  `~/.google_workspace_mcp/credentials/`.

Call `send_gmail_message` directly rather than `draft_gmail_message` then send.
Creating a draft to "test" the attachment leaves a duplicate in Drafts, and the
claude.ai connector lacks the scope to trash it.

## Get context before drafting

Search the relevant mailbox first — the thread usually names the role, the person,
and what was already promised, which beats making Ajay repeat it.
`mcp__claude_ai_Gmail__search_threads` for personal,
`mcp__google-workspace__search_gmail_messages` for work.

## Style

Ajay dictates by voice, so input arrives with restarts and mangled words.
Reconstruct the intent, write it tight, and flag any word you had to guess — "for
the referrals" turned out to be "for your reference". Short beats padded: for a
follow-up after a call, three sentences is the target. Keep his own phrasing where
it already works instead of rewriting it into corporate register.
