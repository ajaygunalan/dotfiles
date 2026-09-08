---
chapter: 17
title: AIs, LLMs, and God Knows What
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch17_AIs_LLMs_and_God_Knows_What.pdf
pages: 12
level: process, cross-cutting
---

# Ch17 — AIs, LLMs, and God Knows What

**Thesis:** AI is not the end of programming; it is the next rung in the same ladder of abstraction that runs from Grace Hopper's paper-tape holes through FORTRAN to Clojure — and like every rung before it, it will grow the profession, not kill it. But "programming by prompt" is in its infancy: natural-language prompts are ambiguous, and LLMs are statistical, not inferential — they do not reason. What's needed is a precise, formal prompt language whose statements are *overloaded* — intent stated at least two ways (formal definitions plus testable scenarios) — so errors in one statement are caught by the other. Programmers become the ones who reason: "the lawyers of AI."

## Named principles & rules

- **Automatic programming** — Hopper's own name for generating machine codes from a more abstract textual representation ("add 10, 12"); the first step on the abstraction ladder AI now continues (p. 318).
- [The abstraction-ladder argument] — every language transition (machine code → FORTRAN → C → C++ → Java/C# → Ruby/Python → Clojure) raised abstraction, was met with predictions of programming's doom, and instead *increased* projects and demand. FORTRAN was a 45× productivity leap over machine code; each later leap was smaller. AI is "just another increase in the level of abstraction of our languages" (pp. 318–319).
- **Programming by Prompt** — the current, unrefined practice of writing programs via natural-language prompts; "we are just now barely able to bumble and stumble our way to write programs with prompts. We have no idea how to do it well" (p. 319).
- **Infancy** — the diagnosis of the current problems: programming large systems by prompt will need AI tools that allow *incremental changes* and ways to *eliminate ambiguity* in prompts — "a formalism—a prompt language that is unambiguous and precise and that cannot be misinterpreted by the statistical and fuzzy nature of the LLM algorithm" (p. 324).
- **Overloading** — "When you say something in two different ways, you are overloading the concept you are trying to communicate. Such overloading is a way to ensure that any error in either of the two statements will be detected by the other. We error-prone humans absolutely require overloading." It is the strategy behind double-entry bookkeeping and the testing disciplines of earlier chapters (p. 324). To ensure precise statements match intent, "we should state our intent in at least two different ways."
- **A SWAG (Scientific Wild-Axx Guess)** — Martin's proposal: a prompt language containing formal definitions and constraints, overloaded by a set of **BDD-style Given-When-Then scenarios** (with an [RSpec] footnote); his example spec "looks like COBOL. That similarity might give us pause" (pp. 324–325).
- [Programmers as the lawyers of AI] — the closing claim: LLMs will handle long formal specifications, programmers will design formal, overloaded specification languages and "provide the ability to reason that the AIs lack… responsible (as we always have been) to reason through and draw up the precise and accurate formal requirements and contracts for the applications our clients need" (p. 328).
- [LLMs do not reason] — "LLMs are statistical in nature; they create their responses through probability and not inference… Inference is the primary operation of reason. If LLMs do not actively infer, then LLMs do not reason!" (p. 328).

## The argument

The historical pattern defuses the panic: "at every stage, there were those who predicted the end of programming… And every time, those fears and predictions were the exact opposite of the actual outcomes" (pp. 318–319). AI is a transition like Java or the Web — several years of stumbling before the rudiments are worked out.

The technical core is prompt fragility. A casual prompt is riddled with undefined terms (What is a *sentence*? A *word*? What does "the found word" mean?). Grok produced working-ish code, but Martin is "not terrified by the power of the AI to generate code. I am terrified by the structure of that horrible prompt" (p. 321). Patching a prompt patches symptoms; worse, "with each new change to the prompt, Grok *regenerates* the program from scratch as opposed to modifying the existing program" (p. 322) — with no guarantee the regeneration preserves prior interpretations, "given the statistical and fuzzy nature of the LLM algorithms, there's a good chance it won't!"

Even overloaded formality is not yet sufficient: Grok generated code and tests from the same overloaded spec, and the tests failed — "The fact that Grok wrote the tests and yet could not use them to infer the desired behavior exposes the limitation of the LLM approach" (p. 328). Yet the direction is settled: "without overloaded formality, the prospect of using AIs to write our systems is doomed to spectacular failure. After all, programming is formal, and humans require overloading" (p. 328).

## Distilled example

The Markov/sentence-walk experiment with Grok 3 beta, March 2025 (pp. 319–328).

- Prompt v1 (casual English: find sentences containing a substring, pick one at random, walk to the next word, repeat) → plausible Clojure that "works—after a fashion" but makes "lots of dumb little mistakes" (double spaces, ambiguous terms).
- Prompt v2 (added "Make sure all accumulated words are separated by just one space.") → a *regenerated* program "look[ing] like [it was] written by two different programmers" that fixed double spaces but broke sentence-ending and case handling.
- Prompt v3 (the SWAG formalism: `Language:`, `Name:`, `Command line arguments:`, `Definitions:` (Word, Sentence), `Constraints:` (ignore case), `Description:`, plus Given-When-Then scenarios to be tested with speclj) → clean code *and* generated tests — but the tests do not pass; Grok ignored its own definition of "word" and the case-insensitivity constraint. "That should drive home just how important it is to overload a prompt with testing scenarios!" (p. 327).

## Smells & checklist

- Prompts with undefined domain terms (what exactly is a "word," a "sentence," a "record"?) — demand definitions and constraints.
- Intent stated only once — no overloading; require formal statement + independent scenarios/tests that can catch each other's errors.
- Iterating on a prompt to patch symptoms without understanding the cause of the misbehavior.
- Relying on whole-program regeneration for each change with no independent verification that prior behavior survived.
- Trusting AI-generated tests (or code) without running them and reconciling failures — the AI cannot be assumed to infer intent from its own artifacts.
- Treating AI output as production-ready: Grok's first result "was by no means ready for production" (p. 321).
- Assuming the LLM reasoned about the spec: it predicted, it did not infer.

## Trade-offs & exceptions

- Martin is explicitly impressed as well as terrified: "It is easy to be impressed by this. I certainly am" (p. 321). The critique targets the medium (ambiguous prompts, statistical generation), not the capability.
- The whole chapter is provisional — a self-labeled SWAG about a technology in its infancy; he expects LLMs to improve until "long, formal specifications will be within their grasp" (p. 328).
- His own formalism failed its first trial (generated tests didn't pass), which he concedes "is not encouraging" (p. 328) — the proposal is direction, not doctrine.
- The COBOL resemblance of the formal prompt language "might give us pause" (p. 325) — formal prompt languages risk reinventing programming languages.

## Process prescriptions

When using AI to generate code: state intent in at least two different ways — formal definitions + constraints, overloaded with BDD-style Given-When-Then scenarios — and have "a way to quickly verify their consistency" (p. 324); run the scenarios as tests against the generated code and reconcile every failure yourself, because the reasoning is your job, not the LLM's (pp. 324–328).

## Open the PDF when

- You want the full three-stage Grok experiment with all Clojure listings and the failing speclj output (pp. 319–327).
- You need the complete SWAG prompt-language example verbatim (p. 325).
- You're quoting the productivity-leap history (45× FORTRAN figure and successors) with its exact numbers (p. 318).
