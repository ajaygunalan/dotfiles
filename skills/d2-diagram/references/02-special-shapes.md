# D2 special shapes: sql_table, class, sequence_diagram, grid, dimensions, positions

Verified against d2 v0.7.1 with `--layout elk` and `--layout dagre`. Every example
below compiled on both engines unless a "FAILS" note says otherwise. Sources:
https://d2lang.com/tour/sql-tables, /tour/uml-classes, /tour/sequence-diagrams,
/tour/grid-diagrams, /tour/dimensions, /tour/positions, /tour/text.

Reserved keys you cannot use as shape IDs: `top`, `left`, `width`, `height`, `near`,
`label`, `shape`, `style`, `grid-rows`, etc. `left: { x -> y }` fails with
`reserved field left does not accept composite`, and `left.y -> rhs.p` fails with
`reserved keywords are prohibited in edges`. Quote them (`"label"`) or rename.

---

## 1. `sql_table`

Each key is a row. The value after the colon is the column type. A row can carry a
`constraint`. Minimal (official):

```d2
my_table: {
  shape: sql_table
  id: int {constraint: primary_key}
  last_updated: timestamp with time zone
}
```

Recognised constraints are abbreviated; anything else is printed as written:

| constraint    | rendered |
| ------------- | -------- |
| `primary_key` | PK       |
| `foreign_key` | FK       |
| `unique`      | UNQ      |
| `not_null`    | not_null |

Multiple constraints use an array: `x: int { constraint: [primary_key; unique] }`.
Reserved keywords as column names must be quoted: `"label": string`.

Foreign-key edges connect column to column (official):

```d2
objects: {
  shape: sql_table
  id: int {constraint: primary_key}
  disk: int {constraint: foreign_key}

  json: jsonb {constraint: unique}
  last_updated: timestamp with time zone
}

disks: {
  shape: sql_table
  id: int {constraint: primary_key}
}

objects.disk -> disks.id
```

With **elk** (and TALA) the edge attaches to the exact row (verified: edge y equals
the `disk` row y). With **dagre** it attaches to the table's border centre.

Tables nest in containers and accept edges from ordinary shapes, e.g. inside
`cloud: { ... }` both `blocks.disk -> disks.id` and `AWS S3 Vancouver -> disks` work.

