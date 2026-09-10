# D2 core language reference (verified on d2 v0.7.1, `--layout elk`)

Sources: the official tour at https://d2lang.com/tour/intro and the docs repo
https://github.com/terrastruct/d2-docs (raw `docs/tour/*.md` plus the `static/d2/*.d2`
example files those pages embed). Reserved-keyword tables come from the D2 source
`d2ast/keywords.go` at tag v0.7.1 because the docs never list them in one place.

Every ```` ```d2 ```` block below compiled cleanly with
`d2 --layout elk file.d2 file.svg` on v0.7.1. Blocks fenced ```` ```d2-fails ```` are
documented failures; the error text follows each one.

## 1. Mental model

A D2 file is a map of keys. A key becomes a shape. `a -> b` becomes a connection and
creates any endpoint that does not exist yet. Everything after `:` is the label. Braces
after a key open a nested map (children, or attributes such as `shape`, `style`).

```d2
x -> y: hello world
```

(https://d2lang.com/tour/hello-world: a connection between shapes `x` and `y`, labelled
`hello world`.)

## 2. Shapes (https://d2lang.com/tour/shapes)

**Declaring.** Any bare line is a shape. Spaces, underscores, apostrophes and a single
hyphen are fine inside an unquoted key. Two hyphens are a connection.

```d2
imAShape
im_a_shape
im a shape
i'm a shape
# notice that one-hyphen is not a connection
# whereas, `a--shape` would be a connection
a-shape
```

Gotcha (verified): `a--shape` fails on 0.7.1 with `reserved keywords are prohibited in
edges`, because it parses as `a -- shape` and `shape` is a reserved keyword. `a--b`
would be a valid connection.

**Semicolons** put several shapes on one line: `SQLite; Cassandra`.

**Label vs key, and shape type.** The key is the identifier; the label is the display
text. They are equal unless you assign one. Use the key everywhere else (connections,
dot paths). Default type is `rectangle`; set `shape` as a nested field or with dots.

```d2
pg: PostgreSQL
Cloud: my cloud
Cloud.shape: cloud
SQLite; Cassandra
```

**Case.** "Keys are case-insensitive, so `postgresql` and `postgreSQL` will reference the
same shape." Verified: `PostgreSQL -> postgresql` yields one self-loop, not two shapes.

**Standard shape catalog** (all verified): `rectangle`, `square`, `page`, `parallelogram`,
`document`, `cylinder`, `queue`, `package`, `step`, `callout`, `stored_data`, `person`,
`c4-person`, `diamond`, `oval`, `circle`, `hexagon`, `cloud`. Special values with their
own pages: `text`, `code`, `class`, `sql_table`, `image`, `sequence_diagram`.
(`hierarchy` exists in source but is undocumented.)

**1:1 ratio shapes.** `circle` and `square` always have width == height. A long label
grows both dimensions. If you set `width` and `height` manually, both become the larger
of the two.

## 3. Connections (https://d2lang.com/tour/connections)

**Four operators**: `--` (undirected), `->`, `<-`, `<->`. Undeclared endpoints are created.
Labels go after a colon.

```d2
Write Replica Canada <-> Write Replica Australia

Read Replica <- Master
Write Replica -> Master

Read Replica 1 -- Read Replica 2: Kept in sync
```

**Connections must reference a shape's key, not its label.** Using the label creates new
shapes.

```d2
be: Backend
fe: Frontend

# This would create new shapes
Backend -> Frontend

# This would define a connection over existing labels
be -> fe
```

**Repeated connections do not override; they add.** Three lines here make three edges.

```d2
Database -> S3: backup
Database -> S3
Database -> S3: backup
```

**Chaining.** Mixed directions are allowed. A trailing label applies to every edge in the
chain. Dot paths chain too (`a.b -> c.d -> e: lbl`, verified). Cycles are fine.

```d2
# The label applies to each connection in the chain.
High Mem Instance -> EC2 <- High CPU Instance: Hosted By

Stage One -> Stage Two -> Stage Three -> Stage Four
Stage Four -> Stage One: repeat
```

