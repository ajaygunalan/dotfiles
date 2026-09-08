---
chapter: 5
title: Comments
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch05_Comments.pdf
pages: 28
level: function
---

# Ch05 — Comments

**Thesis:** Comments are, at best, a necessary evil — a compensation for our failure to express intent in code itself. They are not "pure good": a well-placed comment can be genuinely helpful, but comments rot, drift from the code they describe, and lie; the only reliable source of truth is the code. So minimize comments by making code expressive, keep the few good kinds, and delete the many bad kinds. "Don't comment bad code—rewrite it." (Kernighan & Plaugher, quoted p. 89)

## Named principles & rules

- **Compensating for Failure** — "The proper use of comments is to compensate for our failure to express ourselves in code." Every needed comment is a failure of the language or of our ability; think whether the tables can be turned before writing one. (p. 90)
- **Hidden or Obscured Comments** — IDEs collapse or de-emphasize comments (green/gray) precisely because we don't want to read them; the author paints comments fire-engine red on the theory that an existing comment should be read — and deleted or fixed if it doesn't help. "Comments, when they exist, should be visible!" (p. 90–91)
- **Lying Comments** — Comments often lie, unintentionally: code moves and evolves, comments don't follow, becoming "orphaned blurbs of ever-decreasing accuracy." Inaccurate comments are far worse than none. "Truth can only be certain in one place: the code." (p. 91)
- **Comments That Are Too Intimate** — Comments written from the author's intimacy with the code don't transfer; the reader lacks the context to understand them until they've understood the code anyway. (p. 92)
- **Comments Do Not Make Up for Bad Code** — Don't comment a mess; clean it. "Clear and expressive code with few comments is far superior to cluttered and complex code with lots of comments." (p. 92)
- **Explain Your Intent in Code** — Code is usually a fine vehicle for explanation: `if (employee.isEligibleForFullBenefits())` beats a comment plus flag arithmetic; often it's just a matter of creating a function that says what the comment would say. (p. 92)
- **Good Comments** (p. 92–97), the sanctioned kinds:
  - **Legal Comments** — copyright/license headers required by standards; refer to external documents rather than embedding legal tomes. (p. 93)
  - **Informative Comments** — basic information, e.g. the return value of an abstract method or the format a regex matches; often better replaced by a better name or a conversion class. (p. 93–94)
  - **Explanation of Intent** — documents the *why* behind a decision (sort ordering choice; "best attempt to get a race condition"). Even if you disagree with the solution, you know what the author was trying to do. (p. 94–95)
  - **Clarification** — translating obscure arguments/return values into something readable (e.g. `// a < b` beside `assertTrue(a.compareTo(b) == -1)`), useful when you cannot alter the code (standard library). Substantial risk: the clarifying comment itself may be incorrect and is hard to verify. (p. 95)
  - **Warning of Consequences** — warn other programmers ("SimpleDateFormat is not thread safe, so we need to create each instance independently"). (p. 96)
  - **Amplification** — amplify the importance of something that otherwise seems inconsequential (the `trim()` call whose removal would break parsing). (p. 96–97)
  - **Javadocs (and Their Ilk) in Public APIs** — a well-described public API is genuinely helpful; write good doc comments for public APIs, but they can be just as misleading, nonlocal, and dishonest as any other comment. (p. 97)
