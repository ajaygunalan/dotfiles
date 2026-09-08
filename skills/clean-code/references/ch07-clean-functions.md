---
chapter: 7
title: Clean Functions
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch07_Clean_Functions.pdf
pages: 22
level: function
---

# Ch07 — Clean Functions

**Thesis:** Functions are the first line of organization in any modern program. Six decades of trial and error taught Martin one overriding lesson: functions should be *very* small — a dozen lines or less — each doing one thing at one level of abstraction, each with a descriptive name, each leading to the next in a compelling top-down order. A clean function has five attributes — Nameable, Insulated, Homogenous, Contextual, Pure (the "PINCH" attributes) — and code composed of such functions reads like well-written prose.

## Named principles & rules

- **Small!** — Functions should be very small; Martin's mature practice is "a dozen lines or less." The old eighties rule was "no bigger than a screenful" (~20 lines on a VT100) (pp. 138–139).
- **One Level of Abstraction per Function** — All statements within a function must be at the same level of abstraction, which is one level below the function's name. Mixing levels (high-level looping next to `frequentRenterPoints++`) confuses readers and, broken-windows-style, attracts more details into the function (pp. 139–140).
- **The Stepdown Rule** — Code should read as a top-down narrative: every function is followed by those at the next level of abstraction, so the program reads descending one abstraction level at a time (pp. 140–142). Restated under Homogenous: "The lines of a function should all be at the same level of abstraction, which is one level below the name" (p. 151).
- **Functional decomposition** — The '70s/'80s *structured programming* discipline of decomposing high-level functions into lower-level functions, creating a hierarchy of calls; following it makes functions naturally small (p. 142).
- **Entanglement** — John Ousterhout's named objection: two functions are entangled when, to understand one, you must understand the other. Martin tolerates a bit of it so long as functions step down one abstraction level; Ousterhout would merge entangled functions (p. 142).
- **[Switch statement rule]** — Switch statements (including if/else chains) always do N things and are hard to make small. They can be tolerated if they appear only once, live in a concrete low-level module like `main`, create polymorphic objects, and are hidden behind an interface so the rest of the system can't see them — e.g., buried "in the basement of an Abstract Factory" (pp. 142–144). The bad switch violates the **Single Responsibility Principle (SRP)** and the **Open–Closed Principle (OCP)** (p. 143).
- **PINCH attributes** — "A clean function should have five attributes. It should be nameable, insulated, homogenous, contextual, and pure. If you reorder that, it spells PINCH" (p. 144).
- **Contextual** — Every function lives within a context: a cooperative grouping of functions and data structures with an external interface and internal implementation. The programmer's job is to identify, create, and manage those contexts and their public/private boundaries (pp. 144–145).
- **Nameable / Descriptive** — The name must describe what the function does, be a verb, verb phrase, or implicit verb (like `Math.sign(x)`), and be slightly more abstract than the code — it should hide the implementation (`average`, not `addAtoBandDivideBy2`) (pp. 145–146). Ward Cunningham's principle: "You know you are working on clean code when each routine turns out to be pretty much what you expected" (p. 147). Don't fear long names; experiment with several names in place (p. 147).
- **Nameable / Convenient** — Names must also be short and memorable in proportion to how often they're called, yielding the heuristic: *"The length of the name of a function should be inversely proportional to the size of the containing scope"* (p. 147). Global functions get short general names (`File.open`); deep private functions get long detailed names (pp. 147–148).
- **Insulated** — Old terms: *low coupling* or *encapsulation*. Every input/output of a function is a coupling ("strand"); limit argument counts (Martin prefers "a limit of three where feasible") and use contexts so functions communicate without long argument lists (pp. 148, 151).
- **Homogenous** — Every line of the function sits at the same abstraction level, one below the name (pp. 151–153).
- **Pure** — A pure function's behavior depends on nothing but its arguments, and its execution causes no other function's behavior to change. Rule of thumb: "No Assignment Statements Ever!" — pure functions are immutable (p. 153). Crucially, *purity is an external characteristic, not an internal one*: a function is pure so long as all impurity is hidden from all external observers, including other threads (pp. 153–155).
- **Partial Purity** — Purity is an observed quality; whether a function is pure depends on what is being observed. `fopen` is impure, but `openAndDo` (open, invoke, close) restores the system state and is pure "for all intents and purposes" — to observers who don't care about the file's contents (pp. 155–156).
- **First, make it work. Then, make it right.** — Write the depth-first draft to get it working, then refactor abstraction levels out into nicely named functions (p. 142).

## The argument