### Styling: header vs body (verified by inspecting the SVG)

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  "label": string
  score: float {constraint: [primary_key; unique]}
  region: text {constraint: not_null}
  style.fill: "#1f3a5f"
  style.stroke: "#f4f4f4"
  style.font-color: "#ffffff"
}
```

| style key          | applies to                                             |
| ------------------ | ------------------------------------------------------ |
| `style.fill`       | header background **and** the outer border stroke      |
| `style.stroke`     | body (rows) background                                 |
| `style.font-color` | header (table name) text only                          |

Row text colours are fixed by the theme (name, type, constraint each get their own
colour). Per-row style such as `name: string {style.font-color: red}` compiles but
is ignored.

---

## 2. `class`

Each key is a field or a method. A field's value is its type. Any key containing
`(` is a method and its value is the return type; no value means void. Minimal
(official):

```d2
MyClass: {
  shape: class

  field: "[]string"
  method(a uint64): (x, y int)
}
```

Visibility prefixes (official table):

| prefix | meaning   |
| ------ | --------- |
| none   | public    |
| `+`    | public    |
| `-`    | private   |
| `#`    | protected |

`#` starts a comment, so escape it as `\#` (official):

```d2
D2 Parser: {
  shape: class

  # Default visibility is + so no need to specify.
  +reader: io.RuneReader
  readerPos: d2ast.Position

  # Private field.
  -lookahead: "[]rune"

  # Protected field.
  # We have to escape the # to prevent the line from being parsed as a comment.
  \#lookaheadPos: d2ast.Position

  +peek(): (r rune, eof bool)
  rewind()
  commit()

  \#peekn(n int): (s string, eof bool)
}

"github.com/terrastruct/d2parser.git" -> D2 Parser
```

### Quoting rules (verified)

- Types with `[` `]` must be quoted: `"[]rune"`, `"list[Item]"`. Angle brackets and
  commas are fine unquoted as a *value*: `cache: Map<string, Entry>` renders correctly.
- A **key containing a colon** (typed parameters) is split at the first colon.
  `find(id: string): Optional<Entry>` renders as field `find(id` with type
  `string): Optional<Entry>`. Quote the whole key: `"find(id: string)": "Optional<Entry>"`.
- The prefix goes inside the quotes and still works: `"+add(item: Item)": None`,
  `"#validate()": bool` (inside quotes `#` needs no backslash; `"\#other()"` also works).
- Reserved keyword as member: `"label": string`.
- `static count: int` renders as a public field named `static count`.

### Edges to members

The member key *includes its prefix*. `Order.items -> Item` when the field was
declared `-items` silently creates a second, public `items` row. Use the exact key:

```d2
Order: {
  shape: class
  -items: "[]Item"
  +total(): float
}
Item: {shape: class; +price: float}
Order.-items -> Item
Order."-items" -> Item."+price"
```

Both forms compile. Unlike `sql_table`, elk does not attach the edge to the member
row; it starts at the class border. Class-to-class edges take the usual arrowhead
labels for cardinality (`source-arrowhead: 1; target-arrowhead: 0..*`) and hollow
triangles for inheritance:

```d2
SavingAccount -> Account: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
```

---

## 3. `sequence_diagram`

Set `shape: sequence_diagram` on an object. Plain D2 syntax; two rule changes.

```d2
shape: sequence_diagram
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge or\ngolf as if they were games.
```

**Scoping:** children of a sequence diagram share one scope. `alice` referenced inside
two different groups is the same actor, not two nested copies (official):

```d2
Office chatter: {
  shape: sequence_diagram
  alice: Alice
  bob: Bobby
  awkward small talk: {
    alice -> bob: uhm, hi
    bob -> alice: oh, hello
    icebreaker attempt: {
      alice -> bob: what did you have for lunch?
    }
  }
}
```

**Ordering:** definition order is render order, for messages and actors. Predeclare
actors to fix left-to-right order (official):

```d2
shape: sequence_diagram
# Remember that semicolons allow multiple objects to be defined in one line
# Actors will appear from left-to-right as a, b, c, d...
a; b; c; d
# ... even if the connections are in a different order
c -> d
d -> a
b -> d
```

**Spans** (activation boxes): connect a nested object on an actor. Spans nest (official):

```d2
shape: sequence_diagram
alice.t1 -> bob
alice.t2 -> bob.a
alice.t2.a -> bob.a
alice.t2.a <- bob.a
alice.t2 <- bob.a
```

**Groups** (fragments): a container inside the sequence diagram that has no edges to
it, only edges or objects inside. Actors referenced inside a group must exist at the
top level, so declare them first (official):

```d2
shape: sequence_diagram
# Predefine actors
alice
bob
shower thoughts: {
  alice -> bob: A physicist is an atom's way of knowing about atoms.
  alice -> bob: Today is the first day of the rest of your life.
}
life advice: {
  bob -> alice: If all else fails, lower your standards.
}
```

Verified on 0.7.1: omitting the predeclaration does **not** error, but the actors are
created as `g.alice` / `g.bob` children of the group instead of top-level actors, so
later top-level `bob -> alice` refers to different objects. Spans inside groups work
(`alice.t1 -> bob.t1` inside a group, actors predeclared). An edge *to* a group
(`frag -> a`) compiles on 0.7.1 but is undocumented; avoid it. Groups take
`label`, `style.fill`, `style.stroke`.

**Notes:** a nested object on an actor with no connections. Notes may live in groups
(official):

```d2
shape: sequence_diagram
alice -> bob
bob."In the eyes of my dog, I'm a man."
# Notes can go into groups, too
important insight: {
  bob."Cold hands, no gloves."
}
bob -> alice: Chocolate chip.
```

**Self-messages:** `father -> father: internal debate ensues`.

**Styling.** Actors and messages style like any object: `scorer: {shape: person}`,
and a dashed reply is `scorer.t <- itemResponse.t: item {style.stroke-dash: 5}`.
Lifelines inherit the actor's `stroke` and `stroke-dash` (official):

```d2
shape: sequence_diagram
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge or\ngolf as if they were games.

alice.style: {
  stroke: red
  stroke-dash: 0
}
```

Verified extras: spans take `a.t1: {style.fill: "#ffd166"; style.stroke: "#e07a00"}`;
notes take `db."index is warm" {style.fill: "#fff3c4"}`; an actor can be
`{shape: cylinder}`. Unquoted labels `True`/`false` are parsed as booleans and render
lowercase, so quote them: `order -> caller: "True"`.

Sequence diagrams are ordinary objects: two of them in a container can be connected
(`2007 -> 2012: Five\nyears\nlater`) and they can sit in a grid cell (see section 7).

---

## 4. Grid diagrams

Two keywords: `grid-rows` and `grid-columns`. Rows only (official):

```d2
grid-rows: 3
Executive
Legislative
Judicial
```

Columns only: `grid-columns: 3` with the same three shapes. Both:

```d2
grid-rows: 2
grid-columns: 2
Executive
Legislative
Judicial
```

**Dominant direction:** when both are set, whichever appears first is the fill
order. `grid-rows: 4` then `grid-columns: 2` fills rows first; reversed fills columns.

**Width/height inside a grid** shape cells; elements in a column share a width, in a
row share a height (official):

```d2
grid-rows: 2
Executive
Legislative
Judicial
The American Government.width: 400
```

**Cells expand to fill** when only one dimension is given: with `grid-rows: 3` and six
shapes, the last row's `Voters` and `Non-voters` stretch to the row width.

**Gaps:** `vertical-gap`, `horizontal-gap`, `grid-gap`. `grid-gap` sets both; the
specific ones override it (verified: `grid-gap: 10` + `horizontal-gap: 80`).
`grid-gap: 0` builds tables (official, first two rows):

```d2
# Specified so that objects are written in row-dominant order
grid-rows: 2
grid-columns: 4
grid-gap: 0

classes: {
  header: {
    style.underline: true
  }
}

Element.class: header
Atomic Number.class: header
Atomic Mass.class: header
Melting Point.class: header

Hydrogen
1
"1.008"
"-259.16"
```

Numbers that would parse oddly (`1.008`, `-259.16`) are quoted. For data with repeats, a markdown table is easier: `savings: ||md ... ||`.

**Nesting** grids in grids (official):

```d2
grid-gap: 0
grid-columns: 1
header
body: "" {
  grid-gap: 0
  grid-columns: 2
  content
  sidebar
}
footer
```

The docs say "nesting other types is coming soon"; on 0.7.1 a grid cell may be an
ordinary container (`lhs: { x -> y -> z }`), a sequence diagram, a class, or a code
block, and a grid may sit inside a normal container with edges to it. All verified.

**Connections.** Edges to or from the grid object itself route normally. Edges
between cells of a grid are "center-center straight segments, i.e., no path-finding"
because the layout engine does not own cell positions. Verified:

```d2
grid-columns: 3
grid-gap: 40
a; b; c; d; e; f
a -> f: straight
b -> d
```

Edges between children of different cells (`lhs.y -> rhs.p`) also compile.

**Spacers.** Pad a grid with invisible shapes to align cells. `style.opacity: 0`
makes the shape (border, fill, label) fully transparent while it still occupies its
cell and reserves size. The docs' recipe uses a class (official, abridged: the full
version gives `us-east-1` five cells `a`..`e`):

