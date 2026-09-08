---
name: dr-bell
description: >
  First-principles guide for writing and revising an engineering journal paper from a
  codebase and experiments — turning code, logs, and measured results into an
  argument-driven manuscript. Use whenever the user is drafting or revising any paper
  section (Abstract, Introduction, Methods, Results, Discussion, Conclusion), converting
  implementation details into academic prose, deciding which numbers belong in prose vs a
  table, auditing manuscript claims against source code, handling PI/senior-author review
  feedback, selecting a venue, writing a response-to-reviewers letter, or preparing an
  IEEE-style submission. Trigger even on casual phrasings like "write up the experiment",
  "make this sound academic", "fix the methods section", "the professor commented on the
  draft", or "is this ready to submit".
---

# Dr. Bell — From Code to Journal Paper

Given a codebase and experiment results, produce a journal-quality manuscript. The arc:
what a paper is → what each section does → what earns inclusion → how code becomes
prose → how sentences and math are written → how results are evidenced → how the
process runs → how not to get desk-rejected.

## 1. What a Paper Is

A paper is a machine for reproducing **one idea** in a busy stranger's head. A report
succeeds when the information is complete; a paper succeeds only when the reader
finishes it thinking your thought. Name that single idea in one sentence before writing
anything, and test every sentence, figure, and number against it.

The most common failure when the source material is a codebase: the draft becomes a
build log. Structure must follow **argument** — never chronology, never software flow.
"First the signal is transformed, second it is filtered, third…" is the tell that you
transcribed a pipeline. Methods describes what the system *is* and *why* — a
problem→solution tree ("to make the system do X, we need Y") — never how it was built
or in what order the code runs.

## 2. What Each Section Does

One job per section. Test every passage: does this sentence do *this* section's job?

| Section | Job | Never contains |
|---|---|---|
| Abstract | One paragraph: stakes → gap → "we present" → what was validated → 1–2 headline numbers with dispersion → feasibility close | Citations, equations, footnotes |
| Introduction | Refutable claims the body substantiates; prior-art ladder ending at the gap; hypothesis; contributions as prose ("First, … Second, …"); roadmap | Bulleted contribution lists |
| Methods | What the system is and why, in **dependency order** (the core idea first, supporting modules as things that feed it) — plus setup, protocol, metric definitions, statistical analysis | Runtime/dataflow ordering, build history |
| Results | The evidence chain that makes the reader believe the claim — statements each backed by a figure or table, ordered by importance | Interpretation, protocol, method — zero "which shows that" |
| Discussion | Interpretation: how results fill the Introduction's gap, quantified comparison to prior art, honest limits woven into prose | Re-narrated Results, a second conclusion |
| Conclusion | Significance one level up (~half a page or less) | A summary, headline numbers |

The single highest-leverage restructure of a code-derived draft is evicting every "how
we ran it" sentence from Results into Methods. Expect Results to lose half its words
and improve.

Write the abstract **after** the body, and the title after the abstract — they are
matchmaking, not selling: get the right readers in, the wrong readers out. Draft the
abstract with literal subheadings (Background / Aim / Approach / Results / Conclusions,
1–2 sentences each), then delete the subheadings and smooth into one paragraph. The
abstract describes the work, not the paper: no "in this paper", "is discussed",
"novel". The title states the aim, not the result, as specific as the full scope
allows. A useful drafting order for the whole paper: Methods → Results → Introduction →
Discussion + Conclusion → Abstract → Title.

## 3. What Earns Inclusion

**A number earns prose only when it carries an argument.** "Measurements arrive far
slower than the system acts, so an estimator bridges the gap" is argument; a solver's
iteration cap is inventory. This is a scientific paper, not a technician's reference
note — most top-venue papers report **zero** numeric tuning constants. Triage every
constant:

