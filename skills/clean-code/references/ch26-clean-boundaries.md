---
chapter: 26
title: Clean Boundaries
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch26_Clean_Boundaries.pdf
pages: 14
level: component | class | tests
---

# Ch26 — Clean Boundaries (by James Grenning)

**Thesis:** We seldom control all the software in our systems — third-party packages, open source, other teams' subsystems, and code that does not yet exist. Interesting things happen at boundaries, and change is one of them; good designs accommodate change without huge investments and rework. So we keep boundaries clean: very few places in the code refer to third-party particulars, interfaces at the boundary express *our* application's needs (not the vendor's offerings), and tests — learning tests and boundary tests — define and defend our expectations of the foreign code (p461, 470, 474).

## Named principles & rules

- **Learning tests** — Jim Newkirk's term: instead of experimenting with third-party code in production code, "write some tests to explore our understanding of the third-party code." We call the third-party API as we expect to use it — controlled experiments that check our understanding, focused on what *we* want out of the API (p470–471).
- **Boundary tests** — regardless of whether you needed the learning, "a clean boundary should be supported by a set of boundary tests that exercise the interface the same way that the production code does." Without them we might be tempted to stay with an old version longer than we should (p473).
- **Adapter** — the [GOF95] pattern: wrap third-party dependencies in an ADAPTER "to convert from our application-centered interface to the provided interface," giving a single place to change when the API evolves (e.g., `TransmitterAdapter`) (p474).
- **Seam** — from [WELC] (Working Effectively with Legacy Code): the adapter design gives "a very convenient seam in the code for testing" — a `FakeTransmitter` slots in for testing `CommunicationsController` (p474).
- **Hexagonal architecture (aka Ports and Adapters)** — Alistair Cockburn's name: following the SOLID principles and isolating dependencies on the outside world "naturally leads" to it. Inside the hexagon is all the product's logic and behavior; outside is the execution environment; the application depends on service abstraction layers at the hexagon's edge (p469).
- **SOLID** — invoked as the class-level discipline whose application produces the hexagonal shape (p469).
- **Test-driven development (TDD)** — credited with showing the value of small, verified changes: "it's easier to keep a system working than to fix it after you break it" (p463).
- **[Define the interface you wish you had]** — for code that does not yet exist: define your own interface to the nonexistent system (e.g., `Transmitter` with `transmit(frequency, stream)`) — "the interface we wished we had." It is under our control, keeps client code readable and focused (p473).
- **[Depend on what you control]** — "It's better to depend on something *you* control than on something you don't control, lest it end up controlling you." (p474)
- **[Need-to-know binding]** — from the Hydra review: object creation is separate from object usage; concrete objects are created and bound during initialization; "binding is based on a need-to-know basis" (p468).

## The argument

Learning a third-party API is hard; integrating it is hard too; "doing both at the same time is doubly hard" (p470). Learning tests split the two, cost nothing ("we have to learn the mechanics anyway"), and keep paying: "when there are new releases of the third-party package, we run the learning tests to see whether there are behavioral differences" (p472). Once integrated, there is no guarantee the third-party code stays compatible with our needs — with each release comes new risk, and the tests find incompatibilities right away (p472).

At the design level: "Code at the boundaries needs clear separation and tests that define expectations. We should avoid letting too much of our code know about the third-party particulars" (p474). In the Hydra system this is stated as the hexagon's law: "It's important that the interfaces at the boundary of the hexagon are about the Hydra application's needs and not about ACME's offerings" (p470). We manage third-party boundaries "by having very few places in the code that refer to them" (p474).

## Distilled example

The Hydra IoT case study (p462–470): a water-pump flow-test product built on an off-the-shelf IoT vendor framework ("ACME"), chosen knowing the vendor might be replaced at market time.

- One class, `HydraNetwork`, encapsulates *all* hub-side dependencies on the IoT vendor; its functions (`announceHub`, `broadcast`, `processAck`) are low complexity and delegate to the vendor's infrastructure. "Hydra knows nothing about the ACME IoT" (p463–464, 470).
- The boundary interface is need-shaped: `broadcast()` / `handle_reply()` reflect what Hydra wants from a sensor network, not the vendor's very wide API. A hypothetical BrandX vendor with no broadcast would implement `broadcast()` per-radio inside its own `HydraNetwork` — the vendor changes without touching the Hydra core (p470).
- The UI/application boundary is two processes (Collector, Flask WebServer) joined only by a simple queuing mechanism (`CommandQueue`, `ReplyQueue`); `hydra_run()` wires everything in one messy-but-stable initialization function (p466–468).
- Review of the clean-boundary attributes (p468): business logic free of radio knowledge; IoT- and concurrency-dependent functions low-complexity and unlikely to change; business logic unconcerned with concurrency; creation separate from usage.

Second illustration — code that does not yet exist (p473–474): a radio system's "Transmitter" subsystem had no defined API. The team defined the interface they wished they had (`Transmitter.transmit(frequency, stream)`), insulated `CommunicationsController` from the undefined API, and later wrote a `TransmitterAdapter` to bridge to the real one, with `FakeTransmitter` for tests.

## Smells & checklist

- Are references to a third-party package confined to very few places (ideally one wrapper class/layer) (p474)?
- Do boundary interfaces express the application's needs, or mirror the vendor's offerings (p470)?
- Is there an Adapter giving a single place to change when the third-party API evolves (p474)?
- Do learning tests exist for each third-party mechanism the code relies on, and are they re-run on new releases (p471–472)?
- Are there boundary tests exercising the interface the same way production code does (p473)?
- Are boundary-adjacent functions low complexity, and unlikely to change often or much (p468)?
- Is business logic free of UI, transport/radio, and concurrency knowledge; are concurrency mechanisms in low-complexity functions (p468)?
- Is object creation separated from object usage, with binding done at initialization on a need-to-know basis (p468)?
- When the other side of a boundary is unknown or undefined, did the team define its own interface rather than block or guess at the vendor's (p473)?
- Does the adapter provide a seam (a Fake) so clients can be tested without the real dependency (p474)?

## Trade-offs & exceptions

- It's not our job to test third-party code, "but it may be in our best interest to write tests for the third-party code we use" (p470).
- Learning tests may have no anticipated payback ("who expects Python to change?") — yet the Python 2→3 migration vindicated them: the tests showed the behavior was preserved (p472).
- The wiring function `hydra_run()` is admitted to be "a little messy, as all the dependencies come together here" — acceptable because the code is not complex and probably won't change much (p468).
- Not knowing the hardware abstraction layer (HAL) was an advantage rather than a liability: HALs "usually are not all that abstract from the application perspective," and having no HAL to depend on forced a cleaner application-specific interface (p473).
- The vendor's wide interface was mostly unused on purpose: "we wanted to use the radios for some simple message passing, not marry the vendor (until death do us part)" (p463).

## Process prescriptions

- Start with a working system and grow functionality in small changes that don't break it; TDD shows the value of small, verified changes (p463).
- To adopt a third-party package: write learning tests first to explore the API from test cases, then integrate; keep the tests and re-run them on each new release (p470–472).
- For not-yet-existing code: define the interface you wish you had, code against it, fake it for tests, and bridge with an Adapter once the real API is defined (p473–474).

## Open the PDF when

- You want the full Hydra code listings (HydraNetwork, HydraDataSource, measurement_loop, hydra_run) or the sequence diagrams and hexagonal-architecture diagram (p463–469).
- You want the complete Python `QueueTest` / `ProcessLearningTest` learning-test suites as templates (p471–472).
