---
chapter: 3
title: First Principles
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch03_First_Principles.pdf
pages: 30
level: function | class | component | architecture
---

# Ch03 — First Principles

**Thesis:** Grasp this chapter and "you'll be 90% of the way toward cleaning code" (p. 41). The essence is one heading: keep everything small, well named, organized, and ordered. The chapter demonstrates it end-to-end on the Uncle Bob Conference Room system: extract small functions (SRP), replace growing switch statements with polymorphism (OCP), invert dependencies so high-level policy never depends on low-level details (DIP), and end with an architectural boundary that makes the two sides independently deployable — all justified by anticipated growth, all done while keeping pre-existing tests passing.

## Named principles & rules

- **[Guidelines, not laws]** — "these are not strict laws. They are not rules that must be followed. They are, more or less, guidelines," applied in the context of the problem at hand, with license to deviate (p. 41).
- **Everything Small, Well Named, Organized, and Ordered** — the chapter's master heading: "If you stop now and read nothing more than this heading, you'll have much of the essence of what it takes to clean code" (p. 42). Includes fighting your own understanding bias when naming for those who don't yet understand the code.
- **[Small functions]** — functions should be small, most "just a handful of lines"; if a snippet can be reasonably named, move it into a function named for what it does; the name should be a verb, letting the calling sequence read "like well-written prose" (Grady Booch, p. 42, fn. 1).
- **Extract method refactoring** — the tool used throughout: "create functions that do one thing, and gather together the things that are related and separate the things that are different" (p. 46).
- **The Single Responsibility Principle (SRP)** — keep different stakeholders' responsibilities apart and isolated; tax-concerned stakeholders drive `getTax`, discount-concerned ones drive `calculatePrice`/`isEligibleForDiscount` — "the farther we can keep these different stakeholders' responsibilities apart and isolated, the safer our code will be when changes are made" (p. 48; fn. 3 on p. 46; see Ch. 19).
- **Fragility** — the symptom of ignoring the SRP: "A fragile system breaks in unexpected ways," e.g., modifying taxes inadvertently breaks discounts, giving stakeholders "a glimpse of what's under the hood" (p. 48).
- **The Open–Closed Principle (OCP)** — "when we add a new feature, we should add that new feature in one place, not in many places." Switch statements aren't intrinsically bad, but if the number of cases is likely to grow, they violate the OCP (p. 48); the OCP also "tells us to keep new changes out of old modules" (p. 49).
- **The Dependency Inversion Principle (DIP)** — "violated when high-level policies directly depend on low-level details"; invert with interfaces so "Nothing within the high-level policy depends upon the low-level details. The low-level details depend only on the CatalogItem" — mantra: *High-level policy should not depend on low-level details* (pp. 50, 57).
- **[Plug-in]** — after the DIP inversion, "the low-level details have become a plug-in to the high-level policy" (p. 57).
- **Architectural boundary** — the curvy line dividing the project into two components, high-level policy and low-level detail; "the rule for architectural boundaries is that dependencies cross only toward the higher-level side" (p. 58).
- **Independent Deployability** — the two components separated by a strong architectural boundary "can be independently deployed"; when one changes, only that jar (or browser-cached bundle) redeploys (p. 68).
- **YAGNI** — its original intent was not "You Aren't Going to Need It" as a prohibition but the question "What if you aren't going to need it?" — a prompt to count the cost before making room for things you might not need. Here the answer is "Yes, we are going to need it" (pp. 56–57).
- **[Names grow with the problem]** — "When the problem is small, names can afford to be inconsistent or vague… But as the problem grows, names become much more important because they help us keep the concepts straight in our heads" — driving `ItemList`→`RentalReceipt`, `Statement`→`RentalOrder` (p. 58).
- **[Test/production decoupling]** — the tests written before refactoring were kept passing at every step; test churn was minimized "by keeping the tests and production code decoupled and by isolating the details of the production code from the details of the tests" (p. 68).

## The argument

Systems that start simple grow "much, much more complicated… a living hell for the developers and the organization" (p. 46). The conference-room program *grew* feature by feature, and with the CEO promising expansion it will keep growing: "as it grows, it will become ever more tangled and confusing. It will degrade, like a piece of rotting meat" (p. 46). The whole refactoring is justified as getting ahead of that growth — extra structure "makes room for growth": when tax rules change, only `getTax` grows, not `rent` (p. 48).

Each principle is introduced at the moment its violation hurts: SRP when stakeholder concerns tangle, OCP when a new `CatalogItem` would touch five places, DIP when adding `NotePads` would force recompiling `Statement.java`. The endgame is architectural: business rules "tucked away into their corresponding derivatives," high-level policy untouched by low-level change (p. 64), and the components independently deployable.

