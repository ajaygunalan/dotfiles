---
chapter: 27
title: The Clean Architecture
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch27_The_Clean_Architecture.pdf
pages: 8
level: architecture
---

# Ch27 — The Clean Architecture

**Thesis:** Decades of architectural ideas — Hexagonal, DCI, BCE — all pursue the same objective, separation of concerns, by dividing software into layers with business rules separated from user and system interfaces. The Clean Architecture integrates them into "a single actionable idea": concentric circles where the further in you go the higher-level the software becomes (outer circles are mechanisms, inner circles are policies), governed by one overriding rule — source code dependencies point only inward (p475–476).

## Named principles & rules

- **The Dependency Rule** — "the overriding rule that makes this architecture work," stated verbatim: "Source code dependencies must only point inward, toward higher-level policies." Nothing in an inner circle may know anything about an outer circle — no name (function, class, variable, any named software entity) declared in an outer circle may be mentioned by inner-circle code, and no outer-circle data formats (especially framework-generated ones) may be used inward (p476).
- **The Clean Architecture** — the integrating concentric-circle model itself, with four schematic rings (p476–477).
- **Entities** (ring 1, innermost; legend: *Enterprise Business Rules*) — encapsulate enterprise-wide critical business rules; object with methods or data structures and functions. In a single application, the business objects. "The least likely to change when something external changes"; no operational change to any application should affect this layer (p477).
- **Use Cases** (ring 2; legend: *Application Business Rules*) — application-specific business rules; encapsulate and implement all use cases, orchestrating the flow of data to and from the entities. Isolated from database, UI, and framework concerns, but affected when the operation of the application changes (p477–478).
- **Interface Adapters** (ring 3) — adapters converting data from the format most convenient for use cases/entities to the format most convenient for external agencies (database, Web). Wholly contains the MVC architecture of a GUI (presenters, views, controllers); all SQL restricted here (p478).
- **Frameworks and Drivers** (ring 4, outermost) — frameworks and tools: the database, the Web framework. Mostly glue code. "This layer is where all the details go. The Web is a detail. The database is a detail. We keep these things on the outside, where they can do little harm." (p478)
- **Dependency Inversion Principle (DIP)** — the technique for crossing boundaries against the flow of control: arrange interfaces and implements/inheritance so source code dependencies oppose flow of control at just the right points (p479).
- **Use Case Input Port / Use Case Output Port (InputBoundary / OutputBoundary)** — the inner-circle interfaces through which controllers call in and use cases call back out to presenters without naming them (p477, 479–480).
- **Hexagonal architecture (aka Ports and Adapters)** — Alistair Cockburn; **Data, Context, and Interaction (DCI)** — Coplien & Reenskaug; **Boundary–Control–Entity (BCE)** — Ivar Jacobson: the cited ancestors the Clean Architecture unifies (p475).
- **[Row structure rule]** — unnamed: the convenient data format a database framework returns ("a row structure") must not be passed inward across a boundary; data crossing a boundary is always in the form most convenient for the *inner* circle (p479).

## The argument

Systems built to these layered rules share five properties (p476): independent of frameworks ("use such frameworks as tools, rather than forcing you to cram your system into their limited constraints"); testable (business rules tested without UI, database, Web server, or any external element); independent of UI; independent of database; independent of any external agency — "your business rules simply don't know anything at all about the interfaces to the outside world."

The circles carry an abstraction gradient: "As you move inward, the level of abstraction and policy increases... The innermost circle is the most general and highest level" (p478). Where flow of control runs outward (use case → presenter), DIP restores the rule: the use case calls the Use Case Output Port interface in the inner circle and the presenter implements it — "dynamic polymorphism to create source code dependencies that oppose the flow of control" (p479).

Payoff: "By separating the software into layers and conforming to the Dependency Rule, you will create a system that is intrinsically testable... When any of the external parts of the system become obsolete, like the database or the Web framework, you can replace those obsolete elements with a minimum of fuss" (p481).

## Distilled example

"A Typical Scenario" — a Web system with a database (p479–480):

Controller packages user input into a plain old object → passes it through the **InputBoundary** to the **UseCaseInteractor** → the interactor "controls the dance of the Entities," using the **DataAccessInterface** to bring data into memory from the Database → gathers results into **OutputData** (another plain old object) → passes it through the **OutputBoundary** interface to the **Presenter** → the Presenter repackages it as the **ViewModel** (Strings and flags: Dates and Currency pre-formatted, Button/MenuItem names, gray-out flags) → leaving the **View** "almost nothing to do other than move the data from the ViewModel into the HTML page." Every dependency crosses the boundary lines pointing inward.

## Smells & checklist

- Does any inner-circle file mention a name (class, function, variable) declared in an outer circle (p476)?
- Do framework-generated data formats or database row structures travel inward across a boundary (p476, 479)?
- Is data crossing boundaries a simple, isolated data structure (struct, DTO, function arguments, hash map) rather than an entity or database row (p479)?
- Is all SQL restricted to the Interface Adapters layer, in its database-facing parts; does anything inward of that circle know about the database (p478)?
- Do presenters, views, and controllers live wholly in the Interface Adapters ring, with models as mere data structures passed through (p478)?
- Where flow of control points outward (use case → presenter), is it routed through an inner-circle interface (Output Port) implemented outside (p479)?
- Would a change to page navigation or security touch the Entities? It shouldn't (p477).
- Is the View humble — nothing to do but move ViewModel data into the page (p480)?
- Is code in Frameworks and Drivers limited to glue (p478)?

## Trade-offs & exceptions

- **Only Four Circles?** — "No, the circles are schematic. You may find that you need more than just these four. There's no rule that says you must always have just these four. However, the Dependency Rule always applies." (p478)
- Entities vs. Use Cases is a judged split: without an enterprise, entities are simply the application's business objects (p477).
- The Use Cases layer is *expected* to change when the operation of the application changes — isolation is from externalities, not from requirements (p478).
- Data-crossing form is flexible (structs, DTOs, arguments, hash maps, objects) — what matters is isolation and simplicity, not the mechanism (p479).

## Process prescriptions

None.

## Open the PDF when

- You need the concentric-circle diagram itself or the full typical-scenario class diagram with its `<I>`/`<DS>` markings and double-line boundaries (p477, 480).
- You are mapping a nonstandard layer count onto the model and want the exact wording of "Only Four Circles?" (p478).
