---
chapter: part4
title: Craftsmanship — the disciplines' sharpest rules (Ch28–33, Oath, Afterword)
pdfs:
  - Part_IV_Craftmanship_Intro.pdf (pp. 10–11 of 12; book pp. 492–493, The Oath)
  - Ch28_Harm.pdf (book pp. 495–502)
  - Ch29_No_Defect_in_Behavior_or_Structure.pdf (book pp. 503–509)
  - Ch30_Repeatable_Proof.pdf (book pp. 511–518)
  - Ch31_Small_Cycles.pdf (book pp. 519–528)
  - Ch32_Relentless_Improvement.pdf (book pp. 529–531)
  - Ch33_Maintain_High_Productivity.pdf (book pp. 533–535, viscosity/slow-test section only)
  - Afterword.pdf (book pp. 557–560)
role: disciplines — sharpens the test gate, small-cycles loop, and severity judgments
---

# Part IV — Craftsmanship (selections)

## The Oath (Part IV intro, pp. 492–493)
"In order to defend and preserve the honor of the profession of computer programmers, I promise that, to the best of my ability and judgment:"

1. I will not produce harmful code.
2. The code that I produce will always be my best work. I will not knowingly allow code that is defective either in behavior or in structure to accumulate.
3. I will produce, with each release, a quick, sure, and repeatable demonstration that every element of the code works as it should.
4. I will make frequent, small releases so that I do not impede the progress of others.
5. I will fearlessly and relentlessly improve my creations at every opportunity. I will never degrade them.
6. I will do all that I can to keep the productivity of myself and others as high as possible. I will do nothing that decreases that productivity.
7. I will continuously ensure that others can cover for me and that I can cover for them.
8. I will produce estimates that are honest both in magnitude and precision. I will not make promises without reasonable certainty.
9. I will respect my fellow programmers for their ethics, standards, disciplines, and skill. No other attribute or characteristic will be a factor in my regard for my fellow programmers.
10. I will never stop learning and improving my craft.

## Harm (Ch28) — the severity rubric
- "Messy software is harmful software" (p. 499).
- The review's definition of a structural defect: "Structural harm is harm to the organization and content of the source code. It is anything that makes that source code hard to read, hard to understand, hard to change, or hard to reuse" (p. 500). Thousands of global variables is a structural flaw; so is dead code left in the codebase.
- Two values: "There's the value of its behavior; and then there's the value of its 'softness'" (p. 500).
- The thought experiment: the easy-to-change program that does nothing correctly beats the perfect-but-unchangeable one, "in all but the most urgent of situations" — and urgent means a production disaster losing $10M/minute, not a startup deadline (pp. 500–501).
- Quick-and-dirty patch: allowed in a production crisis — "A stupid idea that works is not a stupid idea" — but "you can't leave that quick-and-dirty patch in place without causing harm. The longer that patch remains in the code, the more harm it can do" (p. 499).
- "When it comes to software, it never pays to rush" — Brian Marick (p. 501).
- The named failure mode is the knowledge deficit. The issue is not perfect knowledge — "the issue is to KNOW that there will be no harm" (p. 498).
- Knight Capital: dead code (Power-Peg) plus a repurposed flag; $460M lost in 45 minutes because "they did not KNOW what their system was going to do" — and the debacle "would not have happened if the old Power-Peg code had been removed from the codebase" (pp. 497–499).
- Toyota: uncontrolled acceleration, as many as 89 deaths; thousands of global variables meant the programmers did not KNOW their code would NOT kill (pp. 498–499).
- Why structure is the safety issue: "The more tangled the structure, the more difficulty in knowing what the code will do. The bigger the mess, the more the uncertainty" (p. 499).
- A testing discipline (TDD, TCR, small bundles) is how you KNOW, "to a high degree of certainty, that the code works" — becoming the minimum mark of a professional (p. 501).

