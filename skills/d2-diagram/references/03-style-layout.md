# D2 reference: styles, classes, themes, fonts, layouts, vars, CLI

Sources: https://d2lang.com/tour/style, /tour/classes, /tour/themes, /tour/fonts,
/tour/layouts, /tour/dagre, /tour/elk, /tour/tala, /tour/vars, /tour/exports,
/tour/sketch, /tour/man, /tour/composition-formats, /tour/auto-formatter.
`/tour/config` and `/tour/cli` do not exist (404); config is on `/tour/vars`
("Configuration variables"), CLI flags on `/tour/man`.
Every example below was rendered with `d2 --layout elk` on d2 v0.7.1 (dagre + elk
bundled, no TALA). Deviations from the docs are marked **0.7.1:**.

## 1. Style keywords

Set under `style` on a shape, a connection, or the root. Validation errors are quoted
verbatim from 0.7.1.

| keyword | docs value | applies to | 0.7.1 behaviour |
|---|---|---|---|
| `opacity` | float 0..1 | shape, connection | `expected "opacity" to be a number between 0.0 and 1.0` |
| `stroke` | CSS color name, hex, or gradient string | shape, connection | error text: `a valid named color ("orange"), a hex code ("#f0ff3a"), or a gradient ("linear-gradient(red, blue)")`; `radial-gradient(...)` also accepted |
| `fill` | same as stroke | shape only | on a connection it compiles but does nothing |
| `fill-pattern` | `dots`, `lines`, `grain`, `none` | shape only, root | **0.7.1** accepts `none, dots, lines, grain, paper` (`paper` undocumented) |
| `stroke-width` | int 1..15 | shape, connection | **0.7.1** accepts `0..15` (`between 0 and 15`) |
| `stroke-dash` | int 0..10 | shape, connection | `between 0 and 10` |
| `border-radius` | int 0..20 | shape, connection (ELK corners only) | **0.7.1** only requires `>= 0`; docs' pill example uses `999` |
| `shadow` | true/false | shape only | ignored on connections |
| `3d` | true/false | rectangle/square | **0.7.1** also hexagon: `key "3d" can only be applied to squares, rectangles, and hexagons` |
| `multiple` | true/false | shape only | |
| `double-border` | true/false | rectangles and ovals | `can only be applied to squares, rectangles, circles, ovals` |
| `font` | `mono` only | shape, connection | `"serif" is not a valid font in our system` |
| `font-size` | int 8..100 | shape, connection | `between 8 and 100` |
| `font-color` | color/hex/gradient | shape, connection | on `sql_table`/`class`: header text only |
| `animated` | true/false | shape, connection | SVG only |
| `bold`, `italic`, `underline` | true/false | shape, connection | shape labels are bold by default; bold beats italic, so set `bold: false` to see italic |
| `text-transform` | `uppercase`, `lowercase`, `title`, `none` | shape, connection | **0.7.1 contradicts docs**: accepted set is `none, uppercase, lowercase, capitalize`; `title` fails with `expected "text-transform" to be one of (none, uppercase, lowercase, capitalize)` |
| `filled` | true/false (not on the style page) | `source-arrowhead.style`, `target-arrowhead.style` | `x -> y: {target-arrowhead.style.filled: false}` works |

`link` and `tooltip` are not style keywords (`invalid style keyword: "link"`); set
`x.link: https://...` and `x.tooltip: text` directly. Hex colors need quotes or `#`
starts a comment. On `sql_table` and `class`, `fill` colors the header and `stroke` is
used as the body fill.

Docs examples (verbatim, all render):

```d2
direction: right
x -> y: hi
y -> z
x.style.fill: "#f4a261"
y.style.fill: honeydew
z.style.fill: "linear-gradient(#f69d3c, #3f87a6)"
```

Transparent: `x: {y; y.style.fill: transparent}` with `x.style.fill: PapayaWhip`.

```d2
direction: right
style.fill-pattern: dots
x -> y: hi
x.style.fill-pattern: lines
y.style.fill-pattern: grain
```

```d2
direction: right
x -> y: hi {
  style: {
    bold: true
  }
}
x.style.underline: true
y.style.italic: true
# By default, shape labels are bold. Bold has precedence over italic, so unbold to see
# italic style
y.style.bold: false
```

