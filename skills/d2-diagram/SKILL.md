---
name: d2-diagram
description: Create, edit, render, and debug D2 diagrams (https://d2lang.com). Architecture maps, code-level class and sequence diagrams, data models, grids, multi-board compositions. Triggers on "diagram", "visualize", "draw the architecture", "show the flow", "explain this file visually", "d2", or any .d2 file.
---

# D2 Diagram Skill

How to write D2 that renders correctly on the installed binary and reads well. The style rules here are mandatory. The syntax lives in `references/`, verified line by line against d2 **v0.7.1** (dagre and ELK bundled; TALA is not installed, so anything the docs mark TALA-only will fail here).

Other skills that produce D2 (`walkthrough`, `index-codebase`, `index-sync`) follow these rules.

## 1. Skeleton

Every file starts like this. ELK, theme 0, `direction: down`, one class per role, palette comment kept in sync with the classes.

```d2
vars: {
  d2-config: {
    layout-engine: elk
    theme-id: 0
  }
}

direction: down

# One color per role:
#   client   purple   the caller (browser, CLI, user)
#   core     blue     the primary component
#   model    teal     the component that owns state
#   native   yellow   hardware-facing or external processes
#   files    green    files, results, outputs
#   neutral  grey     shared vocabulary, test doubles, spacers
#   danger   red      errors and rejected paths
classes: {
  heading: {shape: text; style: {font-size: 24; bold: true; font-color: "#334155"}}
  client: {style: {fill: "#F3E8FF"; stroke: "#9333EA"; font-color: "#6B21A8"; border-radius: 8; font-size: 18}}
  core: {style: {fill: "#DBEAFE"; stroke: "#2563EB"; font-color: "#1E40AF"; border-radius: 8; font-size: 18}}
  model: {style: {fill: "#CCFBF1"; stroke: "#0D9488"; font-color: "#115E59"; border-radius: 8; font-size: 18}}
  native: {style: {fill: "#FEF3C7"; stroke: "#D97706"; font-color: "#92400E"; border-radius: 8; font-size: 18}}
  files: {style: {fill: "#DCFCE7"; stroke: "#16A34A"; font-color: "#166534"; border-radius: 8; font-size: 18}}
  neutral: {style: {fill: "#F1F5F9"; stroke: "#64748B"; font-color: "#334155"; border-radius: 8; font-size: 18}}
  danger: {style: {fill: "#FFE4E6"; stroke: "#E11D48"; font-color: "#9F1239"; border-radius: 8; font-size: 18}}
  group: {style: {fill: "#FFFFFF"; stroke: "#64748B"; font-color: "#334155"; border-radius: 8; stroke-dash: 5; font-size: 18}}
}

title: "The idea in one sentence" {class: heading; near: top-center}
```

## 2. Which structure for which idea

| You want to show | Use | Reference |
|---|---|---|
| Components and who talks to whom | containers + edges, one class per role | 01 §2–4 |
| A file at code level: classes with their methods | `shape: class`, one box per class, values as one-phrase notes | 02 §2 |
| One request or call traced in time | `shape: sequence_diagram`, actors predeclared | 02 §3 |
| Tables and keys | `shape: sql_table`, column-to-column edges | 02 §1 |
| Side-by-side lanes, before/after, file order top to bottom | grid: `grid-columns` or `grid-rows` | 02 §4 |
| A few real lines of code | `\|py … \|` code block | 01 §5 |
| Variants of one diagram (v1 vs v2, happy vs error path) | `scenarios` | 04 §3 |
| Drill-down pages | `layers` + `link` | 04 §3, 05 §8 |
| A step-by-step build-up | `steps` + `--animate-interval` (SVG or GIF) | 04 §3, 05 §9 |
| Shared classes across many files | `classes` in one file, `...@import` | 04 §2, 05 §12 |

Shapes: `rectangle` for everything, `oval` for start and end, `diamond` for a decision, `cylinder` for a store. At most three shape types per diagram. Shapes distinguish categories, never individuals.

## 3. Writing rules

1. **Title states the idea**, not the topic. "A late reply must not act on state that has moved on", not "Concurrency".
2. **A paragraph under the title** in plain engineering language, as a `shape: text` node (see §4 for placement). It says what the picture shows and why it matters.
3. **Boxes read as phrases.** "every request becomes one call to the gatekeeper", not "req→gatekeeper". No file suffixes, no line counts, no arrows or code inside label text.
4. **One vocabulary.** A component keeps one name across every diagram and the prose that goes with them. Never make the reader re-learn a word.
5. **Say colors as the reader sees them**: yellow, not amber. The palette comment at the top is the legend.
6. **Edge labels are one to four words**; omit obvious ones. Drop edges that go everywhere (config, logging); mention them in prose.
7. **Containers hold three to seven nodes.** Fewer is not a group; more gets split.
8. **Classes only, no inline `style.*`** on individual nodes, except `style.opacity: 0` on spacers and invisible edges.
9. **Plain text shapes only for prose.** Never `|md` blocks for titles or paragraphs: they render as HTML `foreignObject`, which many SVG viewers (and every image conversion) drop. Use `shape: text` with `\n` line breaks.
10. **Keep only what earns its place.** If a box cannot say in one breath why it is there, delete it.

## 4. Placement recipes that work on ELK

`near` constants (`top-center`, `bottom-center`, …) work **only on root-level shapes**. Inside any container they fail with `constant near keys can only be set on root level shapes`. `near: <shape>`, `top`/`left`, and per-container `direction` are TALA-only and fail or are ignored here. So:

- **Title**: root-level `shape: text` with `near: top-center`. Only one shape may sit there.
- **Paragraph under the title**: a root-level `shape: text` node connected to the first real node with an invisible edge, `intro -> first {style.opacity: 0}`. It lands above the flow.
- **Horizontal lanes** (ELK ignores nested `direction: right`): a container with `grid-columns: N`, one container per lane.
- **File order, top to bottom, with no edges**: `grid-columns: 1`. Cleaner than chaining invisible edges.
- **Centering a paragraph in a grid row**: put a spacer on each side, `pad: "" {style.opacity: 0; width: 400}`, and size the spacers so the row is as wide as the row below it. A grid row is only as wide as its cells, so a narrow row sits left.
- **Two-column pages** (a code map beside a sequence diagram): outer `grid-rows: 2` (intro row, body row), inner `grid-columns: 2`. A grid cell may be a container with edges, a sequence diagram, a class, or a code block.
- **Straight edges instead of jogs**: give the source a `width` wider than its targets so edges leave from under each target.
- **Layers without edges**: chain invisible edges through dummy nodes, `a -> gap1 -> gap2 -> b {style.opacity: 0}`, when a grid is not an option.
- Edges between cells of one grid are straight center-to-center lines with no routing. Put edges inside a cell's container, not between cells, if they must route around things.

## 5. Gotchas that cost time (all verified on 0.7.1)

- **Reserved words cannot be node ids**: `top`, `left`, `shape`, `label`, `style`, `width`, `height`, `near`, `class`, `icon`, `link`, `tooltip`, `direction`, `grid-rows`, `grid-columns`, `vars`, `layers`, `scenarios`, `steps`. Rename (`spacer_a`, `wellformed`, `leftover`) or quote. Errors look like `reserved field left does not accept composite` or `reserved keywords are prohibited in edges`.
- **Ids are case-insensitive**; `Server` and `server` are one node.
- **Repeated `a -> b` adds a second edge**, it does not restyle the first. Restyle with `(a -> b)[0].style…`.
- **Class shape colors are reversed from intuition**: `fill` colors the header, `stroke` colors the body, `font-color` colors the header text only. For a dark header with a light body: `fill: "#2563EB"; stroke: "#DBEAFE"; font-color: "#FFFFFF"`. Same for `sql_table`.
- **Class members**: a key with `(` is a method; a key with a colon must be quoted whole, `"add(item: Item)": None`; types with brackets must be quoted, `"list[str]"`; `#` for protected must be escaped `\#`; every member shows a `+` unless prefixed. Edges to a member use the prefixed key, `Order.-items -> Item`.
- **Sequence diagrams**: declare actors first on one line (`a; b; c`) to fix left-to-right order; actors referenced inside a group without predeclaration become children of the group. Unquoted `True`/`False` labels become lowercase booleans; quote them.
- **Container width/height** works on ELK and errors on dagre.
- **Root-level `**.class: x` alongside a `classes` block crashes d2** (stack overflow). Scope it: `container.**.class: x`.
- **`text-transform: title` is rejected**; use `capitalize`.
- **A `#` in a link or label starts a comment** unless quoted.
- **`shape: image` needs `icon`**; a missing local icon file is a hard error.
- **`_` at root** fails with `invalid underscore`.

## 6. Educational diagrams

When a diagram teaches a concept, state the learner's problem and define the central idea in plain language before the picture. Show the problem and the solution, side by side when possible (a two-column grid: "without" and "with"). Use the smallest example that exposes the mechanism, keep semantic roles recognizable as the example grows, and map every diagram element to the code or worked state it stands for. The reader should be able to say why the mechanism helps without tracing a listing. Render and inspect the actual source; show the rendered asset, never a redrawn approximation.

This is for concept teaching. An ordinary architecture or relationship map needs no toy example, lesson sequence, or quiz.

## 7. Render and verify

```
d2 --pad 32 path/name.d2 path/name.svg          # render; exit status is the truth, not the file
d2 validate path/name.d2                         # syntax only
d2 fmt path/name.d2                              # normalize formatting
d2 --animate-interval 1200 steps.d2 out.svg      # multi-board flip (SVG or GIF)
```

Look at the result before reporting it done. To see it as an image:

```
W=$(grep -o 'width="[0-9]*"' name.svg | head -1 | tr -dc 0-9)
H=$(grep -o 'height="[0-9]*"' name.svg | head -1 | tr -dc 0-9)
/home/ajay/.cache/ms-playwright/chromium-1134/chrome-linux/chrome --headless --no-sandbox --disable-gpu \
  --hide-scrollbars --window-size=$W,$H --screenshot="$PWD/name.png" "file://$PWD/name.svg"
```

Then Read the PNG. Check: title present, paragraph under it, no overlapping labels, no text overflowing a box, colors match the palette comment, edges go where the prose says.

When words matter to the user, propose the exact title, paragraph, and box labels in the terminal and wait for approval before rendering.

## 8. Icons

Only URLs from `references/d2_validated_icons_list.md`. Sparingly, on key external-facing nodes.

## 9. Reference map

Open the file for the section you need; do not read all five.

| File | Covers |
|---|---|
| `references/01-core-language.md` | shapes, connections, arrowheads, containers, `_`, text/markdown/LaTeX/code blocks, strings and quoting, comments, overrides and `null`, unicode, icons, the full reserved-keyword table, the docs sidebar map |
| `references/02-special-shapes.md` | `sql_table`, `class`, `sequence_diagram`, grids (gaps, spacers, nesting, edge behavior), dimensions, `near` and its limits, a worked code-level diagram of a Python module |
| `references/03-style-layout.md` | every style keyword with ranges and errors, root style, `classes` (arrays, precedence, globs), themes table, fonts, dagre vs ELK vs TALA, ELK and dagre CLI knobs, `vars` and `d2-config`, CLI and exports, docs claims 0.7.1 contradicts |
| `references/04-composition-advanced.md` | globs and filters, imports and spread imports, layers/scenarios/steps, linking, tooltips and links, animation, `d2 fmt`, legend, Go API |
| `references/05-remaining-pages.md` | models (`suspend`), legend syntax, autoformat, sketch, per-engine pages, board linking, multi-board export, import patterns (model-view, modular classes, nested composition, templates), full CLI manual, FAQ, troubleshooting, design stance |
