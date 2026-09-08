---
chapter: 10
title: One Thing
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch10_One_Thing.pdf
pages: 30
level: function | class
---

# Ch10 — One Thing

**Thesis:** "Clean code does one thing well" (Stroustrup) is empty until *one thing* is defined. Martin's definition: a function does one thing if you cannot meaningfully extract another function from it. Therefore extract, and extract, until you can't — and in doing so you will discover the classes that every large function is secretly hiding.

## Named principles & rules
- **[Definition of One Thing]** — "A function does one thing if you cannot meaningfully extract another function from it." If you can split one function into two, the original did two things (p. 212).
- **Extract Method Refactoring.** The IDE operation this chapter is built on: select code, extract it into a named function, the IDE writes the glue (p. 212).
- **Extract till you drop!** The discipline: "We extract, and extract, until we cannot meaningfully extract anymore." Softened immediately: you should *consider* as many extractions as you can; you may not do them all (p. 213).
- **[Meaningful extraction — lower bound].** Extracting the entire body leaving a pure delegator is not meaningful (`addRental` → `doTheAdd`); nor is splitting `clearTotals` into `clearAmount`/`clearPoints` whose names are indistinguishable from their implementations. "You can extract too little, and you can extract too much" (pp. 212–213).
- **The Stepdown Rule.** A meaningful abstraction follows it: the name of a function is more abstract than the implementation (p. 213; developed fully in Ch11).
- **The five fears** (section "This Shouldn't Be Controversial," pp. 214–217): **1. Drowning** — no sea of tiny functions: namespaces/classes form a named hierarchy of guideposts (pp. 214–215). **2. Small Functions Don't Obscure Intent** — well-named structure *reveals* intent (p. 216). **3. Performance** — function calls cost nanoseconds; real only if you must guard every nanosecond; measure, then inline the critical few; compilers inline anyway (p. 216). **4. Bouncing Around** — defeated by polite ordering (below) (p. 216). **5. Entanglement** — the one reasonable complaint (Ousterhout's point); see Trade-offs (p. 217).
- **[Callee-ordering rule]** — organize extracted functions in the order they are called: "If function A calls B and C, then their order in the source file should be A, B, C" (p. 216; Clojure footnote: C, B, A).
- **"Every large function is really hiding a class (or more) inside it."** Large functions have local variables plus indented regions that manipulate them; those variables should be fields and those regions methods of a class (p. 219).
- **Composed assertion.** Test-cleaning device (`assertOwedAndPoints`) that tightens wordy tests (pp. 223–224).
- **[Tests should not contain production data].** Names like `Fred` and `The Cell` say nothing; test data should explain the intent of the test. Also: test the volatile UI format once, not in every test (pp. 222–223).
- **[Switch statements breed]** — "switch statements are like gerbils—given enough time they'll reproduce all over your code"; a switch on a type code suggests polymorphic dispatch (p. 231).
- **Open–Closed Principle (OCP).** The end state of the Video Store: new `RentalType`s can be added with no changes to existing code (p. 234).
- **[Extract to communicate through class scope].** Sometimes extraction is cleanest when extracted functions share variables in the enclosing class instead of passing arguments — even at the cost of promoting locals to fields ("You promoted local variables into instance variables! ... True. I am.") (pp. 218, 237–238).

## The argument
Martin's 3,000-line C function `gi` "interpreted graphics" — one thing, allegedly — yet obviously did many *things*. The definition via Extract Method makes "one thing" operational rather than rhetorical (pp. 211–212). This recommendation has been "the most controversial" since the first edition (p. 214), so the chapter answers each fear in turn. The deeper payoff is structural: extraction exposes the high-level procedure ("How do you make a statement? You clear the totals and then compose the header, details, and footer," p. 227) and flushes out misplaced code — "It was the extraction of all those methods in the Video Store example that allowed us to see that some of that code did not belong in the class it was in. That was not evident before we did the extractions" (p. 239).

On readers who prefer large undulating functions: rotate the listing 90° and it looks like the horizon our hindbrain navigates by — but only the original author knows the terrain "geographically"; the new programmer fumbles in a 3,000-line morass (p. 215).

