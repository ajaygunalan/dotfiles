---
chapter: 19
title: The SOLID Principles
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch19_The_SOLID_Principles.pdf
pages: 22
level: class | component | architecture
---

# Ch19 — The SOLID Principles

**Thesis:** Good systems begin with clean code, but "you can make a substantial mess with well-made bricks" (p. 341). The SOLID principles govern how functions and data structures are arranged into classes ("a class is simply a coupled grouping of functions and data" — not OO-only, p. 341) and how those classes interconnect. Their goal is *mid-level* software structures that tolerate change, are easy to understand, and are the basis of reusable components (p. 342). This chapter is an abridged excerpt from *Clean Architecture*, meant as a quick reference — "a good introduction, but insufficient for a deep understanding" (p. 343).

## Named principles & rules

- **SRP — The Single Responsibility Principle**: final form: "*A module should be responsible to one, and only one, actor*" (p. 343). Earlier phrasings the book walks through: "A module should have one, and only one, reason to change" and "A module should be responsible to one, and only one, user or stakeholder" (p. 343). It is NOT "every module should do just one thing" — that is a lowest-level function rule, "It is not the SRP" (p. 343). The SRP says to "*separate the code that different actors depend upon*" (p. 345). Cohesion is the force binding code responsible to a single actor (p. 343).
- **OCP — The Open–Closed Principle**: coined by Bertrand Meyer, 1988: "*A software artifact should be open for extension but closed for modification*" (p. 347). Behavior should be extendible without modifying the artifact; systems should change by adding new code, not changing existing code (pp. 342, 347).
- **LSP — The Liskov Substitution Principle**: Barbara Liskov's 1988 substitution property: "If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T" (p. 351). Today morphed into a broader design principle about interfaces and implementations: implementations must be substitutable wherever their interface is used (p. 352).
- **ISP — The Interface Segregation Principle**: "advises software designers to avoid depending on things that they don't use" (p. 342). Segregate fat interfaces so each user depends only on the operations it calls (pp. 354–355).
- **DIP — The Dependency Inversion Principle**: "the code that implements high-level policy should not depend on the code that implements low-level detail. Rather, low-level details should depend upon high-level policies" (p. 343). Epigraph (James Grenning): "It's better to depend on something you control than on something you don't control, lest it end up controlling you" (p. 356). Flexible systems have source-code dependencies that "refer only to abstractions, not to concretions" (p. 358).
- **DIP coding practices** (pp. 359–360), stated as rules but "actually more like warnings": **Don't refer to volatile concrete classes** (refer to abstract interfaces; enforces Abstract Factories); **Don't derive from volatile concrete classes** (inheritance is the strongest, most rigid source-code relationship); **Don't override concrete functions** (you inherit their dependencies — make the function abstract with multiple implementations); **Never mention the name of anything concrete and volatile**.
- **Stable Abstractions** — interfaces are less volatile than implementations; good designers "work hard to reduce the volatility of interfaces... find ways to add functionality to implementations without making changes to the interfaces. This is Software Design 101" (pp. 358–359).
- **Accidental Duplication** (SRP symptom) — code shared by different actors (e.g., `regularHours()` used by both `calculatePay()` and `reportHours()`) looks like reuse but couples actors together (pp. 344–345).
- **[ISP bottom line]** — "*Don't depend on things you don't need*" (p. 356). Generalizes ISP beyond language mechanics; foreshadows the Common Reuse Principle (Ch. 20).
- **[Every LSP violation is a latent OCP violation]** — defending against a bad subtype requires `if`/type-detection in the user, which violates OCP (p. 352).
- **Common Closure Principle (CCP)** (forward ref) — the SRP reappears at component level as the CCP, and at the architectural level as the axis of change behind architectural boundaries (p. 346).
- **The Dependency Rule** (forward ref) — dependencies crossing architectural boundaries in one direction, toward more abstract entities; the DIP made architectural (p. 361).

## The argument

**SRP** (pp. 343–346): "the least well understood" principle due to its name. Modules change to satisfy users/stakeholders — grouped as *actors*. Coupling code for different actors means one team's change breaks another's (the CFO/COO `regularHours()` disaster costing "millions", pp. 344–345).

**OCP** (pp. 347–351): when "simple extensions to the requirements force massive changes to the software, the architects... have engaged in a spectacular failure" (p. 347). Good architecture reduces changed code to "the barest minimum; ideally, zero" (p. 347) — achieved by separating things that change for different reasons (SRP) and organizing dependencies properly (DIP). "If component A should be protected from changes in component B, then component B should depend upon component A" (p. 350). This yields a hierarchy of protection by *level*: Interactor (business rules) most protected; Views least (p. 350). Supporting sub-ideas: **Directional Control** (interfaces exist to invert otherwise-wrong-way dependencies) and **Information Hiding** (interfaces like `FinancialReportRequester` prevent transitive dependencies — "software entities should not depend upon things they don't directly use", pp. 350–351).

**LSP** (pp. 351–354): substitutability protects users from caring which implementation they hold; violations force special-casing that pollutes the architecture.

**ISP** (pp. 354–356): depending on a class with unused operations forces recompilation/redeployment on irrelevant changes; "depending upon something that carries baggage that you don't need can cause you troubles that you didn't expect" (p. 356).

