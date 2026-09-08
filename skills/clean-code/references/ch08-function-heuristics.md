---
chapter: 8
title: Function Heuristics
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch08_Function_Heuristics.pdf
pages: 26
level: function
---

# Ch08 — Function Heuristics

**Thesis:** "What follows are some heuristics that I have found helpful in keeping my code clean. I don't follow them as hard-and-fast rules, but when all else is equal, these are my biases" (p. 159). The heuristics govern argument lists, command/query discipline, error handling, duplication, side effects, and control structure — the mechanics of writing functions that together form the domain-specific language in which the system's story is told. Note: the chapter's heuristics are named by section, not numbered; the section names below are exact.

## Named principles & rules

- **Function Arguments** — Every argument added makes a function harder to understand. Easiest is the empty (declared) argument list — the implied `this`/`self`/enclosing-scope argument doesn't count. One argument is easy; two aren't too hard (make them commutative if possible); "three is usually my limit." Arguments are couplings (pp. 159–160).
- **Variadic Arguments** — A variadic function like `String.format(String format, Object… args)` really takes two arguments: the format and the array (p. 161).
- **More Than Three?** — With more than three arguments and no rationale for the order (unlike `distance(x1,y1,x2,y2)`), there are 23 ways to get four wrong; find some other means: group them into an object ("if four things are so cohesive that they can be passed, as a unit, into a function, then why aren't they already an object?"), a hash map with nice names, or fields in the current class (pp. 160–161).
- **Keyword Arguments** — Where the language supports naming arguments at the call site (C#, Clojure hash maps, Ruby), order stops mattering and passing more than three is occasionally acceptable (p. 161).
- **Flag Arguments** — "Flag arguments are ugly. Passing a boolean into a function is generally careless." It complicates the signature and "loudly proclaims that the function does more than one thing." Where possible, split into two functions, one per case: `getLongMonthNames()` / `getShortMonthNames()` (pp. 161–162).
- **Output Arguments** — Arguments used to catch output values violate "the principle of least surprise" (footnoted as **The Law of Least Astonishment**, *PL/1 Bulletin*, 1967): readers expect data to go *in* through arguments and *out* through the return value. Prefer multiple return values, a returned object, two functions, or letting the object act as the output argument of its own methods (`stats.calculate(list); stats.getMean()`) (pp. 162–163).
- **Error Codes** — Go's multiple-return `f, err := os.Open(...)` convention: "So long as this convention is applied narrowly and consistently, I think it's a reasonable convention; especially in a language like Go that does not have exceptions" (pp. 163–164).
- **Command Query Separation (CQS)** — "Under the CQS convention, functions either do something or answer something, but not both. Either a function is a command that creates a side effect … or it is a query that returns some information. Doing both can lead to confusion" — e.g., `if (set("username","unclebob"))` where `set` reads as verb or adjective. Separate: `if (attributeExists(...)) { setAttribute(...); }` (pp. 164–165). Convenient violations like `stack.pop()` cost concurrency safety and exception safety (C++ STL splits it into `top()`/`pop()`) (p. 165).
- **Prefer Exceptions to Returning Error Codes** — Error codes from command functions subtly violate CQS (commands used as expressions in `if` predicates) and force immediate, deeply nested caller handling; exceptions let error processing be separated from the happy path (pp. 165–167). Subsection **Caveat Emptor**: exception reliability varies by language — C++ doesn't guarantee it, Go lacks exceptions (pp. 165).
- **Extract Try/Catch Blocks** — Try/catch blocks "confuse the structure of the code and mix error processing with normal processing," so extract the bodies of `try` and `catch` into functions of their own (`delete` → `deletePageAndAllReferences` + `logError`) (p. 167).
- **Error Handling Is One Thing** — "A function that handles errors should do nothing else": if `try` exists in a function it should be the very first word (after perhaps some variable declarations), with nothing after the `catch`/`finally` blocks (p. 168).
- **The Dependency Magnet of Error Codes** — A global error-code file (`error.h`, `Error.java`) becomes a dependency magnet: everyone imports it, and adding a code forces recompilation/redeployment pressure, so programmers "creatively" reuse old codes. Mitigate with enums (Java), or fully escape with interfaces/dynamic polymorphism — Go's `Error` interface, duck-typed classes in Python (pp. 168–169).
- **DRY: Don't Repeat Yourself** — Duplication of code should be avoided; advice at least as old as *The Pragmatic Programmer* (2000), Codd's normal forms, and Bertrand Meyer's **Single Choice Principle** (1988) (p. 169).
- **Simple Repeated Code** — For L lines repeated in P places: if both L and P are small, the duplication does little harm and eliminating it "may do more harm than good." Decision table: L small & P small → "Maybe extract"; every other cell → "Extract." Larger L means higher odds the snippet will need coordinated change (pp. 169–170).
- **Similar Code** — Repeated snippets differing by only a constant or variable tend to have large L and should be extracted, usually by adding an argument or two to the extracted function, then hoisting shared locals into fields (`TestableHtml`/`includeInheritedPage`, pp. 170–174).
- **Loop Duplication** — When many traversals share a loop but differ in body, eliminate the duplication with a lambda ("block"), or "older, and sometimes better options": the Command pattern, the Strategy pattern, or the TemplateMethod pattern. Martin's '90s C++ name for the TemplateMethod version: "Write a Loop Once" (pp. 174–176).
- **Accidental versus Essential Duplication** — Essential duplicates change together; accidental duplicates evolve apart, and combining them is a mistake. The test is the **Single Responsibility Principle (SRP)**: similar code in modules responsible to *different actors* is accidental — extracting it "you are likely to break the system for one actor while you try to satisfy the other"; similar code responsible to the *same actor* is essential — extract it (p. 177).
- **Side Effects** — Modern definition: "a side effect [is] any state change that outlives the function, even if that state change is the primary intent of the function. In other words, a function with a side effect is impure." Side effects introduce **temporal coupling** — coupling in time: the order of lines must be preserved (pp. 177–178). Side-effect functions come in pairs (`open/close`, `seize/release`, `malloc/free`): "always two there are" (p. 178).
- **We Are Bad at This** — Garbage collection exists because programmers proved unable to balance `malloc` with `free`; but GC addresses only memory, not file descriptors, graphics contexts, or semaphores. Temporal couplings from side effects "are at the root of all concurrent update problems, all reentrancy problems, all race conditions, and nearly all initialization and finalization problems" (p. 178).
- **Functional Languages** — Suppress side effects by lacking assignment: names are assigned to values but values are never overwritten ("named values cannot be varied"). Not a cure-all: atoms (Clojure), OS facilities, and simulation mean side effects remain possible (pp. 178–180).
- **Object-Oriented Languages** — OOPLs are accused of promoting side effects, but they "have very good facilities to suppress and hide side effects": the `LineCounter` class hides impure private methods behind one pure-looking public `count`, "preventing temporal couplings from leaking out into the application at large" (single-threaded caveat noted) (pp. 180–181).
- **Structured Programming** — Dijkstra's 1968 discipline ("Go To Statement Considered Harmful"): all programs written from three control structures — **Sequence**, **Selection**, **Iteration** — recursively applied as single-entry/single-exit units (depicted in a **Nassi–Schneiderman flowchart**). Restricted control flow keeps every path easy to reason about; `goto` makes reasoning impractical (pp. 181–183).
- **First, make it work. Then, make it right.** — Closing restatement of the drafting discipline (p. 184).

## The argument

Arguments, error codes, duplication, and side effects are all forms of coupling — between caller and callee, between modules, and between lines of code across time. Each heuristic reduces one coupling: fewer arguments mean fewer strands to hold in mind; CQS prevents verb/adjective ambiguity at call sites; exceptions detach error processing from the happy path; DRY puts each decision in one place (Meyer's Single Choice); avoiding side effects removes temporal coupling, which "when order matters … can leak out into other parts of the code, creating situations that are as difficult to debug as a memory leak" (p. 178).

The chapter closes by reframing functions as vocabulary: "Every system is built from a domain-specific language designed by the programmers to describe that system. Functions are the verbs of that language, and contexts are the nouns … the art of programming is, and has always been, the art of language design" (p. 184). The heuristics are means; "your real goal is to tell the story of the system" (p. 184).

## Distilled example

Error handling (pp. 166–167). Before — nested error-code checks:

```java
if (deletePage(page) == E_OK) {
  if (registry.deleteReference(page.name) == E_OK) {
    if (configKeys.deleteKey(page.name.makeKey()) == E_OK) { ... } else { ... }
  } else { ... }
} else { ... }
```

(Guard-clause variants only pretend the nesting is gone.) After — exceptions, then Extract Try/Catch:

```java
public void delete(Page page) {
  try { deletePageAndAllReferences(page); }
  catch (Exception e) { logError(e); }
}
```

`delete` is all about error processing; `deletePageAndAllReferences` is all about deletion — each does one thing.

For DRY, the `TestableHtml` example (pp. 170–174) collapses four near-identical setup/teardown snippets into one `includeInheritedPage(pageName, includeString)` after moving `buffer` and `wikiPage` into fields.

## Smells & checklist

- More than three declared arguments without keyword-argument support or an ordering rationale.
- Boolean flag argument selecting between two behaviors — split the function.
- Output arguments (`out`, pointer/reference params used for results) — return values, objects, or method state instead.
- A function that both changes state and returns an answer (CQS violation) — especially one whose return feeds an `if` predicate.
- Error codes returned from command functions; nested or guard-style error-code ladders.
- `try` that is not effectively the first word of its function, or code after `catch`/`finally`.
- A single global error-code file imported everywhere (dependency magnet).
- Duplicated snippets: apply the L/P table; check SRP actors before merging similar code (accidental vs. essential).
- The same traversal loop rewritten around different bodies — lambda/Command/Strategy/TemplateMethod.
- Function pairs like `open/close` whose ordering constraints leak across the codebase (temporal coupling).
- Control flow not reducible to sequence/selection/iteration; `goto`-like jumps.

## Trade-offs & exceptions

- The whole chapter is explicitly biases, not hard-and-fast rules (p. 159). "Yes, a limit of three is arbitrary. You might be comfortable with more. You do you, I'll do me" (p. 160).
- Flag arguments: objects with internal binary flags set via `setFlag(boolean)` are exempt — "I'm not going to complain about them" (p. 162).
- Keyword arguments legitimately relax the three-argument limit (p. 161).
- Go's error-code-return convention is reasonable when applied narrowly and consistently (p. 164).
- CQS "should be considered where practical" — Martin admits `stack.pop()`-style violations are sometimes convenient and says "I take the advice seriously and violate it only after considering the possible outcomes" (p. 165).
- Small-L, small-P duplication is often better left alone; extraction there is a readability convenience, not a DRY necessity (pp. 169–170).
- Never DRY-merge accidental duplicates — SRP actors decide (p. 177).
- Functional languages help with side effects "but cannot, and will not, eliminate them" (p. 180); OOPLs, despite their reputation, are good at *hiding* side effects (pp. 180–181).

## Process prescriptions

- Draft-then-refine, like prose writing: first drafts of functions "come out long and complicated," with duplication and temporal couplings — but covered by "a suite of unit tests that cover every one of those clumsy lines." Then massage: split out functions, rename, eliminate duplication, make functions purer, shrink and reorder methods, sometimes break out whole classes, "all the while keeping the tests passing." "I don't write them that way to start. I don't think anyone could. First, make it work. Then, make it right" (pp. 183–184).

## Open the PDF when

- You need the full `TestableHtml` before/intermediate/after listings to demonstrate the Similar Code refactoring stepwise (pp. 170–174), or the lambda vs. TemplateMethod versions of the building-scoring Loop Duplication example (pp. 174–176).
- You need the `LineCounter` C++ listing showing OO side-effect hiding in full (pp. 180–181).
- You need the Nassi–Schneiderman quadratic-solver diagram or the exact structured-programming unit definitions (pp. 182–183).
