---
chapter: 14
title: Testing Disciplines
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch14_Testing_Disciplines.pdf
pages: 14
level: process
---

# Ch14 — Testing Disciplines

**Thesis:** Writing tests is not an ad hoc afterthought but a *discipline* — a committed way of working. Three disciplines (TDD, TCR, Small Bundles) all produce the same asset: a test suite you can trust with your life. That trust is the real payoff, because it "muzzles the devil" of fear — the fear that stops programmers from cleaning code — and thereby prevents the rot that degrades every untested system.

## Named principles & rules

- **Test-Driven Development (TDD)** — Discipline 1. Proposed by Kent Beck in the mid-to-late '90s; not merely "tests first" but an intricate discipline locking test and production code into a seconds-long cycle (p. 291).
- **The Three Laws of TDD** — the foundation of the TDD discipline (pp. 291–292):
  - **The First Law:** "Write no production code until you have first written a test that fails due to the lack of that production code." (p. 291)
  - **The Second Law:** "Write no more of a test than is sufficient to fail, or fail to compile. Resolve the failure by writing some production code." (p. 291)
  - **The Third Law:** "Write no more production code than will resolve the currently failing test. Once the test passes, write more test code." (p. 292)
- **Test && Commit || Revert (TCR)** — Discipline 2. Proposed by Kent Beck in 2018. Code that passes tests is immediately committed; code that fails tests is immediately *reverted* (usually by a script on save). The threat of losing work forces tiny steps and tests written together with code (pp. 292–293).
- **Small Bundles** — Discipline 3. Proposed to Martin by John Ousterhout. No ordering of tests vs. code and a longer cycle (minutes, not seconds); the programmer concludes each small bundle of code+tests with high coverage and all tests passing, testing every branch and condition (p. 293).
- **The Humble Object Pattern** — design systems so untestable stretches at hardware/framework boundaries are very thin; move intelligence away from the boundary and keep the code that touches it "as anemic as possible" (p. 298).
- **The Boy Scout Rule** (referenced from Ch. 1) — continuous cleaning is only possible when a trusted test suite removes the fear of change (pp. 297–298).
- [Hammock-driven development] — Martin's referenced term (Rich Hickey's) for strategic up-front thinking; vital, but must be "brought back to reality on a frequent basis" (p. 293).
- [Test code is a first-class citizen] — "Test code is just as important as production code. It is not a second-class citizen. It requires thought, design, and care. It must be kept as clean as production code." (p. 300)
- [Tests enable the -ilities] — tests are what keep code flexible, maintainable, and reusable; "Tests enable all the -ilities, because tests enable change." (pp. 300–301)

## The argument

Following any of these disciplines yields four goods (Reprise, p. 296): drastically reduced debugging time; "a stream of nearly perfect low-level documentation"; a test suite trusted enough to deploy on green; and a less-coupled design (you cannot write a hard-to-test module if the tests are written along with the code).

But those are not the deepest reason. The deepest reason is fear (**The Angel and the Devil**, p. 297): facing messy code, the devil screams "Don't touch it! …if you break it, it will become yours FOREVER," and fearful programmers let the code rot. "Because of that fear, the only thing that can happen to the code in that system is that it must rot" (p. 297). With a trusted suite, "the devil does not appear. The devil has no power. Because you have the test suite" (p. 297) — cleaning becomes virtually risk free and the whole team follows the Boy Scout Rule.

Half-hearted after-the-fact testing leaves holes: "When you know that the test suite is full of holes, there is no safe decision you can make when it passes" (p. 296). And tests double as documentation: they are "utterly unambiguous… so formal that it executes, and it cannot get out of sync with the application" — "an almost perfect form of low-level documentation" (p. 295), though explicitly *not* high-level documentation.

## Distilled example

The mid-'90s `Timer::ScheduleCommand(Command*, int milliseconds)` story (pp. 290–291). Before: Martin's "test" was a keyboard driver — he tapped a melody, waited five seconds, and listened for it to replay ("I want a girl…"), then threw the test away. After (today's discipline): mock the OS timing functions with test doubles, schedule commands that set boolean flags, step time forward in the test and assert the flags flip at the right instant — then keep the tests, clean them, decouple them, and ship them with the code in the same package.

Also the coached-team cautionary tale (pp. 299–300): a team allowed "quick and dirty" tests → dirty tests grew harder to change than production code → suite discarded → fear returned → defect rate rose → production code rotted. "It was their decision to allow the tests to be messy that was the seed of that failure" (p. 300).

## Smells & checklist

- Is every module covered by tests written *with* it (any of the three disciplines), not concocted after the fact?
- Does the suite have holes — modules skipped because they were "hard to test"? A hard-to-test module signals coupled design.
- Would the team deploy (or promote DEV → QA) on a green run? If not, the suite is not trusted — find out why.
- Is intelligence pushed away from hardware/framework boundaries (Humble Object), leaving boundary code thin and anemic?
- Are third-party frameworks isolated behind a layer so they can't render large swaths untestable?
- Are tests kept in the same package as the code, convenient for anyone to run?
- Are tests held to production-code standards of naming, size, design, and partitioning?
- Heavy debugger use is a smell: with a discipline, "the time I spend in the debugger is vanishingly small" (p. 294).

## Trade-offs & exceptions

- No discipline is universally applicable or to be followed blindly; like a pilot's *memory items* vs. checklists, some situations demand a different discipline (p. 294).
- TDD vs. TCR is temperament: "I find TCR to be stressful, while I find TDD to be relaxing" (p. 293). Small Bundles is a "softer ritual" but "can be just as effective" if bundles stay small and every branch is tested (p. 293).
- These are *tactical* disciplines; they don't supplant strategic design. "Months of strategic planning, without any coding, is suicide. Coding without any strategic planning is equally suicidal" (p. 293). TDD verifies lowest-level designs "but it does not help much in higher-level design and architecture… I have seen some pretty bad designs implemented with TDD" (p. 294).
- Three cases where tests are impractical (pp. 298–299): (1) code beyond the hardware boundary (final GUI pixels, mouse movement, socket wire data); (2) untestable third-party frameworks (Swing experience report: ~70% coverage was the ceiling); (3) subjective results (does the font look "right"?) — there is no way to write a test for a judgment call. Response: make those areas small and simple and protect the rest of the system from them. Open question raised: "how do you test the results of an AI?" (p. 299).
- Cost concession: thousands of tests a year can rival production code in sheer bulk — "a daunting management problem" (p. 299).

## Process prescriptions

- **TDD cycle:** alternate line-by-line per the Three Laws — test line (fails/doesn't compile) → minimal production code → next test increment → repeat; the full cycle is "just a few seconds long" (p. 292).
- **TCR cycle:** on every save, a script runs the tests and executes `commit` on pass or `revert` on fail; write in very small steps (pp. 292–293).
- **Small Bundles cycle:** in minutes-long cycles, produce a small bundle of code + tests (any internal order), ending with all tests passing, every branch and condition tested (p. 293).
- Alternate strategic design ("hammock-driven") with tactical discipline, returning to reality frequently (p. 293).

## Open the PDF when

- You need the full Angel-and-Devil narrative or the coached-team failure story verbatim (pp. 297, 299–300) for persuasion rather than review.
- You must argue the edge cases of impractical testing (GUI/socket/subjective) with the Swing experience report (pp. 298–299).
- You want the exact wording of the Three Laws for quotation (pp. 291–292).
