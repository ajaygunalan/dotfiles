#!/bin/bash
# Link every skill in ~/dotfiles/skills into the folders each tool reads.
# Claude Code reads ~/.claude/skills; Codex reads ~/.agents/skills; OpenCode reads both.
# One symlink per skill directory (Codex ignores symlinked SKILL.md files, follows symlinked dirs).
set -u
SK="$(cd "$(dirname "$0")" && pwd)/skills"
for target in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$target"
  for s in "$SK"/*/; do
    n=$(basename "$s")
    ln -sfn "$SK/$n" "$target/$n"
  done
done
# Skills that live elsewhere on purpose (large, or referenced by other pipelines):
EXTRA=(
  "$HOME/gdrive/lecture/chapter-to-synced-lecture"
)
for e in "${EXTRA[@]}"; do
  [ -d "$e" ] || continue
  for target in "$HOME/.claude/skills" "$HOME/.agents/skills"; do ln -sfn "$e" "$target/$(basename "$e")"; done
done
echo "linked $(ls -1 "$SK" | wc -l) skills + ${#EXTRA[@]} external into ~/.claude/skills and ~/.agents/skills"