## Distilled example
The **Video Store** example (from Fowler's *Refactoring*, 1999), redone in Go with tests, pp. 219–234.
- Before: `Customer.statement()` — one ~30-line function mixing loop, switch on `movieType`, amount rules, points rules, and string formatting.
- First: fix the tests (fragile UI-string assertions everywhere → test format once; production data → intent-revealing data; wordy → composed assertion `assertOwedAndPoints`) (pp. 222–224).
- Then extract till you drop: `makeStatement` = `clearTotals` + `makeHeader` + `makeDetails` + `makeFooter`; `makeDetail` = `determineAmount`, `determinePoints`, `formatDetail` (pp. 225–227). Locals `totalAmount`/`frequentRenterPoints` promoted to fields to enable extraction (p. 225).
- Extraction reveals misplacement: the `determine` functions never touch `Customer` — move them to `Rental`; the type code belongs on `Rental` not `Movie` ("The Tigger Movie" rents as both NewRelease and Childrens); the switch becomes a `RentalType` interface with `NewReleaseRental`/`ChildrensRental`/`RegularRental` polymorphic dispatch; `Customer` renames to `RentalStatement` (pp. 228–233). The tests survived the class-level redesign unchanged — "the tests have a design that tolerates change!" (p. 229). Net: one large function became three new classes plus one existing, with an implicit architectural boundary below `RentalType` — OCP at work (p. 234).

Secondary example: **Extraction and Classes** — Java `QuadraticFormula.solve` extracted into `linearSolution`/`quadraticSolution`/`complexSolution`/`singleQuadraticSolution`/`twoQuadraticSolutions`; then arguments replaced by class-scope statics; Clojure version communicates through `let`-scoped closures with no static/concurrency worries (pp. 235–239).

## Smells & checklist
- Can another function be *meaningfully* extracted? If yes, the function does more than one thing — at least consider the extraction.
- Extraction produced a pure delegator, or names that merely restate the implementation → too much; inline back.
- Function bodies of if/else and for/while statements, and their predicates, are prime extraction targets; statements should become "little more than the keywords and the function calls" — reading "like well-written prose" (pp. 213–214).
- Are extracted functions ordered A, B, C in call order? Bouncing-around pain is an ordering smell, not an extraction smell.
- A cluster of methods manipulating a shared set of variables → a class is hiding there; name it.
- A switch on a type code → consider polymorphic dispatch before the gerbils breed.
- After extracting, ask of each function: does it use the class it lives in? Its arguments more than its host? → move it (Video Store `determine*` → `Rental`).
- Tests: fragile UI-format assertions repeated everywhere; production data instead of intent-revealing data; missing composed assertions.
- Class whose name no longer matches what it does after cleanup → rename (`Customer` → `RentalStatement`).
- Performance objection raised? Demand measurements; inline only the measured-critical functions.

## Trade-offs & exceptions
- "Meaningfully" is left partly to judgment: you can extract too little and too much (p. 213). Footnote exception: a pure-delegator extraction is fine when you're creating a delegator to move the function to another module (p. 213 n2).
- **Entanglement (fear 5) is conceded as reasonable:** extracting may entangle the logic of the two functions — the lower-level function may not be independent of the higher-level one. If entanglement is severe (several facts from the parent must be kept in mind), the extraction "might not be worth doing." If minimal, a good name plus placement directly after the parent makes it worthwhile. "It's a judgment call. Choose wisely" (p. 217).
- Function size targets are style: "three, or four, or six" lines, larger for some switch/formatting statements or certain languages (p. 213); readers comfortable with 20–25-line functions may stay there — "That's up to you" (p. 239) — but must not miss the misplaced-code discoveries extraction yields; consider extract-then-strategic-inline. "But remember, when you inline a function, you destroy its name" (p. 239).
- Promoting locals to instance variables trades encapsulation for extractability (pp. 218, 225); class-scope statics risk corruption under multithreading — fixable by making them instance members (p. 238).
- Nanosecond-critical domains (first-person shooters, high-speed trading, missile guidance) legitimately fear call overhead (p. 216).
- **Future Bob** note: Robert Laszczak's Golang-idiomatic improvements at https://threedots.tech/clean-code/ — Martin agrees with most, keeps longer names and `get` prefixes (p. 235).

## Process prescriptions
Not a process chapter, but the demonstrated order matters: (1) fix the tests' design first; (2) extract till you drop; (3) let extraction reveal misplaced responsibilities; (4) move code to where it belongs; (5) replace type-switches with polymorphism; (6) rename what the cleanup exposed. Optionally extract-then-strategically-inline (p. 239).

## Open the PDF when
- You need the full Video Store code at any intermediate stage, or the exact before/after class diagram (pp. 219–234).
- You want the complete rebuttal text of the five fears for teaching (pp. 214–217).
- You need the quadratic-formula Java/Clojure listings for the "communicate through scope" argument (pp. 235–239).
