---
chapter: 16
title: Acceptance Testing
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch16_Acceptance_Testing.pdf
pages: 4
level: process
---

# Ch16 — Acceptance Testing

**Thesis:** Whatever the requirements document says, the *true* requirements of a system are the tests QA runs before blessing a deployment. The acceptance testing discipline embraces that fact: all requirements are specified as tests, authored by BA and QA just before each feature is built, automated by programmers in a language BA/QA can read (and ideally write), and run continuously. Those tests are the definition of done and the requirements document of the entire system.

## Named principles & rules

- **The Acceptance Testing Discipline** — all requirements are specified *as tests*, written by business analysts (BA) and QA feature-by-feature shortly before implementation; programmers (not QA) run them, and therefore automate them; the automation language must be one BA and QA understand and can eventually write (pp. 314–315).
- **Arrange/Act/Assert (AAA)** — behavior specification is always input data + action + expected output; the AAA pattern (credited to Bill Wake) covers acceptance tests too (p. 314).
- **Given-When-Then** — the equivalent discipline of behavior-driven development (BDD); e.g. "Given a page with the wiki text: !1 header / When that page is rendered. / Then the page will contain: <h1>header</h1>" (pp. 314–315).
- **The definition of done** — "A feature is not complete until all its acceptance tests pass. And when all the acceptance tests pass, the feature is done." (p. 315)
- [Acceptance tests ARE the requirements] — "The suite of acceptance tests *is* the requirements document for the entire system"; by writing them, BA and QA certify that passing means the features are done and working (pp. 315–316).
- **The Continuous Build** — an automated procedure triggered on every check-in (within a few minutes): build from source, run all automated unit tests and all automated acceptance tests, and visibly post results everyone stays aware of. A previously passing acceptance test that fails must be repaired before any other change; "Allowing failures to accumulate in the continuous build is suicidal." (p. 316)

## The argument

Organizations already decide deployment readiness by QA running a battery of manual tests: "It does not matter what the requirements document says, it is only the tests that matter… Therefore, it is those tests that are the requirements" (p. 314). The discipline simply makes this honest and mechanical.

The division of labor is self-enforcing: "No programmer in their right mind wants to manually test the system over and over again. Programmers automate things" (p. 314). But since BA/QA author the tests, programmers must prove the automation performs the authored tests — hence readable formalisms and tools like FitNesse (https://fitnesse.org/), JBehave, SpecFlow, and Cucumber. "But tools are not really the issue" (p. 314): a spreadsheet or text editor works, because behavior specification is always just AAA.

Martin calls acceptance testing "one of the weakest aspects of software development in the first half of the twenty-first century" — it is the discipline programmers control least, because it "requires the participation of the business," which has often "proven unwilling to properly engage" (pp. 313, 316). "The advent of AI makes this need doubly important" (p. 316).

## Distilled example

A FitNesse acceptance test as a simple table (p. 315): action row "widget should render"; columns "wiki text" → "html text"; data rows like `''italic''` → `<i>italic</i>`, `!1 header` → `<h1>header</h1>`, a bare URL → an anchor tag. The same specification restated in Given-When-Then style. Point: input/action/expected-output tables in any medium are "relatively easy to automate."

## Smells & checklist

- Requirements live only in prose documents, not as executable tests — the real spec is then whatever QA manually does.
- Deployment readiness decided by manual QA regression passes rather than automated acceptance suites.
- Acceptance tests written by programmers alone in a programmer-only language BA/QA cannot read or bless.
- Tests written long after the feature instead of at the same time or just before (first days of the sprint).
- "Done" claimed on features whose acceptance tests don't yet pass, or with no acceptance tests at all.
- No continuous build; or build results not visibly posted; or check-ins that don't trigger the full unit + acceptance suites.
- Failures allowed to accumulate in the continuous build instead of being repaired before any other change.
- BA covering only happy paths with no QA exploration of failure modes (or vice versa).

## Trade-offs & exceptions

- Programmers have the *least* control over this discipline; it fails without business participation, and many businesses refuse to engage (p. 313).
- Tool choice is explicitly secondary — formalisms can live in a spreadsheet or text editor (p. 315).
- If BA and QA are unaccustomed to writing formal, detailed specifications, programmers may write the acceptance tests with BA/QA guidance: the intermediate goal is tests BA and QA can *read and bless*; the ultimate goal is BA/QA writing them (p. 316).
- The discipline puts "a huge responsibility on BA and QA": their tests must be full specifications of the features (p. 315).

## Process prescriptions

- Strictest form: BA writes happy-path scenarios; QA explores the myriad ways the system can fail (p. 315).
- Tests are written at the same time as, or just before, the features they test — in an Agile sprint, during the first few days; all should pass by sprint's end (p. 315).
- Programmers automate the tests in a manner that keeps BA and QA engaged (p. 315).
- Once an acceptance test passes, it joins the continuous-build suite forever; a regression halts other work until repaired (p. 316).

## Open the PDF when

- You need the full widget-rendering test table verbatim (p. 315).
- You're weighing acceptance-test tooling and want Martin's exact framing that tools are secondary (pp. 314–315).
- You need the precise organizational-role prescriptions (BA vs. QA vs. programmer) for a process debate (pp. 315–316).
