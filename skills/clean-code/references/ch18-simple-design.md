---
chapter: 18
title: Simple Design
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch18_Simple_Design.pdf
pages: 12
level: class | component | tests | cross-cutting
---

# Ch18 — Simple Design

**Thesis:** The best design is the simplest one that supports all required features while affording the greatest flexibility for change — but "simple does not mean easy. Simple means untangled" (p. 331). The most expensive entanglements convolve high-level policies with low-level details; a simple design keeps high-level policies ignorant of and isolated from low-level details, chiefly through abstraction and polymorphism. Kent Beck's four rules of simple design — covered by tests, reveals intent, minimizes duplication, minimizes size — applied in that priority order, get you most of the way there.

## Named principles & rules

- **Kent Beck's four principles of simple design** — the chapter's frame; a design is simple if it: 1. Covered by tests, 2. Reveals intent, 3. Minimizes duplication, 4. Minimizes size — in that priority order (p. 332). Beck's claim: follow these four diligently and all other design principles are satisfied — "the principles of design can be reduced to coverage, expression, singularization, and reduction" (p. 339).
- **YAGNI** ("You aren't gonna need it") — every time you think "I'm going to need this hook," ask what would happen if you left it out; if the cost of leaving it out is tolerable, don't put it in. Also ask the inverse: "What if I'm *not* gonna need it?" (p. 333). This discernment is "one of the most important disciplines of good software design" (p. 333).
- **Covered by Tests** (rule 1) — the only reasonable coverage goal is 100%, held as an **asymptotic goal**: you may never reach it, but that's no excuse for not getting closer with every check-in (pp. 333–334).
- **[Testable code is decoupled code]** — the book's italicized maxim (p. 334): achieving high coverage forces each part to be isolatable and invokable from a test, so tests "are also tests of decoupling"; being tested is itself an act of design.
- **Maximize Expression / Reveals intent** (rule 2) — modern languages are immensely expressive; with discipline, code can read "like well-written prose" (p. 335). Expressivity is not just good names: it is also "the separation of levels and the exposition of the underlying abstraction" (p. 336) — each line, function, and module lives in a well-defined partition depicting its level.
- **[Code and tests together communicate]** — Kent Beck's original phrasing of the expression rule: "The system (code and tests) must communicate everything you want to communicate" (p. 337). Production code cannot communicate the context in which it is used; that's the job of the tests — well-written isolated tests are example use cases.
- **Minimize Duplication** (rule 3) — reduce similar stretches of code to a single instance by abstracting into a function with arguments that communicate the differences in context (p. 338). Duplication leads to fragility: duplicates must be found and modified together, in different contexts.
- **Accidental Duplication** — not all duplication should be eliminated: two stretches may be identical yet change for very different reasons. "Accidental duplicates should not be eliminated. The duplication should be allowed to persist" — as requirements change, the duplicates evolve separately and dissolve (pp. 338–339). Test: accidental duplications have *divergent intent*; real duplications have *convergent intent* (p. 339).
- **Minimize Size** (rule 4) — "A simple design is composed of as few simple elements as possible without compromising test coverage and expression" (p. 339). Only after tests pass, expression is maximal, and duplication minimal do you decrease modules, classes, functions, and lines.
- **Dependency Inversion Principle (DIP)** (referenced) — keeping all source-code dependencies pointing from low-level details to high-level policies via polymorphic interfaces "is the essence of the Dependency Inversion Principle" (p. 332); it is the physical means of the abstraction simple design requires.

## The argument

Entanglement of high-level policy with low-level detail (SQL with HTML, frameworks with core values, report format with business rules) is easy to write but makes systems hard to extend, fix, and clean. "A simple design is a design in which high-level policies are ignorant of low-level details" (p. 332). The primary means of separation is *abstraction* — "the amplification of the essential and the elimination of the irrelevant" (p. 332) — physically realized via polymorphic interfaces so low-level details depend on high-level policies.

