# D2 reference, part 5: models, legend, formatter, sketch, layout engines, linking, imports, CLI, FAQ, troubleshooting

Sources: https://d2lang.com/tour/<page> and the raw markdown + `static/d2/*.d2` examples in
https://github.com/terrastruct/d2-docs. Every example below was rendered with local `d2 v0.7.1`
using `--layout elk` and `--layout dagre`. All passed unless a
"0.7.1 result" line says otherwise. Bundled engines: dagre, elk. TALA is not installed.

## 1. Models (`suspend` / `unsuspend`) — https://d2lang.com/tour/models

**Rule.** Define every shape and connection once, then hide all of them with `suspend` and
selectively bring back the ones a view needs with `unsuspend`. Both are keywords applied like
any other attribute; they are meant to be combined with globs.

Exact syntax, verbatim from the docs:

```d2
**: suspend
(** -> **)[*]: suspend
```

- `suspend` marks the shape or connection for deletion.
- `unsuspend` restores it.
- `**` matches all shapes at every depth; `(** -> **)[*]` matches every connection at every depth.

Model definition used by all four examples (`static/d2/suspend.d2`):

```d2
restaurants: Restaurants {
  style.stroke-dash: 2
  *.style.fill: "#66c4e3"
  chip: Chipotle
  cfa: Chick-Fil-A
  bk: Burger King

  chip -> bk: competes with
}

diners: Diners {
  daniel
  zack
}
diners -> restaurants: eat at

diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.cfa: dislikes

diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: likes
```

**Show only top level** (append to the models above):

```d2
**: suspend
(** -> **)[*]: suspend

*: unsuspend
(* -> *)[*]: unsuspend
```
0.7.1 result: renders only `Restaurants`, `Diners`, `eat at`.

**Show only connections to one shape** (glob filter `&dst`):

```d2
**: suspend
(** -> **)[*]: suspend

(** -> **)[*]: unsuspend {
  &dst: restaurants.bk
}
```
0.7.1 result: renders `Burger King`, `Chipotle`, `zack`, both containers, `competes with`, `likes`.

**Show only connections with a given label** (glob filter `&label`):

```d2
**: suspend
(** -> **)[*]: suspend

(** -> **)[*]: unsuspend {
  &label: likes
}
```
0.7.1 result: renders daniel, zack, Chipotle, Burger King and the three `likes` edges only.

Gotchas:
- Unsuspending a connection also unsuspends both endpoints and their ancestor containers (verified: `&dst: restaurants.bk` brought back `Chipotle` because of `chip -> bk`).
- Order matters: the two `suspend` globs must come after the model definitions and before the `unsuspend` globs.
- Filters go in a map on the glob target (`&dst`, `&label`, `&src`, ...), see the globs page.
- To avoid repeating the model block in each view, put it in its own file and import it (section 11).
- The docs mark these examples `language-d2-incomplete` only because the models block is elided; the full files compile.

## 2. Legend — https://d2lang.com/tour/legend

**Rule.** Declare a legend with the special variable `d2-legend` inside `vars`. Each child of
`d2-legend` is a shape or connection whose label and style become one legend row.

Exact syntax (`static/d2/legend.d2`):

```d2
vars: {
  d2-legend: {
    a: {
      label: Microservice
    }
    b: Database {
      shape: cylinder
      style.stroke-dash: 2
    }
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
      style.stroke-width: 1
    }
    a -> b: Bad relationship
    a -> b: Tenuous {
      target-arrowhead.shape: circle
    }
  }
}

api-1
api-2

api-1 -> postgres
api-2 -> postgres

postgres: {
  shape: cylinder
}
postgres -> external: {
  style.stroke: black
}

api-1 <-> api-2: {
  style.stroke: red
  style.stroke-dash: 2
}
api-1 -> api-3: {
  target-arrowhead.shape: circle
}
```
0.7.1 result: SVG contains a box titled `Legend` with rows `Microservice`, `Database`, `Good relationship`, ...

