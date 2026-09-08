---
chapter: 11
title: Be Polite
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch11_Be_Polite.pdf
pages: 8
level: function | component | surface
---

# Ch11 — Be Polite

**Thesis:** Modules should be organized like well-written newspaper articles: an abstract headline at the top, detail increasing downward, one level of abstraction per function, so readers can escape as early as their question is answered. Code that makes the reader wade through low-level detail to learn high-level intent is *rude*; code that lets the reader out early is *polite*.

## Named principles & rules
- **Ward Cunningham's definition of cleanliness.** Polite modules follow it: as you read the code, you find it to be "pretty much what you expected" (p. 241).
- **[Module = component].** A module is a bounded set of functions and variables — one class, several, or none; one source file or several. What matters is the cohesion of the functions and variables, not the artificial boundaries; another common word for module is *component* (p. 241).
- **Extract Till You Drop** (carried from Ch10). Following it yields modules of a few public functions plus many private functions extracted from them — possibly organized as a few public classes and several private classes. The public functions are the module's interface; the private ones its implementation (p. 242).
- **[Narrow interface, deep implementation].** Borrowed from John Ousterhout's *A Philosophy of Software Design*: such a module has a narrow interface and a deep implementation — "and that's a good thing" (p. 242).
- **The Stepdown Rule** (section "The Stepdown Rule: Once Again"). Each public function creates a tree of calls to private functions at lower levels of abstraction; each descending call goes *one level of abstraction* down — "Not two, not three. Just one" (p. 243). Restated: each function's name defines what it does; its lines all sit at the same level of abstraction, and each line, if not already at the lowest level, calls a function at the next level down (pp. 245–246). How big is one level? "Use your best judgment. For me... If I *can* meaningfully extract, then I do the extraction and check that it makes sense" (p. 246).
- **The Newspaper Metaphor.** Headline → synopsis paragraph → increasing detail. Readers sit in the loop `while (interested) readMore;`. "Articles that allow us to use that loop are *polite*—they let us out early. Articles that force us to waste time reading a lot of unnecessary detail are rude." Many short articles make the newspaper *usable*; a module should read the same way: name tells you if you're in the right module; topmost parts give high-level concepts; detail increases downward (pp. 243–244).
- **[One topic per module].** A newspaper article mixing two stories would be an abomination; so is a module containing two or more topics. Classes and functions within a module should all relate to a single topic — a single responsibility (footnote: the Single Responsibility Principle, SRP) — structured from high-level policy to low-level detail (p. 244).
- **Be Polite** (the titular rule). Functions that encapsulate a single level of abstraction let readers escape early; they read what a function does at their level of concern and are done. Rude code forces a minutes-long detour through 30 lines of deep detail, destroying the reader's train of thought — "It's as rude as the guy who bursts into your cubicle and throws a question at you without waiting for you to acknowledge him" (pp. 244–245).
- **The Abstraction Roller Coaster.** The failure mode: code that lurches between abstraction levels (zeroing totals, then a header string, then a loop, then a switch...). Every high-to-low transition forces the reader to push their mental model onto a mental stack — "The problem with that is that we do not have a mental stack," so the train of thought is lost (p. 246).
- **Kent Beck's rule, completed** — "First, make it work. Then, make it right." With the Ch11 criterion for *right*: "You are not done when the code works. You are done when the code reads well" — the tree of functions extracted, organized, and laid out conveniently for the reader (p. 247).

## The argument
We inevitably *write* on the roller coaster (section "This Is How We Write, but Not How We Want to Read"): the author of the rude `statement` function wrote the loop first, then remembered to zero `totalAmount`, then bolted on renter points — construction rolls through undulating abstractions and the code comes out shaped like its writing history (pp. 246–247). That is precisely why make-it-right is a separate, mandatory pass.

The cost model is reader attention. Reading a call to polite `makeStatement()` and wanting to confirm the footer is included: click through, see four abstract lines, click back — "just a simple question asked and answered in two seconds." With the rude 30-line `statement()`: a noun name describing no action, a minute or two spent verifying the footer among deep details, and by the time you return "you've forgotten why you were worried about that" (p. 245).

## Distilled example
The Video Store `RentalStatement` from Ch10, examined as reader experience (pp. 242–245).

Polite (after Extract Till You Drop):
```go
func (statement *RentalStatement) makeStatement() string {
  statement.clearTotals()
  return statement.makeHeader() +
    statement.makeDetails() +
    statement.makeFooter()
}
```
Abstract name; four calls one level down; `makeDetails` is a loop calling `makeDetail`, one further level down; `clearTotals` bottoms out in "excruciating detail" with "no meaningful lower level to descend to" (p. 242).

Rude (the original): 30-line `customer.statement()` mixing zeroed totals, header string, rental loop, movie-type switch, points logic, and Sprintf formatting — the abstraction roller coaster in one function (pp. 244–245).

## Smells & checklist
- Does the module have a few public functions (narrow interface) whose names state their task in abstract terms, backed by private extracted functions (deep implementation)?
- Does each function body sit at one level of abstraction, calling exactly one level down — never two or three?
- Can a reader answer a one-question concern ("does it include the footer?") in seconds and escape early?
- Function named as a noun (`statement()`) that actually performs an action → rude; name should describe the action at its level.
- First line of a high-level function is a low-level detail (zeroing a variable) → roller coaster; extract.
- Module mixes two or more topics → split; everything in the module should relate to one responsibility.
- Top of the module/file: highest-level concepts; detail increasing downward (invert for languages like Clojure that require declaration-before-use — footnote, p. 244).
- Code was declared done when it worked, with no reads-well pass → not done.

## Trade-offs & exceptions
- Martin himself sometimes allows two levels of abstraction within a function: "Do I always follow that rule? No... Generally, however, I consider that to be rude" (p. 243).
- The size of "one level of abstraction" is explicitly judgment: the operational test is whether a meaningful extraction exists (p. 246).
- Closing concession: "I don't follow these rules religiously or dogmatically. There are situations in which following them is inappropriate. But these rules are my default. I will follow them unless I have a good reason not to" (p. 247).
- Vertical ordering inverts in declaration-before-use languages (Clojure): low-level details at top, high-level policy toward the bottom (p. 244, footnote 2).

## Process prescriptions
None as a cycle — but it defines the exit criterion for Ch09's make-it-right loop: you are done only when the code reads well, i.e., the tree of functions descending from the public functions is extracted, organized, and laid out for the reader (p. 247).

## Open the PDF when
- You want the full rude `statement()` listing verbatim for a before/after demonstration (pp. 244–245).
- You need the complete reader-experience narrative (footer-question walkthrough, cubicle-interruption analogy) for teaching politeness as attention cost (p. 245).