**Arrowheads.** Define the special sub-shapes `source-arrowhead` and/or
`target-arrowhead` inside the connection's map. Their label is the shorthand value
(`source-arrowhead: 1`) or `label:`; their type is `shape:`.

```d2
a -> b: To err is human, to moo bovine {
  source-arrowhead: 1
  target-arrowhead: * {
    shape: diamond
  }
}

b <-> c: "Reality is just a crutch for people who can't handle science fiction" {
  source-arrowhead.label: 1
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}
```

Arrowhead `shape` values (docs list, all verified):

| value | note |
|---|---|
| `triangle` | default; `style.filled: false` allowed |
| `arrow` | "like triangle but pointier" |
| `diamond`, `circle`, `box` | `style.filled: true` allowed |
| `cf-one`, `cf-one-required` | crow's foot |
| `cf-many`, `cf-many-required` | crow's foot |
| `cross` | |

```d2
a -> b: {source-arrowhead.shape: cf-many-required; target-arrowhead.shape: cross}
c -> d: {target-arrowhead: {shape: circle; style.filled: true}}
e -> f: {target-arrowhead.shape: box; source-arrowhead.shape: arrow}
g -> h: {target-arrowhead: {shape: triangle; style.filled: false}}
i -> j: {source-arrowhead.shape: cf-one; target-arrowhead.shape: cf-one-required}
k -> l: {target-arrowhead.shape: cf-many; source-arrowhead.shape: diamond}
```

Gotchas from the docs:
- "Keep arrowhead labels short." They skip autolayout and can collide.
- "If the connection does not have an endpoint, arrowheads won't do anything." On `x -> y`
  a `source-arrowhead` is silently ignored (compiles, no visible effect).

**Referencing an existing connection.** Wrap the edge in parentheses and index it, zero
based, in declaration order.

```d2
x -> y: hi
x -> y: hello

(x -> y)[0].style.stroke: red
(x -> y)[1].style.stroke: blue
```

## 4. Containers (https://d2lang.com/tour/containers)

**Dot syntax** declares a child; the parent is created if needed. Dots work inside
connections as well.

```d2
server
# Declares a shape inside of another shape
server.process

# Can declare the container and child in same line
im a parent.im a child

# Since connections can also declare keys, this works too
apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal
```

**Nested maps** avoid repeating the prefix. Connections inside a map are scoped to it,
so `db` under `aws` and `db` under `gcloud` are two shapes. From outside, use the full
dotted path from the root. Container labels: shorthand `key: Label {` or the reserved
keyword `label` inside the map.

```d2
clouds: {
  aws: AWS {
    load_balancer -> api
    api -> db
  }
  gcloud: {
    label: Google Cloud
    auth -> db
  }

  gcloud -> aws
}

users -> clouds.aws.load_balancer
users -> clouds.gcloud.auth

ci.deploys -> clouds
```

**Referencing the parent with `_`.** Inside a map, `_` means the enclosing container;
`_._` goes two levels up. Works for connections and attribute paths.

```d2
christmas: {
  presents
}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
  _.christmas.style.fill: "#ACE1AF"
}
```

Gotcha (verified): `_` at the root scope fails with `invalid underscore`.

```d2-fails
_.x -> y
```

## 5. Text, Markdown, LaTeX, code (https://d2lang.com/tour/text)

**Block strings.** `|` opens a block string, an optional language tag follows on the same
line, and a line holding only `|` closes it. Standalone text uses `|md` and renders as
GitHub-style Markdown. "If you want to set a Markdown label on a shape, you must
explicitly declare the shape." Otherwise it is standalone text with no box.

```d2
explanation: |md
  # I can do headers
  - lists
  - lists

  And other normal markdown stuff
|
# Explicitly declare, even though the default shape is rectangle
explanation.shape: rectangle
```

**LaTeX** via `|latex` or `|tex`. MathJax underneath, so it is math notation only.

```d2
plankton -> formula: will steal
formula: |latex
  \lim_{h \rightarrow 0 } \frac{f(x+h)-f(x)}{h}
|
```

LaTeX gotchas from the docs:
- `font-size` styling is ignored; size inside the script with `\tiny{ }`, `\small{ }`,
  `\normal{ }`, `\large{ }`, `\huge{ }`.
