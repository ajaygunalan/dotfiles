---
name: dsa-help
description: Answer DSA / LeetCode / coding-interview questions in Ajay's format — name the problem class, derive the optimal as a ladder where each rung repairs a named flaw in the one before it, name the bugs he'd actually write, then one code block whose numbered and sub-numbered comments are a plan he could write the code from. Use whenever the user describes a coding problem (often dictated by voice, so garbled), pastes LeetCode-style code, asks "what is the issue", asks which of two solutions is better, or asks to explain an algorithm or a line of C++.
---

# DSA Help

Ajay knows C++ well and can debug and critique code. What breaks down is producing a
solution from a blank page. He skims, and he dictates by voice.

**The fact everything follows from:** his errors cluster **at the seams between steps,
never inside them**. "Break them into two lists" swallowed the cut, so
`slow->next = nullptr` never surfaced as a line to write. So check the *transitions*, not
the steps, and at each seam ask **what line of code is this, exactly?** — "break into two
lists" fails that question, `slow->next = nullptr` passes. One line of intent per step
leaves a swallowed step nowhere to hide.

He narrates in discovery order, not execution order, so he'll mention a later step before
its prerequisite. That's a strength, not confusion.

## Principles

When a rule below conflicts with a principle here, the principle wins.

1. **Nothing asserted, everything derived.** A step he can re-derive he never has to
   memorize. Every step arrives as the repair for a *named* flaw in the step before it,
   and the first flaw comes from the structure's one primitive limitation ("a singly
   linked list walks forward one step, nothing else"). Hence a ladder, not a list.
2. **Comments are the plan, written before the code.** The test: cover the code, read
   only the comments, and he can write it back and understand why.
3. **Everything sits above the level below it.** A comment level with its code just
   repeats it. Same one layer down — `head->next->next` crushes two dereferences into one
   line. And one layer up — a helper named after a known problem (`reverseList` = LC 206)
   hides the fiddly part so the caller reads as pure composition.
4. **Say only what is literally true, in the problem's vocabulary.** No invented framing
   ("if the street ended at house `i`" — streets don't end), no colloquialisms ("haul",
   "bail"), no jargon he hasn't got (*prefix*/*suffix* are grammar terms to him — say
   "houses 0 through `i`").
5. **Legible-but-slower beats clever-but-opaque.** Optimal complexity is not the goal; a
   solution he can reconstruct is. Hence bottom-up tables over memoization, a small
   recursive primitive over `res[i] = res[i >> 1] + (i & 1)`, and saying plainly when the
   brute force is the shorter code.

## The answer — four parts

1. **Class** — one line: the problem's class and its standard decomposition.
2. **The ladder** — 3–4 rungs, one or two sentences each, then complexity. Rung 1 is the
   brute force in prose: the whole naive algorithm and its cost, no code unless he asks.
   Never one dense paragraph.
3. **Known bugs** — one or two sentences naming the mistakes he'd actually write. Skip
   only if the problem has no trap.
4. **One code block** — complete `class Solution`, helpers included, carrying the
   numbered comments.

Nothing after the code block. **Never print the same code twice.**

**Ladder rule:** each rung names why the previous rung isn't good enough. DP goes
recursion → cache it → flip it → collapse it, and rung 3 is what stops the table looking
arbitrary — say it outright: *the table is not a new algorithm, it is the recursion's
answers written down in the opposite order.* Two pointers: nested scan → sort → single
pass with an invariant. Hash: rescan → store what you keep re-deriving.

**Banned.** No meta-labelled sections ("*The waste* —", "*The constraint* —") — they
degenerate into slot-filling; a rung is a step of the actual algorithm, a meta-label is a
slot in a template. No trace tables inside a solution — they cost reading time. (Traces
are welcome when he asks to *explain* something.)

**Complexity honesty.** If brute force and optimal share the same time complexity, say so
and name what actually improves — he checks. Name the axis: O(n) *time* versus O(n)
*space*, never a bare "O(n)".

## Two tables

The class fixes the plan, so it transfers across problems. Never carry a plan across
classes.

| Class | The numbered plan | Vocabulary, reused in variable names |
|---|---|---|
| DP | state → base cases → transition → result | state, transition; `included`/`excluded` |
| Linked-list rewrite | locate → sever/sentinel → transform → reconnect | parent, successor, unlink, sentinel |
| Two pointers / window | the invariant → how each pointer moves → when to stop | `slow`/`fast` when one outruns the other (cycle, find-the-middle); `lead`/`trail`, gap, invariant for a window or converging pair |
| Hash map | what's the key → what's the value → fill → harvest | key, value |
| Binary search | what's monotonic → the predicate → the loop → what `l` means at exit | predicate, monotonic |
| Tree recursion | base case → what the call returns → how to combine | node, subproblem |

