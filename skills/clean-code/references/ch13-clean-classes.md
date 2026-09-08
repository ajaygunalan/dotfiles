---
chapter: 13
title: Clean Classes
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch13_Clean_Classes.pdf
pages: 22
level: class
---

# Ch13 — Clean Classes (by Jeff Langr)

**Thesis:** The advice of Clean Functions echoes one organizational level up: a class (or module) should gather a small number of closely related behaviors under a name that concisely summarizes them. Class design quality can only be assessed in the face of change — a clean class has one reason to change (SRP), stays closed to modification while open to extension (OCP), and separates policy from implementation detail. You get there not by speculation but by responding to each actual demand for change: extract, move code to where it wants to live, and let small, closed, cohesive, single-purpose classes accumulate.

## Named principles & rules

- **[One class/module per file]** (pp. 267–268): "Just because you can doesn't mean you should. Generally, stick to a single module or class per source file" — with concessions for very closely related types (small structs/records, exception types) consumed alongside the file's primary type.
- **Kent Beck's four rules of emergent design** (p. 270): Ensure all code is testable as you go; eliminate logical redundancies; ensure all programmatic elements are clearly and concisely named; minimize the number of elements. Cited as the exemplar of *positive heuristics*.
- **Copy-paste programming** (p. 270): The exemplar antipattern (*negative heuristic*) — don't habitually create new logic by duplicating existing code and changing it ("grab and stab," "snatch and patch").
- **SOLID** (p. 270): Bob Martin's five class-design principles — the exemplar of *positive characteristics* — "withstood around three decades of scrutiny, and can be practically applied to functional code as well."
- **Code smells / shotgun surgery** (p. 270): Fowler's code smells are the exemplar *negative characteristics*; shotgun surgery means "your code forces you to make updates to numerous classes in order to effect simple changes."
- **Design perspective** (p. 270): The chapter's umbrella term for any codified collection of heuristics (steps to take/avoid) and characteristics (desired/undesired traits), at method (micro) or class (macro) level. Outcomes of SOLID, simple design, and code smells are comparable: all foster small, cohesive modules and functions.
- **Single Responsibility Principle (SRP)** (pp. 271–273): An ideal class is small, cohesively defined, performs a single well-defined task — "It has one reason to change." Benefits: locatable behaviors, reuse, likelier OCP adherence, easier testing, flexibility (p. 272).
- **[Policies in code]** (pp. 272–275): Each behavior implements a *policy* — a set of rules established by the domain and implemented in code. Policies that can change independently suggest a class each; a buried conditional (`//late?`) is a policy decision and thus another reason to change.
- **"Extract till you drop"** (p. 275): From Ch10 "One Thing" — step 1 of fixing a buried policy is extracting the conditional into an intention-named method (`isLate`). A clear method name obviates the guiding comment: "Comments are the distracting footnotes of code."
- **Feature envy** (p. 276): A method that asks another class multiple questions to compute a result while showing disinterest in its own class. Soothe the envy by moving the method to the class it envies ([Refactoring]).
- **Open–Closed Principle (OCP)** (p. 278): "We want to minimize 'opening up' existing classes to make changes, and instead find ways to enhance a system by adding new, single-purpose classes." Open classes introduce risk and cost.
- **Strategy** (pp. 278–282) (also **State**, p. 284; both [GOF95]): The chapter's chosen mechanism for closing classes — extract each branch's calculation into a small class implementing a common interface (`LateStrategy`), then let the type (`MaterialType` enum) carry its strategy so the switch disappears.
- **[Prefactoring]** (p. 278): "We'll prepare for the new requirement by first factoring the code (prefactoring it) so that the change effort is smoother and has minimal impact."
- **[Don't mix policy with implementation detail]** (p. 284): An SRP-compliant service should either contain only orchestration logic that declares policy and delegates, or contain only implementation specifics for related behaviors. A policy change and a detail change are two different reasons to change.
- **"Sub-behavioral unit"** (p. 286): A small, closed unit (like a days-late fine policy) that is a concept, testable in isolation without exposing implementation specifics, movable to any context where it's useful.
- **Method object** (p. 287): A new class embodying a single troubled method — sometimes the best route when getting AI (or a human) to untangle a long method ([WELC]).

## The argument

"The quality of a design can only truly be assessed in the face of change" (p. 269). Without sensible class organization you can't find code, you bloat the system with redundancy, you create defects from inconsistency and complexity, and you drown in test-writing effort (p. 268). The chapter traces modularization from von Neumann/Goldstine's subroutine premise through Wilkes and Wheeler's EDSAC to today's heuristics.

The core demonstration is change-reason archaeology on a library `HoldingService`: policies (due dates, fines, check-in) hide inside long methods, and "change reasons are buried within the body of a long method" (p. 274). Extraction reveals feature envy; moving methods puts code where it belongs: "Do this enough, and eventually most code makes it to the right place, and each such place is reasonably small, cohesive, and easy to work with" (p. 277). SRP and OCP are ideals, not laws: "You want to almost always move in their direction, not away from them. It might be OK that you'll never hit the ideal" (p. 285). The closing sections argue clean, SRP/OCP-compliant modular design matters *more* with AI code generation, since regenerating a module from examples and tests only works if modules are single-purpose (pp. 286–287).

## Distilled example

The `HoldingService.checkIn` refactoring arc (pp. 274–282):

```java
// Before: policy buried in a conditional inside a long method
if (holding.dateLastCheckedIn().after(holding.dateDue())) { //late?
```

1. Extract predicate: `if (isLate(holding))` — comment disappears into the name (p. 275).
2. `isLate` shows feature envy of `Holding`; move it there: `if (holding.isLate())` (p. 276).
3. `calculateLateFine` also envies `Holding`; moved, it exposes a drippy `switch` over material types with three reasons to change — an OCP violation (pp. 277–278).
4. Extract each branch into Strategy classes (`DaysLateStrategy`, `ConstrainedFineStrategy` implementing `LateStrategy`), attach a strategy to each `MaterialType` enum value; `calculateLateFine` collapses to one delegating line (pp. 278–282).
5. New requirement (games & puzzles, new fine scheme): test-drive `DegradingFineStrategy`, add one enum line — under 20 minutes, no existing tests changed (pp. 282–283).

## Smells & checklist

- Class name can't concisely summarize its behaviors; methods not closely related and focused (pp. 270–271).
- More than one reason to change: list a class's behaviors/policies and ask which could change independently (pp. 272–273).
- Change reasons buried in long method bodies; line-level comments (`//late?`) marking policy decisions (pp. 274–275).
- Guiding comments over a few related lines — extract to a method named from the comment (p. 275).
- Predicates with complex conditionals — "particularly ripe for extraction" (p. 275).
- Feature envy: a method asking another class multiple questions; move it to its peers (pp. 276–277).
- Drippy switch statements over type tags inside domain classes; three-plus reasons to change in one method (pp. 277–278).
- Policy (orchestration) mixed with implementation detail in one service class (p. 284).
- Shotgun surgery: simple changes forcing updates to numerous classes (p. 270).
- Retrospective metric: "assess each change you make — how many existing classes did you have to open for change?" (p. 285).
- Tests targeting implementation details rather than outcomes of small behavioral concepts (p. 286).

## Trade-offs & exceptions

- "Virtually no principle is absolute" (p. 271). Beck's rule 4 (minimize elements) counterweights the drive toward tiny classes; Future Bob notes this is one of John Ousterhout's fears about the "One Thing" rule (p. 271).
- No "ravioli" system required — but nothing wrong with tiny classes of one to three methods (p. 273).
- SRP doesn't license speculation about the nexus of change: "wait for the next demand for change" and shape the system then (p. 273). Likewise "Should We Do Anything Now?": if change is a given, waiting is best; "Speculative cleanup creates unnecessary risk from improvements no one yet needs" (p. 278).
- Extreme SRP/OCP ("Is This Overengineering?", pp. 284–285) would make everything plug-and-play; it sounds ridiculous, but such systems truly support OCP and were the Smalltalk norm — though highly compliant systems initially disorient newcomers ("There's all these objects and none of 'em are doing anything!").
- Corollary on testing: an extracted small class not useful in other contexts shouldn't be made publicly accessible; test it indirectly at a higher level, directly only as a last resort (p. 286).
- File organization concessions: closely related small types may share a file; "the file part of things" is mostly irrelevant to class design (p. 268).
- Future Jeff: creating new classes is cheap in an IDE and developers over-resist it — "Just do it" (p. 273).

## Process prescriptions

- **Continuous design** (p. 277): with every change, keep asking — does this class now have too many reasons to change? Should the method move again? What can be simplified?
- **Respond-to-change cycle** (pp. 273, 278, 285): don't speculate; when a change demand arrives, *prefactor* first so the change lands smoothly, make the change, then assess how many classes you had to open.
- **Extract-then-move rhythm** (pp. 275–277): extract implementation detail into named methods (especially predicates); watch for feature envy; move methods to the class they envy; re-evaluate in the new home.
- **Test-driving new strategies** (pp. 282–283): write focused unit tests on now-public policy classes; they double as official documentation of intentional behavior.
- **With AI** (pp. 286–287): provide examples plus a style demanding small single-purpose modules/functions, more-functional solutions, clarity; have it generate tests from the examples, vet the tests, then run them — comprehensive testing for behavioral intent is essential.

## Open the PDF when

- You need the full HoldingService/Strategy code sequence (pp. 274–283) verbatim — the arc spans many listings only sketched here.
- You're weighing how far to push SRP/OCP — the "Is This Overengineering?" and "Simpler Testing" discussions (pp. 284–286) carry nuance beyond these bullets.
- You want the AI-era rationale in full ("Enter AI" / "It Will Be Wrong", pp. 286–287), including the named pluggable-design patterns list.
