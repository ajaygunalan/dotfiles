---
chapter: 4
title: Meaningful Names
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch04_Meaningful_Names.pdf
pages: 18
level: cross-cutting
---

# Ch04 — Meaningful Names

**Thesis:** Names are everywhere in software — variables, functions, arguments, classes, packages, files — and because we name so much, we had better do it well. Good naming is not subjective free-for-all: code is written for an audience (the community of people who will work in the codebase), and a system of intention-revealing names can make code understandable without any change to its logic. Choosing good names takes time but saves more than it takes, and names should be revised whenever better ones are found.

## Named principles & rules

- **Use Intention-Revealing Names** — A name should answer all the big questions: why it exists, what it does, how it is used. "If a name requires a comment to communicate to its audience, then the name does not reveal its intent." (p. 72)
- **[Build a System of Names]** (book subsection heading) — Names must supply the context the code implicitly requires; a good *system* of names (`gameBoard`, `getFlaggedCells`, `cell.isFlagged()`) communicates a great deal about the whole application. (p. 73–74)
- **Avoid Disinformation** — Leave no false clues: don't call something `accountList` unless it's actually a `List`; beware names that vary in small ways (`XYZControllerForEfficientHandlingOfStrings` vs `...StorageOfStrings`); "Spelling similar concepts similarly is *information*. Using inconsistent spellings is *disinformation*." Avoid lowercase `l` / uppercase `O` confusable with 1 and 0. (p. 74–75)
- **Make Meaningful Distinctions** — If names must differ, they should mean something different. Number-series naming (`a1, a2, … aN`) is uninformative; noise words (`Info`, `Data`, `ProductInfo` vs `ProductData`, `Customer` vs `CustomerObject`) are meaningless distinctions. (p. 75–76)
- **Use Pronounceable Names** — Humans are wired for words; unpronounceable names (`genymdhms`, `DtaRcrd102`) block the social activity of discussing code. (p. 76–77)
- **Use Searchable Names** — Single letters and raw numeric constants are hard to grep; `MAX_CLASSES_PER_STUDENT` beats `7`. "Longer names trump shorter names, and any searchable name trumps a constant in code." Very short names only inside very short scopes. (p. 77–78)
- **Use Names of Appropriate Length** — with sub-rules (p. 78–80):
  - **Variable Names:** length proportional to the length of the containing scope (loop counter `n` fine for two lines; instance/global names longer).
  - **Function Names:** length *inversely* proportional to scope — global functions short and general (`open`), private methods long and specific.
  - **Class Names:** same inverse rule — global classes short; derived, inner, private classes longer.
  - **Property and Attribute Names:** follow the variable rule (proportional to scope) since they sit on the left of assignments.
  - **Namespace Names:** descriptive and longish; alias length varies with the module that uses the alias.
- **Avoid Encodings** — Don't encode type or scope into names; Hungarian notation (HN) and its ilk are obsolete impediments in modern typed languages (`PhoneNumber phoneString; // name not changed when type changed!`). Includes **Member Prefixes** (no `m_`) and **Interfaces and Implementations** (no `I` prefix; if you must encode, suffix the implementation, e.g. `ShapeFactoryImp`). (p. 80–81)
- **Use Appropriate Parts of Speech** — Classes get noun/noun-phrase names, generally singular (`Customer`, `AddressParser`); a collection class holding many may be plural. Methods get verb/verb-phrase names (`postPayment`, `deletePage`); accessors/mutators/predicates follow local convention (`get`, `set`, `is` per JavaBeans). Overloaded constructors are better exposed via static factory methods that describe arguments (`Complex.FromRealNumber(23.0)`). (p. 81–83)
- **Consider Keyword Parameters** — Where the language allows (Python, C#, Ruby, Clojure), limit positional parameters and use explicit keyword-only parameters for most variations. (p. 82–83)
- **Don't Be Cute** — Choose clarity over entertainment value; no colloquialisms or in-jokes (`HolyHandGrenade`, `whack()`, `eatMyShorts()`). "Say what you mean. Mean what you say." (p. 83)
- **Pick One Word per Concept** — One word for one abstract concept, used consistently (`amount` vs `fee` vs `price` vs `cost` across modules is chaos). Audit and harmonize names per class/module/test suite; a consistent lexicon (a Ubiquitous Language, per DDD) is a boon. (p. 83)
- **Use Solution Domain Names** — Readers are programmers: use CS terms, algorithm names, pattern names, math terms freely in implementation-level code (`AccountVisitor`, `JobQueue`, `FIFO`). (p. 83–84)
- **Use Problem Domain Names** — Code that has more to do with problem-domain concepts should draw names from the problem domain, so a maintainer can at least ask a domain expert. Separating solution- and problem-domain concepts is part of the job. (p. 84)
- **Add Meaningful Context** — Most names aren't meaningful alone; enclose them in well-named classes, functions, or namespaces (`state` alone is ambiguous; inside an `Address` class it isn't). Avoiding classes/structures for too long is the Primitive Obsession smell. (p. 84–86)
- **Don't Add Gratuitous Context** — Don't prefix every class with an application abbreviation (`GSD...`); it fights the IDE and adds redundant or irrelevant characters. Shorter precise names (`Address`, `PostalAddress`, `MAC`, `URI`) beat prefixed ones. (p. 86–87)