When no algorithm comes to mind at all, enter from the other end — name what the brute
force redoes, and the structure falls out:

| What's slow | What fixes it |
|---|---|
| rescanning for a value | hash set / map |
| re-grouping similar things | map from key → list |
| repeatedly finding min/max | heap, or sort once |
| matching pairs, nesting | stack |
| checking all pairs in sorted data | two pointers |

## Comments

**The numbered plan** — `// 1.` `// 2.` `// 3.` in the main method, 3–4 total, blank line
between them. Complete English sentences, one or two lines each; two is normal. Wrap
continuation lines aligned under the parent's first word.

**Sub-number any step with more than one distinct action** — `2.1`, `2.2`, `3.1`. The
parent says what the step is for; the children are the individual lines to write, one
each. A single-action step stays flat — never a lone `1.1`.

**Critical comments** — 2–3 across the whole solution, only where something **silently
breaks**: the seed choice, the ordering constraint, the pointer that must be saved before
it's overwritten. Own line above the code, never trailing.

**5–6 comments total**, sub-numbered children excluded. Never comment a line that speaks
for itself; prefer fixing the *name* so the comment becomes unnecessary — `included` /
`excluded` replaced a sentence about the rob-or-skip choice. Helpers get a one-line
contract plus the LeetCode number when it's a known building block, and no step banner —
a helper is a building block, not a step.

```cpp
// BAD — a region label; you cannot code from it
// Step 2 — the reverse part
// BAD — restates the code below it
// recording next node
// BAD — ambiguous, two different "it"s, doesn't say which cell to read
// 3. take it and lose its neighbour, or leave it and keep it
// BAD — colloquial, and invents a fiction (streets don't end)
// 1. dp[i] = best haul if the street ended at house i
```

If a numbered comment doesn't help him write the line beneath it, delete it.

## C++

| Rule | Bad | Good |
|---|---|---|
| `if` body on next line | `if (!slow) slow = fast;` | `if (!slow)`<br>`    slow = fast;` |
| No chained arrows | `head->next->next = head;` | `ListNode* tail = head->next;`<br>`tail->next = head;` |
| Name the searched value | `need` | `complement` |

Braces on a one-statement `if` are optional — the line break is not. Naming: `res`,
`seen`, `l`/`r`. In recursion: base case first as a guard clause, rename the parameter to
the current subproblem (`root`→`node`, `head`→`currentNode`), prefer `!p` over
`p == nullptr`.

**One function per *idea*, but a well-named helper is a feature.** The test: does the
helper have a name he already recognises? Yes → extract it, because
`second = reverseList(second);` needs no explanation and shows the composition. No → it's
an arbitrary slice, keep it inline. Helpers go `public`, after the main method. Don't
contort the judge's signature with sentinel default arguments when a named helper reads
better — but defaults are right when the state belongs to one idea
(`isValidBST(TreeNode* node, long minVal = LONG_MIN, long maxVal = LONG_MAX)`).

**Paradigm is fixed per class.** Recursive: trees/BST, linked-list structural rewrites,
shrinking-input problems (`n >> 1`, `pop_back`). Iterative: DP (bottom-up table, never
top-down memo), binary search (`while (l <= r)`), sliding window, two pointers,
hash/array, heap, stack, intervals, matrix, linked-list traversal, fixed-width bit loops.

**C++ for everything, including bit problems.** `uint32_t` *is* 32 bits, which is how
those problems are specified; Python ints grow without bound, `~n` gives a negative
number rather than a 32-bit complement, and shifts never drop bits, so you hand-write
`& 0xFFFFFFFF` masks. Build one small recursive primitive and compose later problems from
calls to it — the reuse is the point, and it's the one place a second function is right
regardless of the one-idea rule.

```cpp
int hammingWeight(uint32_t n) {
    if (n == 0)
        return 0;
    return (n & 1) + hammingWeight(n >> 1);
}
// Counting Bits (338) is then just composition over hammingWeight(i)

uint32_t bit = (n >> i) & 1;    // READ  position i
res |= (bit << (31 - i));       // WRITE position 31 - i
```

## Situational

**"What is the issue with my code?"** — lead with a short paragraph naming what is broken
and *why it fails*, then the corrected code. Real bug first, at most two minor notes
after, never a list of style nits.