## No Defect in Behavior or Structure (Ch29)
- Eisenhower's Matrix, "the engineer's motto": "The greater the urgency, the less the relevance" (p. 506).
- "Structure is long term; therefore, it is important. Behavior is short term; therefore, it is merely urgent" (p. 506). Structure comes first; behavior is secondary.
- The chicken-and-egg resolution — shrink the unit until Beck's "First, make it work. Then, make it right" fits inside ONE TEST, not one story:
  - "Except stories are too big. We need to go smaller. Not stories … tests. Tests are the perfect size" (pp. 506–507).
  - "First you get a test to pass, then you fix the structure of the code that passes that test, before you get the next test to pass" (p. 507).
  - This is the moral foundation of the Red-Green-Refactor cycle.
- "That's why we consider our testing discipline to be a design technique as opposed to a testing technique" (p. 507).
- The smell triad (p. 505):
  - **Rigidity** — the effort to integrate a change is much greater than the change itself; minor changes force large rebuilds and redeployments.
  - **Fragility** — minor behavior changes force corresponding changes in many modules; small changes silently break other behaviors that get inadvertently deployed.
  - **Immobility** — a behavior you want to reuse is so tangled in the existing system that you can't extract it.
  - All structural, not behavioral: the system can pass every test, meet every requirement, and still be "close to worthless because it is too difficult to manipulate."
- Shipping imperfect structure is allowed — "If the structure is close but not quite right, and customers are expecting the release tomorrow, then so be it" (p. 508).
- ACCUMULATING it is not: "You will not pile more and more behavior on top of known bad structure. You will not allow those defects to accumulate" (p. 508).
- "We, programmers, are stakeholders too" (p. 507) — as stakeholder and engineer you have the right, and the duty, to refuse an order to ignore structure (p. 508).

## Repeatable Proof (Ch30) — the test gate's acceptance criteria
- Dijkstra's formal-proof dream failed; what replaced it: "software is a kind of science. We validate that science with experiments. We build up a superstructure of theories based upon passing tests" (p. 517).
- "And the tests are the proof" — not mathematical proof, but "experimental empirical proof. The kind of proof we depend upon every day" (p. 517).
- Why structured, decomposed code matters even without written proofs: "If something is provable, it means you can reason about it. If something is unprovable, it means you cannot reason about it. And if you can't reason about it, you can't properly test it" (p. 516).
- Quick / sure / repeatable defined (p. 518):
  - "Quick means that the test suite should run in a very short amount of time. Minutes instead of hours."
  - "Sure means that when the test suite passes, you know you can ship."
  - "Repeatable means that those tests can be run by anybody at any time … we want the tests run many times per day."
- What you owe: "the scientific suite of tests that covers all the required behavior, runs in seconds or minutes, and produces the same clear pass/fail result every time it is run" (p. 518).

## Small Cycles (Ch31)
- "Cycle" means everything, not just releases: "It's about iterations and sprints. It's about the edit/compile/test cycle. It's about the time between commits. It's about everything" (p. 525).
- Rationale: "long cycles impede the progress of the team" — the longer between commits, the more likely someone (perhaps the whole team) waits on you (p. 525).
- Toggles over branches (pp. 525–526):
  - A branch is "a long-term checkout"; days or weeks off the main line means a big merge and an impeded team.
  - Keep new feature development on the main line; toggle unfinished features off — flags, or the Command / Decorator / special Factory patterns, or simply no button on the page.
  - Long-lived branches are acceptable only for well-isolated big rewrites (the FitNesse parser case) backed by comprehensive unit and acceptance tests.
- Continuous integration depends critically on a very reliable unit-test suite; committing every few minutes makes merges rare and trivial (pp. 524–525).
- The test-quality test: "Your tests are good enough if, when they pass, you feel comfortable deploying. If passing tests don't allow you to deploy, your tests are deficient" (p. 527).
- Dev team standard: always be ready to deploy, even if the business isn't (p. 527).
- "A build failure is a red alert. It's an emergency" (p. 528). Run the build plus all tests locally before you push; push only when all tests pass.
- NEVER disable a failing test to make the build green: "the more tempted you are to turn the failing tests off until you can fix them—later … And that's when the tests become lies" (p. 528).

