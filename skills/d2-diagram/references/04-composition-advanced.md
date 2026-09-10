# D2 reference, part 4: globs, imports, composition, interactivity, formatting

Sources (all under https://d2lang.com/tour/ ): globs, imports, imports-use-cases,
model-view, modular-classes, nested-composition, version-visualization, imported-template,
models, legend, composition, layers, scenarios, steps, linking, composition-formats,
interactive, auto-formatter, exports, man, faq, troubleshoot, sketch, api.
Every example below was rendered with `d2 --layout elk` on d2 v0.7.1; failures are marked.
`/tour/animations`, `/tour/best-practices`, `/tour/formatting` do not exist (404). The
formatter page is `/tour/auto-formatter`; animation is `style.animated` + `--animate-interval`.

## 1. Globs

Globs make global changes in one line. Matching is case-insensitive (`*kong` matches
`Donkey Kong`), and several wildcards may appear in one key (`t*h*r.shape: person`).

```d2
iphone 10
iphone 11 mini
iphone 11 pro
iphone 12 mini

*.height: 300
*.width: 140
*mini.height: 200
*pro.height: 400
```

**Globs apply backwards and forwards.** A glob applies to shapes that already exist and
is re-evaluated for every shape declared later. Here `a`, `b`, `c` all connect to `y`:

```d2
a

* -> y

b
c
```

### Glob connections

`* -> *` connects every pair; self-connections are deliberately omitted.

```d2
Spiderman 1
Spiderman 2
Spiderman 3

* -> *: 👉
```

Modify existing connections with a glob on the edge and glob index `[*]`:

```d2
lady 1
lady 2

barbie

lady 1 -> barbie: hi barbie
lady 2 -> barbie: hi barbie

(lady* -> barbie)[*].style.stroke: pink
```

### Scoped globs

A glob only applies inside the scope where it is written.

```d2
foods: {
  pizzas: {
    cheese
    pineapple
    *.shape: circle
  }
  humans: {
    john
    *.shape: person
  }
  humans.* -> pizzas.pineapple: eats
}
```

### Recursive globs `**`

`**` targets all nesting levels (`**.style.border-radius: 7`). In connections it only
matches leaf (non-container) shapes, so `machine B` below is not connected:

```d2
zone-A: {
  machine A
  machine B: {
    submachine A
    submachine B
  }
}

zone-A.** -> load balancer
```

### Filters `&` and inverse filters `!&`

`&key: value` restricts a glob to targets where that reserved keyword has that value;
`!&key: value` excludes them. Multiple filter lines are ANDed.

```d2
bravo team.shape: person
charlie team.shape: person
command center.shape: cloud
hq.shape: rectangle

*: {
  &shape: person
  style.multiple: true
}
```

Swap `&shape: person` for `!&shape: person` to target the cloud and rectangle instead.

Special property filters `&connected: true|false` and `&leaf: true|false`:

```d2
**: {
  &connected: true
  style.fill: yellow
}

**: {
  &leaf: true
  style.stroke: red
}

container: {
  a -> b
}
c
```

Array values match if any element matches (`&class: server` matches
`class: [server; deployed]`). A glob as a filter value means "key is set at all":

```d2
*: {
  &link: *
  style.fill: red
}

x.link: https://google.com
y
```

Connection endpoint filters `&src` / `&dst` take absolute IDs (`a.c`, not `c`, even
inside `a`) or endpoint properties: `&src.style.fill: blue`, `&dst.shape: rectangle`
(verified with `(* -> *)[*]: { &src.shape: rectangle; &dst.style.fill: green; ... }`).

```d2
*: {
  &shape: person
  &connected: true
  style.fill: red
}
(** -> **)[*]: {
  &src: a
  &dst: c
  style.stroke: yellow
}
a -> b
a.shape: person
a -> c
```

### Nested globs

Globs nest and combine with filters. Verified: `**: { &shape: sequence_diagram; **: {shape: person} }`
turns every actor of every sequence diagram into a person.

### Global globs `***`

A triple glob applies to the whole diagram: unlike `**` it also reaches nested `layers`
boards and persists across imports.

```d2
***.style.fill: yellow
**.shape: circle
*.style.multiple: true

x: {
  y
}

layers: {
  next: {
    a
  }
}
```

Verified on 0.7.1: `a` in layer `next` is yellow but not a circle. Import nuance verified
on 0.7.1: a `***` glob declared in an imported file reaches the importing diagram's root
scope only through a top-level spread import (`...@file`). With `x: @file` or
`x: {...@file}` it applies only inside `x`. Ordinary `*`/`**` globs in an imported file
are never carried over.

Changing theme defaults is the common use. Put at the top of the diagram:
`***.style.fill: lightblue` and `(*** -> ***)[*]: { style.stroke: red }` (verified).

### Models with `suspend` / `unsuspend`

`suspend` marks a shape or connection for deletion, `unsuspend` restores it. Define
everything, suspend all with globs, then unsuspend selectively:

```d2
restaurants: Restaurants {
  chip: Chipotle
  bk: Burger King
  chip -> bk: competes with
}
diners: Diners {
  daniel
  zack
}
diners -> restaurants: eat at
diners.daniel -> restaurants.chip: likes
diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: dislikes

# Treat the above as models
**: suspend
(** -> **)[*]: suspend

# Display only who likes what
(** -> **)[*]: unsuspend {
  &label: likes
}
```

Other verified selections: `*: unsuspend` plus `(* -> *)[*]: unsuspend` shows only the
top level; `(** -> **)[*]: unsuspend { &dst: restaurants.bk }` shows only edges into `bk`.
A `$` glob leader is not documented on any tour page and was not tested.

## 2. Imports

Two forms. Both read `x.d2` from the importing file's directory:

```d2
# y.d2
a: @x
a -> b
```

Regular import (`a: @x`) assigns the whole file as a map value; spread import
(`a: { ...@x }`) inserts the file's contents into the current map. Both verified.
Rules, all verified on 0.7.1:

- Omit the `.d2` extension. `d2 fmt` rewrites `@x.d2` to `@x` and `@./x` to `@x`.
- Only `.d2` files import. `a: @x.txt` fails with
  `import key [...] doesn't exist inside import`.
- Spread imports only work inside a map. `a: ...@x` fails with
  `unquoted strings cannot begin with ...@ as that's import spread syntax`.
- Partial import `@file.object` imports one object and its subtree.
- File name containing `.`: quote it, `@"schema-v0.1.2"`.
- Relative paths resolve from the importing file's directory, not the cwd: `y: @../y`
  inside `dev/d2-stuff/x.d2` looks in `dev/`.
- Absolute paths: `x: @/absolute/path/to/file`; Windows must quote,
  `x: @"C:\absolute\path\to\file"`.
- An imported file may contain anything a normal file may: shapes, connections, styles,
  `classes`, `vars`, `layers`, globs, and a root `label`/`style` (the "template" pattern
  spreads a file holding only `style: {...}` and `label: ""` into a wrapper container).

### Partial import

```d2
# people.d2
management: {
  joe: {
    shape: person
    label: Joe Donutlover
  }
  jan: Jan Donutbaker {
    shape: person
  }
}
# Notice how these do not appear in the rendered diagram
employees: {
  toby: Toby Simonton
}
```

```d2
# donut-flowchart.d2
...@people.management
joe -> donuts: loves
jan -> donuts: brings
```

### Patterns from the docs

Model-view: define models once, spread them into several view files.

```d2
# models.d2
postgres: {
  shape: cylinder
}
it: IT Guy {
  shape: person
}
vpn: {
  tooltip: IP is 192.2.2.1
}
```

```d2
# access-view.d2
...@models
it -> vpn -> postgres
```

Modular classes: `...@classes` at the top of `main.d2`, then `user.class: person`,
`error.class: [base; error]`. Version visualization: `Users 1: Users Table (v0.1) {
...@"users-v0.1" }` next to `Users 2: { ...@users-current }` with `Users 1 -> Users 2`.
Reasons the docs give for splitting files: compliance (a spec file that must not
change), domain experts owning their part, smaller review diffs, one shared
`color-classes.d2`, don't-repeat-yourself.

## 3. Composition: layers, scenarios, steps

Every diagram is a root board. Three keywords declare extra boards:

| Keyword     | Inheritance                                       |
|-------------|---------------------------------------------------|
| `layers`    | Boards which do not inherit. They are a new base. |
| `scenarios` | Boards which inherit from the base layer.         |
| `steps`     | Boards which inherit from the previous step.      |

```d2
# Root board
x -> y
layers: {
  # Board named "numbers" that does not inherit anything from root
  numbers: {
    1 -> 2
  }
}
```

**Layers** are "a layer of abstraction"; each starts blank. **Scenarios** inherit the
whole base layer; new objects are added, and base objects can be referenced to change
them. **Steps** inherit from the previous step; the first step inherits from its parent
(scenario or layer). Boards nest: a scenario may hold `steps`, a layer may hold `layers`
(verified: `scenarios.alt.steps.1` exports as `x/alt/1.svg`).

Scenario: reference base objects and edges by index to restyle them, add new ones.

```d2
direction: right
title: Normal deployment {
  near: bottom-center
  shape: text
}
local.code -> github.dev: commit
github.dev -> github.master: merge
github.master -> aws.ec2: deploy
local.code -> aws.ec2: {
  style.opacity: 0.0
}

scenarios: {
  hotfix: {
    title.label: Hotfix deployment
    (local.code -> github.dev)[0].style.opacity: 0.1
    github.style.opacity: 0.1
    (local.code -> aws.ec2)[0]: {
      style.opacity: 1
      style.stroke-dash: 5
      style.stroke: "#167c3c"
    }
  }
}
```

Steps: in step 3 `Approach road` still exists, inherited via step 2.

```d2
Chicken's plan: {
  style.font-size: 35
  near: top-center
  shape: text
}

steps: {
  1: {
    Approach road
  }
  2: {
    Approach road -> Cross road
  }
  3: {
    Cross road -> Make you wonder why
  }
}
```

### Links between boards

`link` can target a board path. Board names containing `.` must be quoted
(`a.link: layers."2012.06"`). In a `link` value `_` means the parent board (not the
parent container) and `_._` the grandparent board.

```d2
The shire

journey: {
  link: layers.rivendell
}

layers: {
  rivendell: {
    elrond -> frodo: gives advice
    take me home sam.link: _
    go deeper: {
      link: layers.moria
    }

    layers: {
      moria: {
        dwarves

        take me home sam.link: _._
      }
    }
  }
}
```

The rendered navigation bar at the top is clickable, giving backlinks to every ancestor.

### Nested composition through imports

Each file stays flat; the layer value is an import.

```d2
# overview.d2
serviceA -> serviceB
serviceB.link: layers.serviceB

layers: {
  serviceB: @serviceB
}
```

`serviceB.d2` is itself a flat file (`aws vault.key -> data`, `data.link: layers.data`,
`layers: { data: @data }`), and `data.d2` holds a plain `sql_table`. Verified: three
files render to `overview/index.svg`, `overview/serviceB/index.svg`,
`overview/serviceB/data.svg`.

### Exporting multi-board diagrams (verified on 0.7.1)

- **Multiple SVGs (default).** `d2 tiktok.d2 out/tiktok.svg` writes a directory, not a
  file: `out/tiktok/index.svg`, `out/tiktok/tiktok/index.svg`,
  `out/tiktok/tiktok/virginia.svg`, ... Board links are rewritten to relative paths
  (`href="tiktok/index.svg"`, `href="virginia.svg"`; `_` becomes `href="index.svg"`),
  so clicking works from the file system.
- **Single animated SVG.** `d2 --animate-interval=1200 in.d2 out.svg` packs all boards
  into one SVG that shows each for 1200 ms via CSS keyframes. Docs: good for a few steps
  or scenarios; too many boards confuse the viewer.
- **Animated GIF.** `d2 --animate-interval=800 in.d2 out.gif` works (needs the Playwright
  browser, like PNG). With `.png` it fails:
  `bad usage: --animate-interval can only be used when exporting to SVG or GIF.` The
  0.7.1 `--help` text says "SVG exports" only; that text is stale.
- **PDF.** One page per board (root + 3 steps = 4 pages). Links stay clickable and jump
  between pages; docs call PDF the most suitable medium for layers. `style.animated` is
  not shown in PDF.
- **PPTX.** `d2 in.d2 out.pptx`, one slide per board; works in Google Slides.
- **Target a board.** `--target=''` renders only the root; `--target='layers.x.*'`
  renders layer `x` with all its children; `--target=layers.x` just that board.
  Default `*`. `-b/--bundle` (default true) bundles assets and layers into the SVG.

## 4. Interactive: tooltips and links

```d2
x: {tooltip: Total abstinence is easier than perfect moderation}
y: {tooltip: Gee, I feel kind of LIGHT in the head now,\nknowing I can't make my satellite dish PAYMENTS!}
x -> y
```

- Tooltips appear on hover; the shape gets a small icon. Docs' two uses: secondary
  context, and tidying a crowded diagram by tucking text away.
- Tooltips are HTML `title` attributes. Markdown is not rendered inside them (a `|md`
  block compiles but shows raw text).
- Static exports (PNG, PDF) replace icons with numbers and add a numbered appendix;
  `--force-appendix` adds the appendix to SVG too.

```d2
x: I'm a Mac {
  link: https://apple.com
}
y: And I'm a PC {
  link: https://microsoft.com
}
x -> y: gazoontite {
  link: https://google.com
}
```

Links work on shapes and connections. An unquoted `#` starts a comment, so a URI
fragment must be quoted or escaped. Verified: `x` and `y` keep `#fragment`, `z` loses it.

```d2
x.link: "https://example.com/page#fragment"
y.link: https://example.com/page\#fragment
z.link: https://example.com/page#fragment
```

SVG interactivity depends on embedding: inline `<svg>`, `<object>`, `<iframe>`, `<embed>`
keep links clickable; `<img>` and CSS background images do not.

## 5. Animation

`style.animated: true` animates a connection's stroke or a shape. SVG only; PNG and PDF
drop it. Board transitions are `--animate-interval` (section 3). `--sketch` renders a
hand-drawn look.

```d2
direction: right
x -> y: hi {
  style.animated: true
}
x.style.animated: true
```

## 6. Formatting and tooling

`d2 fmt file.d2 ...` rewrites files in place; `d2 fmt -` formats stdin to stdout. It
normalizes spacing, indentation, and arrow length: verified that
`aws_s3:    AWS S3 California{` / `  Monitoring ---------->California` / `}` becomes

```d2
aws_s3: AWS S3 California {
  Monitoring -> California
}
```

- `d2 fmt --check file.d2` exits 1 with `err: found 1 unformatted file. Run d2 fmt to
  fix.` when unformatted, exits 0 otherwise.
- `d2 validate file.d2` compiles without rendering: `Success! [...] is valid D2.`
- `d2 layout` lists engines; `d2 layout elk` shows an engine's options. `d2 play file.d2`
  opens https://play.d2lang.com . Env vars mirror flags: `D2_LAYOUT`,
  `D2_ANIMATE_INTERVAL`, `D2_BUNDLE`, `D2_CHECK`.

### Practical guidance the docs give (FAQ, troubleshooting, use-case pages)

- A label that will not compile has reserved characters: quote it, `"x(int y)": "[]int"`.
  A reserved keyword used as a key must be quoted: `"width": width`.
- Text too wide: add `\n` inside the label.
- Cluttered connections: set explicit `width`/`height` on heavily connected shapes so
  edges have more surface to route to.
- Use ASCII `:` `;` `.` even in non-English diagrams; full-width `：` is not a separator.
- HTML inside Markdown must be well-formed XML (`<br/>`), and Markdown blocks need an
  HTML-capable SVG viewer (not Illustrator or Inkscape).
- An object cannot belong to two containers; ports are not supported.
- Move secondary detail into tooltips instead of longer labels.
- Split large diagrams into imported files (models, classes, per-domain files) and link
  layers with `link: layers.x` to go from overview to detail; keep each file flat.
- `layers` for abstraction levels, `scenarios` for alternate views of the same objects,
  `steps` for sequences; animated SVG/GIF only for short compositions.
- Put `***` default-style globs at the top so every later shape inherits them.

## 7. Legend

`vars.d2-legend` declares a legend from ordinary shapes and connections. `a -> b` adds
three entries; set the shapes' opacity to 0 to keep only the connection. Give
`d2-legend` a label (`d2-legend: "凡例" {...}`) to rename the legend.

```d2
vars: {
  d2-legend: {
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
    }
    a.style.opacity: 0
    b.style.opacity: 0
  }
}
api-1 <-> api-2: {
  style.stroke: red
  style.stroke-dash: 2
}
```

## 8. API (Go)

`d2oracle` (https://d2lang.com/tour/api) edits diagrams on the AST: `Create`, `Set`,
`Delete`, `Rename`, `Move`, plus `*IDDeltas` helpers returning old-to-new ID maps. All
functions are pure and return a new graph. Not exercised here.
