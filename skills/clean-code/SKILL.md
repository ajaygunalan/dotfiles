---
name: clean-code
description: Apply Clean Code 2nd ed (Robert C. Martin) to a project — clean existing working code, design a new system from a spec or a bare idea, or review architecture, components, classes, and functions against the book's named principles. Use when the user says "clean code", asks to clean/refactor/review code against the book, or wants to design something the clean way. Interactive — teaches each principle as it applies, judges with trade-offs, never blindly enforces.
---

# Clean Code — the book as a working discipline

This skill applies *Clean Code, 2nd edition* to real projects. Two commitments:

1. **Teach while doing.** Present each principle by its book name, with the book's argument for it and how it applies to the code at hand — then decide together with the user. Every session is also a lesson. Cite principles by name and chapter ("SRP — responsible to one, and only one, actor; Ch19").
2. **Judge, don't enforce.** The book calls its own rules "guidelines, not laws" (Ch03), "biases" (Ch08), "warnings" (Ch19). Before flagging a violation, look for a stated reason in the code, comments, or docs. When a call is contested — decompose or not, comment or not, TDD or not — read `references/appendix-clean-code-debate.md` first. "Complexity is in the eye of the reader": if the user finds a structure confusing, that is a finding regardless of the rules. Critique code, never people.

## The whole skill in one picture

```
                              ╭──────────────╮
                              │ /clean-code  │
                              ╰──────┬───────╯
                 INPUT: where is your project right now?
   ┌─────────────────────┬──────────┴──────────┬─────────────────────┐
   │  working code       │  spec, no code      │  bare idea          │
   └──────────┬──────────┴──────────┬──────────┴──────────┬──────────┘
              ▼                     ▼                     ▼
      "CLEAN THAT CODE"      CONTINUOUS DESIGN      UP-FRONT DESIGN
       walk the ladder        Up-front (thin)        policy vs detail,
       top → down:            sketch + boundaries    boundaries, table
                                     │               of decisions NOT
       ▸ Architecture                ▼               made
       ▸ Components           slice into small              │
       ▸ Classes              behavioral units              ▼
       ▸ Functions                   │               then build like
       ▸ Names & format              ▼               the spec path ──┐
              │               test by test:                          │
              │               make it WORK, then                     │
              │               make it RIGHT ◄────────────────────────┘
              │                      │
              └─────────┬────────────┘
                        ▼
        ╔═══════════════════════════════════════════════╗
        ║  EVERY RUNG · EVERY CYCLE — the same loop     ║
        ║                                               ║
        ║  teach the principle (book name + why)        ║
        ║   → examine the code → diagram (D2)           ║
        ║   → discuss (user decides, book cited)        ║
        ║   → clean one little thing, tests stay green  ║
        ║   → grade: Clarity·Concise·Confirm·Cohesion   ║
        ║                                               ║
        ║  gate: trusted tests first, always            ║
        ║  stance: judge with trade-offs, never enforce ║
        ╚═══════════════════╤═══════════════════════════╝
                            ▼
                          OUTPUT
   ┌────────────┬──────────────────┬──────────────┬─────────────────┐
   │ design.md  │ state.md         │ cleaner code │ a smarter user  │
   │ diagrams,  │ where you are;   │ checked in   │ learned the     │
   │ verdicts,  │ next session     │ cleaner than │ principles that │
   │ exceptions │ resumes here     │ checked out  │ applied to THIS │
   │ (the proof)│ (multi-session)  │ (Boy Scout)  │ actual code     │
   └────────────┴──────────────────┴──────────────┴─────────────────┘
```

## Knowledge base

- `references/chNN-*.md` — one distillation per chapter (Ch01–27): named principles with page refs, the argument, a distilled example, smells, trade-offs, process prescriptions.
- Each reference file's frontmatter carries the absolute path of its chapter PDF. When the distillation is not enough for the case at hand, open the PDF at the cited pages.
- `references/appendix-clean-code-debate.md` — calibration: the Martin/Ousterhout debate, including Martin's own concessions.
- `references/part4-craftsmanship.md` — the disciplines' sharpest rules (the Oath, Ch28–33 selections, the Afterword).

Load only what the current rung or activity needs; never all files at once. For a first overview lesson — or a user new to the book — ch03 (First Principles) demonstrates the whole ladder on one worked example: "you'll be 90% of the way toward cleaning code." ch01 and ch02 carry the founding arguments (the Boy Scout Rule, clean-as-a-verb) worth teaching once, early.

## Entry: where is the project?

Determine which situation applies at trigger (ask the user if ambiguous):

| Situation | Book term | What happens |
|---|---|---|
| Working code exists | **Clean That Code** (Ch02) | The Cleaning Process, top of the ladder downward |
| Spec exists, no solution code | **Continuous Design** (Ch21) | Up-front Design → Readying → Starting → Doing Work |
| Bare idea, nothing written | **Up-front Design** (Ch21/25) | Thin boundary sketch first, then Continuous Design |
| Expanding existing code | Both | Clean That Code on what exists, Continuous Design on what's new |

## The precondition — before any cleaning

References for this gate: ch09, ch14, ch15, ch16, part4-craftsmanship.

"Clean code depends on fast, convenient, and comprehensive tests" (Ch09). Before restructuring anything:

- Is there a suite the team would deploy on when green? "Your tests are good enough if, when they pass, you feel comfortable deploying" (Ch31).
- If the suite is thin where you are about to work, write tests there first (Ch14–16). The proof must be **quick, sure, repeatable** (Ch30).
- Never disable a failing test — "that's when the tests become lies" (Ch31).
- Coverage numbers are a developer tool, never a gate (Ch32). Never issue a "raise coverage to N%" finding; judge semantic stability instead.

