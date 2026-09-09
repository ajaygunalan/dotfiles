---
name: pdf-tools
description: Housekeeping for folders of PDFs, e.g. paper_inbox — rename PDFs by their real title (Claude reads the first pages), extract a PDF to markdown with marker, strip a References section from markdown, normalize file names to lowercase_underscore. Use for "tidy paper_inbox", "rename these PDFs", "extract this paper to markdown", "clean up file names".
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

All scripts live in `scripts/`. Run them from the folder being tidied. Ask before any rename touches more than a handful of files.

| Task | Command | Notes |
|---|---|---|
| Rename PDFs by title | `python3 scripts/rename_by_title.py [DIR]` | reads the first 3 pages, asks `claude -p` for the title, confirms each rename |
| PDF to markdown | `scripts/extract.sh FILE.pdf` | uses marker; install once with `uv tool install marker-pdf`. Output folder named from the document title |
| Strip references | `scripts/strip_references.sh FILE.md` | writes `FILE_clean.md` with everything from the References/Bibliography heading onward removed |
| Normalize names | `python3 scripts/normalize_names.py [DIR]` | lowercase_underscore for files and folders, git-aware (uses `git mv` inside a repo) |

Book-to-chapter splitting is not here; that belongs to the `chapter-to-synced-lecture` skill.