**Hiding shapes.** `a -> b` declares three things (two shapes and one connection), so three legend
rows appear. To show only the connection, set the shapes' opacity to 0:

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
api-1 -> api-3: {
  target-arrowhead.shape: circle
}
```

**Rename "legend".** Give `d2-legend` a label (useful for non-English diagrams):

```d2
vars: {
  d2-legend: "凡例" {
    a -> b: relation
  }
}
x -> y
```
0.7.1 result: legend title renders as `凡例`.

Gotchas:
- Legend keys (`a`, `b`) live in their own namespace; they do not create shapes in the diagram and do not collide with diagram keys.
- The legend row text is the label, so give legend entries a label (`a: {label: ...}` or `a -> b: text`), not just a key.
- Legend styling copies the entry's own style; the diagram is not styled by the legend.

## 3. Autoformat — https://d2lang.com/tour/auto-formatter

**Rule.** D2 normalises indentation, spacing and arrow length on compile; run it explicitly with
`d2 fmt file.d2`.

```d2
aws_s3:    AWS S3 California{
  Monitoring ---------->California
}
```
becomes
```d2
aws_s3: AWS S3 California {
  Monitoring -> California
}
```
0.7.1 result: `d2 fmt` produced exactly the second form. `d2 fmt --check file.d2` exits 1 with
`err: found 1 unformatted file. Run d2 fmt to fix.` when the file is unformatted.

Gotchas: extra hyphens in `---->` carry no meaning and are collapsed. `fmt` rewrites in place.

## 4. Sketch (hand-drawn) — https://d2lang.com/tour/sketch

**Rule.** Pass `--sketch` (or `D2_SKETCH=1`) on the CLI, or `&sketch=1` on the playground URL.
No in-language syntax. 0.7.1 result: `d2 --sketch a.d2 out.svg` OK. Gotcha: sketch output is
larger (55 KB vs 10 KB for a one-shape diagram) because every stroke is jittered.

## 5. Dagre — https://d2lang.com/tour/dagre

**Rule.** Dagre is the default engine (`--layout dagre`). Reference: https://github.com/dagrejs/dagre

Pros stated: very fast; battle tested (Mermaid uses it exclusively for flowcharts); generally
good results; algorithms come from the Graphviz papers; renders hierarchical layouts well.

Cons / limitations stated:
- Unmaintained since 2018.
- Occasional inexplicable edge routing (dagre issue #256).
- Strictly hierarchical even when the diagram is not.
- Container-child to container (or container-child) connections are not natively supported; D2 adds a shim, but core algorithm considerations are missed.
- Multi-segment routes are curved, not orthogonal, so long routes can look squiggly.

Engine-specific CLI options (`d2 layout dagre`, verified on 0.7.1):
- `--dagre-nodesep int` pixels separating nodes horizontally (default 60)
- `--dagre-edgesep int` pixels separating edges horizontally (default 20)
0.7.1 result: `d2 --layout dagre --dagre-nodesep=100 --dagre-edgesep=40` OK.

## 6. ELK — https://d2lang.com/tour/elk

**Rule.** `--layout elk`. Layered algorithm, bundled. Reference: https://www.eclipse.org/elk/reference.html

Pros stated: clean orthogonal routes; highly customizable; fast; good at minimizing crossings;
native container-to-container routing (better than dagre); active releases; routes `sql_table`
connections to exact columns.

Cons / limitations stated: strictly hierarchical like dagre; some routes have unnecessary bends;
minimal consideration for symmetry.

The doc page itself documents no knobs. Knobs exposed by 0.7.1 (`d2 layout elk`):
- `--elk-algorithm string` layout algorithm (default "layered")
- `--elk-nodeNodeBetweenLayers int` spacing between nodes of adjacent layers (default 70)
- `--elk-padding string` padding inside a parent, default `"[top=50,left=50,bottom=50,right=50]"`
- `--elk-edgeNodeBetweenLayers int` spacing between nodes and edges routed beside a layer (default 40)
- `--elk-nodeSelfLoop int` spacing between a node and its self loops (default 50)
0.7.1 result: `--elk-nodeNodeBetweenLayers=120 --elk-padding='[top=20,left=20,bottom=20,right=20]'` OK.

## 7. TALA — https://d2lang.com/tour/tala

**Rule.** Proprietary Terrastruct engine, separate install (https://github.com/terrastruct/tala#installation),
selected with `--layout tala`. Manual: https://github.com/terrastruct/TALA/blob/master/TALA_User_Manual.pdf

Pros / capabilities stated (features that only work under TALA):
- General orthogonal layout, not limited to hierarchies, trees or radial; whiteboard-like results for non-hierarchical diagrams.
- `top` and `left` lock positions.
- Considers and prefers symmetry; first-class containers.
- `direction` can be set per container.
- `near` can target another shape.
- `sql_table` connections point to the exact row.
- Dynamic label positioning to avoid obstructions.
- Grid-cell connections use TALA routing instead of always straight lines.

Cons stated: not free; relatively new (~2 years in production vs 10+ for alternatives); more random,
a small label change can cascade into an entirely different layout.

0.7.1 result: `d2 --layout tala a.d2` fails with
`err: failed to compile design-cyl.d2: bad usage: D2_LAYOUT "tala" is not bundled and could not be found in your $PATH.`
`err: The available options are: dagre, elk.`
So `top`/`left`, per-container `direction`, and `near: <shape>` must not be relied on locally.

## 8. Linking between boards — https://d2lang.com/tour/linking

**Rule.** `link` normally points at an external URL; give it a board path (`layers.x`,
`scenarios.x`, `steps.x`) to jump to another board instead ("internal link").

```d2
how does the cat go?: {
  link: layers.cat
}