## The ladder — Clean That Code order

Clean code makes bricks; SOLID arranges bricks into walls and rooms; component principles arrange rooms into buildings; architecture draws the boundary lines (Ch19–20). Examine top-down, one rung per session-sized pass. A discovery at a lower rung may legitimately reopen a higher one — in the book's own Video Store example, function extraction is what revealed the hidden classes (Ch10).

| Rung | References | Anchors |
|---|---|---|
| Architecture | ch23, ch24, ch25, ch27 | The Dependency Rule; policy vs detail; "a good architecture maximizes the number of decisions not made"; use cases visible |
| Components & boundaries | ch20, ch26 | REP/CCP/CRP, ADP/SDP/SAP, the tension diagram; adapters, learning tests, boundary tests |
| Classes | ch12, ch13, ch19, ch18 | SRP (one actor), OCP, Data/Object Antisymmetry, Law of Demeter, Beck's four rules of simple design |
| Functions | ch07, ch08, ch10, ch11, ch05 | Small, One Thing, Extract Till You Drop, the Stepdown Rule, PINCH, CQS, comments compensate for failure |
| Names & formatting | ch04, ch06 | Intention-revealing names, scope-proportional length, Team Rules |

Naming (ch04) is checked at **every** rung, not just the last — "rename as insight accrues" (Ch03).

**Per rung: teach → examine → diagram → discuss → clean → grade → record.**

- Teach the rung's principles briefly, from the reference files, before pointing at the user's code.
- Diagram the current (and, if cleaning, proposed) structure with D2; the diagram goes in `design.md`.
- Clean via the refactoring loop (Ch09): clean one little thing, run the tests, revert if they fail. One change at a time, suite green after each.
- Duplication verdicts use **Accidental vs Essential Duplication** (Ch08/Ch18): duplicates with divergent intent (different actors, per SRP) must persist; convergent intent gets extracted.
- Grade the rung with **the Four Cs** (Ch21): Clarity / Conciseness / Confirmability / Cohesion — Pass/Fail each, as the book itself grades modules.
- Verdict per finding: **conforms** / **deliberate exception** (record the stated reason) / **cleaned**.
- The user approves before any change is applied. Session ends when the rung is discussed and recorded, not necessarily when everything is fixed.

## The disciplines — always on while writing or changing code

References: ch02, ch09, ch14 (and part4-craftsmanship for the sharpest rules); ch15/ch16 when writing tests; ch17 when AI generates code; ch22 when the code has concurrency.

- Kent Beck's law: "First, make it work. Then, make it right" — at the size of **one test, not one story** (Ch29). Never check in the work half alone; "later equals never" (LeBlanc's law, Ch01).
- The Clean Method's nested loops (Ch09): writing loop → refactoring loop → outer loop, transitioning "as often as possible."
- A testing discipline — TDD, TCR, or Small Bundles (Ch14) — chosen with the user, then followed.
- "The greater the urgency, the less the relevance" (Ch29): behavior is urgent, structure is important; the skill defends structure precisely when deadlines press.
- The Boy Scout Rule (Ch01): every touched file goes back cleaner than it came out.
- Done means "the code reads well" (Ch11), not "it works."
- Severity is judged by Ch28's definition: structural harm = anything that makes source hard to read, understand, change, or reuse. Rigidity / fragility / immobility (Ch29) are the named smells of accumulated harm.
- AI-generated code is never implicitly trusted; the programmer is the final arbiter (Ch02/Ch17). State intent at least two ways — code plus tests/scenarios — so each catches the other's errors (Overloading, Ch17). Honor project-specific rules (e.g., AI-declaration comments).
- Concurrency in the touched code? Load ch22 for that pass.

## Continuous Design — new work

References: ch21, plus the architecture rung's files (ch23, ch24, ch25, ch27) for the Up-front Design session.

- **Up-front Design** (Ch21): summary diagrams and speculative sketches only. Draw the few boundaries that defer decisions (Ch25 — the FitNesse move: define the interface, stub it, let the real thing wait, possibly "into nonexistence"). Record a **deferred-decisions table** — "a good architecture maximizes the number of decisions not made" (Ch23). Make the use cases visible in the structure (Ch24). Do **not** design the component structure top-down before modules exist (Ch20) — it evolves and "jitters" as code accumulates.
- **Readying for Work / Starting Work** (Ch21): slice the feature into small behavioral units.
- **Doing Work** (Ch21): test by test under the disciplines; edit each unit for clarity, conciseness, and cohesion before the next test.
- Let abstractions **emerge** — don't build the hierarchy until the third feature reveals it (Afterword, the Ward Cunningham story).
- When the new code is in place, finish with a pass down the ladder — a light one, because cleaning happened inside every cycle.

## Project artifacts — multi-session state

In the target repo, `docs/clean-code/`:

- **`design.md`** — the durable record: per-rung D2 diagrams, Four Cs grades, verdicts, deliberate exceptions with their reasons, the deferred-decisions table. Written to be readable on its own; for spec'd projects it can *be* the deliverable design document.
- **`state.md`** — bookkeeping only: current situation and rung, open questions, agreed next step. Read it first on every trigger; update it before ending every session.

## Session shape

1. Read `state.md` (or establish the situation on first run).
2. Confirm with the user what this session covers (which rung, or which behavioral unit).
3. Run the pass: teach → examine → diagram → discuss → clean → grade → record.
4. Update `design.md` and `state.md`. Tell the user where the descent stands and what comes next.
