---
chapter: appendix
title: The Clean Code Debate (Martin vs Ousterhout)
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Appendix_The_Clean_Code_Debate.pdf
pages: 54
role: calibration — load when a principle's application is contested
---

# Appendix — The Clean Code Debate

**What this is:** A transcript of discussions between Robert "Uncle Bob" Martin (UB) and John Ousterhout (JOHN, author of *A Philosophy of Software Design*) held September 2024 – February 2025, published as the appendix to *Clean Code, 2nd ed.* (book pp. 561–614). Three topics — method length, comments, TDD — each ending with a negotiated agree/disagree list both authors signed off on. It is the book's own record of where its principles are contested and where Martin concedes limits.

## When to load this file

- A finding would demand decomposing a method, removing or adding a comment, or requiring TDD — before stating it as mandatory.
- The user pushes back on a Clean Code principle ("this is over-decomposed", "this comment is useful").
- You are about to cite a numeric threshold (function length, comment count) as if it were a rule.
- You need the canonical "where reasonable experts differ" record to calibrate confidence.

## Method length & decomposition

### Martin's positive test for extraction

- Extract only "meaningfully": "'Meaningfully' means that the extracted functionality can be given a descriptive name, and that it does less than the original method" (p. 565).
- Naming alone is not enough. Extracting `clearAmountOwed()`/`clearTotalPoints()` is "poor judgment... The implementation is not more deeply detailed than the interface" (p. 566).
- Extracting `clearTotals()` may be good judgment "because the interface is abstract, and the implementation has deeper detail" (p. 566).
- So: extract when the name is more abstract than the body; don't when the name merely restates the body.

### Ousterhout's stop tests

- *Shallow interfaces*: "As methods get smaller and smaller... The amount of functionality hidden behind each interface drops, while the interfaces often become more complex" — eventually "someone using the method needs to understand every aspect of its implementation. Such methods are usually pointless" (p. 563). The best methods are *deep*: much functionality behind a simple interface.
- *Entanglement*: "If you've ever found yourself flipping back and forth between the implementations of two methods as you read code, that's a red flag that the methods might be entangled" (p. 564).
- "If two pieces of code are tightly related, the solution is to bring them together. Separating the pieces, even in physically adjacent methods, makes the code harder to understand" (p. 574).
- "If methods are entangled, there is no clever ordering of the method definitions that will fix the problem" (p. 574).
- Names cannot rescue a bad split: "the 'can it be named' qualification doesn't help: Anything can be named" (p. 565).

### Martin's concessions

- No guardrails given: "You make a good point that I don't talk much in the book about how to make the judgment call" (p. 566); the agreed list records that *Clean Code, 1st ed.* "doesn't provide much guidance on how to recognize over-decomposition" (p. 576).
- His own 8-method `PrimeGenerator` failed him: "When I returned to the algorithm for the first time in a few days ago, I struggled with the names and structure" (p. 571).
- The buried side effect: "The side effect buried down in `smallestOddNth…` is a bit more problematic. Now that you've pointed it out, I don't like it much" (p. 573). Ousterhout's point: a trusted predicate name (`isMultipleOfNthPrimeFactor`) hiding a side effect means "thinking you understand it when you don't" (p. 573).
- The performance regression: Martin's rewrite split one loop into two methods; Ousterhout measured "a factor of three to four times slowdown" (p. 601). Martin: "Good catch! I would have caught that too had I thought to profile the solution" (p. 602) — and merged them back.
- Final state: Martin's last rewrite is "down to four methods, from eight in the *Clean Code* version" (p. 603). Ousterhout judged Martin's four-method version and his own single-method rewrite roughly comparable: "the additional methods you created didn't particularly help, but they didn't hurt either" (p. 601).

### The agree/disagree list (pp. 575–576) — verbatim

- "We agree that modular design is a good thing."
- "We agree that it is possible to over-decompose, and that *Clean Code, First Edition* doesn't provide much guidance on how to recognize over-decomposition."
- "We disagree on how far to decompose: You recommend decomposing code into much smaller units than I do. You believe that the additional decomposition you recommend makes code easier to understand; I believe that it goes too far and actually makes code more difficult to understand."
- "You believe that the One Thing rule, applied with judgment, will lead to appropriate decompositions. I believe it lacks guardrails and will lead to over-decomposition."
- "We agree that the internal decomposition of `PrimeGenerator` into methods is problematic. You point out that your main goal in writing `PrimeGenerator` was to show how to decompose into classes, not so much how to decompose a class internally into methods."
- "Entanglement between methods in a class doesn't bother you as much as it bothers me. You believe that the benefits of decomposing methods can compensate for problems caused by entanglement. I believe they can't: When decomposed methods are entangled, they are harder to read than if they were not decomposed, and this defeats the whole purpose of decomposition."
- "You believe that ordering the methods in a class can help to compensate for entanglement between methods; I don't."