layers: {
  cat: {
    meoowww
  }
}
```

Board names containing `.` must be quoted in the link target:

```d2
a.link: layers."2012.06"

layers: {
  "2012.06": {
    hello
  }
}
```

**Parent reference.** In a `link` value `_` means the parent *board* (not the parent container);
`_._` two boards up.

```d2
The shire

journey: {
  link: layers.rivendell
}

layers: {
  rivendell: {
    elves: {
      elrond -> frodo: gives advice
    }

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
0.7.1 result: all three compile under elk and dagre. A multi-board SVG target becomes a
directory: `out.svg` -> `out/index.svg`, `out/cat.svg`, `out/rivendell/index.svg`,
`out/rivendell/moria.svg`. Internal links are rewritten to relative file paths (`href="cat.svg"`,
`href="../index.svg"`), so clicking works when the SVG is opened in a browser.

Gotchas: backlinks (the breadcrumb bar at the top of a child board) are generated automatically.
PDF is the medium the docs use to demo linking.

## 9. Export formats for compositions — https://d2lang.com/tour/composition-formats

**Rule.** A multi-board diagram cannot be one image, so the export options differ:
- Multiple SVGs (default): one file per board in a directory tree; internal links rewritten to those paths.
- Single animated SVG: `--animate-interval=1200` keeps each board for 1200 ms. Good for a few steps/scenarios; confusing with many boards.
- Single animated GIF: same, for contexts where SVG is not rendered.
- PDF: one page per board, objects link to pages. "The most suitable medium for layers currently."
- PowerPoint: output `.pptx`; also opens in Google Slides.

0.7.1 results on the cat example: `.pdf` OK, `.pptx` OK, `--animate-interval=1200 out.svg` OK,
`--animate-interval=1200 out.gif` OK. `--animate-interval` with `.png` fails: `err: You provided: .png`.
Gotcha found: `.txt` (ASCII) output of a multi-board file fails on 0.7.1 with
`open .../out/cat/cat.txt: no such file or directory` (the board directory is not created). Single-board `.txt` works.

## 10. Imports: use-case overview — https://d2lang.com/tour/imports-use-cases

**Rule.** D2 imports behave like dependencies in a programming language. Patterns: model-view,
modular classes, nested composition. Principles: compliance (a spec file that must not change),
domain-driven design (experts diagram their part), smaller code-review diffs, reusability (one
`color-classes.d2` for the org), don't repeat yourself. More examples: version visualization, template.

Syntax reminder used throughout: `...@file` spreads `file.d2` into the current scope;
`key: @file` imports it as a nested object; `@"quoted-name"` when the file name has a dot or
special char. No `.d2` extension in the reference.

## 11. Model-view — https://d2lang.com/tour/model-view

**Rule.** Define models once, spread them into each view file, add only the relationships.

`models.d2`
```d2
postgres: {
  shape: cylinder
  icon: https://icons.d2lang.com/dev%2Fpostgresql.svg
  icon.near: bottom-center
}
it: IT Guy {
  shape: person
  style: {
    fill: maroon
  }
}
vpn: {
  style: {
    shadow: true
  }
  tooltip: IP is 192.2.2.1
}
```
`access-view.d2`
```d2
...@models
it -> vpn -> postgres
```
`ssh-view.d2`
```d2
...@models
it -> postgres: ssh, bypassing VPN
```
0.7.1 result: both views OK. Gotcha: files are resolved relative to the importing file; render the view file, not `models.d2`.

## 12. Modular classes — https://d2lang.com/tour/modular-classes

**Rule.** Keep `classes` in one file (the "CSS") and the diagram in another (the "HTML").

`classes.d2`
```d2
classes: {
  base: {
    style: {
      border-radius: 4
      shadow: true
    }
  }
  error: {
    style.fill: pink
    style.stroke: red
  }
  med: {
    width: 200
    height: 200
    style.font-size: 24
  }
  # large / xlarge omitted: same shape with 300/400 px and font-size 28/32
  person: {
    shape: person
    style.stroke-dash: 3
  }
}
```
`main.d2`
```d2
...@classes
user.class: person
error.class: [base; error]
modal.class: [base; med]

user -> app.signup: click
app.signup -> error: invalid fields
app.signup -> modal: continue registration
```
0.7.1 result: OK. Gotchas: multiple classes use array syntax `[a; b]`, applied left to right (later wins). A shape key may equal a class name (`error`) without conflict.

## 13. Nested composition — https://d2lang.com/tour/nested-composition

**Rule.** Each file stays flat; `layers.x: @file` nests a whole file as a child board, and the
imported file may itself declare `layers`, so drill-down diagrams compose recursively.

`overview.d2`
```d2
serviceA -> serviceB
serviceB.link: layers.serviceB

layers: {
  serviceB: @serviceB
}
```
`serviceB.d2`
```d2
aws vault: {
  key
  token
}
stripe: {
  customer id
}
aws vault.key -> data
aws vault.token -> data
stripe.customer id -> data
data.link: layers.data

layers: {
  data: @data
}
```
`data.d2`
```d2
users: {
  shape: sql_table
  id: int
  token: string
  customer_id: string
}
```
0.7.1 result: OK; output tree `index.svg`, `serviceB/index.svg`, `serviceB/data.svg`.
Gotcha: a `link` inside the imported file (`data.link: layers.data`) is relative to that file's own board, which becomes the nested board, so links keep working after nesting.

## 14. Version visualization — https://d2lang.com/tour/version-visualization

**Rule.** Because each schema lives in its own file, older versions can be checked out with git,
renamed, and spread side by side.

`history.d2`
```d2
direction: right
Users 1: Users Table (v0.1) {
  ...@"users-v0.1"
}

Users 2: Users Table (current) {
  ...@users-current
}

Users 1 -> Users 2
```
`users-current.d2`
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: int {constraint: foreign_key}
  name: string
  password: text
  created_at: timestamp
  last_updated: timestamp
}

emails: {
  shape: sql_table
  id: int {constraint: [primary_key; unique]}
  local: string
}
users.email -> emails.id
```
`users-v0.1.d2`
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: string
  name: string
  verified_email: boolean
  password: string
  created_at: timestamp
}
```
Shell shown by the docs:
```sh
cp users.d2 users-current.d2
git checkout tags/v0.1 users.d2
mv users.d2 users-v0.1.d2
```
0.7.1 result: OK. Gotchas: a file name with a dot (`users-v0.1`) must be quoted: `...@"users-v0.1"`.
Spreading the same file twice into two containers is fine because the keys are scoped per container.
The "Compare" section is a sketch (`Schema: { ...@alpha-schema }` etc.) with no rendered output; it uses the same spread-into-container pattern.

## 15. Imported template — https://d2lang.com/tour/imported-template

**Rule.** Spread a file that holds only root-level `style` and `label` into a wrapper container
to brand every diagram consistently.

`diagram.d2`
```d2
template: {
  ...@imports-wrapper-template
  synergy: {
    our firm -> yours: value add
  }
  stakeholders: {
    george.shape: person
    tim.shape: person
    tim.tooltip: is this web scale?
  }
}
```
`wrapper-template.d2`
```d2
style: {
  fill: "#E3EDE6"
  fill-pattern: dots
  stroke: "#820758"
  stroke-width: 3
  border-radius: 2
  shadow: true
}
label: ""
```
0.7.1 result: OK. Gotchas: `label: ""` blanks the container title. The docs note this pattern
"will be made much more powerful when D2 finishes glob support" (globs now exist, so a template
can also carry `*.style...` rules).

## 16. CLI manual — https://d2lang.com/tour/man

Synopsis: `d2 [--watch false] [--theme 0] [--salt string] file.d2 [file.svg | file.png]`,
`d2 layout [name]`, `d2 fmt file.d2 ...`, `d2 play file.d2`, `d2 validate file.d2`.
Output defaults to `file.svg`. Pass `-` to read stdin or write stdout. Never test for the output
file to detect success, use the exit status: d2 may write a partial render on error.

Flags (one line each, as documented):
- `-w, --watch` watch input and live reload; `$HOST`/`$PORT` set the address.
- `-h, --host localhost` listening host in watch mode.
- `-p, --port 0` listening port in watch mode.
- `-t, --theme 0` theme ID.
- `--dark-theme -1` theme when the viewer's browser is in dark mode; unset means `--theme` for both. Explicit styles still apply.
- `-s, --sketch` hand-drawn rendering.
- `--ascii-mode extended` character set for `.txt` / `--stdout-format ascii`: `standard` or `extended`.
- `--center` center the SVG in its viewbox.
- `--scale -1` scale output; -1 fits SVG to screen, 1 turns fitting off, e.g. 0.5 halves.
- `--font-regular`, `--font-italic`, `--font-bold` path to a `.ttf` replacing Source Sans Pro.
- `--pad 100` pixels of padding around the diagram.
- `--animate-interval 0` package multiple boards as one SVG/GIF that flips every N ms.
- `--browser true` browser executable opened by watch; `0` opens none.
- `-l, --layout dagre` layout engine; `d2 layout` lists them.
- `-b, --bundle true` bundle all assets and layers into the output SVG.
- `--force-appendix false` add the tooltip/link appendix (always added for PNG) to SVG too.
- `--target` board to render; `''` = root only, `'layers.x.*'` = layer x with all children; default `*`.
- `-d, --debug` debug logs.
- `--img-cache true` cache icon images between watch recompiles.
- `--timeout 120` seconds before d2 exits; raise for large diagrams.
- `--check false` check files are formatted (used as `d2 fmt --check`).
- `--salt string` appended to element IDs so several diagrams can share one HTML page.
- `-h, --help`, `-v, --version`.
- `--stdout-format string` format when writing to `-`: png, svg, ascii per the man page.
- `--no-xml-tag false` omit `<?xml ...?>` for direct HTML embedding.

Subcommands: `layout` (list engines), `layout [name]` (engine options), `themes`, `fmt file.d2 ...`,
`play file.d2` (open in https://play.d2lang.com), `validate file.d2`.

Environment variables: `D2_WATCH`, `D2_LAYOUT`, `D2_THEME`, `D2_DARK_THEME`, `D2_PAD`, `D2_CENTER`,
`D2_SKETCH`, `D2_BUNDLE`, `D2_FORCE_APPENDIX`, `D2_FONT_REGULAR`, `D2_FONT_ITALIC`, `D2_FONT_BOLD`,
`D2_FONT_SEMIBOLD`, `D2_ANIMATE_INTERVAL`, `D2_TIMEOUT`, `D2_CHECK`, `DEBUG`, `IMG_CACHE`, `HOST`,
`PORT`, `BROWSER`, `D2_STDOUT_FORMAT`, `D2_ASCII_MODE`, `D2_NO_XML_TAG`.

Where 0.7.1 `d2 --help` differs from the man page (man page is dated March 12, 2025):
- Extra output extensions in the synopsis: `.pdf`, `.pptx`, `.gif`, `.txt`.
- Extra flags: `--omit-version` (`$OMIT_VERSION`), `--font-semibold`, `--font-mono`, `--font-mono-bold`, `--font-mono-italic`, `--font-mono-semibold`, and `-c` as the short form of `--center`.
- `--stdout-format` accepts svg, png, ascii, txt, pdf, pptx, gif (man says png, svg, ascii).
- `--help` text says `--animate-interval` is SVG-only, but the man page is right: GIF works (verified).
- `d2 play` also takes `--theme` and `--sketch`.
- Verified: `d2 validate` prints `Success! [...] is valid D2.`; `d2 themes` lists IDs (0 Neutral Default, 1 Neutral Grey, 3 Flagship Terrastruct, ...); `--target='layers.cat'` renders only that board.

## 17. FAQ — https://d2lang.com/tour/faq

- How does D2 compare to Mermaid, Graphviz, PlantUML? See the community comparison site https://text-to-diagram.com.
- Small or complex diagrams? Both; minimal syntax for small ones, IDE features (formatter, errors, comments) for large ones, but not "big data" (not tested on thousands of nodes).
- Telemetry? No; the only network use after install is a periodic GitHub version check.
- Needs a browser? No, runs fully server-side.
- Runs in a browser? Yes via WebAssembly (the playground); a packaged browser build is planned.
- Use online? https://play.d2lang.com.
- Object in more than one container (Venn style)? Not now, not planned; see https://github.com/d2lang/d2/discussions/328.
- Ports? Not yet, planned; see https://github.com/d2lang/d2/discussions/605.
- No interactivity in the SVG export? Links/tooltips work only when the SVG is not treated as an image: inline `<svg>`, `<object>`, `<iframe>`, `<embed>` keep links clickable; `<img>` and CSS background do not.

## 18. Troubleshooting — https://d2lang.com/tour/troubleshoot

- A label or value won't compile: it has reserved characters; quote it: `"x(int y)": "[]int"` or `'$dollarbills$'`. (verified)
- Text too wide: insert `\n` in the label: `x: When you go out to buy,\ndon't show your silver.` (verified)
- Connections look cluttered: set explicit `width`/`height` on heavily connected shapes so edges have more surface to attach to.
- Reserved keyword as a key: quote it, `x: { "width": width }`. (verified)
- Markdown with HTML breaks: HTML must be well-formed XML, e.g. `<br/>` not `<br>`.
- Markdown SVG blank in some viewers: markdown is rendered as an xhtml foreignObject; pure SVG editors such as Illustrator cannot show it.
- SVG not interactive in HTML: `<img>` blocks interactivity; see https://docs.asciidoctor.org/asciidoc/latest/macros/image-svg/#options-for-svg-images and https://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html#SVG_in_HTML.
- Non-ASCII text "breaks": full-width `：` is not ASCII `:`, so `hello世界：مرحبا بالعال` is one key with no label. Use ASCII `:`, `;`, `.` in foreign-language diagrams. (verified: compiles as a single shape)

## 19. Design decisions and dev-tool stance — https://d2lang.com/tour/design, https://d2lang.com/tour/experience

Only the points that change how to write D2:
- Readability over compactness: write `A: Christmas {shape: cylinder}` rather than a terse encoding; autofmt is expected to normalise whatever you type. (verified)
- Warnings over errors: applying a non-existent class or a no-op style compiles and at most warns (verified: `x.class: nope` exits 0). Do not rely on the compiler to catch typos in class names.
- Good defaults: zero-customization output is meant to look fine; the default theme is coloured, not monochrome. Add styling only when needed.
- Separate system from styling: keep nodes and edges in one file and import styles/classes from another so aesthetics can be swapped (sections 12 and 15).
- Single use case: D2 is for documenting software. No mind maps, Gantt, Sankey, Venn, or geographic maps, and these will not be added.
- Whiteboard-fit: D2 targets diagrams that fit on a large whiteboard; around 1000 nodes it is the wrong tool.
- Desktop/server first: CLI with watch mode, stdin/stdout, embedded fonts and images so exports are standalone; the browser library is secondary.
- Declarative diagramming is the point: describe the system, let the engine lay it out; avoid hand-positioning unless the engine (TALA) supports it.

## Verification summary (d2 v0.7.1)

Every example in sections 1-19 rendered with both `--layout elk` and `--layout dagre`.
Failures / contradictions on 0.7.1:
- `--layout tala`: not installed (`D2_LAYOUT "tala" is not bundled and could not be found in your $PATH`).
- Multi-board `.txt` export: `open .../out/cat/cat.txt: no such file or directory`.
- `--animate-interval` with `.png`: `err: You provided: .png` (docs say SVG and GIF only, so consistent).
- No documented D2-language claim on these pages was contradicted; only the man page is stale relative to `d2 --help` (section 16).