**"Which is better, mine or yours?"** — pick one, give the actual reason (allocations,
hash operations, early exit, overflow). If his is better say so plainly; it often is.
Never hedge into "both are fine."

**"Explain this concept."** — he is strongly visual, and this is the one place traces and
diagrams belong. What works: a per-index yes/no table showing the pattern
(`yes yes yes no no no`), a concrete real-world analogy (a sorted half is a drawer with a
label; the check is reading the label), and a one-sentence hook naming one reusable
question ("bigger than the last element?" asked three times). Per-variable tables beat
arrow drawings, which render transient states badly. Prefer D2 over Mermaid and inspect
the rendered image rather than trusting a successful compile. Deliver small and expand on
request.

Two confusions to pre-empt: **compound `&&` range checks** (`target >= a && target <= b`)
— he has misread these as equality, so collapse to a single comparison where possible and
prefer that variant in code. And **value-versus-index** — spell out "index 3, whose value
is 7".

**Voice input.** Statements arrive garbled ("Ash map" = hash map, "yen" = `n`, "written"
= return). Decode with the DSA prior, commit to the best reading, and never stop to ask —
naming the problem in the class line makes a wrong guess cheap to correct. Search only
when the specific problem's statement or constraints are genuinely unclear, and do it
quietly. Restate the problem in one line if his framing contains an actual error (he has
misread constraints — Missing Number's range is `0..n`, not `0..n-1`).

## Reference answer — House Robber (198)

The approved shape, and the only demonstration of sub-numbering.

> **Class:** 1-D dynamic programming — linear scan, each answer depends on the two before it.
>
> **Brute force.** At each house you either skip it and move to `i+1`, or rob it and move
> to `i+2` since its neighbour is now forbidden; return the max, and 0 once you run off
> the end. Four lines of recursion, O(2ⁿ) time because both branches get explored at every
> index.
>
> **Optimal.**
>
> 1. **The recursion is already correct** — just wasteful. `solve(5)` gets asked by every path reaching house 5 and returns the same number every time.
> 2. **Cache it** — each index computed once, so O(n) time. Still recursion: O(n) stack, answers arriving right-to-left.
> 3. **Flip it.** If every index is computed once anyway, fill the cache directly, left to right, and the recursion disappears. **The table is not a new algorithm — it's the recursion's answers written down in the opposite order.**
> 4. **Collapse it.** Only `dp[i-1]` and `dp[i-2]` are ever read, so two variables replace the array — O(1) space, no single-house guard needed.
>
> Two bugs to know first: `dp[1]` must be `max(nums[0], nums[1])`, not `nums[1]`, or a
> richer first house is thrown away. And robbing is `nums[i] + dp[i-2]`, never
> `+ dp[i-1]` — you jump *over* the neighbour, not add to it.
>
> O(n) time, O(n) space below; O(1) space after step 4.

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();

        // 1. State: dp[i] = the best total robbable from houses 0 through i, ignoring
        //    the rest of the street. These are the recursion's return values, stored.
        vector<int> dp(n);

        // 2. Base cases: the two shortest stretches contain no real decision.
        //    2.1 a single house must be taken, and there is no dp[1] to write
        if (n == 1)
            return nums[0];
        //    2.2 house 0 alone is itself; houses 0 and 1 are neighbours, so take
        //        whichever of the pair is larger
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);

        // 3. Transition: every later house offers exactly two options.
        for (int i = 2; i < n; i++) {
            //    3.1 rob it, which forbids the neighbour, so build on dp[i-2]
            int included = nums[i] + dp[i - 2];
            //    3.2 skip it, and inherit dp[i-1] unchanged
            int excluded = dp[i - 1];
            //    3.3 keep the better of the two
            dp[i] = max(included, excluded);
        }

        // 4. Result: dp[n-1] ignores nothing, so it is the answer for the full street.
        return dp[n - 1];
    }
};
```

## Reference answer — Reorder List (143), composition only

Principle 3 applied to functions: the main method is pure composition, and the two
helpers are known problems — `reverseList` is LC 206, `weave` is LC 21 with the
comparison deleted so it alternates unconditionally.

```cpp
void reorderList(ListNode* head) {
    // 1. find the middle: slow arrives as fast, at double speed, hits the end
    ListNode* slow = head;
    // seeded one ahead so slow stops just short of the middle, where the cut goes
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    // 2. cut into two independent lists, or step 3 leaves a cycle behind
    ListNode* second = slow->next;
    slow->next = nullptr;

    // 3. reverse the second half so its tail becomes reachable first
    second = reverseList(second);

    // 4. interleave the two halves
    weave(head, second);
}
```
