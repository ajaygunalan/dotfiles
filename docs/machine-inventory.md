# Machine Inventory

Everything installed on the laptop, what it does, when to use it, and whether it stays.
Written 2026-09-08 after the pre-reinstall cleanup. Source of truth for the Ubuntu 26.04 bootstrap.

**Need column:** `core` = I chose it and use it · `default` = comes with Omabuntu, harmless · `optional` = keep, rarely used · `replace` = must change on 26.04

---

## 1. System

| Item | What it is | Usage | Need |
|---|---|---|---|
| Ubuntu 24.04 → 26.04 | the OS, GNOME desktop on Wayland (26.04 is Wayland-only, X11 gone) | everything | core |
| [Omabuntu](https://github.com/omakasui/omabuntu) | community fork of DHH's retired Omakub; turns fresh Ubuntu into a themed dev desktop with one command | run once after install; `omakub` menu for themes | core, wait for its 26.04 release |
| NVIDIA driver 595 + CUDA | RTX 4060 laptop GPU | PyTorch, Drake rendering | core |
| Real-time kernel | PREEMPT_RT for robot control | `sudo apt install ubuntu-realtime` on 26.04, no Pro needed; pick at GRUB; no NVIDIA on that kernel | core |
| [input-remapper](https://github.com/sezanzeb/input-remapper) | remaps the Kensington trackball buttons | preset lives in dotfiles | core |
| autorandr + hotplug scripts | switches monitor layouts on dock/undock | X11-only | replace on 26.04 with a Wayland tool |
| GNOME extensions | Tactile (tiling), Space Bar (workspaces), Just Perfection, Blur my Shell, TopHat (monitor), Undecorate, AlphabeticalAppGrid, auto-move-windows | installed by Omabuntu via `gext` | default, all have GNOME 50 builds |

## 2. Terminal and shell

| Item | What it is | Usage | Need |
|---|---|---|---|
| [Ghostty](https://ghostty.org) | GPU terminal, tabs and splits built in | the only terminal; config repo on GitHub | core |
| [Starship](https://starship.rs) | draws the prompt line (folder, git branch, status) | invisible, runs each time you press Enter | default |
| [bat](https://github.com/sharkdp/bat) | `cat` with colour and line numbers | `bat file.py` | default |
| [eza](https://eza.rocks) | `ls` with colour, icons, git status | aliased to `ls` already; `eza --tree` | default |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | search *inside* files, fast, skips .git | `rg "admittance"`, `rg -i rcm --type py`, `rg "def solve" -A 3` | core |
| [fd](https://github.com/sharkdp/fd) | search file *names* | `fd controller`, `fd -e launch.py`, `fd --changed-within 7d` | core |
| [fzf](https://github.com/junegunn/fzf) | interactive picker over any list | `Ctrl+R` history search, `Ctrl+T` file picker | core |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | `cd` that remembers folders | `z rcm`, `z lect` jumps by fragment | core |
| [btop](https://github.com/aristocratos/btop) | live CPU/RAM/GPU/process dashboard | `btop`, `q` to quit; use when fans spin | core |
| [fastfetch](https://github.com/fastfetch-cli/fastfetch) | system summary card on terminal open | decoration | default |
| [lazygit](https://github.com/jesseduffield/lazygit) | git as a keyboard menu | `lazygit` inside a repo; good for stash conflicts | optional |
| [lazydocker](https://github.com/jesseduffield/lazydocker) | same for Docker | rarely | optional |
| [gum](https://github.com/charmbracelet/gum) | menus/prompts for bash scripts | Omabuntu's installer uses it; write your own scripts in Python instead | default |
| [chafa](https://hpjansson.org/chafa/) | draws an image in the terminal | `chafa figure.png` to peek at a plot | default |
| [ranger](https://ranger.fm) | three-column file manager in the terminal | `ranger`; hjkl move, Enter open, `dd`/`yy`/`pp` cut/copy/paste, `q` quit | core |
| [fresh](https://github.com/sinelaw/fresh) | non-modal terminal editor with multi-cursor, no modes to learn | `fresh file`; **default `$EDITOR`** (git commit messages, crontab open here). Set in `.bashrc`, overrides Omabuntu's nvim | core |
| nano | modeless fallback editor, commands shown on screen | `Ctrl+O` save, `Ctrl+X` exit; present on any Linux box | default |

## 3. Editors and AI tools

| Item | What it is | Usage | Need |
|---|---|---|---|
| [Zed](https://zed.dev) | fast GUI code editor | main editor; C++/Python LSP, git, terminal | core |
| JupyterLab (via uv) | notebooks in the browser | Zed cannot open `.ipynb`; `uv tool install jupyterlab` when needed | optional |
| Claude Code | Anthropic's coding agent, CLI | daily; settings, CLAUDE.md, hooks in `~/.claude` | core |
| [Codex](https://github.com/openai/codex) | OpenAI's coding agent, CLI + ChatGPT desktop app | daily | core |
| Skills | 22 custom skills in `~/dotfiles/skills`, linked into Claude and Codex by `link-skills.sh` | `chapter-to-synced-lecture` stays in gdrive (lecture scripts import it) | core |
| MCP servers | [Context7](https://context7.com) docs, Google Workspace | configured in `~/.claude.json` and `~/.codex/config.toml` (keys inline, move to env) | core |
| [roborev](https://github.com/roborev-dev/roborev) | AI review of git commits | used before, kept | optional |
| Claude Desktop | GUI app | rarely | optional |

## 4. Browsers

| Item | Note | Need |
|---|---|---|
| Google Chrome | passwords and sync live in the Google account | core |
| Chromium | Chrome without Google branding, Omabuntu default | default, could drop |
| Alternatives considered | [Brave](https://brave.com) (Chromium + ad block), [Firefox](https://www.mozilla.org/firefox/), [Zen](https://zen-browser.app), [Helium](https://helium.computer) | not installed |

## 5. Screen, input, and sharing

| Item | What it is | Usage | Need |
|---|---|---|---|
| [gromit-mpx](https://github.com/bk138/gromit-mpx) | draw on the screen while sharing | F8/F9 keys | core |
| [Flameshot](https://flameshot.org) | screenshots with annotation | flatpak, plus own tray indicator script | core |
| [OBS Studio](https://obsproject.com) | screen recording | occasional | optional |
| [Pinta](https://www.pinta-project.com) | simple image editor | flatpak | optional |
| [LocalSend](https://localsend.org) | file transfer laptop ↔ phone over Wi-Fi, AirDrop-style | phone app needed | core |
| wofi | app launcher on Super+Space | **never worked here**: Wayland-only, session is X11 because GDM disabled Wayland for NVIDIA | replace (Omabuntu 1.4 uses Walker) |
| Zoom | meetings | | core |

## 6. Documents, LaTeX, diagrams

| Item | What it is | Need |
|---|---|---|
| TeX Live full + latexmk | LaTeX for the papers | core |
| [Tectonic](https://tectonic-typesetting.github.io) | self-contained LaTeX engine | optional |
| [Typst](https://typst.app) | modern LaTeX alternative | optional |
| [D2](https://d2lang.com) | diagrams from text; used by the walkthrough skill | core |
| [Marp](https://marp.app) | slides from markdown | core |
| [pandoc](https://pandoc.org) | convert between document formats | core |
| [Obsidian](https://obsidian.md) | notes; vaults in gdrive | core |
| [Xournal++](https://xournalpp.github.io) | PDF annotation with a pen | core |
| LibreOffice | docx/xlsx when needed | optional |
| PDF tools | poppler, qpdf, pdftk, pymupdf, pdfplumber, [surya](https://github.com/VikParuchuri/surya) OCR, nano-pdf, jupytext | install per project with uv, not globally | optional |

## 7. Dev toolchains

| Item | What it is | Rule | Need |
|---|---|---|---|
| [uv](https://docs.astral.sh/uv/) | Python packages, venvs, tools | **the only Python tool.** No pip, pipx, conda. One shared GPU venv in `~/scratch`; CPU torch unless GPU needed; `uv cache prune` monthly | core |
| [mise](https://mise.jdx.dev) | Node versions | `node latest`; globals: marp-cli, codex | core |
| Docker | isolated environments | UR simulator (`ursim`) ships only as an image; grouting project container | core |
| gh, git-lfs, direnv, pre-commit, [stow](https://www.gnu.org/software/stow/) | git and dotfiles plumbing | stow links dotfiles into `~` | core |
| build-essential, cmake, clang | C++ for ROS | | core |

## 8. Robotics

| Item | What it is | Need |
|---|---|---|
| ROS 2 Jazzy → **Lyrical Luth** on 26.04 | desktop, ros2_control, ros2_controllers, UR driver + description + MoveIt config, Gazebo bridge, RViz, PlotJuggler, xacro | core (Jazzy has no 26.04 packages) |
| [Drake](https://drake.mit.edu) | dynamics/optimisation, via uv in rcm_qp_drake | core |
| MuJoCo | via uv | optional |
| [Rerun](https://rerun.io) | log viewer for experiments | core |
| PyTorch + CUDA | via uv, GPU wheel only in the scratch venv | core |
| UR simulator | Docker image `universalrobots/ursim_e-series`, pull when needed | optional |

## 9. Media

| Item | Need |
|---|---|
| VLC, mpv, ffmpeg, [yt-dlp](https://github.com/yt-dlp/yt-dlp) | core |
| [Transmission](https://transmissionbt.com) torrent client | core |
| imv image viewer | default |

---

## 10. Removed on 2026-09-08

| Removed | Why |
|---|---|
| Warp, terminator, Alacritty | Ghostty does everything they did |
| Neovim + LazyVim (Omabuntu's `omakub-nvim`) | modal editing not worth learning; fresh is the terminal editor. Omabuntu will reinstall it on 26.04, remove again or skip in the installer |
| Zellij, tmux | did not want multiplexers; Ghostty splits |
| VS Code | replaced by Zed; notebooks via JupyterLab |
| Opera, Blender, MeshLab, geany | unused |
| Calibre | unused |
| Rust toolchain (rustup, cargo, rustc), termula, rust-research-mcp | nothing used them |
| Vibe Typer | dictation tool, found annoying; no voice input now |
| td, sidecar | AI task/dashboard experiments from February, unused |
| onshape-mcp | unused MCP server, config entries removed |
| Global pip packages in `~/.local/lib` (4.7 GB) | belong in project venvs |
| miniconda3, nvm, zig | superseded by uv and mise |
| All Docker containers and images | re-pullable |
| App Center autostart | 667 MB idle; store still works from the menu |
| rt_kernel_build (40 GB), caches (27 GB), TTS venvs (27 GB), movies (21 GB) | regenerable or junk |

## 11. Rules that came out of this

1. **Every file has one home.** Code in git. Documents and data in gdrive. Everything else is disposable.
2. **Home layout:** `~/code` (repos), `~/gdrive` (synced), `~/scratch` (experiments, purge freely), `Downloads` (auto-purge). Nothing loose in `~`.
3. **Repo data lives outside the repo.** `data/` and `runs/` are gitignored symlinks into `~/gdrive/data/<project>`.
4. **uv only.** One shared GPU venv for experiments. Finishing an experiment means deleting its model too (`hf cache delete`).
5. **Skills have one source:** `~/dotfiles/skills`, linked by `link-skills.sh`.
6. **Machine setup is code.** This file plus dotfiles plus an install script is the bootstrap. Secrets go in one age-encrypted file, never in git.
7. **Delete nothing without looking at it first.**

## 12. Open for the 26.04 install

- Partition: EFI + ~100 GB root + rest as `/home`. Decide on deleting Windows.
- autorandr and the hotplug scripts need a Wayland replacement.
- Launcher: Omabuntu's Walker, or bind rofi.
- ROS 2 Lyrical: rebuild admittance and hybrid-force controllers, check API changes.
- Move API keys out of `~/.codex/config.toml` into env vars.
- Still to move: `~/to-gdrive` remainder, rcm_qp_drake `data/` + `runs/` (12 GB), jhu_eirb has no remote, ajay-websites not in git.
