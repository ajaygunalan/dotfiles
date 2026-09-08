---
chapter: 25
title: Architectural Boundaries
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch25_Architectural_Boundaries.pdf
pages: 8
level: architecture | component
---

# Ch25 — Architectural Boundaries

**Thesis:** Software architecture is the art of drawing lines — boundaries — that separate software elements and restrict what each side may know about the other. The goal of architecture is to minimize the manpower required to build and maintain the system; what saps manpower is coupling, especially coupling to premature decisions (frameworks, databases, web servers, utility libraries, dependency injection — anything not driven by the use cases). Boundaries drawn early exist to defer those decisions as long as possible and to keep them from polluting the core business logic (p453–454).

## Named principles & rules

- **Boundaries** — the lines architecture draws to "separate things that matter from things that don't." The GUI doesn't matter to the business rules; the database doesn't matter to the GUI or to the business rules; each pair gets a line (p453–454).
- **The Dependency Rule of Architecture** — the chapter's capstone rule, stated verbatim: "Dependencies that cross architectural boundaries must always point toward the higher-level side." (p459)
- **Plug-in Architecture** — the GUI and the DB are plug-ins to the BusinessRules; arrows point from lower-level components to the high-level BusinessRules component. The pattern repeats for any component that is optional or can be implemented in many forms (p456–457).
- **Dependency Inversion Principle (DIP)** — boundary-drawing is named as an application of DIP: arrange dependency arrows to point from lower-level details toward higher-level abstractions (p459).
- **Stable Abstractions Principle (SAP)** — cited alongside DIP as the second principle the boundary arrangement applies (p459).
- **Download and Go** — Martin's FitNesse rule: nothing produced should require users to download more than one jar file. A product-level constraint that drove architectural decisions such as writing their own web server (p457).
- **[Interface on the business side]** — unnamed but load-bearing: the interface the business rules call (e.g., DatabaseInterface) lives in the BusinessRules component; the implementation (DatabaseAccess) lives in the plug-in component. The boundary is drawn across the inheritance/implements relationship, just below the interface (p455–456).

## The argument

Premature decisions are those "that have nothing to do with the business requirements—the use cases—of the system" (p453). A good architecture renders them "ancillary and deferrable" and "allows those decisions to be made at the latest possible moment, without significant impact" (p454).

The controversial case is the database. "Many of us have been taught to believe that the database is inextricably connected to the business rules... But this idea is misguided. The database is a tool that the business rules can use indirectly" (p454). All the business rules need to know is that a set of functions exists to fetch and save data — so the database goes behind an interface.

Direction of knowledge is everything. Once the boundary is drawn with the arrow pointing at BusinessRules, "the Database does not matter to the BusinessRules. But the Database cannot exist without the BusinessRules" (p456) — because the Database component holds the translation code from business-rule calls into query language. The payoff: "drawing the boundary lines that helped us delay and defer decisions saved us an enormous amount of manpower and headaches. And that's what a good architecture should do" (p459).

## Distilled example

FitNesse case study (p457–458). Boundary: data access behind an interface named `WikiPage`, whose methods find, fetch, and save pages.

- Before persistence existed: `MockWikiPage` (stubs) — three months of wiki-text-to-HTML work with no storage at all.
- Then `InMemoryPage` (hash table in RAM) — a full year of features; the entire first FitNesse version worked this way.
- Then `FileSystemWikiPage` (flat files) — judged good enough; MySQL was abandoned: "We deferred that decision into nonexistence, and never looked back" (p458).
- Yet a customer who needed MySQL wrote a `MySqlWikiPage` derivative and had the whole system working in a day — the boundary neither prevented nor impeded the deferred option.

For 18 months of development there were no schema, query, server, password, or connection issues, and all tests ran fast because there was no database to slow them down (p458).

## Smells & checklist

- Do business rules mention the schema, the query language, or any other database detail? They should know only a set of fetch/save functions (p454).
- Is each abstraction interface located on the high-level side of the boundary (DatabaseInterface in the BusinessRules component), with implementations on the low-level side (p455–456)?
- Do all dependency arrows crossing a boundary point toward the higher-level side (p459)? Any arrow from business rules out to GUI, DB, or framework is a violation.
- Could the database be swapped (Oracle, MySQL, Couch, Datomic, flat files) without the business rules caring (p456)? Could the UI (Web, client/server, SOA, console) (p457)?
- Are framework/database/web-server choices deferrable, or has the system been built to depend on them from day one (p453–454)?
- Can the business rules be written and tested before the database decision is made (p456)?

## Trade-offs & exceptions

- Plug-in replacements "might not be trivial." Swapping a Web UI for a client/server UI could be challenging, and some communications with the business rules would likely need rework. The plug-in structure's promise is that such a change is made *practical*, not free (p457).
- Some boundary lines are legitimately drawn much later than others; only those drawn early carry the decision-deferral purpose (p453).
- Writing your own web server "might sound absurd" — the FitNesse team accepted duplicated effort because a bare-bones server is simple and it postponed the web-framework decision (a framework, Velocity, was slipped in years later) (p457).
- The deferred MySQL option was eventually built, then dropped for lack of use — deferral can end in adoption, or in "nonexistence" (p458).

## Process prescriptions

Draw the decision-deferring boundaries early — some before any code is written (p453). Then: stub the interface (MockWikiPage), grow to an in-memory implementation, promote to a simple durable one, and only bind to heavyweight technology if reality ever demands it (p457–458). Partition the system into components — core business rules plus plug-ins — and arrange the code so all arrows point one direction: toward the core business (p459).

## Open the PDF when

- You need the exact class/component diagrams showing where the boundary line cuts the inheritance/implements relationship (p455–456).
- You want the full FitNesse narrative and its timeline details for teaching (p457–458).
