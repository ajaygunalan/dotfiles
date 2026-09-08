# All the default Omabuntu aliases and functions
# (don't mess with these directly, just overwrite them here!)
source ~/.local/share/omakub/default/bash/rc

# Add your own exports, aliases, and functions here.
#
# Make an alias for invoking commands you use constantly
# alias p='python'
# alias cx="claude --permission-mode=plan --allow-dangerously-skip-permissions"
#
# Use VSCode instead of neovim as your default editor
# export EDITOR="code"
#
# Set a custom prompt with the directory revealed (alternatively use https://starship.rs)
# PS1="\W \[\e]0;\w\a\]$PS1"
export TERMINAL=ghostty

# secure-askpass for sudo in Claude Code
export SUDO_ASKPASS="$HOME/.local/share/secure-askpass/askpass"

# robot-learning lab runner: `rl <N> <args...>` from anywhere — no cd, no UV_PROJECT_ENVIRONMENT prefix.
# e.g.  rl 4 src/hw1_imitation/train.py --policy-type flow
rl() {
  local root="$HOME/gdrive/_robo_thesis/repositories/robot-learning"
  local n; printf -v n '%02d' "$1" 2>/dev/null || { echo "rl: need a lab number 1-10"; return 1; }
  shift
  local match=("$root/${n}-"*/)            # glob the lab dir (avoids aliased ls)
  [ -d "${match[0]}" ] || { echo "rl: no lab matching '$n'"; return 1; }
  local lab; lab=$(basename "${match[0]}")
  ( builtin cd "$root/$lab" && UV_PROJECT_ENVIRONMENT="$HOME/.venvs/robot-learning/$lab" uv run "$@" )
}

# ElevenLabs narrator for chapter-to-synced-lecture (Mark)
export ELEVENLABS_VOICE_ID=8sGzMkj2HZn6rYwGx6G0   # thomas (lecture default)

# editor: fresh (non-modal); overrides Omabuntu default of nvim
export EDITOR="fresh"
export SUDO_EDITOR="fresh"