- No line breaks in current MathJax; use `\displaylines{a \\ b}` as a workaround.
- Bundled plugins: amscd, braket, cancel, color, gensymb, mhchem, physics, multlines
  (`\displaylines`). Command list: https://docs.mathjax.org/en/latest/input/tex/macros/index.html

**Code blocks.** Replace `md` with a language name; syntax highlighting comes from Chroma
(https://github.com/alecthomas/chroma?tab=readme-ov-file#supported-languages).

```d2
explanation: |go
  awsSession := From(c.Request.Context())
  client := s3.New(awsSession)

  ctx, cancelFn := context.WithTimeout(c.Request.Context(), AWS_TIMEOUT)
  defer cancelFn()
|
```

Aliases: `md`→markdown, `tex`→latex, `js`→javascript, `go`→golang, `py`→python,
`rb`→ruby, `ts`→typescript. Unknown languages fall back to plain text, no error.

**Plain (non-Markdown) text**: `shape: text`. Often paired with `near` for titles.

```d2
title: A winning strategy {
  shape: text
  near: top-center
  style: {
    font-size: 55
    italic: true
  }
}

poll the people -> results
```

**Alternate block delimiters** when the body contains `|`. Use `||`, `|||`, or any run of
non-alphanumeric, non-space, non-`_` symbols after the first pipe, mirrored at the close.
A one-line block string also works (verified): `x: |md # hi |`.

```d2
my_code: |||ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
|||
# Much cleaner!
my_code2: |`ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
`|
```

## 6. Strings and quoting (https://d2lang.com/tour/strings)

**Unquoted is the default.** Leading and trailing whitespace is trimmed.

```d2
   Office Bulb   :     Philips
            Switch   ->   Office Bulb
```

**Characters that end an unquoted string** (from `d2parser/parse.go` v0.7.1; the docs only
say "certain characters that are used elsewhere in the language"):

| where | terminators |
|---|---|
| anywhere | newline, `;`, `#`, `{`, `}`, `[`, `]` |
| in a key | additionally `:`, `.`, `<`, `>`, `&`, and `--`, `->`, `-*` |
| in a value | `$` starts a variable substitution (`${x}`) |

Also: `*` in an unquoted key is a glob, `\` starts an escape (`\n` is a newline), and a
string may not begin with `...@` (import spread). Parentheses are not terminators, but
`[]` is: `x(int y): []int` fails with `unexpected text after array`.

```d2-fails
x(int y): []int
```

**Quoted strings.** Single or double quotes admit any symbol. Use double quotes when the
text has single quotes and vice versa; if it has both, use double quotes and `\`-escape.
`\n` inside an unquoted or double-quoted label breaks the line.

```d2
'$$$' -> "###"
"x(int y)": "[]int"
'$dollarbills$'
z: "He said \"it's\" fine"
x: When you go out to buy,\ndon't show your silver.
```

Gotchas (verified):
- Dots in labels are fine (`x: v1.2.3`); dots in keys mean nesting unless quoted
  (`"a.b" -> c` is one shape named `a.b`).
- Colons in labels must be quoted: `x: "a: b"`. Unquoted `y: a: b` compiles but the second
  colon is part of the label text.
- Full-width or look-alike punctuation such as `：` is not the ASCII `:` and will not act as
  a separator (troubleshooting page).

**Autoformat.** Under-indented block-string lines still parse; `d2 fmt` prepends the right
indent while keeping relative indent, and converts tabs in the base indent to two spaces.

## 7. Comments (https://d2lang.com/tour/comments)

Line comments start with `#`, own line or trailing. Block comments are wrapped in `"""`.

```d2
# Comments start with a hash character and continue until the next newline or EOF.
x -> y # I am at the end

"""
This is a
block comment
"""

y -> z
```

## 8. Overrides and `null` (https://d2lang.com/tour/overrides)

**Redeclaring merges.** The latest explicit label wins. Keys are case-insensitive, so all
of these are the same shape; final label is the last one set. Redeclaring a container
merges its children too.

```d2
visual studio code text editor
visual studio code text editor: visual_studio_code_text_editor
# Remember that shape keys are case insensitive
visual studio CODE text editor: VisualStudioCodeTextEditor
visual studio code TEXT editor: Visual Studio Code Text Editor
visual STUDIO code text editor

aws_s3: AWS S3 California {
  Monitoring -> California
}
aws_s3: "AWS S3 San Francisco, California" {
  California.San Francisco
}
# Result: one container with both Monitoring -> California and California.San Francisco
```

**`null` deletes** a shape, a connection, or an attribute. Useful after imports, in
multi-board composition, or to exempt one object from a glob.

```d2
one
two
one: null

three -> four
(three -> four)[0]: null

five: {
  style: {
    fill: pink
    stroke: green
  }
}
five.style.stroke: null
```

**Implicit nulls.** Nulling a shape also nulls its connections (every connection needs an
endpoint) and all its descendants.

```d2
one -> two
two: null

three: {
  four: {
    five
  }
}
three.four: null
```

## 9. Unicode (https://d2lang.com/tour/text#most-languages-are-supported)

There is no `/tour/unicode` page on the site (404); the content is a section of the Text
page and the example file is `static/d2/unicode.d2`. Any script works, including CJK,
Lao, Khmer and emoji. Use ASCII punctuation for D2 syntax.

```d2
a: |md
  床前明月光，

  疑是地上霜。
|

b: "トマトが赤くなったのはなぜですか？\nBecause it saw the salad dressing!👩‍👩‍👧‍👶" {
  style.font-size: 55
}

c: ສະບາຍດີ (sabaai dii) - Lao
d: ជំរាបសួរ (jomreab suor) - Khmer
a -> b -> c -> d
```

## 10. Icons and images (https://d2lang.com/tour/icons)

`icon:` takes any URL. Free catalog: https://icons.d2lang.com. Connections can carry icons.
`icon.near` overrides placement (see below).

```d2
deploy: {
  icon: https://icons.d2lang.com/aws%2FDeveloper%20Tools%2FAWS-CodeDeploy.svg
  icon.near: top-right
}
backup: {
  icon: https://icons.d2lang.com/aws%2FStorage%2FAWS-Backup.svg
}
deploy -> backup: {
  icon: https://icons.d2lang.com/infra%2F002-backup.svg
}
```

**Local files** with the CLI: `icon: ./my_cat.png` (relative to the .d2 file). Verified: a
missing file is a hard compile error, `failed to bundle local images`.

**Placement** is automatic: container icons go top-left, leaf-shape icons are centred
under or beside the label. Override with `icon.near: <position>`, same vocabulary as
labels (https://d2lang.com/tour/positions#label-and-icon-positioning):
inside `top-left`, `top-center`, `top-right`, `center-left`, `center-center`,
`center-right`, `bottom-left`, `bottom-center`, `bottom-right`; plus `outside-`
and `border-` prefixed forms such as `outside-top-center`, `outside-left-center`,
`border-bottom-right`. Note the order flip: `outside-left-center` vs `center-left`.

**Standalone icon shapes**: `shape: image`. The label sits below the picture.

```d2
direction: right
server: {
  shape: image
  icon: https://icons.d2lang.com/tech/022-server.svg
}

github: {
  shape: image
  icon: https://icons.d2lang.com/dev/github.svg
}

server -> github
```

Gotcha (verified): `shape: image` without `icon` fails with `image shape must include an
"icon" field`.

```d2-fails
x: {shape: image}
```

## 11. Reserved keywords (d2ast/keywords.go, v0.7.1)

An unquoted key that matches one of these is an attribute, never a shape. The docs' rule
(troubleshooting and SQL tables pages): "If you'd like to use a reserved keyword as a key,
just quote it."

**Simple keywords** (take a scalar value): `label`, `shape`, `icon`, `constraint`,
`tooltip`, `link`, `near`, `width`, `height`, `direction`, `top`, `left`, `grid-rows`,
`grid-columns`, `grid-gap`, `vertical-gap`, `horizontal-gap`, `class`, `vars`.

**Holder** (only meaningful with a nested map): `style`.

**Composite keywords** (may hold a map): `source-arrowhead`, `target-arrowhead`,
`classes`, `constraint`, `label`, `icon`, `tooltip`, plus the board keywords `layers`,
`scenarios`, `steps`.

**Style keywords** (only valid under `style`): `opacity`, `stroke`, `fill`, `fill-pattern`,
`stroke-width`, `stroke-dash`, `border-radius`, `font`, `font-size`, `font-color`, `bold`,
`italic`, `underline`, `text-transform`, `shadow`, `multiple`, `double-border`, `3d`,
`animated`, `filled`.

Value vocabularies from the same file: `fill-pattern` ∈ `none|dots|lines|grain|paper`;
`text-transform` ∈ `none|uppercase|lowercase|capitalize`; `near` on a shape ∈ the eight
`top-left … bottom-right` constants (no `center-center`); `near` on a label or icon ∈ the
33 inside/outside/border positions listed in section 10.

```d2
x: {
  "width": width
}
```

Gotchas (verified):
- A bare reserved key with no value fails: `x: { width }` gives `reserved field "width"
  must have a value`.
- Reserved keywords cannot be connection endpoints: `a -- shape` fails with `reserved
  keywords are prohibited in edges`.
- At root level, `label: hi` and `shape: circle` compile silently and do nothing visible.

```d2-fails
x: {
  width
}
```

## 12. Sidebar pages

Every path below is relative to `https://d2lang.com/`. Titles are the sidebar labels
(frontmatter `sidebar_label` where set, otherwise the H1). Source: `sidebars.ts` in
d2-docs. Category landing pages redirect to their first child.

- **Introduction**: What is D2 (tour/intro); Dev tool vs design tool (tour/experience);
  Design decisions (tour/design); Getting help & community (tour/community);
  Roadmap (tour/future)
- **Getting Started**: Install (tour/install); Hello World (tour/hello-world);
  Shapes (tour/shapes); Connections (tour/connections); Containers (tour/containers)
- **Special Objects**: Text & Code (tour/text); Icons & Images (tour/icons);
  SQL Tables (tour/sql-tables); UML Classes (tour/uml-classes);
  Sequence Diagrams (tour/sequence-diagrams); Grid Diagrams (tour/grid-diagrams)
- **Customization**: Themes (tour/themes); Styles (tour/style); Classes (tour/classes);
  Dimensions (tour/dimensions); Positions (tour/positions);
  Sketch (Hand-drawn) (tour/sketch); Interactive (tour/interactive); Fonts (tour/fonts)
- **Layouts**: Overview (tour/layouts); Layout engines: Dagre (tour/dagre),
  ELK (tour/elk), TALA (tour/tala)
- **In Depth**: Strings (tour/strings); Variables & Substitutions (tour/vars);
  Globs (tour/globs); Comments (tour/comments); Overrides (tour/overrides);
  Models (tour/models); Legend (tour/legend); Autoformat (tour/auto-formatter)
- **Composition**: Intro to Composition (tour/composition); Board types: Layers
  (tour/layers), Scenarios (tour/scenarios), Steps (tour/steps);
  Linking between boards (tour/linking); Export formats (tour/composition-formats)
- **Imports**: Syntax (tour/imports); Use cases: Overview (tour/imports-use-cases);
  Patterns: Model-view (tour/model-view), Modular classes (tour/modular-classes),
  Nested composition (tour/nested-composition); More examples: Version visualization
  (tour/version-visualization), Template (tour/imported-template)
- **Extensions**: Overview (tour/extensions); Official: VSCode extension (tour/vscode),
  Vim plugin (tour/vim), Obsidian plugin (tour/obsidian)
- **API**: D2 Oracle (tour/api)
- **Top level**: CLI manual (tour/man); Exports (tour/exports); Cheat Sheet
  (tour/cheat-sheet, PDF at documents/d2_cheat_sheet.pdf); Frequently asked questions
  (FAQ) (tour/faq); Troubleshooting (tour/troubleshoot); Contributing (tour/help);
  Sponsor D2 (sponsor) with child Donors (donors)

Not in the sidebar: `tour/unicode` (404; content lives on the Text page).