Martin's sign-off: "We both value decomposition, and we both avoid entanglement; but we disagree on the relative weighting of those two values" (p. 576).

## Comments

### The two positions

- Martin: "I'm not hostile to comments in general. I *am* very hostile to gratuitous comments" (p. 578). Comments are "a necessary evil — or, if you prefer, *an unfortunate necessity*" (p. 578).
- Martin's trust criterion: "I look at every comment as potential misinformation... the best comments tell me something surprising and verifiable about the code. The worst are those that waste my time telling me something obvious or incorrect" (p. 586).
- Ousterhout: "Without comments, there is no way to have abstraction or modularity" (p. 583); interface comments define the contract that "there is no way to specify... in code" (p. 587).
- Ousterhout's cost claim: "For me, the cost of missing comments is easily 10 to 100 times the cost of incorrect comments" (p. 580).
- Ousterhout on long names as relocated comments: "super-long names are awkward and hard to understand... it would be better to use shorter names supplemented with comments" (p. 590).
- The scope rule for names vs comments (Martin, p. 581): "The larger the scope of a method, the shorter its name should be, and vice versa: The shorter the scope, the longer the name." Ousterhout accepts short-scope names like `isTooHot` but not "megasyllabic" ones like `isLeastRelevantMultipleOfLargerPrimeFactor` (p. 581).

### Concessions each way

- Martin, on Ousterhout's header comment for `isMultiple…`: "I think it's accurate. I wouldn't delete it if I encountered it... The warning of the side effect is useful" (p. 585).
- Martin: "There are times when precision is better expressed in a comment" (p. 585); interface comments are required "especially... when the interface is part of a public API" (p. 584).
- Ousterhout: "the first sentence is largely redundant with the name" (p. 585).
- Ousterhout's comments can be wrong too — Martin caught a bug in his `multiples` comment: "There is a bug in this comment that you exposed... good catch!" (p. 598).
- Ousterhout: "if a comment causes confusion in the reader, then it is not a good comment. Thus, I would rewrite this comment" (p. 598).

### The agree/disagree list (p. 590) — verbatim

- "Our overall views of comments are fundamentally different. I see more value in comments than you do, and I believe that they play a fundamental and irreplaceable role in system design. You agree that there are places where comments are necessary, but that comments don't always make it easier to understand code, so you see far fewer places where comments are needed."
- "I would probably write 5 to 10 times more lines of comments for a given piece of code than you would."
- "I believe that missing comments are a much greater cause of lost productivity than erroneous or unhelpful comments; you believe that comments are a net negative, as generally practiced: Bad comments cost more time than good comments save."
- "You view it as problematic that comments are written in English rather than a programming language. I don't see this as particularly problematic and think that, in many cases, English works better."
- "You recommend that developers should take information that I would represent as comments and recast it into code if at all possible. One example of this is super-long method names. I believe that super-long names are awkward and hard to understand, and that it would be better to use shorter names supplemented with comments."
- "I believe that it is not possible to define interfaces and create abstractions without a lot of comments. You agree for public APIs, but see little need to comment interfaces that are internal to the team."
- "You are unwilling to trust comments until you have read code to verify them. I generally trust comments; by doing so, I don't need to read as much code as you do. You think this exposes me to too much risk."
- "We agree that implementation code only needs comments when the code is nonobvious. Although neither of us argues for a large number of implementation comments, I'm more likely to see value in them than you do."

Ousterhout: "Overall, we struggled to find areas of agreement on this topic" (p. 590).

## TDD