1. **Nowhere (the default)** — tuning values of supporting components: filter
   coefficients, gains, solver settings, thresholds, retry counts, plus all plumbing
   (inter-process wiring, logging, failure fallbacks, unused modes). Name the
   component and move on: "the signal was smoothed with an exponential moving average
   filter" — no coefficient. One sentence of physical reasoning beats five constants.
2. **Prose, when the number is an argument or an experimental condition** — a rate
   mismatch that forces a design choice; a target value the experiment measures
   against. Setup-specific values carry a scope disclaimer ("selected empirically for
   this apparatus, not a general limit").
3. **A settings table, only if the target venue's corpus demands one.** Check how
   comparable papers handle it; if they publish no constants, publish none.

Supporting components that are not the contribution (an estimator, a numerical solver,
an off-the-shelf model) get exactly: named in one sentence, one physical-reason
sentence for why they exist, tuning symbolic or omitted. Reproducibility detail is
owed to roughly 3 readers in 100 — a code/data release serves them better than
constants in the text, and their needs must never set the paper's tone.

**No defensive completeness.** Anything that exists only to preempt an unasked
question — unused capabilities, assert-retract pairs ("inspired by X … but not
formally X"), signpost sentences ("X is described in Section Y"), facts stated twice —
reads as anxiety, not rigor. Delete it, and the citations that only supported it.

**Claims sized to evidence:**
- Check **every** claim against the source code before writing or defending it. The
  source file, not memory, is the authority. "Hard"/"exact" is false if the code
  applies a tolerance or penalty; "guarantees"/"bounds" is false if the data shows
  exceedances — write "reduces X when it exceeds a threshold".
- If experiments isolated subsystems separately, the paper cannot say "validated the
  integrated system" or "simultaneously" — say "each study isolating one component".
- Never soften a number; only soften the sentence that reaches past it ("expected to
  transfer" → "a necessary step toward — though not a substitute for — validation
  on…").
- "We built X" is not a contribution. Use achievement verbs; the contribution is the
  idea the artifact demonstrates.
- Volunteer your weakest definition where the reader would first be misled (in
  Methods, in place), not buried in Limitations.
- Reframe limitation as capability-vs-validation where true: "the method is not
  restricted to the validated case; validation was bounded by the apparatus." Never
  tell the reader what the lab lacked ("a second stage was not available" → "would
  require only an additional stage").

## 4. How Code Becomes Prose

Never put code identifiers, SDK calls, or config keys in prose. Patterns:

- **A mode/config flag** becomes a named method **only** when it is an experimental
  variable (two compared modes → two named methods and table columns). Every other
  branch in the codebase disappears.
- **A library with literature presence** is citable by role ("a real-time
  device-interface library [n]"); a raw API call is not.
- **An estimator/filter/model**: named with its governing assumption in one sentence;
  coefficients never in prose.
- **A multi-step processing function**: one sentence with the operations as a list
  ("transformed to the common frame, filtered to reject noise, bias-compensated");
  steps that do not affect the claim vanish.
- **A solver option** survives only if a claim depends on it (a time cap certifies
  "real-time"); the rest die.
- **A sign/axis convention** is translated to meaning ("positive in compression"),
  never left as array code.
- **A constraint or penalty**: the expression in display math + one plain-language
  sentence saying what it permits and forbids.
- **A mutable state flag with hysteresis**: a cased equation with explicit
  previous-step state and initial condition, glossed "(i.e., …)" at first use.
- **A state machine**: a table (State | Entered when | Action), small caps — no
  pseudocode or algorithm environments in experimental-systems venues.
- **A pretrained model's thresholds** become qualitative adjectives ("set deliberately
  low so every plausible candidate reached the selection stage").
- **Rate/timing constants** appear as premises, not specs ("the processing rate
  exceeds the measurement rate by an order of magnitude; therefore most cycles execute
  without a new measurement").
- **Plumbing** (ports, queues, processes, logging, retries, watchdogs): entirely
  absent — one named module, one arrow in the block diagram. Parity across
  environments ("the same implementation ran unchanged in simulation and deployment")
  earns one sentence only because it certifies the validated system is the described
  one.
- **The code's actual formula wins** over the tidy formula you wish you had
  implemented. Record deliberate omissions as decisions (a comment in the source),
  or later passes will "helpfully" re-add them.

**The claim-vs-code audit (a dedicated pass):** for every claim, find the implementing
code and reconcile. Trace every reported threshold through the actual unit conversion
in the code — report the *implemented* value, not the intended one. Counts (dimensions,
degrees of freedom) must be counted, not asserted. Record each reconciliation as a
source comment adjacent to the changed claim (old claim → new claim → the code fact
that forced it) — comments travel with the text; do not rely on commit messages.

**Provenance:** keep a map of which run/dataset produced which reported number and
which figure; every reported statistic must reproduce from committed code + raw data;
track which config constant was in force when each dataset was recorded. If trials
ended at an arbitrary timeout, do not present it as a design choice AND ban
criterion-implying words ("converged", "settled") paper-wide.

## 5. How Sentences and Math Are Written

**Prose:**
- First-person plural; no contractions; active voice for claims, passive acceptable
  for procedure.
- One term per concept, defined before first use, repeated verbatim — never varied for
  elegance. One home per concept; other sections cross-reference. Grep every
  ambiguous term, count its senses, assign one sense per term.
- One idea per sentence (no prose semicolons — full stops); one job per paragraph; no
  single-sentence paragraphs.
- Kill ambiguous pronouns: where the referent crosses a clause boundary, repeat the
  noun.
- Parentheses only when load-bearing: vendor/model specs, acronyms, cross-refs,
  compact numeric specs, "(i.e., …)" gloss at first use of jargon (~one per
  subsection).
- No compound adjectives coined for compression ("CAD-derived" → "from the CAD model
  of the device"). No invented vocabulary; no jargon imported from adjacent fields.
- Vocabulary follows your group's own published papers; style follows the field —
  mine 3–5 exemplar papers in the target venue for their verbs and rhythm.
- Delete on sight: signposts, assert-retract pairs, "Two observations follow.
  First…", excuses about what the lab lacked.

**Math:**
- Derivation order, not solver order: phenomenon → prose statement of the requirement
  → error/objective definition → constraint or update law → the optimization. Put the
  model in the section title, not the machinery ("Formulation of X", not "X via
  [solver]").
- Every symbol defined at first use in a "where"-list following the display, same
  order as the expression. Define functionally ("the matrix relating the inputs to
  the rate of change of X"), never structurally ("the top three rows of M").
- One symbol per concept; no dead symbols. If a reader cannot parse a symbol, suspect
  the model, not the notation — opaque compound symbols hide unrelated jobs and wrong
  dimension counts.
- Promote an expression to a numbered equation only when the argument reads it;
  demote the rest to prose. Slack in the cost, constraint right-hand side clean.
- Present tense with the field's fixed verbs for what math does ("is given by",
  "yields", "enters the cost"); past for what was done. Equation punctuation: period
  at sentence end, comma before "where". After a large display, term-by-term
  exegesis in equation order. Non-obvious structure earns exactly one causal chain;
  obvious structure earns none.

**Phrasing patterns** (from the [Academic Phrasebank](https://www.phrasebank.manchester.ac.uk/)):
- Gap, graded by claim strength — absence ("no previous study has…") > scarcity ("few
  studies have…") > weakness-in-method ("such approaches fail to address…", best for
  engineering) > open mechanism ("the extent to which X affects Y remains unclear").
  Pick the weakest form the facts support.
- Results: location then highlight ("Table I shows… What stands out is…"). Null
  results stated plainly, never softened.
- Comparison: factual, never adversarial ("these results are consistent with [n]";
  "in contrast to earlier findings, no evidence of X was detected").
- **The hedging ladder** — match the rung to the evidence, never climb higher, never
  hedge a measured result: assertion ("X reduces Y") → near-certainty ("will almost
  certainly") → probability ("is likely") → possibility ("may") → distancing ("it has
  been reported that") → appearance ("appears to"). Scope controls are orthogonal:
  most/many/some, often/generally/occasionally.
- Limitations: state the bound, its consequence, then stop — no apology.
  "Notwithstanding these limitations, the study suggests…" couples limitation to
  contribution.
- Tense: dated single study → past; body of recent work / state of the field →
  present perfect; what this paper or a figure does → present; aims, methods, results
  → past; interpretation and established facts → present.

## 6. How Results Are Evidenced

- **Survey 5–10 papers of the same experiment type and N in the target venue before
  designing figures or choosing statistics** — conventions are an empirical question,
  not taste.
- Default headline for small-N accuracy experiments: aggregate absolute error,
  mean ± SD. No batch/direction splits unless the split *is* the finding; no
  convergence bookkeeping ("8 of 10 trials converged") unless the field reports it.
- Two levels of summary, each with its stated reason: dispersion (mean ± SD) and
  inference (paired difference with 95% CI). Paired designs use paired tests;
  multiple metrics get a multiplicity correction. p-values once in text, never per
  table row.
- Quantify comparisons ("a 32% reduction", "4.2× lower"), never "better". Every
  printed percentage must be reproducible from the printed numbers.
- **Figures**: identify the figure's single message before drawing it; never trust
  software defaults; colormap follows data type (sequential/diverging/qualitative);
  markers must survive grayscale. The overview figure is a diagram, not a photo —
  draft it before Methods; if it doesn't sketch cleanly, the story isn't ready.
  Block diagrams linear left-to-right (feedback through the world implicit),
  all-black unlabeled arrows. Methods needs conceptual figures (notation conventions,
  problem geometry) — a code-derived draft will have none; create them. Derivations
  belong in equations, setups in annotated photos; one representative photo per
  experiment; video covers time sequences.
- **Captions**: self-contained, never opening with "A/An/The" or a bare label;
  decode every visual element; carry the reading convention ("mean ± SD, N=10 paired
  trials per condition"); no protocol, no statistics methodology. Multi-panel: empty
  subcaptions, all description in the parent as "(a) … (b) …".
- **Tables**: booktabs only, no vertical rules, no "Notes" column; units in the
  header or Description column; a settings table (if the venue demands one) is a
  symbol dictionary: Symbol | Description | Value.
- **Deduplication sweep once per revision**: one home per fact — hunt sentences
  appearing in two sections, values repeated where a table has them, a Discussion
  paragraph that is a second Conclusion.

## 7. How the Process Runs

- **Write a scope anchor before the manuscript**: the one idea in one sentence,
  per-item done/future status, an explicit out-of-scope list, contributions,
  validations mapped to Results subsections. Verify each claimed contribution's entry
  points actually run in the codebase — a defined-but-never-called function is not a
  contribution. A claim that doesn't fit the anchor doesn't enter the paper.
- **Venue selection is a written comparison** decided by the senior author: per
  candidate — impact, timeline, cost, page limit, special requirements, and *fit
  evidence* (DOIs of published papers at your validation maturity), plus an
  "evaluated and excluded" table with one-line reasons.
- **Budget 4–6 review cycles with the senior author.** Make the diff legible:
  highlight every changed span (only the changed words); approval = the highlight
  comes off; one comment at a time — show text → objection → proposal → explicit OK →
  apply → rebuild → next. Lock approved sections to a commit hash; log every retained
  deviation with its reason. Adopt their wording verbatim, sweep for instances they
  missed — but verify their technical corrections against the code. Keep the record
  in the text as adjacent comments (uncertain rewrites marked "DRAFT — pending author
  review"), not in commit messages. After each pass, audit the untouched neighborhood
  of every change for coherence; track which sections have actually been reviewed.
- **What senior authors actually fix** (calibrate self-review to this): protocol out
  of Results, superlatives and transfer claims hedged while measurements stay
  untouched, definitions demanded before use, one term per concept enforced.
- **An AI review is not a review.** Use AI for the claim-vs-code audit and the
  mechanical checklist — it excels there. Never let it set the register, the hedging
  level, or "reviewer demands" for more implementation detail. Never justify content
  with "the reviewer asked for it" unless a human reviewer exists.
- **Response to reviewers**: interleave the complete reviews with responses; begin
  each reply with a direct yes/no; quote the changed text with its location; every
  comment gets a definite action; default to doing what the reviewer asks; accept
  blame for misunderstandings; never defensive. If a review angered you, write the
  venting draft, discard it, write the real one days later.

## 8. How Not to Get Desk-Rejected

70–80% of submissions die at editor triage, usually tripping several causes at once:
ignoring the journal's instructions, excessive length, poor English, scope mismatch,
thin literature review, missing paperwork. A formatting-and-completeness pass against
the *specific journal's* instructions is a mandatory step of its own.

IEEE-family mechanics (verify against the venue's own style manual): abstract single
paragraph with no citations; Index Terms alphabetized; "Fig." always abbreviated;
citations as grammatical objects ("in [1]", never "in reference [1]"); "[1, Fig. 2]"
not "Fig. 2 of [1]"; numerals for 10+; equations end with period or comma-before-
"where"; en dash for ranges but "from 5 to 50"; captions never start with "A/An/The";
table captions take no terminal period; figures cited in numerical order; serial
comma; that/which distinction; supplementary video cited inline at the claim it
supports; AI-generated content disclosed in the Acknowledgment (current IEEE policy);
compile with the venue's engine — its build is the authority on page count.

Final checklist: strip review-only markup and highlight packages; grep for TODO/
leftover code identifiers; every number reproduces from committed code; captions
self-contained; floats in citation order, none after the Conclusion; DOIs verified;
vector figures (PDF/EPS — never SVG/JPEG) with fonts embedded; page limit met.

## 9. Sources

| Source | Core lesson |
|---|---|
| [Gopen & Swan, *The Science of Scientific Writing*](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) | Reader expectations; no interpretation inside Results |
| [Peyton Jones, *How to Write a Great Research Paper*](https://simon.peytonjones.org/great-research-paper/) | One "ping" per paper; details are 5 pages for 3 readers |
| [Whitesides, *Writing a Paper*](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adma.200400767) | Order by importance; Conclusion is higher-level analysis, not summary |
| [Tellex / Brown H2R, *Writing a Technical Paper*](https://h2r.cs.brown.edu/writing-a-technical-paper/) | Problem→solution tree; no material before its motivation |
| [Shaw, *Writing Good SE Research Papers*](https://www.cs.cmu.edu/~Compose/shaw-icse03.pdf) | "We built X" is not a contribution |
| [Mensh & Kording, *Ten Simple Rules for Structuring Papers*](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005619) | Results as an evidence chain |
| [Morley, *Academic Phrasebank*](https://www.phrasebank.manchester.ac.uk/) | Sentence patterns by rhetorical function; hedging taxonomy |
| [Noble, *Ten Simple Rules for Writing a Response to Reviewers*](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005730) | Rebuttal structure and register |
| [Rougier et al., *Ten Simple Rules for Better Figures*](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833) | Message-first figure design |
| [Mack, *Title, Abstract, and Keywords*](https://www.lithoguru.com/scientist/litho_papers/JM3%20editorial%202012%20q2_Title%20and%20Abstract.pdf) | Matchmaking framing; structured-abstract procedure |
| [Jawaid & Jawaid, *Desk-rejection causes*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6408665/) | 70–80% die at triage, on multiple causes at once |
| [IEEE Editorial Style Manual for Authors](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf) | Authoritative IEEE mechanics |