```d2
classes: {
  invisible: {
    style.opacity: 0
    label: a
  }
}

grid-columns: 1
us-east-1: {
  grid-rows: 1
  a; b; c; d; e
}

us-west-1: {
  grid-rows: 1
  pad1.class: invisible
  pad2.class: invisible
  a
  # Move the label so it doesn't go through the connection
  label.near: bottom-center
}

us-east-1.c -> us-west-1.a
```

Inline form also works: `pad: "" {style.opacity: 0}`. Give spacers a label (or
`width`) matching real cells, otherwise the row or column gets the wrong size.

**Uneven padding** comes from labels of different lengths in one row or column; fix by
setting the same `width` on the cells (official `grid-padding-2` sets `width: 180`
on every pod).

---

## 5. Dimensions

`width` and `height` work on most shapes (official example uses `shape: image`):

```d2
a: {width: 300; height: 80}
b: {width: 40; height: 40; shape: circle}
a -> b
```

The docs say "These keywords cannot be set on containers, since containers resize to
fit their children." On 0.7.1 that is engine-specific:

- **elk**: `box: { width: 500; height: 300; a -> b }` compiles and is honoured.
- **dagre**: FAILS with
  `Object "box" has attribute "width" and/or "height" set, but layout engine "dagre" does not support dimensions set on containers.`
