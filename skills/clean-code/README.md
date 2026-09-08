# clean-code — a Claude Code skill built from *Clean Code, 2nd edition*

A skill that applies the principles of *Clean Code, 2nd ed.* (Robert C. Martin, 2025) to real
projects — and teaches them at the same time. Every session presents each principle by its book
name with the book's argument, examines the actual code against it, and decides *with* the user.
Rules are treated the way the book treats them: "guidelines, not laws."

**Goal in one sentence:** turn any project — finished, spec'd, or imaginary — into code that has
been argued clean against the book, with a written proof (`design.md`) and a smarter user as the
by-products.

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

## Layout

```
skill/
├── SKILL.md                 the skill itself — entry situations, the ladder,
│                            the disciplines, verdict formats, artifacts
├── README.md                this file
└── references/              29 files
    ├── ch01 … ch27          one distillation per chapter: named principles
    │                        with page refs, the argument, smells, trade-offs;
    │                        frontmatter carries the chapter PDF's path
    ├── appendix-clean-code-debate.md   calibration — the Martin/Ousterhout
    │                        debate; loaded when a principle's application
    │                        is contested
    └── part4-craftsmanship.md          the disciplines' sharpest rules
                             (the Oath, Ch28–33 selections, the Afterword)
```

The chapter PDFs live one directory up; the reference files are distillations, the PDFs remain
ground truth and are opened when a distillation isn't enough.

## Install

The skill is used via a symlink so it is available in every project:

```
ln -sfn "<this repo>/skill" ~/.claude/skills/clean-code
```

Then, in any project: `/clean-code` — or just ask to "clean this code" or "design this the
clean-code way". Per-project progress lives in that project's `docs/clean-code/` (`design.md`
and `state.md`), so the descent resumes across sessions.

*Private use only — the reference files distill a copyrighted book and must not be published.*