```d2
direction: right
TOM -> jerry: hi {
  style: {
    text-transform: capitalize
  }
}
TOM.style.text-transform: lowercase
jerry.style.text-transform: uppercase
```

The remaining docs examples are one-liners of the same shape (verified):
`x.style.opacity: 0`, `y.style.opacity: 0.7`, connection `opacity: 0.4`;
`x.style.stroke: "#f4a261"`, connection `stroke: deepskyblue`;
`x.style.stroke-width: 1` / connection `stroke-width: 8`; `x.style.stroke-dash: 5` /
connection `stroke-dash: 3`; `x.style.border-radius: 3`, `y.style.border-radius: 8`,
`tylenol.style.border-radius: 999` (pill); `x.style.shadow: true`; `x.style.3d: true`;
`x.style.multiple: true`; `x.style.double-border: true` (also `y.shape: circle`);
`x.style.font: mono` (also on connections); `x.style.font-size: 8`,
`y.style.font-size: 55`, connection `font-size: 28`; `x.style.font-color: "#f4a261"`,
connection `font-color: red`; `x.style.animated: true` and `x -> y: hi {style.animated: true}`.

Verified that one connection accepts all of these together in a `style: {}` map:
`opacity`, `stroke`, `stroke-width`, `stroke-dash`, `border-radius`, `font`,
`font-size`, `font-color`, `animated`, `bold`, `italic`, `underline`, `text-transform`.

### Root style (diagram background and frame)

Docs list: `fill` (background), `fill-pattern`, `stroke` (frame), `stroke-width`,
`stroke-dash`, `double-border` (two frames).

```d2
direction: right
x -> y: hi
style: {
  fill: LightBlue
  stroke: FireBrick
  stroke-width: 2
}
```

```d2
style: {
  fill: "#FAF3E0"
  fill-pattern: dots
  stroke: "#333333"
  stroke-width: 3
  stroke-dash: 4
  double-border: true
}
x -> y
```

Docs render with `pad=0`; add `--pad` when the root `stroke` is used as a frame.
**0.7.1:** unlisted root keys (`style.shadow`, `style.font-size`, `style.opacity`)
compile silently with no effect; unknown names error (`invalid style keyword: "bogus"`).