Future Bob's closing note bounds the AI question: "Grok3 did not invert the dependencies, nor did it attempt to separate high-level policy from low-level detail. LLMs/AIs have their uses; but they are not human and are not adept at understanding higher architectural goals" (p. 69).

## Distilled example

Two examples. Small one (pp. 42–43): JCommon's `getPreviousDayOfWeek` — a comment-delimited monolith becomes three lines: `checkWeekdayArgument(weekday); return addDays(-daysBefore(weekday, from), from);` — "It's short, and it's obvious. If you need to know more, all you have to do is look down."

Main one, the **Uncle Bob Conference Room system** (pp. 44–68), evolved in stages, tests green throughout:
1. One `Statement` class; `rent()` is switch-laden (prices, discounts, taxes inline).
2. Extract method → `rent()` reads `getUnitPrice; calculatePrice; getTax` (SRP).
3. Enum-with-fields kills two switches (OCP), then enum → `CatalogItem` **interface** with `SmallRoom`/`LargeRoom`/`Coffee`/`Cookies` classes deferring to polymorphic `getUnitPrice()`, `getTaxRate()`, `isEligibleForDiscount()`, `getName()` (DIP).
4. Split out `RentalItem`, `ItemList`; extract `Bonus` interface + `CookieBonus`; rename `ItemList`→`RentalReceipt` (it *finalizes* bonuses), `Statement`→`RentalOrder`.
5. Result: high-level component (`RentalOrder`, `RentalReceipt`, `Bonus`, `CatalogItem`, `RentalItem`) and low-level plug-in component (`catalogItems`, `bonuses`) with all dependencies crossing the boundary toward the high level; "virtually all of the business rules have fled" the high-level module (p. 60).

## Smells & checklist

- Snippet of lines that could be reasonably named? Extract it into a verb-named function.
- Function doing several separable things (like the original `rent`)? Pull apart into functions that do one thing.
- Changes for one stakeholder able to break another's behavior (fragility)? Separate the responsibilities.
- `switch`/`if`-on-type whose case count is likely to grow? OCP violation — move to data structures or polymorphism.
- Adding one new variant (a `NotePads`) touching many places? Should be one place.
- High-level module needing recompilation when a low-level detail changes? DIP violation — introduce an interface owned by the high level.
- Dependencies crossing an architectural boundary toward the low-level side? Reverse them.
- Vague or now-inaccurate names after restructuring (`ItemList` that finalizes, `getItems` that computes bonuses)? Rename to match the concept; renaming reveals design insight.
- Tests coupled to production details, churning with every refactor? Decouple them.

## Trade-offs & exceptions

- **These are guidelines, not laws** — apply in context; "every programmer should feel free to take whatever license is necessary" (p. 41).
- **More code, more indirection** — "it's not more *executable* code; it's just more names and more structure" (p. 48), but critics who find it harder to read "are not without a point. Yes, adding structure adds complexity… There's a cognitive price to pay" (p. 68). A first-edition commenter called such code "just dreadful" (p. 56). The justification is *expected growth*; without it the restructuring may not be warranted (YAGNI's cost question, pp. 56–57).
- **Performance** — the new structure is "probably" slower (more references, switch optimizes better than polymorphic dispatch), "but the difference… is probably so tiny that you could not easily measure it" (pp. 68–69).
- **Static type safety sacrificed** — `RentalItem.type` became a `String` after dropping the enum: "This minor loss of static type safety always accompanies the effort to reduce the recompile and redeployment burden" (p. 54).
- **Known residual debts** — the concrete `RentalItem` record still forces wide recompiles ("a battle for another day," pp. 58, 62); `getItems` "smells of an SRP violation" flagged for later (p. 51); switch statements "aren't intrinsically bad" when cases won't grow (p. 48).
- **Small projects** — if recompiling everything is cheap, "you could be right" to not care about DIP-driven module splits; the burden matters for larger projects and browser-delivered JavaScript (p. 50).

## Process prescriptions

- Write tests first; refactor in steps, keeping all tests passing at each step (p. 68).
- Order of the cleaning campaign as demonstrated: (1) extract methods for one-thing functions; (2) collapse type-switches into data (enum fields), then into polymorphism; (3) split modules and invert dependencies with interfaces; (4) rename as insight accrues; (5) draw the boundary and verify all dependencies point high-level-ward.
- Answer YAGNI's cost question explicitly before investing in room for growth (p. 57).

## Open the PDF when

- You need any full listing of the conference-room system at a particular stage, its IDE dependency diagrams (pp. 57, 59), or directory structures (pp. 52, 58).
- You want the complete test suite showing test/production decoupling in practice (pp. 65–68).
- You need the exact wording of the YAGNI reinterpretation or the Future Bob verdicts on Grok3 (pp. 47, 56–57, 69).