## The argument

Naming is audience-directed communication. "As an author of code, your audience is the set of people who will work in your codebase… they collectively will decide what is welcome and what is unwelcome." (p. 72) The author's experience writing the code matters less, and is more transient, than the audience's experience reading it.

The Minesweeper example carries the central claim: renaming alone — no structural change — converts opaque code into obvious code. "Notice that the simplicity of the code has not changed. Only the clarity has improved." (p. 74) A system of names supplies the context that questions like "what is the zeroth subscript?" would otherwise demand.

Finally, naming is iterative: "We rename things. As Josh Kerievsky reminds us, *all good writing is based on revision*." (p. 87) Don't defer renaming out of fear of surprising other developers; the book's authors report being grateful when names change for the better.

## Distilled example

Before (p. 73):

```java
public List<int[]> getThem() {
  List<int[]> list1 = new ArrayList<int[]>();
  for (int[] x : theList)
    if (x[0] == 4)
      list1.add(x);
  return list1;
}
```

After — same operators, constants, nesting; only names changed, then a small `Cell` class added (p. 74):

```java
public List<Cell> getFlaggedCells() {
  List<Cell> flaggedCells = new ArrayList<Cell>();
  for (Cell cell : gameBoard)
    if (cell.isFlagged())
      flaggedCells.add(cell);
  return flaggedCells;
}
```

## Smells & checklist

- Any name that needs a comment to explain it (`int d; // elapsed time in days`).
- Container-type words in names that lie or over-specify (`accountList` that isn't a `List`).
- Near-identical long names differing in the middle; inconsistent spellings of the same concept.
- `l`/`O` used as names; number-series names (`a1, a2`); noise words (`Info`, `Data`, `Object`, `variable`, `table`, `Manager`, `Processor` in class names).
- Unpronounceable abbreviations (`genymdhms`); magic numbers instead of searchable constants.
- Scope-length mismatch: long names in tiny scopes, one-letter names in wide scopes; short vague names on narrowly scoped private functions (should be long and descriptive); tests should have the longest function names of all.
- Encodings: Hungarian notation, `m_` member prefixes, `I` interface prefixes.
- Classes named with verbs, or methods named with nouns (against team convention).
- Same concept named differently across modules (`fetch`/`retrieve`/`get`).
- Bare context-free variables that should live inside a named class/structure (Primitive Obsession).
- Gratuitous application-wide prefixes on every class.

## Trade-offs & exceptions

- Clear beats short, but long doesn't automatically beat short: `getElapsedTimeInDays()` returning into `d` is fine in a small scope (p. 72–73).
- `e` for the caught error in Python/Go `try/catch` is acceptable — familiar convention, tiny scope (p. 77–78).
- The noun-for-return-value convention (`name()` instead of `getName()`): the authors don't prefer it "but we will follow it when working with teams that use it" (p. 82).
- The book concedes real subjectivity: goodness is defined by acceptance of the audience, and every codebase change means restarting the process of learning what that audience finds "weird" or "alien" (p. 87).
- Deliberately bad temporary names are legitimate: the authors "will often call a variable by an intentionally bad name temporarily, until a better name comes to mind" (p. 87).
- Solution-domain vs problem-domain naming is a judgment call — don't force every name to read as English prose; "use the level of abstraction that works best for the algorithm and the audience" (p. 84).

## Process prescriptions

- Rename whenever a better name is found; don't let fear of surprising others stop you (p. 72, 87).
- Periodically audit names for consistency using the IDE's outline/fold view; harmonize all names in a class, module, or test suite (p. 83).
- Consider making constructors private to enforce descriptive static factory methods (p. 82).

## Open the PDF when

- You need the full worked `GuessStatisticsMessage` refactoring showing how a context class enables further decomposition (p. 85–86).
- A team debates language-specific conventions (JavaBeans accessors, keyword parameters, namespace aliases) and wants the exact wording.