Changing theme defaults with globs (docs, /tour/globs#changing-defaults):

```d2
# Add to the top of your diagram
***.style.fill: lightblue
(*** -> ***)[*]: {
  style.stroke: red
}

x -> y
```

## 2. Classes

`classes` is a reserved top-level map that bundles any attributes (shape, label, width,
height, icon, link, tooltip, style, arrowheads, grid keys). It is never rendered.

```d2
direction: right
classes: {
  load balancer: {
    label: load\nbalancer
    width: 100
    height: 200
    style: {
      stroke-width: 0
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }
  unhealthy: {
    style: {
      fill: "#FE7070"
      stroke: "#F69E03"
    }
  }
}

web traffic -> web lb
web lb.class: load balancer
web lb -> api1
web lb -> api2
api2.class: unhealthy
```

Connection classes, at declaration `a -> b: {class: something}` or by targeting
`(a -> b)[0].class: something`.

Overriding: the object's own attribute beats the class attribute.

```d2
classes: {
  unhealthy: {
    style.fill: red
  }
}
x.class: unhealthy
x.style.fill: orange
```

Multiple classes as an array, applied left-to-right (later wins):

```d2
classes: {
  d2: {
    label: ""
    icon: https://play.d2lang.com/assets/icons/d2-logo.svg
  }
  sphere: {
    shape: circle
    style.stroke-width: 0
  }
}

logo.class: [d2; sphere]
```

```d2
classes: {
  uno: {
    label: 1
  }
  dos: {
    label: 2
  }
}

x.class: [uno; dos]
y.class: [dos; uno]
```

Verified: `x` labels `2`, `y` labels `1`; an explicit `z.label` after `z.class: uno`
wins. Inline `y: {class: [base; error]}` also works. Undefined class names compile
silently.

Classes carrying connection attributes and applied by glob (verified):

```d2
classes: {
  svc: {shape: hexagon; style.fill: "#E8F4FF"}
  flow: {
    label: flows to
    style.stroke: green
    source-arrowhead.shape: diamond
    target-arrowhead.shape: triangle
  }
}
api
db: {shape: cylinder}
api -> db
*.class: svc
(* -> *)[*].class: flow
```

Scoped recursive glob works: `outer.**.class: red`. **0.7.1 bug:** unscoped
`**.class: red` at root with a `classes` block present crashes the compiler
(`fatal error: stack overflow`) because `**` matches the class definitions themselves.
`**.style.fill: red` is fine. Prefer `*.class`, `container.**.class`, or `***.style...`.

Modular classes (docs /tour/modular-classes): keep the `classes` map in `classes.d2`,
spread it into `main.d2` with `...@classes`, then `user.class: person`,
`error.class: [base; error]`. Every applied class is also written as a `class`
attribute on the SVG element, so CSS like `.stuff { ... }` or JS hooks work when the
SVG is embedded.

## 3. Themes

Set with `-t/--theme <id>`, `D2_THEME=<id>`, or `vars.d2-config.theme-id`. Dark-mode
variant: `--dark-theme <id>`, `D2_DARK_THEME`, or `dark-theme-id`; unset means the
light theme is used in both modes. Passing a dark id to `--theme` makes the diagram
always dark. `d2 themes` on 0.7.1:

| Light | id | Light | id | Dark | id |
|---|---|---|---|---|---|
| Neutral Default | 0 | Vanilla Nitro Cola | 100 | Dark Mauve | 200 |
| Neutral Grey | 1 | Orange Creamsicle | 101 | Dark Flagship Terrastruct | 201 |
| Flagship Terrastruct | 3 | Shirley Temple | 102 | | |
| Cool Classics | 4 | Earth Tones | 103 | | |
| Mixed Berry Blue | 5 | Everglade Green | 104 | | |
| Grape Soda | 6 | Buttered Toast | 105 | | |
| Aubergine | 7 | Terminal | 300 | | |
| Colorblind Clear | 8 | Terminal Grayscale | 301 | | |
| | | Origami | 302 | | |
| | | C4 | 303 | | |

All 20 ids render; id 2 does not exist (`bad usage: -t[heme] could not be found`).
Ids 200..299 are treated as dark by the engine.

Special themes change defaults. `Terminal` (300): caps-lock labels, no border radius,
mono font, `fill-pattern: dots` on containers, `double-border` on the outermost
container; cancel with `text-transform: none` / `fill-pattern: none`. `C4` (303)
applies C4 fills by nesting level. Docs' terminal example sets it in-file:
`vars: {d2-config: {layout-engine: elk; theme-id: 300}}`.

### Theme color codes and overrides

From https://github.com/terrastruct/d2/blob/master/d2themes/d2themes.go and the
exporter defaults: `N1..N7` neutrals, darkest (N1, foreground/text) to lightest (N7,
background). `B1..B6` base colors for shapes and containers. `AA2, AA4, AA5`
alternative palette A; `AB4, AB5` alternative palette B.

- shape stroke `B1` (dashed shapes `B2`); leaf shape fill `B6`; top-level container
  fill `B4`, nesting level 2 `B5`, level 3 `B6`, deeper `N7` (lighter as nesting deepens).
- connection stroke `B1`, connection label `N2`.
- `sql_table` / `class`: header `N1`, body `N7`, accents `B2`, `AA2`, `N2`.
- `text` shape `N1`; sequence groups `N5`, notes `N7`, spans `B3..B5`.
- `AB4`/`AB5` unused by defaults (docs: "Not all color codes are currently used").

Override in `vars.d2-config.theme-overrides` (light) or `dark-theme-overrides` (dark,
only applies when a dark theme id is set). Docs example (verified):

```d2
vars: {
  d2-config: {
    theme-overrides: {
      B1: "#2E7D32"; B2: "#66BB6A"; B3: "#A5D6A7"
      B4: "#C5E1A5"; B5: "#E6EE9C"; B6: "#FFF59D"
      AA2: "#0D47A1"; AA4: "#42A5F5"; AA5: "#90CAF9"
      AB4: "#F44336"; AB5: "#FFCDD2"
    }
  }
}
```

Accepted keys: `N1`..`N7`, `B1`..`B6`, `AA2`, `AA4`, `AA5`, `AB4`, `AB5`. Others fail:
`"N8" is not a valid theme code`.

## 4. Fonts

Four bundled families: Source Sans Pro (labels, Markdown), Source Code Pro (code
blocks, `class` shape text, `style.font: mono`), and a blend of Architect's Daughter +
Fuzzy Bubbles for sketch mode. `style.font` accepts only `mono`.

Replace with `.ttf` paths; supply none or all (missing styles fall back to Source Sans
Pro): `d2 --font-regular=./helvetica-regular.ttf input.d2`. Flags `--font-regular`,
`--font-italic`, `--font-bold`, `--font-semibold` (env `D2_FONT_REGULAR` etc.).
**0.7.1 adds** `--font-mono`, `--font-mono-bold`, `--font-mono-italic`,
`--font-mono-semibold` (`D2_FONT_MONO*`); the docs page wrongly lists the regular flags
again under "Mono fonts". In sketch mode a supplied font replaces the hand-drawn blend.

## 5. Layout engines

Choose with `--layout=<name>`, `D2_LAYOUT=<name>`, or `vars.d2-config.layout-engine`.
`d2 layout` lists engines; `d2 layout <name>` prints engine flags. 0.7.1 bundles
`dagre` (default) and `elk`; TALA is a separate proprietary install
(https://github.com/terrastruct/tala).

| feature | dagre | ELK | TALA |
|---|---|---|---|
| `near` to a constant (`top-center`, ...) | yes | yes | yes |
| `near` to another object | no | no | yes |
| `width`/`height` on containers | no | yes | "soon" |
| `top`/`left` position locking | no | no | yes |
| connection from a container to its descendant | no | yes | yes |
| `direction` per container | no | no | yes |
| `border-radius` on connections | no corners | yes | yes |
| ASCII export | switches to ELK | yes | yes |

Verified 0.7.1 errors: dagre `Object "box" has attribute "width" and/or "height" set,
but layout engine "dagre" does not support dimensions set on containers`; dagre
`Connection "(box -> box.child)[0]" goes from a container to a descendant, but layout
engine "dagre" does not support this`; both `Object "y" has "near" set to another
object, but layout engine "elk" only supports constant values for "near"`. A
per-container `direction` compiles on dagre and ELK but is ignored.

Docs' notes: dagre is fast, DOT-based, unmaintained since 2018, curved multi-segment
edges. ELK is maintained, orthogonal routes, good crossing minimization, native
container-to-container routing, routes `sql_table` edges to exact columns. TALA is
non-hierarchical, symmetric, per-container direction, paid.

Global direction: `direction: up | down | right | left`, e.g. `direction: right` then
`x -> y -> z: hello`.

Engine flags on 0.7.1 (`d2 layout elk`, `d2 layout dagre`; CLI only, no `d2-config` key):

```
--elk-algorithm string             layout algorithm (default "layered")
--elk-nodeNodeBetweenLayers int    spacing between nodes of adjacent layers (default 70)
--elk-padding string               padding inside a parent (default "[top=50,left=50,bottom=50,right=50]")
--elk-edgeNodeBetweenLayers int    spacing between nodes and edges beside a layer (default 40)
--elk-nodeSelfLoop int             spacing between a node and its self loops (default 50)
--dagre-nodesep int                pixels separating nodes horizontally (default 60)
--dagre-edgesep int                pixels separating edges horizontally (default 20)
```

Verified: `d2 --layout elk --elk-padding "[top=20,left=20,bottom=20,right=20]" --elk-nodeNodeBetweenLayers 100 in.d2`.

## 6. Variables and substitutions

```d2
direction: right
vars: {
  server-name: Cat
}

server1: ${server-name}-1
server2: ${server-name}-2

server1 <-> server2
```

Nested with dots, usable inside `style`:

```d2
vars: {
  primaryColors: {
    button: {
      active: "#4baae5"
      border: black
    }
  }
}
button: {
  style: {
    fill: ${primaryColors.button.active}
    stroke: ${primaryColors.button.border}
  }
}
```

Scoped like program variables (inner wins; inner cannot leak out). Single quotes
bypass substitution:

```d2
vars: {
  region: Global
  names: John and Joyce
}
lb: ${region} load balancer
zone1: {
  vars: {
    region: us-east-1
  }
  server: ${region} API
}
lb -> zone1: 'Send field ${names}'
```

Spread `...${x}` expands a map into a map or an array into an array:

```d2
vars: {
  base-constraints: [NOT NULL; UNQ]
  disclaimer: DISCLAIMER {
    I am not a lawyer
    near: top-center
  }
}

data: {
  shape: sql_table
  a: int {constraint: [PK; ...${base-constraints}]}
}

custom-disclaimer: DRAFT DISCLAIMER {
  ...${disclaimer}
}
```

Also verified: vars inside `classes` values, `...${base-style}` spreading a style map
into a shape, `x.class: [...${base}; c]`, `theme-id: ${t}` inside `d2-config`.
Unknown variable: `could not resolve variable "nope"`.

### `d2-config`

```d2
vars: {
  d2-config: {
    theme-id: 4
    dark-theme-id: 200
    pad: 0
    center: true
    sketch: true
    layout-engine: elk
  }
}

direction: right
x -> y
```

Equivalent to `d2 --layout=elk --theme=4 --dark-theme=200 --pad=0 --sketch --center input.d2`.
Complete key list accepted by 0.7.1 (`compileConfig` in d2compiler): `sketch`,
`theme-id`, `dark-theme-id`, `pad`, `layout-engine`, `center`, `theme-overrides`,
`dark-theme-overrides`, `data`. Others fail: `"scale" is not a valid config`. `data` is
a free-form map for third-party tooling (`data: {power-level: 9000}`). Precedence:
flags and env vars beat `d2-config` (`D2_PAD=2 d2 --theme=1 input.d2` ignores the
file's `pad` and `theme-id`).

## 7. CLI, exports, animation, sketch

```
d2 [--watch=false] [--theme=0] file.d2 [file.svg | file.png | file.pdf | file.pptx | file.gif | file.txt]
d2 layout [name]    d2 themes    d2 fmt file.d2 ...    d2 play file.d2    d2 validate file.d2
```

Output format follows the output extension; default `<input>.svg`. `-` reads stdin or
writes stdout (`echo "x -> y" | d2 - - > example.svg`); stdout is SVG unless
`--stdout-format png|svg|ascii|txt|pdf|pptx|gif` (`d2 input.d2 --stdout-format png - > output.png`).
Check the exit status, not the output file: d2 writes partial renders on error.

Flags from `d2 --help` on 0.7.1 (env var in parentheses):

- `-w, --watch` (`D2_WATCH`) live reload; `-h/--host` (`HOST`, localhost), `-p/--port`
  (`PORT`, 0 = random), `--browser` (`BROWSER`, `0` opens none), `--img-cache`
  (`IMG_CACHE`, true).
- `-l, --layout` (`D2_LAYOUT`, dagre); `-t, --theme` (`D2_THEME`, 0); `--dark-theme`
  (`D2_DARK_THEME`, -1 = unset; emits a `prefers-color-scheme` media query).
- `--pad` (`D2_PAD`, 100 px); `-c, --center` (`D2_CENTER`); `--scale` (`SCALE`, -1 =
  SVG fits to screen and others use native size; `1` disables fitting; `0.5` halves).
- `-s, --sketch` (`D2_SKETCH`) hand-drawn look.
- `--animate-interval <ms>` (`D2_ANIMATE_INTERVAL`) cycle boards in one SVG or GIF.
- `--target`: `''` root only, `'layers.x'` one board, `'layers.x.*'` board plus
  descendants, default `'*'`.
- `-b, --bundle` (`D2_BUNDLE`, true) inline assets and layers; `--force-appendix`
  (`D2_FORCE_APPENDIX`) add the tooltip/link appendix (always on for PNG) to SVG.
- `--font-regular|italic|bold|semibold`, `--font-mono[-bold|-italic|-semibold]`.
- `--ascii-mode standard|extended` (`D2_ASCII_MODE`, default extended).
- `--no-xml-tag` (`D2_NO_XML_TAG`); `--salt <s>` unique ids for several diagrams on one
  page; `--omit-version` (`OMIT_VERSION`).
- `--timeout` (`D2_TIMEOUT`, 120 s); `-d, --debug` (`DEBUG`); `--check` (`D2_CHECK`)
  formatting check; `-v, --version`.

Verified: `d2 --layout elk --sketch --center --scale 0.5 --pad 40 -t 300 --dark-theme 200 --no-xml-tag --omit-version --salt abc in.d2`
and `D2_LAYOUT=elk D2_THEME=6 D2_DARK_THEME=201 D2_PAD=10 D2_SKETCH=1 D2_CENTER=1 d2 in.d2`
both succeed; `--watch --browser 0` serves on `http://127.0.0.1:<port>`.
With `steps: {1: {...}; 2: {...}}`: `--target steps.2`, `--target ''`,
`--target 'steps.2.*'`, `--target '*'` work; `--target 'steps.*'` fails with
`render target "steps" not found` (the wildcard must follow a board name).

### Export formats (docs /tour/exports; all verified on 0.7.1)

| format | command | notes |
|---|---|---|
| SVG | `d2 in.d2 out.svg` | default; injected CSS and `<foreignObject>` for Markdown, so it needs a web context (not Inkscape/Illustrator). Shape ids become base64 CSS classes (`my-shape` -> `bXktc2hhcGU`) plus a per-diagram `d2-<hash>` prefix |
| PNG | `d2 in.d2 out.png` | Playwright headless browser screenshots the SVG; first run downloads deps. On `failed to launch Chromium`: `npx playwright install --with-deps chromium` |
| PDF | `d2 in.d2 out.pdf` | PNG pages plus headers and fonts; links clickable, `animated` not shown; one page per board |
| PPTX | `d2 in.d2 out.pptx` | one slide per board (layers, scenarios, steps) |
| GIF | `d2 in.d2 out.gif` | looping animation of a short composition |
| ASCII | `d2 in.d2 out.txt` | beta in 0.7.1; dagre is swapped for ELK; shadow, multiple, animated are moot |

ASCII of `server1 <-> server2` (extended, then `--ascii-mode standard`):

```
 ┌────────┐      ┌────────┐        +--------+      +--------+
 │ Cat-1  │◀────▶│ Cat-2  │        | Cat-1  |<---->| Cat-2  |
 └────────┘      └────────┘        +--------+      +--------+
```

### Animation

Two mechanisms. `style.animated: true` animates a shape or connection stroke in SVG
only. `--animate-interval <ms>` turns a multi-board composition (`layers`,
`scenarios`, `steps`) into one SVG that cycles boards (CSS `@keyframes d2Transition-*`)
or a GIF; docs: `--animate-interval=1200` stays 1200 ms per board. Other targets are
refused: `--animate-interval can only be used when exporting to SVG or GIF. You provided: .png`.

```d2
a -> b
steps: {
  1: {b -> c}
  2: {c -> d}
}
```

`d2 --layout elk --animate-interval 1000 anim.d2 anim.svg` and `... anim.gif` verified.

### Sketch, formatting, validation

Sketch: `--sketch`, `D2_SKETCH=1`, or `d2-config.sketch: true`; https://play.d2lang.com
supports `&sketch=1`. `d2 fmt file.d2` rewrites in place and `d2 --check file.d2`
fails when unformatted. Verified: `aws_s3:    AWS S3 California{ Monitoring ---------->California }`
becomes `aws_s3: AWS S3 California {` / `  Monitoring -> California` / `}`.
`d2 validate file.d2` prints `Success! [...] is valid D2.` or the compile error
(`1:1: connection missing destination`).

Library API (docs /tour/api): Go package `d2oracle` with pure `Create`, `Set`,
`Delete`, `Rename`, `Move`, `*IDDeltas`; e.g. `d2oracle.Set(g, "a.style.fill", nil, "red")`.

## 8. Docs claims that 0.7.1 contradicts

1. `text-transform: title` is rejected; use `capitalize` (the docs' own example does).
2. `fill-pattern` also accepts `paper`.
3. `stroke-width` accepts `0`; `border-radius` has no upper bound.
4. `3d` also applies to hexagons.
5. Root `style` silently accepts unlisted keys (`shadow`, `font-size`, `opacity`).
6. Mono fonts use `--font-mono*` flags, not the regular flags the fonts page repeats.
7. Root-level `**.class: x` with a `classes` block crashes (stack overflow).
8. `--target 'steps.*'` errors; `--target 'steps.2.*'` works.
9. `/tour/config` and `/tour/cli` pages do not exist; use `/tour/vars` and `/tour/man`.
10. Per-container `direction` compiles on dagre and ELK but is ignored.
