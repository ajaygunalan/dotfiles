# Omabuntu Productivity Guide

## The Big Picture

Omabuntu turns your Ubuntu into a keyboard-driven workstation. The core idea: **your hands stay on the keyboard, you stop reaching for the mouse.**

You only need to learn three things, in this order:

1. **Navigate** — launch apps, switch workspaces, arrange windows
2. **Terminal** — split panes, switch tabs, use shell shortcuts
3. **Customize** — change themes, install apps, update

---

## 1. Navigate — Launch, Switch, Arrange

### Launch Anything

| Shortcut | What it does |
|---|---|
| `Windows + Space` | **App launcher** — type any app name, hit Enter |
| `Windows + Enter` | Open terminal |
| `Ctrl + Alt + T` | Open terminal (alternate) |
| `Windows + Shift + B` | Open browser |
| `Windows + Shift + F` | Open file manager |
| `Windows + Shift + N` | Open editor (Neovim) |
| `Windows + Shift + M` | Open Spotify |

### Switch Workspaces

You have 6 workspaces — think of them as separate desks.

| Shortcut | What it does |
|---|---|
| `Windows + 1` through `Windows + 6` | Switch to workspace 1–6 |
| `Windows + Shift + 1` through `Windows + Shift + 6` | Move current window to workspace 1–6 |

**Suggested layout:**

| Workspace | Use for |
|---|---|
| 1 | Terminal (coding) |
| 2 | VS Code |
| 3 | Browser |
| 4 | Obsidian (notes) |
| 5 | Communication (WhatsApp, ChatGPT) |
| 6 | Misc |

### Arrange Windows

**Quick snap:**

| Shortcut | What it does |
|---|---|
| `Windows + Left` | Snap to left half |
| `Windows + Right` | Snap to right half |
| `Windows + Up` | Maximize |
| `Windows + Down` | Un-maximize / restore |
| `Windows + W` | Close window |
| `Windows + Backspace` | Resize window (drag edges) |
| `Shift + F11` | Toggle fullscreen |

**Precise tiling with Tactile:**

Press `Windows + T` — a grid overlay appears. Press a letter to snap the window:

```
 ┌─────┬─────┬─────┬─────┐
 │  Q  │  W  │  E  │  R  │
 ├─────┼─────┼─────┼─────┤
 │  A  │  S  │  D  │  F  │
 └─────┴─────┴─────┴─────┘
```

| What to press | Result |
|---|---|
| Single key (e.g., `Q`) | Quarter of screen (top-left) |
| Two adjacent keys (e.g., `Q` + `W`) | Half of screen (top-left half) |
| `Q` + `W` + `A` + `S` | Left half (full height) |
| `Space` | Move window to other monitor |
| `Escape` | Cancel |

### Dock Pinned Apps

| Shortcut | What it does |
|---|---|
| `Alt + 1` through `Alt + 9` | Open/switch to pinned app 1–9 on the dock |

---

## 2. Terminal — Alacritty + Zellij

When you press `Windows + Enter`, Alacritty opens with Zellij inside. Zellij gives you tabs and split panes without leaving the terminal.

### Everyday Pane & Tab Shortcuts

These work at all times — no mode switching needed:

| Shortcut | What it does |
|---|---|
| `Alt + N` | **New pane** (split) |
| `Alt + Arrow keys` | **Move between panes** |
| `Alt + Left / Right` | **Switch tabs** |
| `Alt + F` | Toggle floating pane |
| `Alt + +` / `Alt + -` | Resize pane bigger / smaller |
| `Alt + [` / `Alt + ]` | Cycle through layouts |

### Advanced Zellij (press `Ctrl + G` first to enter normal mode)

| Press | Then press | What it does |
|---|---|---|
| `t` | `n` | New tab |
| `t` | `x` | Close tab |
| `t` | `r` | Rename tab |
| `t` | `1–9` | Jump to tab by number |
| `p` | `n` | New pane |
| `p` | `x` | Close pane |
| `p` | `r` | New pane to the right |
| `p` | `d` | New pane below |
| `s` | `j / k` | Scroll up / down |
| `s` | `f` | Search in scrollback |
| | `Esc` | Back to normal typing |

### Shell Shortcuts

**Navigation:**

