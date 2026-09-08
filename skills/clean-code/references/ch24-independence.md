---
chapter: 24
title: Independence
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch24_Independence.pdf
pages: 4
level: architecture | component
---

# Ch24 — Independence

**Thesis:** A good architecture must support four things — the use cases, the operation, the development, and the deployment of the system (p. 449) — and it satisfies all four with one mechanism: partitioning the system into well-isolated, independently developable components, which leaves as many options open as possible, for as long as possible, even though the real-world goals are "indistinct and inconstant" (p. 451).

## Named principles & rules

- **[The four supports of a good architecture]** — a good architecture must support the *use cases*, *operation*, *development*, and *deployment* of the system (p. 449).
- **Use Cases** — the architecture must support the intent of the system; this is its first priority. Since architecture has few behavioral options to leave open, "the most important thing a good architecture can do to support behavior is to clarify and expose that behavior so that the intent of the system is visible at the architectural level" — a shopping cart application should *look* like a shopping cart application, its use cases first-class, prominently placed, clearly named elements (p. 450).
- **Operation** — architecture plays a substantial, less cosmetic role in throughput and response time. The choice among services on many servers, lightweight threads in one process, a few isolated processes, or a monolith "is one of the options that a good architecture leaves *open*" (p. 450), enabling transition through the spectrum of threads, processes, and services as operational needs change (p. 451).
- **Development** — where **Conway's law** and the **Single Responsibility Principle (SRP)** come into play: many teams with many concerns need an architecture that lets them act independently without interfering, achieved by partitioning into well-isolated, independently developable components allocated to teams (p. 451).
- **Deployment** — the goal is **"immediate deployment"**: no dozens of configuration scripts and property-file tweaks, no manually arranged directories; the system should be immediately deployable after each build, via proper partitioning and isolation including the master components that start, integrate, and supervise the rest (p. 451).
- **Leaving Options Open** — a good architecture balances all these concerns with one component structure, despite not knowing the use cases, operational constraints, team structure, or deployment requirements — which will all change anyway. Closing maxim: "A good architecture makes the system easy to change, in all the ways that it must change, by leaving options open." (pp. 451–452).

## The argument

Each of the four supports is served by the same structural move — isolation. Use cases are served by making behavior visible in the structure ("Developers will not have to hunt for behaviors, because those behaviors will be first-class elements visible at the top level of the system," p. 450). Operation is served by not baking in the execution topology: "A system that is written as a monolith and that depends upon that monolithic structure cannot easily be upgraded to multiple processes, multiple threads, or microservices should the need arise" (p. 450). Development is served by components teams can own independently; deployment by components that assemble without hand-arranged configuration (p. 451).

The honest admission: balancing all four "is pretty hard" because "the goals we must meet are indistinct and inconstant. Welcome to the real world" (p. 451). The answer is not prediction but cheap-to-apply principles of architecture that partition systems into well-isolated components, keeping options open when you can't see the target (p. 452).

## Distilled example

No code. Two central illustrations:
- The shopping cart: with a good architecture the application *looks like* a shopping cart application — use cases visible as named, top-level classes/functions/modules (p. 450).
- The execution-topology spectrum: the same system might need parallel services on many servers, many lightweight threads in one process, a few isolated processes, or a single monolith — and a good architecture defers that decision by isolating components and not assuming the means of communication between them (pp. 450–451).

## Smells & checklist

- The system's structure does not reveal its intent — use cases must be hunted for rather than being first-class, top-level, well-named elements (p. 450).
- The code depends on its monolithic (or threaded, or service) structure, so the execution topology cannot change without rewrites; components assume the means of communication between them (pp. 450–451).
- Component boundaries that cut across team ownership, forcing teams to interfere with each other during development (p. 451).
- Deployment needs dozens of configuration scripts, property-file tweaks, or manually created directories arranged just so — not immediately deployable after each build (p. 451).
- Missing or ad hoc master components for starting, integrating, and supervising the rest of the system (p. 451).
- Architecture decisions justified by predicted requirements rather than by keeping options open despite unknown, shifting requirements (pp. 451–452).

## Trade-offs & exceptions

- Architecture "does not wield much influence over the behavior of the system" — its support for use cases is clarification and exposure, not behavioral control (p. 450).
- Some systems legitimately "can even survive as simple monolithic programs running in a single process" — the monolith is not the smell; *depending* on the monolithic structure is (p. 450).
- The chapter concedes the balancing act is genuinely hard and the inputs unknowable and changing; the principles are a hedge, not a formula (pp. 451–452).

## Process prescriptions

None.

## Open the PDF when

- You need the exact wording of the four supports or the "immediate deployment" passage for an architecture review (pp. 449, 451).
- You are weighing a monolith-to-services (or reverse) transition and want the operation-spectrum argument verbatim (pp. 450–451).