Small functions with descriptive names turn code into narrative. Martin's formative evidence was pairing with Kent Beck on the *Sparkle* program in 1999: "Every function in this program was just two, or three, or four lines long. Each had a descriptive name. Each was transparently obvious. Each told a story. And each led you to the next in a compelling order" (p. 138). Small functions force the blocks inside `if`/`else`/`while` to be one or two lines — usually a well-named call — so control statements "read like well-written prose" (p. 139), and nesting depth stays at one or two.

Mixing abstraction levels is the root confusion: "Readers may not be able to tell whether a particular expression is an essential concept or a detail. Worse, like broken windows, once details are mixed with essential concepts, more and more details tend to accrete within the function" (p. 140).

The PINCH attributes generalize this: contexts create insulation boundaries between what changes often (low-level) and what doesn't (high-level); naming trades descriptiveness against convenience by scope; and purity — even the engineered illusion of purity — eliminates race conditions, eases testing, composition, and distribution (p. 153). "That is how all functional programming languages claim purity. They just hide the impurity of the underlying implementation" (p. 155).

## Distilled example

The Video Store `statement()` function (Golang, pp. 139–140): one function mixing looping over rentals, a `switch` on movie type, price arithmetic, and string formatting — three abstraction levels tangled together.

After (pp. 140–141), via the Stepdown Rule:

```go
func (statement *RentalStatement) makeStatement() string {
  statement.clearTotals()
  return statement.makeHeader() +
         statement.makeDetails() +
         statement.makeFooter()
}
```

with `clearTotals`, `makeHeader`, `makeDetails`, `makeDetail`, `formatDetail`, `makeFooter` each a few lines, each one level below its name. The remaining `switch` in `determineAmount()` is then hidden behind a `RentalTypeFactory` interface creating polymorphic `RentalType` derivatives (pp. 143–144).

Secondary example (Homogenous, pp. 151–152): `orientation(a,b,c)` computing a cross product plus a four-line sign test → extract `sign()`; then rename to `getChirality`/`crossProduct`/`chirality` returning a `Chirality` enum — twice as long, far more readable.

## Smells & checklist

- Function longer than a dozen lines or so; indent depth greater than one or two.
- Blocks inside `if`/`else`/`while` longer than one or two lines, or not a named call.
- Statements at mixed abstraction levels within one function; lines more than one level below the function's name.
- Function name that exposes implementation (`addAtoBandDivideBy2`) instead of intent (`average`).
- Name length inverted against scope: long-winded names on global/public functions, cryptic short names on deep private ones.
- Repeated or visible `switch`/`if-else` chains on a type code — should appear once, low, behind an interface, creating polymorphic objects.
- More than three arguments — ask why they aren't an object/data structure, or whether the data belongs in separate contexts (p. 151).
- Callees positioned before or far from callers, breaking the top-down read.
- Impurity visible to external observers (shared state mutated across function boundary) where it could be hidden.

## Trade-offs & exceptions

- Smallness "is not a hard-and-fast rule, and it can be overdone. There are certain functions that read better if they are not decomposed into smaller four-line functions. But these are exceptional cases" (p. 139).
- Entanglement is a real cost of decomposition; Martin and Ousterhout genuinely differ on how much to tolerate (p. 142).
- Switch statements can't always be avoided — the rule is to bury and not repeat them, not to ban them (pp. 142–144).
- Descriptive vs. convenient naming is an explicit trade-off governed by scope size (p. 147).
- Functions will sometimes legitimately take three or more arguments; the trigger for redesign is passing more than three (p. 151).
- The homogenized/renamed `orientation` refactoring costs a few CPU cycles; unless you desperately need 50ns, maintainer time is worth more (pp. 152–153).
- Strict purity ("no assignment ever") is relaxed pragmatically: internal mutation, mutable helper objects, even partial purity are fine so long as observers can't tell (pp. 154–156).

## Process prescriptions

- Write functions depth-first to get them working, then refactor the abstraction levels out into nicely named functions: "So, first, make it work. Then, make it right" (p. 142). Refactoring discipline is "a critical element of this approach."
- When naming, try several different names and read the code with each in place; hunting for a good name often triggers a favorable restructuring (p. 147).

## Open the PDF when

- You need the full TurnstileFSM state-machine example showing contexts/insulation in working code (pp. 148–151).
- You need the four `sigma` implementations demonstrating the spectrum from strict purity to hidden mutation via `SigmaCalculator` (pp. 153–155).
- You're debating decomposition granularity with someone citing Ousterhout — the Entanglement passage's exact wording matters (p. 142).