- Ousterhout opens by admitting his APOSD description of TDD was wrong: "Oops! I plead 'guilty as charged' to inaccurately describing TDD. I will fix this in the next revision of APOSD" (p. 604).
- His alternative — write "a few tens of lines to a few hundred lines", then tests — is named **bundling**, Martin's own term from *Clean Code, 2nd ed.* (p. 604).
- Ousterhout's core objection: TDD "forces developers to work too tactically, in units of development that are too small; it discourages design thinking" (p. 607); "TDD guarantees that developers will initially write bad code" (p. 608).
- Martin's reply: "Those who do not value design will not design, no matter what discipline they practice" (p. 610).
- Martin's near-equivalence concession: "I think a disciplined programmer could effectively work that way [bundling]. Indeed, I think such a programmer would produce code that I could not distinguish from code written by another programmer following TDD" (p. 605); "someone adept at bundling and someone adept at TDD would produce very similar designs, with very similar test coverage" (p. 611).
- Both agree on where the value is. Ousterhout: "Enabling fearless refactoring? Bingo! This is the where almost all of the benefits from unit testing come from, and it is a really, really big deal." Martin: "Agreed" (p. 607).
- Explicitly unresolved for lack of empirical data: "I don't think we're going to resolve our disagreements on TDD. To do that, we'd need empirical data about the frequency of good and bad outcomes from TDD. Unfortunately, I'm not aware of any such data" (Ousterhout, p. 612).

### The agree/disagree list (pp. 612–613)

Prose preamble: "We agree that unit tests are an essential element in software development. They allow developers to make significant changes to a system without fear of breaking something. We agree that it is possible to use TDD to produce systems with good designs" (pp. 612–613). Then, verbatim:

- "I believe that TDD discourages good design and can easily lead to very bad code. You do not believe that TDD discourages good design and don't see much of a risk of bad code."
- "I believe that there are better approaches than TDD for producing good unit test suites, such as the bundling approach discussed above. You agree that bundling can produce outcomes just as good as TDD but think it may lead to somewhat less test coverage."
- "I believe that TDD and bundling have similar best-case outcomes, but that the average and worst-case outcomes will be much worse for TDD. You disagree and believe that, if anything, TDD may produce marginally better outcomes than bundling. You also think that preference and personality are larger factors in making the choice between the two."

Martin's sign-off: "We seem to disagree over the best application of discipline... We disagree on the risks and rewards of these two disciplines" (p. 613).

## Rules the skill adopts from this debate

- **"Complexity is in the eye of the reader"** (Ousterhout, p. 582 — Martin later invokes it against himself, p. 596): "If you write code that someone else thinks is complicated, then you must accept that the code is probably complicated... It is not OK to make excuses or suggest that it is really the reader's problem." The author cannot overrule a reader's confusion — and neither can a review finding.
- **No final authority.** Martin, on his own recommendations: "I claimed no final authority, nor even any absolute 'rightness.' They are offered for consideration" (p. 564). Cite Clean Code rules as considered defaults, not laws.
- **Decomposition's cheap-reversal default, bounded.** Martin: "if I must err, I'd rather err on the side of decomposition... They can always be inlined if we judge them to have gone too far" (p. 567). But the performance-regression catch (pp. 601–602) bounds it: an unprofiled extraction cost 3–4x runtime. "Err toward extraction" does not cover hot paths, and inlining back is the required remedy when a split goes wrong.
- **Ousterhout's closing frame** for weighing any finding: most of his concerns "result from two general errors... failure to focus on what is important, and failure to balance design trade-offs" (p. 613; elaborated pp. 613–614). Before enforcing a rule, ask whether it targets what matters here and whether the advice is balanced by a stop condition.
- **A Tale of Two Programmers (p. 596).** Both authors' own artifacts failed future readers, including themselves. Martin: "I refactored that old algorithm 18 years ago, and I thought all those method and variable names would make my intent clear — *because I understood that algorithm*... But my names didn't help me 18 years later. They didn't help you or your students either. And your comments didn't help me" (p. 596). Neither long names nor dense comments guarantee comprehension by someone outside the author's intimacy with the solution — humility applies to both camps' remedies.

## Open the PDF when

- You need the full code evolution of `PrimeGenerator` (Knuth's original p. 570, Martin's 8-method version pp. 568–569, Ousterhout's commented rewrite pp. 591–592, Martin's final 4-method version pp. 599–602) to ground an argument with a concrete example.
- A dispute turns on the exact wording of an exchange not quoted here (e.g., the `addSongToLibrary` interface-comment discussion pp. 583–584, or the comment-by-comment critique pp. 593–598).
- You need the full three laws of TDD and the Red-Green-Refactor description as stated in the debate (pp. 603–604).