- **Bad Comments** (p. 97–111) — "usually crutches or excuses for poor code"; the author deletes them on sight:
  - **Mumbling** — a comment plopped in out of obligation whose meaning doesn't come through (`// No properties files means all defaults are loaded` — loaded by whom? when?). Any comment forcing you to look in another module has failed. (p. 97–98)
  - **Redundant Comments** — a header comment saying nothing the code doesn't; less precise than the code and takes longer to read. (p. 98–99)
  - **Misleading Comments** — subtly wrong statements ("returns *when* closed" vs actually *if*) that send readers into debugging sessions. (p. 99)
  - **Redundancy and Imprecision** — legions of useless Javadocs (Tomcat's `ContainerBase`) that clutter, restate names, and use terms (`component`/`container`) imprecisely. (p. 99–102)
  - **Mandated Comments** — rules requiring a Javadoc for every function/variable produce clutter and abominations (`@param title The title of the CD`). (p. 102)
  - **Journal Comments** — per-edit change logs at the top of modules; source control does this now; remove them completely. (p. 102–103)
  - **Noise Comments** — restate the obvious (`/** Default constructor. */`); we learn to skip them, then fail to notice when they begin to lie; venting (`//Give me a break!`) should be redirected into refactoring. (p. 103–105)
  - **Scary Noise** — noisy Javadocs on fields, including cut-paste errors (`/** The version. */ private String info;`). (p. 105–106)
  - **TODO Comments** — 2nd-edition reversal: "TODO means *Don't Do*." He still writes them but will not check them in — do the thing, eliminate the need, or move it to the backlog. (p. 106)
  - **Use a Function or a Variable Instead of a Comment** — extract explanatory variables/functions so the code reads like the comment would have (`moduleDependants.contains(ourSubSystem)`). (p. 106–107)
  - **Position Markers** — banners like `// Actions ////////`; use very sparingly or they become background noise ("the little boy who cried 'Wolf!'"). (p. 107)
  - **Attributions and Bylines** — `/* Added by Rick */` is graffiti; source control remembers who added what; PR numbers and JIRA tags belong in commit comments, not source. (p. 107)
  - **Commented-Out Code** — "an abomination"; others won't dare delete it, so it gathers like dregs. Commenting out while debugging is fine; don't check it in. (p. 107–108)
  - **HTML Comments** — HTML markup in source comments makes them unreadable where it matters most; formatting for tools like Javadoc is the tool's job. (p. 108–109)
  - **Nonlocal Information** — a comment must describe the code it appears near, not system-wide facts (a function documenting a default port it doesn't control). (p. 109)
  - **Too Much Information** — no historical discussions or arcane RFC details (base64 bit-packing) irrelevant to the reader. (p. 109–110)
  - **Unobvious Connection** — the link between comment and code should be obvious; a comment that needs its own explanation ("What is a filter byte?") has failed. (p. 110)
  - **Function Headers** — short functions don't need description; "a well-chosen name and signature for a small function that does one thing is usually better than a comment header." (p. 110)
  - **Javadocs in Nonpublic Code** — for code maintained by a small team and not for public consumption, Javadoc formality is cruft and distraction. (p. 111)

## The argument

Comments decay because "programmers can't realistically maintain them" — code moves, bifurcates, recombines, and comments become separated from what they described (p. 91). Inaccurate comments "delude and mislead. They set expectations that will never be fulfilled." Rather than demanding discipline to keep comments accurate, the author "would rather that discipline and energy go toward making the code so clear and expressive that it does not need the comments in the first place." (p. 91)

He preempts the abuse of this advice: "Shame on any programmers, young or old, who use these recommendations as an excuse for their laziness and/or unwillingness to add proper explanations and context." (p. 90)

The closing verdict: "Comments are not like Schindler's list—they are not 'pure good.'… The only language of 'truth' at our disposal is our code." When code cannot express intent, the risk of ambiguous English "can sometimes be worth it. But tread carefully—there dwell dragons." (p. 115)

## Distilled example

The `GeneratePrimes` module (p. 111–114): a "well documented" class — Javadoc with a biography of Eratosthenes, `@author`, `@version`, and a comment on nearly every line (`// declarations`, `// sieve`, `// bump count.`). Kent Beck's refactoring (`PrimeGenerator`) replaces almost all of them with named functions: `uncrossIntegersUpTo`, `crossOutMultiples`, `determineIterationLimit`, `putUncrossedIntegersIntoResult`, `notCrossed`. Exactly two comments survive, both explanatory: a class header easing the reader into the algorithm, and the rationale for using the square root as the iteration limit — "I could find no simple variable name, nor any different coding structure that made this point clear." (p. 114)

## Smells & checklist

- Comment restates the adjacent code or a name (redundant/noise) → delete.
- Comment explains *what* confusing code does → refactor into a well-named function/variable instead.
- Comment is wrong, imprecise, or describes code far away (misleading/nonlocal) → fix or delete.
- Checked-in commented-out code → delete (source control remembers).
- Checked-in TODOs → do it, eliminate it, or move to the backlog.
- Journal entries, bylines, PR/JIRA tags in source → delete; they belong in source control.
- Mandated doc comments on every member; Javadocs on nonpublic code → remove the mandate/cruft.
- Position-marker banners more than very rarely → remove.
- HTML markup inside comments → remove; let the doc tool format.
- Keep and verify: intent, clarification (double-check correctness), warnings of consequences, amplification, legal headers, public-API docs.
- Passes review only if the comment gives information the code cannot: *why*, warnings, amplification.

## Trade-offs & exceptions

- Comments are sometimes genuinely necessary — "we cannot always figure out how to express ourselves without them"; their use just isn't cause for celebration (p. 90).
- Clarification comments are simultaneously endorsed and flagged as risky: one of the book's own `compareTo` clarifications is wrong, and verifying them is hard (p. 95).
- Explanation-of-intent comments are worth keeping even when flagging the code for refactoring (extract `attemptRaceCondition`), and even when the documented approach is technically flawed (the 2nd-edition "Future Bob" sidebar notes the race-condition test is a terrible way to force a race) (p. 94–95).
- Informative comments like a regex-format note may be a lie in detail (the pattern matched non-timestamps) — the fix is to correct the code and let the comment remain (p. 93–94).
- Commenting out code *while debugging* is a useful technique; the rule is only against checking it in (p. 108). Same for TODOs (p. 106).
- Even a redundant class-header comment can be kept if it "serves to ease the reader into the algorithm" (p. 114).
- Public APIs genuinely deserve doc comments; the prohibition targets internal code (p. 97, 111).

## Process prescriptions

- Before writing any comment, "think it through and see whether there isn't some way to turn the tables and express yourself in code" (p. 90).
- Make comments visible in your editor (the author colors them red); read every comment you encounter, and delete or fix on the spot any that don't help (p. 91).
- TODO discipline: never check TODOs in — act, eliminate, or backlog (p. 106).

## Open the PDF when

- You need the full Tomcat `ContainerBase` or `GeneratePrimes`/`PrimeGenerator` listings to demonstrate redundancy or the refactoring end-to-end (p. 99–102, 111–114).
- Judging a borderline clarification/intent comment and you want the book's exact worked examples and caveats (p. 93–97).
