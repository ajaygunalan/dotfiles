---
chapter: 2
title: Clean That Code!
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch02_Clean_That_Code.pdf
pages: 24
level: function | class | process
---

# Ch02 — Clean That Code!

**Thesis:** "Clean" is a verb, not an adjective: nobody writes clean code, because functionality and cleanliness are competing orthogonal concerns our minds cannot balance at once. So we first make it work — making a mess in the process — and then clean that mess in a sequence of small, test-protected improvements. The chapter demonstrates this end-to-end on a Roman-numeral converter, including honest retrospective doubts ("Future Bob") and an AI postscript: LLMs can help, but the programmer remains the final arbiter and must keep the skill of cleaning alive to judge the machine's output.

## Named principles & rules

- **[Clean as a verb]** — "This is a chapter and a book about cleaning code. One does not simply write clean code. To create code that is clean one must clean it" (p. 19). Cleanliness and functionality are "competing orthogonal concerns" our limited minds can't pursue simultaneously (p. 20).
- **Kent Beck's law** — *First, make it work. Then, make it right.* Making it work takes all our cognitive energy; only afterward can we pull back and improve (p. 20; conclusion restated p. 37: "First, I made it work. Then, I made it right—or at least better").
- **The Cleaning Process** — the chapter's named procedure: "just a matter of making smallish improvements while keeping all the tests passing" — one simple change after the next, "pretty much the procedure that Martin Fowler recommends in his wonderful book, *Refactoring*" (pp. 30, 37).
- **[Cleaning is the ultimate second look]** — during cleaning Martin found one or two bugs "simply through the effort of organizing my thoughts"; like a pilot's walk-around after the close-up preflight, things obvious from a distance are invisible during closer inspection (p. 24, fn. 2).
- **Future Bob** — recurring retrospective boxes in which Martin rereads his own code months later; institutionalizes the "look after a few months can be both humbling and profitable" discipline (pp. 22, 26–27, 30).
- **[Understanding bias]** (the Ousterhout debate) — "your own understanding of what you are cleaning will work against your ability to communicate with the next person," whether via extracted method names or comments; e.g., `addValueConsideringPrefix` made sense only while he understood the algorithm (p. 27).
- **[Anti-cleverness rule of thumb]** — "if you think something is clever and sophisticated, beware—it is probably self-indulgence" (p. 34, fn. 7, quoting [DOET]); this condemned the "49FNGO" digraph-replacement trick.
- **[Team standard of cleanliness]** — there is no single standard for cleanliness; develop your own and apply it with discipline; a team "should have a single standard of cleanliness that is negotiated, and then followed and supported, by all members" (p. 28). Fn. 5: the document that represents the standard should be *the code itself*.
- **[Objects as communication scopes]** — "one good use for an object is to allow the helper functions that operate within the execution of a pure function to easily communicate through the instance variables of the object" — answering the functional-purity objection (p. 28).
- **[Oversee the autopilot]** — an LLM "can vastly reduce the workload. But under no circumstances should it be implicitly trusted"; the programmer is "the final arbiter of the code that gets produced," and must stay in practice to competently oversee the automation (p. 40).

## The argument

Code "does not pour from your mind and out through your fingers in a clean state. That's not the way our brains work" (pp. 19–20). Like essays and drawings, programs are produced ugly and then massaged. Martin proves it on himself: his Copilot-assisted first draft of a Roman-numeral converter (Listing 2-1) is a working horror; cleaning it took "roughly equal" time to writing it and surfaced latent bugs and missing tests (pp. 24, 28).

The chapter is deliberately self-critical. Future Bob finds the cleaned version choppy — "I am annoyed because I already understand it and find the chopped-up functions and the instance variables redundant" — yet still concludes "the cleaner version is better… ask yourself which of these two pieces of code you would rather have read *first*. Which tells you more about the intent?" (pp. 26–27).