| Type | What it does |
|---|---|
| `..` | Go up one directory |
| `...` | Go up two directories |
| `....` | Go up three directories |
| `ff` | Fuzzy find files with preview |
| `eff` | Fuzzy find and open in editor |

**File listing:**

| Type | What it does |
|---|---|
| `ls` | Pretty file listing with icons |
| `lsa` | Including hidden files |
| `lt` | Tree view (2 levels deep) |
| `lta` | Tree view including hidden files |

**Quick commands:**

| Type | What it does |
|---|---|
| `n` | Open Neovim |
| `g` | Short for `git` |
| `d` | Short for `docker` |
| `lzg` | Open Lazygit (visual git interface) |
| `lzd` | Open Lazydocker (visual Docker interface) |
| `gcm "msg"` | `git commit -m "msg"` |
| `gcam "msg"` | `git commit -a -m "msg"` |
| `open file` | Open any file with its default app |

---

## 3. Customize — Themes, Apps, Updates

### Change Theme (syncs everything at once)

One command changes your terminal, VS Code, Obsidian, wallpaper, and GNOME accent color:

```bash
omakub-theme-list                # see all 19 themes
omakub-theme-set tokyo-night     # apply one
```

Or use keyboard shortcuts:

| Shortcut | What it does |
|---|---|
| `Windows + Shift + Ctrl + Space` | Open theme picker |
| `Windows + Ctrl + Space` | Cycle wallpapers within current theme |

### Install & Remove Apps

```bash
omakub-app-install visual-studio-code
omakub-app-install obsidian
omakub-app-install spotify
omakub-app-install 1password
omakub-app-install discord
omakub-app-install zoom
omakub-app-install firefox
omakub-app-install ollama

omakub-app-remove discord
```

### Install Dev Environments

```bash
omakub-install-dev-env python
omakub-install-dev-env node
omakub-install-dev-env ruby
omakub-install-dev-env go
omakub-install-dev-env rust
```

### Change Font

```bash
omakub-font-list                 # see available fonts
omakub-font-set "JetBrains Mono" # change font everywhere
omakub-font-size-set 14          # change size
```

### Update Omabuntu

```bash
omakub-update
```

### Full Visual Menu

```bash
omakub-menu
```

Or press `Alt + Windows + Space` for the keyboard shortcut.

---

## 4. Utilities

### Screenshots

| Shortcut | What it does |
|---|---|
| `Print Screen` | GNOME screenshot tool |
| `Ctrl + Print Screen` | Flameshot (annotate, crop, draw) |

### Screen Annotation (Gromit-MPX)

Draw on your screen during presentations:

| Shortcut | What it does |
|---|---|
| `F9` | Start / stop drawing |
| `Shift + F9` | Clear all drawings |
| `F8` | Undo last stroke |
| `Shift + F8` | Redo |
| `Alt + F9` | Quit Gromit-MPX |

### Quick Launchers

| Shortcut | Opens |
|---|---|
| `Windows + Shift + T` | System monitor (btop) |
| `Windows + Shift + D` | Docker manager (lazydocker) |
| `Windows + Shift + A` | ChatGPT |
| `Windows + Shift + Y` | YouTube |
| `Windows + Shift + H` | GitHub |
| `Windows + Shift + Alt + G` | WhatsApp |
| `Windows + Shift + Alt + B` | Incognito browser |
| `Windows + Ctrl + N` | Toggle night light |
| `Windows + Escape` | System menu (lock, logout, reboot, shutdown) |

### Caps Lock = Compose Key

Caps Lock is remapped for typing special characters. Hold Caps Lock, then type a sequence:

| Sequence | Result |
|---|---|
| `'` then `e` | accent (e.g. cafe) |
| `-` then `>` | arrow |
| `o` then `c` | copyright |

---

## Top 10 — Memorize These First

| # | Shortcut | What it does |
|---|---|---|
| 1 | `Windows + Space` | Launch any app |
| 2 | `Windows + 1–6` | Switch workspace |
| 3 | `Windows + Shift + 1–6` | Move window to workspace |
| 4 | `Windows + T` | Tile window (grid overlay) |
| 5 | `Windows + W` | Close window |
| 6 | `Windows + Enter` | Open terminal |
| 7 | `Alt + N` | Split terminal pane |
| 8 | `Alt + Arrows` | Move between panes |
| 9 | `omakub-theme-set <name>` | Change theme everywhere |
| 10 | `omakub-menu` | Full management menu |