## Relentless Improvement (Ch32)
- Coverage is a developer tool, never a management metric: "Don't turn them into management metrics. Don't fail the build if your test coverage is too low" (p. 529).
- Naive use "sets up perverse incentives to cheat" — coverage is trivially gamed by pulling assertions out of failing tests, since tools measure code executed, not code tested (p. 529).
- "One hundred percent test coverage is always the goal, but it is also an asymptotic goal" — most systems never reach it; keep driving toward it with actual tests (p. 530).
- Mutation testing (p. 530): a tool mutates the code semantically (`>` to `<`, `==` to `!=`, assignment to null) and expects every mutation to fail the tests; "Mutations that do not fail the tests are called surviving mutations" — the goal is zero survivors. Slow; run over weekends or at month's end.
- Semantic stability (pp. 530–531): "A test suite that ensures semantic stability is one that fails whenever a required behavior is broken. We use such test suites to eliminate the fear of refactoring and cleaning the code."
- No single discipline suffices for full semantic stability — coverage, mutation testing, and acceptance testing together push it toward completeness (p. 531).
- Cleaning as flexing: "Every little bit of cleaning I do is actually a test of the code's flexibility. If I find a small cleanup to be a bit difficult, I have detected an area of inflexibility that I can now correct" (p. 531).

## Viscosity (Ch33, slow-test section only)
- Viscosity — an inefficient development environment — is a named productivity defect; writing code faster barely helps because building, testing, debugging, and deploying dominate (pp. 533–534).
- Builds: "There is no reason … that builds should take more than a minute or two. … Find whatever is causing the build to be slow, and fix it. Consider it a design challenge" (p. 534).
- Tests: a laptop runs ~10 billion instructions per second, so a whole system should test "in less than a second" unless instructions are executed repeatedly (p. 534).
- Test login once — any more is waste. "Build a special testing API that allows the tests to quickly force the system into the state you need, without logging in, and without navigating" (p. 535). Same for UI navigation pathways: once each.
- "Mock out your databases for the majority of your tests" — a query needs testing once (p. 535).
- Peripherals, disks, web sockets, UI screens are slow: "Mock them out. Bypass them. Get them out of the critical path of your tests. Don't tolerate slow tests. Keep your tests running fast!" (p. 535).

## The Afterword's two arguments
- The Ward Cunningham / Hunt the Wumpus story (pp. 558–559) — the canonical case against speculative abstraction:
  - Justin Martin planned an Arrow/FireArrow inheritance hierarchy up front for a "fire arrow" feature; Cunningham asked "whether we really ought to introduce such complexity so early."
  - Cunningham's counter: "rather than jumping to our end-state architecture, we might try to add the functionality gradually and allow the test-driven process to reveal an appropriate shape."
  - They drove red → green → refactor; fire arrow took "a line or two of code," crossbow bolt turned out "remarkably simple."
  - Only at that third feature did the code speak: the Projectile interface was extracted, with every test "still a beautiful shimmering green."
- On AI-generated code (p. 560): "AI can churn out code like a factory, but it's often like raw dough—tasty maybe, but not a fully baked pie." Even cleaned-up-by-AI code can end as "a knot of interdependencies. Without Clean Code as a compass, AI's output can quickly become a maintenance nightmare." Clean Code is the compass for reviewing and guiding AI output, "whether you're refactoring by hand or tweaking AI prompts."

## Open the PDFs when
- You need the full Knight Capital / Toyota / Healthcare.gov narratives, or Ch28's discussion of harm to society and accountability by seniority.
- You want the boss-negotiation dialogue (Ch29, pp. 508–509), the Dijkstra history and structured-programming derivation (Ch30), or the source-control history behind small cycles (Ch31).
- You need the parts deliberately excluded here: Ch33's meetings/music/mood/flow/Pomodoro material, or Ch34–37 (team logistics, estimation, respect, career).