The four rules are ordered by dependency: without a covering test suite the other three rules "become impractical, because those rules are best applied *after the fact*" — they are refactoring rules, and "refactoring is virtually impossible without a good, comprehensive suite of tests" (p. 334). Expression comes next because telling real from accidental duplication "depends strongly on how well the code expresses its intent" (p. 339). Duplication removal is third; size reduction last.

## Distilled example

Payroll (pp. 336–337). Requirements: hourly employees paid Fridays with overtime; commissioned employees paid 1st/3rd Friday base + commission; salaried monthly. A switch/if-else chain over employee types would obscure the underlying abstraction. The expressive high-level form:

```java
public List<Paycheck> run(Database db) {
  Calendar now = SystemTime.getCurrentDate();
  List<Paycheck> paychecks = new ArrayList<>();
  for (Employee e : db.getAllEmployees()) {
    if (e.isPayDay(now))
      paychecks.add(e.calculatePay(now));
  }
  return paychecks;
}
```

No mention of any of the hideous details that dominate the requirements: "The underlying truth of this application is that we need to pay all employees on their payday" (p. 337). Contrast: a 1960s PAL-8 assembly listing (pp. 334–335) where ubiquitous comments were mandatory because code revealed nothing, vs. the small Java `RentalCalculator` whose intent is clear at a glance (pp. 335–336).

## Smells & checklist

- Is every part of the changed code reachable by an isolated test? Coverage moving toward 100% with each check-in?
- Do high-level policies mention low-level details (SQL, HTML, frameworks, formats)? Dependencies should point detail → policy through interfaces.
- Does each function/module sit at one clearly-depicted level of abstraction, in a well-defined partition?
- Would a cursory glance reveal the designer's basic intent (names of variables, functions, types deeply descriptive)?
- Do tests demonstrate intended usage — example use cases for each part?
- Similar stretches of code: convergent intent (real duplication — abstract it) or divergent intent (accidental — leave it)?
- Repeated traversal of a complex data structure: encapsulate once and pass operations in via lambdas, Command objects, Strategy, or Template Method (p. 338).
- Speculative hooks: was "what if I'm not gonna need it?" asked? Cost of carrying the hook vs. odds of needing it weighed?
- After the other three rules: can the count of modules, classes, functions, lines be reduced?

## Trade-offs & exceptions

- 100% coverage "may, in fact, be impractical depending on the situation" — it is asymptotic, not attained (p. 333).
- YAGNI is discernment, not a ban: "It is always wise to think of the future, and there are times when putting a particular hook in is a good idea" — count costs on both sides (p. 333).
- Accidental duplication must persist; eliminating it couples things that change for different reasons (pp. 338–339). Managing duplication is nontrivial and "requires a significant amount of thought and care" (p. 339).
- Historical note: in the 1950s duplication avoidance was driven by memory cost — "often a good trade-off" the other way (p. 338); the calculus depends on context.
- Martin himself hedges on Beck's reduction claim: "I don't know if this is true or not" — a covered, expressed, singularized, reduced program may not automatically conform to OCP or SRP; knowing SOLID still matters (p. 339).

## Process prescriptions

Apply the four rules in priority order: (1) get tests covering the system first — they enable everything else; (2) refactor for expression; (3) *then* eliminate real duplication (needs expression to judge intent, needs tests to refactor safely); (4) *then* minimize size. YAGNI questioning ("what if I don't need it? what if I do?") applies continuously at every design decision.

## Open the PDF when

- You need the full 1960s assembly listing or the complete `RentalCalculator` code for teaching contrast (pp. 334–336).
- Debating a specific duplication case — the traversal-code discussion and pattern options (p. 338) carry more nuance than summarized here.
- Tracing the connection to Clean Craftsmanship (this chapter is an abridged excerpt from it, authored with/attributed to Kent Beck, p. 331).
