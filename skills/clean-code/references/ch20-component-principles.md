---
chapter: 20
title: Component Principles
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch20_Component_Principles.pdf
pages: 26
level: component | architecture
---

# Ch20 — Component Principles

**Thesis:** If the SOLID principles arrange bricks into walls and rooms, the component principles arrange the rooms into buildings (p363). Components are the units of deployment — jar, gem, DLL — and well-designed components stay independently deployable and therefore independently developable (p364). Three cohesion principles (REP, CCP, CRP) decide which classes belong together in a component; three coupling principles (ADP, SDP, SAP) govern the dependency relationships between components. These forces are in tension, the right balance shifts as the project matures, and so the component structure cannot be designed up front — it evolves with the logical design of the system.

## Named principles & rules

- **REP — The Reuse/Release Equivalence Principle:** "The granule of reuse is the granule of release." (p369) People reuse components only if those components are tracked through a release process with release numbers, notifications, and documentation; classes grouped into a component must form a cohesive, releasable group with an overarching theme.
- **CCP — The Common Closure Principle:** "Gather into components those modules that change for the same reasons and at the same times. Separate into different components those modules that change for different reasons or at different times." (p370) This is the SRP restated for components, and it is "closure" in the OCP sense — components closed to the same types of changes.
- **CRP — The Common Reuse Principle:** "Don't force users of a component to depend on things they don't need." (p371) Classes/modules that tend to be reused together belong in the same component; modules not tightly bound to each other should not share a component, else dependents get recompiled/revalidated/redeployed for changes they don't care about.
- **[Relation to ISP — sound bite]:** the CRP is the generic version of the ISP; all this advice reduces to "Don't depend on things you don't need." (p372)
- **The Tension Diagram for Component Cohesion:** REP and CCP are inclusive (make components larger); CRP is exclusive (makes them smaller). The triangle's edges name the cost of abandoning the opposite vertex: too many unneeded releases (drop CRP), hard to reuse (drop REP), too many components change (drop CCP). (p372)
- **ADP — The Acyclic Dependencies Principle:** "Allow no cycles in the component dependency graph." (p374) The graph must be a DAG; cycles collapse the components involved into one de facto component with no correct build order.
- **the morning-after syndrome:** your work stops working overnight because someone changed something you depend upon; occurs when many developers modify the same sources, and cannot be avoided if dependency cycles exist (p374).
- **The "Jitters":** the component structure is volatile in the presence of changing requirements; the dependency structure must be continually monitored for cycles and broken (via DIP or by extracting a new component), so the structure jitters and grows (p377).
- **SDP — The Stable Dependencies Principle:** "Depend in the direction of stability." (p379) A component designed to be easy to change must not be depended upon by one that is harder to change.
- **Stability metrics — Fan-in, Fan-out, I (Instability):** I = Fan-out ÷ (Fan-in + Fan-out), range [0,1]; I=0 maximally stable ("adult" — responsible, independent), I=1 maximally unstable ("teenager" — irresponsible, dependent). SDP restated: "I metrics should decrease in the direction of dependency." (pp380–381) "Stability is a continuum, not a boolean value." (p379)
- **Abstract Components:** components containing nothing but interfaces — common and necessary in statically typed languages, very stable, ideal targets for less stable components; they don't exist in dynamically typed languages, whose dependency structures are simpler (p383).
- **SAP — The Stable Abstractions Principle:** "A component should be as abstract as it is stable." (p383) Stable components should consist of interfaces/abstract modules so stability doesn't prevent extension; unstable components should be concrete. SAP + SDP amount to the DIP for components (p384).
- **A (Abstractness) metric:** A = Na ÷ Nm (abstract modules and interfaces over total modules), range 0–1 (p384).
- **The Main Sequence:** on the A/I graph, the line from (0,1) to (1,0); the most desirable positions are its endpoints, and components off the endpoints are best on or near the line (pp385, 387).
- **Zone of Pain:** area near (0,0) — stable and concrete; rigid, hard to extend, painful if volatile (e.g. database schemas). Nonvolatile concrete components (e.g. String) are harmless there (p386).
- **Zone of Uselessness:** area near (1,1) — maximally abstract with no dependents; leftover abstract classes and superfluous interfaces nobody implements (p386).
- **D (Distance) metric:** D = |A+I−1|, range [0,1]; zero means directly on the Main Sequence; any component with D not near zero should be reexamined and restructured (p387).
- **[Murphy's law of program size]:** "Programs will grow to fill all available compile and link time." (p368) — the historical driver, beaten by Moore's law in the late '80s, which made the component plug-in architecture the casual default (p368).

## The argument

Cohesion is not the simple "one function per module" idea of the past — the three cohesion principles describe opposing forces of reusability and developability that must be balanced for the *current* concerns of the team: "early in the development of a project, the CCP is much more important than the REP, because developability is more important than reuse" (p373). Projects start on the CCP side of the tension triangle and slide toward REP as they mature — so "the component structure of a project can vary with time and maturity" (p373) and its changes "become a normal part of any Agile iterative cycle" (p373).

Coupling is governed by buildability. Cycles produce the morning-after syndrome; partitioning development into releasable components with an acyclic graph lets each team decide when to adopt others' releases, so "none of the teams are at the mercy of the others" (p374). Component dependency diagrams "have very little to do with describing the function of the application. Instead, they are a map to the buildability and maintainability of the application" (p378) — which is why top-down design of the component structure fails: with no modules yet, you'd know nothing of common closure and would almost certainly create cycles.

Finally, volatility must be isolated: high-level policy belongs in stable (I=0) components, but stability must not make them rigid — the OCP answer is abstraction, hence the SAP and the Main Sequence.

## Distilled example

The Entities/Authorizer cycle (pp376–377). A typical DAG: Main → View/Controllers → Presenters/Interactors/Authorizer → Entities → Database, buildable bottom-up. A new requirement makes `User` (in Entities) use `Permissions` (in Authorizer) — now Entities → Authorizer → Interactors → Entities is a cycle: Interactors, Entities, and Authorizer effectively become one giant component with no correct build order. Two fixes:

1. **DIP:** create an interface with the methods `User` needs, put it in Entities, implement it in Authorizer — the dependency inverts and the cycle breaks (p376). Generalized on p383: extract interface `US` into a new `UServer` component (I=0); `Stable` depends on `UServer`, `Flexible` implements it and keeps I=1 — all dependencies flow toward decreasing I.
2. **New component:** move the modules both Entities and Authorizer need into a new component (e.g. Permissions) that both depend upon (p377) — this is the mechanism behind the jitters.

## Smells & checklist

- Does every component have an overarching theme, and would its contents sensibly share one version number and release notes? (REP, p369)
- Do modules that always change together live in the same component? Does a typical requirement change touch one component or scatter across many? (CCP, p370)
- Does a component mix high-volatility and low-volatility elements, or elements that change at different times? (p371)
- When you depend on a component, do you use the majority of its modules? Are its modules inseparable? (CRP, p371)
- Is the component dependency graph a DAG? Is there a correct bottom-up build order? (ADP, pp374–376)
- Draw unstable components above stable ones: any dependency arrow pointing *up* violates the SDP (p382).
- Is anything hard-to-change depending on something designed to be easy to change? Compute I if in doubt (pp380–382).
- Is high-level policy in stable components, and are those stable components abstract enough to extend without modification? (SAP, p384)
- Any volatile, concrete, heavily-depended-upon component (Zone of Pain)? Any unimplemented abstract detritus (Zone of Uselessness)? D = |A+I−1| near zero? (pp386–387)

## Trade-offs & exceptions

- The three cohesion principles *fight each other*; there is no single right grouping — only a position in the tension triangle matching current team concerns, which shifts over time (pp372–373). A REP+CRP focus makes too many components change on simple edits; a CCP+REP focus causes too many unneeded releases (p373).
- 100% closure (OCP) is not attainable; closure must be strategic — close against the most common expected changes (p370).
- Not all components should be stable — a fully stable system would be unchangeable; some components are *designed* to be volatile (p382).
- Nonvolatile components in the Zone of Pain are harmless (String); the zone hurts in proportion to volatility (p386).
- Abstract components and their heavier dependency structures are a statically-typed-language concern; dynamic languages make dependency inversion nearly free (p383).
- On the metrics: "I am not suggesting that you should measure and calculate all these metrics… understanding the theory and using it to 'feel' the relationships is good enough" (pp387–388); calculation is helpful in extreme cases or via IDE tooling.
- The chapter is an overview; full treatment is in [PPP02] and [Clean Arch] (p363).

## Process prescriptions

Not a full cycle, but a prescribed order of evolution (p378): the component structure grows with the logical design — first modules accumulate and SRP/CCP guide collocating things that change together; the dependency graph is molded to protect stable high-value components from volatile ones; as the app grows, CRP begins shaping reuse; as cycles appear, ADP is applied and the graph jitters and grows. Never design the component structure top-down before modules exist. Release-based workflow under ADP: get a component working → give it a release number → move it to a directory for other teams → keep modifying privately while others use the released version (p374).

## Open the PDF when

- You need the exact metric worked example (Cc with Fan-in 3, Fan-out 1, I=1/4, p381) or the A/I graph and zone diagrams (pp385–386).
- You want the full component-history narrative (PDP-8 origin statements through linkers to plug-in architecture, pp364–368).
- You need the before/after component diagrams for the cycle-breaking mechanisms (pp375–377, 383).