The postscript feeds the cleaned code to Grok3, which produces a tighter regex-based version; Martin approves it but insists the human must do enough of the work to judge the machine: "no pilot should ever fly without possessing the necessary flying skills that they continuously maintain and refine. So it is with us" (p. 40).

## Distilled example

**Before** (Listing 2-1, pp. 21–22): one giant static `convert(String roman)` — a wall of `contains()` checks for illegal patterns, ad hoc digraph replacement mapping "IV"→"4", "CM"→"O" (the "49FNGO" trick), a switch translating letters and fake letters to values, an ordering check, then a sum.

**After** (pp. 24–26): a small class whose public `convert` delegates to an instance: `doConversion()` reads as a table of contents — `checkInitialSyntax(); convertLettersToNumbers(); checkNumbersInDecreasingOrder(); return numbers.stream().reduce(0, Integer::sum);` — with short, well-named helpers communicating through instance variables, functions listed in the order they are called, digraph trick gone. "You can read the code from the top to the bottom and it reads rather like a story" (p. 26). Intermediate steps (pp. 31–36) show the path: extract low-hanging functions, dislike argument-passing, introduce the object, remove the clever digraphs one at a time — tests green throughout.

## Smells & checklist

- Was the "make it right" pass performed at all, or did working code ship as-is?
- Long function readable only as a wall? Extract until the top-level function reads as a story, functions listed in call order.
- Helper functions passing the same arguments around? Consider an object whose instance variables let them communicate.
- Anything you're proud of for being clever (encoded tricks like 49FNGO)? Probably self-indulgence — replace with the straightforward form.
- Names that only make sense to someone who already understands the algorithm (understanding bias)? Rename for the first-time reader.
- Ad hoc test suites: look for patterns in test data, reorganize, and hunt missing cases — Martin's initial tests "were inadequate" (p. 28).
- AI-generated code accepted without the author cleaning and evaluating it themselves?
- Cleanup done in big leaps rather than smallish always-green steps?

## Trade-offs & exceptions

- **The cleaned code is longer** — conceded; "most of that extra length is due to the nicely named functions that explain what's going on" (p. 27).
- **Object creation costs** — allocating and garbage-collecting, plus call overhead of small methods: for embedded real-time, high-performance simulators, or games "this decision could seem insane"; Martin trades speed for clarity "within reason" because he doesn't need the speed (pp. 27–28).
- **Over-decomposition has a floor** — `convertLettersToNumbers` is "a bit longer than I like; but it hangs together pretty well," and decomposing it further "would be more obscuring than helpful" (p. 27).
- **Choppiness is real** — Future Bob found the scrolling to check instance-variable types annoying; extraction helps the first reader more than the already-informed reader (pp. 26–27).
- **Cleanliness is negotiated, not absolute** — "There is no single standard… This is mine, and mine may not be yours" (p. 28).
- **LLMs genuinely help** — Grok3's version "reduces things to the bare essence" (p. 39) — but its tests over-relied on the regex and missed cases like "IM"; help must be verified (p. 40).

## Process prescriptions

1. Make it work first (throw ideas away freely — Martin discarded a state-machine attempt, p. 31), with tests.
2. Then clean: find low-hanging fruit, extract and name functions, one simple change after the next, keeping all the tests passing (the Fowler *Refactoring* procedure, pp. 32, 37).
3. Improve the tests as part of cleaning — organize test data, add missing cases (pp. 28, 37).
4. Revisit code months later (Future Bob) to audit your naming against understanding bias.
5. When using an AI: still write and clean enough yourself to competently judge its output (p. 40).

## Open the PDF when

- You need the full listings of any intermediate cleaning stage (Listings on pp. 21–26, 31–36) or the Grok3 version (pp. 37–39).
- You want the complete Future Bob commentaries or the Ousterhout debate reference (p. 27; full debate in the book's appendix).
- You need the complete final test suite as a model of test reorganization (pp. 28–30).
