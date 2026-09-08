---
chapter: 6
title: Formatting
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch06_Formatting.pdf
pages: 20
level: surface
---

# Ch06 — Formatting

**Thesis:** Code formatting is about communication, and "communication is the professional developer's first order of business" — more important, in the long run, than getting it working, because the functionality you write today will change, while your style and discipline set precedents that outlive the code itself. Formatting should be governed by a simple, consistently applied set of rules — agreed by the team and ideally enforced by an automated tool — so the codebase reads as one consistent document rather than the work of "a bevy of drunken sailors."

## Named principles & rules

- **The Purpose of Formatting** — "Code formatting is *important*. It is too important to ignore and it is too important to treat religiously." Readability sets precedents affecting maintainability and extensibility long after the original code is gone. (p. 118)
- **Vertical Formatting** — file size: analysis of seven Java projects shows significant systems (FitNesse ~50,000 lines) can be built of files typically 200 lines, upper limit ~500. "Not a hard-and-fast rule, [but] it should be considered very desirable. Small files are usually easier to understand and maintain than large files." (p. 118–119)
- **Vertical Openness between Concepts** — each blank line is a visual cue for a new and separate concept; separate package declaration, imports, and each function with blank lines. Removing them has "a remarkably obscuring effect." (p. 120–121)
- **Vertical Density** — the converse: tightly related lines should appear vertically dense; useless comments between two instance variables break their close association. Code should fit in an "eye-full." (p. 121–122)
- **Vertical Distance** — closely related concepts should be kept vertically close (in the same file unless there is very good reason — one reason `protected` variables should be avoided); vertical separation should measure how important each is to understanding the other. (p. 122)
- **Variable Declarations** — declare variables as close to their usage as possible; with short functions, locals go at the top of the function; loop control variables inside the loop statement; rarely, at the top of a block before a loop in a long function. (p. 122–123)
- **[Instance variable placement]** — instance variables go at the top or bottom of the class, in one well-known place everybody knows; the important thing is a single well-known location, not which one. Includes the C++ **scissors rule** (public at top, privates at bottom); in Java/C# follow the top-of-class convention because it's pervasive. Counterexample: JUnit's `TestSuite` hiding two declarations mid-listing. (p. 123–124)
- **Dependent Functions** — if one function calls another, keep them vertically close, with the caller above the callee where possible (inverted in languages like Clojure); called functions appear in the order they are called, giving the program a natural top-down flow readers can trust. (p. 125–126)
- **[Constants at the appropriate level]** — keep constants where they make sense to know (pass `"FrontPage"` down from `makeResponse` rather than burying it in a low-level function). (p. 126)
- **Conceptual Affinity** — "Certain bits of code want to be near other bits… The stronger that affinity is, the less vertical distance there should be between them." Affinity can come from calling, variable use, or performing variations of the same basic task with a common naming scheme (JUnit's `assertTrue`/`assertFalse` overloads). (p. 126–127)
- **Horizontal Formatting** — line width: across the seven projects, programmers clearly prefer short lines (sizes 20–60 each ~1% of lines; sharp drop-off above 80). "The old Hollerith limit of 80 is a bit arbitrary… lines edging out to 100 or even 120" are OK; beyond that is careless. Rule: "never force your readers to scroll to the right"; the author sets his IDE limit at 120. (p. 127–128)
- **Horizontal Openness and Density** — use horizontal white space to associate strongly related things and disassociate weakly related ones: spaces around assignment operators; no space between a function name and its opening parenthesis; spaces after commas; white space to accentuate operator precedence (`b*b - 4*a*c`). Reformatting tools are blind to precedence, so such subtle spacing tends to be lost. (p. 128–129)
- **Horizontal Alignment** — aligning declaration names or r-values in columns is not useful: it emphasizes the wrong things (you read the column of names without seeing types or operators). Prefer unaligned declarations; if a list is long enough to beg alignment, "the problem is the length of the list, not the lack of alignment" — split the class. (p. 129–130)
- **Indentation** — a source file is a hierarchy of scopes; indent proportionally to position in that hierarchy. Programmers rely heavily on the scheme, visually lining up the left edge to see scope; "Without indentation, programs would be virtually unreadable by humans." (p. 130–132)
- **Breaking Indentation** — resist collapsing scopes to one line for short ifs/whiles/functions; the author almost always goes back and puts the indentation in; though "there are times… when a simple one-liner is more visually appealing than dangling braces" (`public int getCount() {return count;}`). (p. 132)
- **Team Rules** — "Every programmer has their own favorite formatting rules, but if they work in a team, then the team rules." Agree on a single style, encode it in the IDE's formatter, and stick with it — even rules you personally wouldn't prefer. Good source code "read[s] nicely… with a consistent and smooth style," never "a jumble of different individual styles." (p. 132–133)
- **Uncle Bob's Formatting Rules** — the author's own simple rules, illustrated entirely by the `CodeAnalyzer` listing "as an example of how code makes the best coding standard document." (p. 133–135)

## The argument

"When people look under the hood, we want them to be impressed with the neatness, consistency, and attention to detail that they perceive… If instead they see a scrambled mass of code… they are likely to conclude that the same inattention to detail pervades every other aspect of the project." (p. 118)

The deeper claim is about longevity: "The functionality that you create today has a good chance of changing in the next release, but the readability of your code will have a profound effect on all the changes that will ever be made… Your style and discipline survive, even though your code does not." (p. 118) Both file-length and line-width prescriptions are grounded in empirical measurement of seven real projects (JUnit, FitNesse, TestNG, Time and Money, JDepend, Ant, Tomcat) rather than taste alone.

## Distilled example

`BoldWidget` (p. 120–121): the same class shown with blank lines separating package, imports, constants, constructor, and `render()` — and then with every blank line removed. Same code, but the second version "looks like a muddle"; the groupings pop out only when vertical openness is present. "The difference between these two examples is just a bit of vertical openness." The chapter's other pillar example is the unindented-vs-indented `FitNesseServer` pair (p. 131): syntactically and semantically identical; one is "virtually impenetrable without intense study," the other understandable in seconds.

## Smells & checklist

- Files well over ~200 lines (hard ceiling ~500) — consider splitting.
- Missing blank lines between concepts (imports, functions); or blank lines/comments wedged between tightly related lines (e.g. paired instance variables).
- Related concepts split across files without very good reason; `protected` variables enabling such splits.
- Variables declared far from first use; loop counters declared outside the loop; instance variables buried mid-class instead of one well-known place.
- Callee defined far above/below its caller; call order not matching top-down reading order.
- Well-known constants buried in low-level functions.
- Lines forcing horizontal scrolling (author's limit: 120).
- Space between function name and `(`; missing spaces around assignments or after commas; spacing that fights operator precedence.
- Column-aligned declarations/assignments — and the long member lists that motivated them.
- Collapsed scopes (statement on same line as `if`/`while`); indentation not reflecting scope hierarchy.
- Mixed personal styles within one codebase; no formatter-encoded team standard.

## Trade-offs & exceptions

- The 200/500-line file guidance "should not be a hard-and-fast rule" — Tomcat and Ant ship files of several thousand lines; it's about what's *possible* and desirable (p. 119).
- 80 columns is arbitrary; up to 100–120 is fine; the real rule is no rightward scrolling (p. 128).
- Precedence-accentuating spacing is fragile: most reformatting tools destroy it (p. 129).
- Scissors rule vs privates-at-top: the Java/C# convention is "likely better to follow… than to confuse everyone by appealing to logic and common sense" — pervasive convention beats personal logic (p. 123–124).
- Caller-above-callee inverts in languages like Clojure (p. 125, fn. 2).
- One-liners: occasionally more visually appealing than dangling braces (p. 132).
- Team rules trump personal preference — the FitNesse rules "were not the rules that I preferred; they were rules decided by the team," and the author followed them (p. 133).

## Process prescriptions

- Choose a simple set of formatting rules and apply them consistently; on a team, agree a single set and have all members comply (p. 118, 132).
- Encode the agreed rules into the IDE's/an automated code formatter and "stick with them ever since" — the FitNesse team did this in about ten minutes (p. 118, 133).
- Let a well-formatted piece of real code serve as the coding standard document (p. 133).

## Open the PDF when

- You want the file-length and line-width charts of the seven projects to argue limits empirically (p. 119, 127).
- You need the full `CodeAnalyzer` listing as a model standards document (p. 133–135), or the complete `WikiPageResponder` dependent-functions example (p. 125–126).