- A grid container with `width: 600` compiles on both engines.

---

## 6. Positions

### `near` constants

`top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`,
`bottom-center`, `bottom-right`. There is no `center-center`; it fails with
`near key "center-center" must be the absolute path to a shape or one of the following constants: ...`.

Title (official):

```d2
title: |md
  # A winning strategy
| {near: top-center}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people
```

Legend (official, abridged):

```d2
direction: right
x -> y: {style.stroke: green}
y -> z: {style.stroke: red}

legend: {
  near: bottom-center
  color1: foo {
    shape: text
    style.font-color: green
  }
  color2: bar {
    shape: text
    style.font-color: red
  }
}
```

Longform text: a `|md` block with `near: center-left` beside the graph.

**Constants only work on root-level shapes.** Inside a container,
`title: |md ... | {near: top-center}` FAILS with
`constant near keys can only be set on root level shapes`. A near-positioned shape may
still have edges (`legend -> x` compiles).

### Label and icon `near`

`label.near` and `icon.near` accept the constants plus `outside-` forms:
`outside-top-left`, `outside-top-center`, `outside-top-right`, `outside-left-center`,
`outside-right-center`, `outside-bottom-left`, `outside-bottom-center`,
`outside-bottom-right` (note `outside-left-center`, not `center-left`), and
`border-x` forms for labels on the border. A `tooltip` with a `near` shows permanently.

### TALA-only

- `near: <object id>` (e.g. `{near: aws}`): FAILS on 0.7.1 elk with
  `Object "note" has "near" set to another object, but layout engine "elk" only supports constant values for "near".`
  Same message for dagre.
- `top` / `left` coordinates: FAILS with
  `Object "a" has attribute "top" and/or "left" set, but layout engine "elk" does not support locked positions.`

---

## 7. Code and markdown blocks inside these shapes

`|md` for markdown, `|py`, `|go`, `|ts`, `|js`, `|rb`, `|tex` for highlighted code
(Chroma; unknown languages fall back to plain text). Code containing `|` uses a
longer or symbol-decorated fence (official):

```d2
my_code: |`ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
`|
```

Long code lines are not wrapped and can overrun the box edge; keep lines short.

---

## 8. Worked example: a code-level diagram of a Python module

Two classes with methods, one free function as a code block, and a sequence diagram
tracing one call, placed side by side with a two-column grid. Renders on elk and
dagre.

```d2
# orders.py at a glance
grid-columns: 2
grid-gap: 60

orders_py: orders.py {
  Order: {
    shape: class
    -items: "list[Item]"
    +customer_id: int
    +total(): float
    "+add(item: Item)": None
    \#validate(): bool
  }
  Item: {
    shape: class
    +sku: str
    +price: float
    +qty: int
  }
  checkout: |py
    def checkout(order: Order):
        assert order.validate()
        return bill(order.total())
  |
  Order -> Item: "items 0..*"
  checkout -> Order: calls
}

trace: checkout(order) call trace {
  shape: sequence_diagram
  caller; checkout; order; item
  caller -> checkout.t: checkout(order)
  checkout.t -> order.t: validate()
  order.t -> checkout.t: "True"
  checkout.t -> order.t: total()
  order.t -> item.t: price * qty
  item.t -> order.t: 12.5
  order.t -> checkout.t: 12.5
  checkout.t -> caller: Receipt
}
```

Render check: code block, `Order`, `Item` stack inside the container with routed
edges; one span per actor; `"True"` keeps its capital; `"+add(item: Item)"` keeps
its `+` prefix and the parameter's colon.