**DIP** (pp. 356–361): historically source-code dependencies followed flow of control (high calls low). "OO gave us a different option: polymorphic interfaces" — inserting an interface inverts the source-code dependency *against* the flow of control, giving "absolute control over every source code dependency in the system... This ability is power!" (p. 357). It enables plug-in architectures where business rules are independent of UI and database (p. 357).

## Distilled example

**SRP — Employee** (pp. 344–346): `Employee {calculatePay, reportHours, save}` serves three actors (CFO/accounting, COO/HR, CTO/DBAs). Shared `regularHours()` is tweaked for the CFO; the COO's reports silently corrupt. After: separate `PayCalculator`, `HourReporter`, `EmployeeSaver` classes sharing a methodless `EmployeeData` structure, optionally behind an `EmployeeFacade` (or keeping the most important method in `Employee` as facade to the lesser functions).

**LSP — Square/Rectangle** (p. 352): `Square` is not a proper subtype of `Rectangle` (independent height/width vs. coupled): `r.setW(5); r.setH(2); assert(r.area()==10)` fails if r is a Square — the User must type-check, breaking OCP. **Taxi Aggregator** (pp. 353–354): one company abbreviating a REST field (`/dest` vs `/destination`) forces `if (driver.getDispatchUri().startsWith("acme.com"))`-style special cases; the cure is a config-driven dispatch-format table keyed by URI — "a simple violation of the LSP... can cause our architecture to be polluted with a significant number of extra mechanisms" (p. 354).

**ISP — OPS** (pp. 354–355): `User1..3` each use only `op1..3` of class `OPS`; segregating into interfaces `U1Ops/U2Ops/U3Ops` implemented by `OPS` means a change to `op2` no longer recompiles/redeploys `User1`.

**DIP — Abstract Factory** (p. 360): `Application → Service` (interface) with `ServiceFactory` interface + `ServiceFactoryImpl` creating `ConcreteImpl`. The curved line is an architectural boundary: all source-code dependencies cross it pointing toward the abstract side, while flow of control crosses opposite — "That is why we refer to this principle as *dependency inversion*" (p. 360).

## Smells & checklist

- List the actors behind a module's methods; more than one actor → SRP violation. Watch for "convenient" shared functions serving different actors (accidental duplication).
- Does a new requirement (e.g., a second output format) force edits to existing high-level code? OCP failure. Ideal changed-code for an extension: zero.
- Are dependency arrows pointing at the components you want to protect? Higher-level components must not depend on lower-level ones.
- Any `if`/type-check that detects which implementation it's talking to → LSP violation (and latent OCP violation). Any special-case keyed to one implementation's name in the code (`"acme.com"`).
- Do clients depend on interfaces carrying operations they never call? Segregate.
- `use`/`import`/`include` referring to volatile concrete modules? Deriving from or overriding volatile concrete classes? Object creation scattering concrete dependencies instead of factories/`main`?
- Transitive dependencies on internals a client doesn't directly use (missing information-hiding interface)?

## Trade-offs & exceptions

- SRP's name misleads; the do-one-thing rule belongs to functions, not modules (p. 343). SRP solutions cost extra classes to instantiate/track — Facade is the standard mitigation; and classes won't degenerate to one function each, since each responsibility typically holds many methods (pp. 345–346).
- Future Bob sidebar (p. 349): he would never draw the full class diagram in practice — a whiteboard abbreviation suffices; most classes "would be so obvious to the team that drawing them would be superfluous."
- ISP could look like a mere statically-typed-language issue (Ruby/Python have no source-code interface dependencies, p. 355) — but the deeper design concern stands at every level: don't depend on modules carrying more than you need (pp. 355–356).
- DIP hard-and-fast is "unrealistic": stable concretions like Java's `String` and OS/platform facilities are fine to depend on — "It is the *volatile* concrete elements... that we want to avoid depending upon" (p. 358). The four rules are warnings: "A pragmatic programmer will violate this principle frequently... Slavishly obeying this principle can lead to an explosion of interfaces that no one really needs" — conform *gradually*, inverting dependencies as needs arise, backed by a trusted test suite (p. 359).
- DIP violations can't be entirely removed — gather them into a few concrete components (typically `main`, which instantiates factories) kept separate from the rest (pp. 360–361).
- The chapter itself disclaims depth: a quick reference; study the footnoted sources ([PPP02], Liskov 1988, [OOSC]) for real understanding (p. 343).

## Process prescriptions

None as a working cycle; the DIP section prescribes an ordering of adoption: conform gradually as the system evolves, using a trusted test suite to invert dependencies when interfaces need to be added, rather than pre-building abstractions (p. 359).

## Open the PDF when

- You need the full financial-report component diagram and its <I>/<DS> notation walkthrough (pp. 348–350) — the richest OCP illustration, only sketched here.
- Discussing SOLID history and the Michael Feathers naming story, or the exact executive-summary phrasings (pp. 342–343).
- Mapping SOLID upward: CCP, Common Reuse Principle, and Dependency Rule forward references (pp. 346, 356, 361) connect to Chapters 20+.
