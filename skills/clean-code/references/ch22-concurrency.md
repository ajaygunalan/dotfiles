---
chapter: 22
title: Concurrency
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch22_Concurrency.pdf
pages: 20
level: cross-cutting | class | tests
---

# Ch22 — Concurrency

**Thesis:** Writing clean concurrent programs is very hard: code that looks fine on the surface can be broken at a deeper level and only fail under stress. Concurrency is a *decoupling strategy* — it decouples *what* gets done from *when* it gets done — which can improve both throughput and structure, but it demands its own defense principles: separate thread-aware code from thread-ignorant code, severely limit shared data, know your library and execution models, and test relentlessly in many configurations because concurrency bugs hide as unrepeatable "one-offs." (Chapter by Brett L. Schuchert; a Future Bob note says everything in it applies equally to services and microservices, p. 424.)

## Named principles & rules

- **[Concurrency as a decoupling strategy]** — Concurrency decouples *what* gets done from *when* it gets done; structurally the application looks like many little collaborating computers rather than one big main loop (p. 424).
- **Myths and Misconceptions** — three named myths: *Concurrency always improves performance* (only sometimes, when there is shareable wait time); *Design does not change when writing concurrent programs* (it can change remarkably); *Understanding concurrency issues is not important when working with a Web server* (you'd better know what your server is doing) (p. 425). Balanced sound bites: concurrency incurs overhead, is complex even for simple problems, its bugs aren't usually repeatable (so are dismissed as one-offs), and it often requires a fundamental change in design strategy (pp. 425–426).
- **Concurrency Defense Principles** — the chapter's umbrella name for its series of principles and techniques for defending systems from the problems of concurrent code (p. 427). They are:
- **Single Responsibility Principle (SRP)** — concurrency design is complex enough to be a reason to change in its own right; keep your concurrency-related code separate from other code (p. 427).
- **Corollary: Limit the Scope of Data** — restrict the number of critical sections; take data encapsulation to heart and severely limit the access of any data that may be shared (p. 427).
- **Corollary: Use Copies of Data** — avoid sharing by copying objects and treating them as read-only, or merging results from copies in a single thread; savings from avoiding locks usually repay the creation/GC overhead (p. 428).
- **Corollary: Threads Should Be as Independent as Possible** — write threaded code so each thread exists in its own world, sharing no data; partition data into independent subsets operable by independent threads (p. 428).
- **Know Your Language and Library** — use provided thread-safe collections, threading frameworks (e.g., `Executor`), nonblocking solutions where possible; know which library modules are and are not thread safe (pp. 428–429). In Java: `java.util.concurrent` (start with `ConcurrentHashMap`), `ReentrantLock`, `Semaphore`, `CountDownLatch` (p. 429).
- **Know Your Execution Models** — basic definitions: **Bound resources**, **Mutual exclusion**, **Starvation**, **Deadlock**, **Livelock** (pp. 429–430); and the three fundamental models: **Producer-Consumer** (p. 430), **Readers-Writers** (p. 430), **Dining Philosophers** (p. 431). Most concurrent problems are variations of these three — study and practice them (p. 431).
- **Beware Dependencies Between Synchronized Methods** — avoid using more than one method on a shared object; when you must, make it correct via **client-based locking**, **server-based locking**, or an **adapted server** (p. 431).
- **Keep Synchronized Sections Small** — locks create delays and overhead; guard critical sections but design with as few and as small critical sections as possible (pp. 431–432).
- **Writing Correct Startup and Shutdown Code Is Hard** — graceful shutdown commonly deadlocks (parent waiting on a deadlocked child; a consumer blocked on a producer that already quit). Think about startup and shutdown early and get it working early; it will take longer than you expect (p. 432).
- **Testing Threaded Code** — testing cannot guarantee correctness but minimizes risk: write tests that can expose problems and run them frequently under different programmatic/system configurations and load; if tests ever fail, track down the failure — don't ignore it because it passes on a subsequent run (pp. 432–433). Fine-grained recommendations, each a named section (pp. 433–437):
  - **Treat Spurious Failures as Candidate Threading Issues** — assume one-offs do not exist (p. 433).
  - **Get Your Nonthreaded Code Working First** — don't chase nonthreading and threading bugs at the same time (p. 433).
  - **Make Your Threaded Code Pluggable** — runnable as one thread, several, or varied; real or test doubles; fast/slow/variable; many iterations (p. 434).
  - **Make Your Threaded Code Tunable** — allow thread counts to be tuned, possibly while running, even self-tuning (p. 434).
  - **Run with More Threads Than Processors** — encourages task swapping that flushes out missing critical sections and deadlocks (p. 434).
  - **Run on Different Platforms** — different OS threading policies expose different failures; run on all target platforms early and often (p. 434).
  - **Instrument Your Code to Try and Force Failures** — force different orderings with `wait()`, `sleep()`, `yield()`, `priority()`; two options: **hand-coded** and **automated** (a `ThreadJigglePoint.jiggle()` inserted via CGLIB/ASM that randomly sleeps, yields, or falls through). "Use jiggling strategies to ferret out errors." (pp. 435–437).
- **2025 Update and Report from the Field** — new second-edition section: modern stacks handle multiple users well *when those users do not share data*; five field cases (joining a game, working on a shared design, players creating a deck of cards in parallel, double-deleting resources on rerender with a 2D library in React Native, loading icon resources) and five different approaches: isolate non-thread-safe code into a single thread; lock objects with a flag in a relational DB; do nothing (humans recover); gate a second rendering thread; use a parent–child loading relationship (pp. 437–441).

## The argument

Concurrent code that "works fine" can be broken at a deeper level: the trivial `getNextId()` example shows that even one line (`return ++lastIdUsed;`) shared by two threads has 12,870 possible bytecode execution paths — some of which are wrong (p. 426). Since "concurrency bugs aren't usually repeatable, so they are often ignored as one-offs instead of actual defects" (p. 426), defense must be structural, not reactive.

The core defense is SRP plus data discipline: "Keep your concurrency-related code separate from other code" (p. 427) and "severely limit the access of any data that may be shared" (p. 427). The conclusion restates it: break the system into simple modules that separate thread-aware code from thread-ignorant code; keep the number of shared objects and the scope of sharing as narrow as possible; "change designs of the objects with shared data to accommodate clients rather than forcing clients to manage shared state" (p. 442).

Because proving correctness is impractical, testability becomes the safety net: run thread-related code "in many configurations on many platforms repeatedly and continuously" (p. 442), and instrument early — "You want to be running your thread-based code as long as possible before you put it into production" (p. 442).

## Distilled example

The Challenges example (p. 426):

```java
public class X {
  private int lastIdUsed;
  public int getNextId() { return ++lastIdUsed; }
}
```

Shared by two threads with `lastIdUsed = 42`, three outcomes are possible: (43, 44), (44, 43), or — the surprise — both threads get 43 and the field ends at 43. One innocuous line hides thousands of execution paths, a minority of which are wrong. This is why shared mutable state, not visible code shape, is the enemy.

The testing counterpart (pp. 435–437): insert `Thread.yield()` (hand-coded) or `ThreadJigglePoint.jiggle()` (automated, with a production no-op implementation and a test implementation that randomly sleeps/yields/falls through) between statements of a synchronized method — jiggling plus well-written tests dramatically increases the chance of exposing latent ordering bugs.

## Smells & checklist

- Concurrency implementation details embedded directly in production/domain code (SRP violation, p. 427).
- Shared mutable data updated from many places; unguarded or partially guarded critical sections (p. 427).
- Data shared when a copy would do, or threads that could be independent but share state (p. 428).
- Hand-rolled constructs where thread-safe collections or `java.util.concurrent` classes exist (pp. 428–429).
- More than one `synchronized` method used together on a shared object without client/server/adapted-server locking (p. 431).
- Oversized synchronized sections extending beyond the minimal critical section (pp. 431–432).
- Startup/shutdown paths written last and never exercised for deadlock (p. 432).
- Transient test failures dismissed as one-offs (p. 433).
- Threaded code not pluggable/tunable; tests only run single-configuration, single-platform, threads ≤ processors (pp. 433–434).
- Calling one locked section from another; locking regions that don't need it (Conclusion, p. 442).
- Multiuser systems (Lambdas, eventually consistent stores, parallel rendering loops) doing unserialized updates to shared data (pp. 437–441).

## Trade-offs & exceptions

- Concurrency incurs real overhead in performance and extra code; it only sometimes improves performance — when there is wait time that can be shared (p. 425).
- Use Copies of Data concedes the cost of extra object creation — worth experimenting to see if it's actually a problem (p. 428).
- Threads-independent is bounded: most applications eventually hit shared resources such as database connections (p. 428).
- Readers-Writers is an explicit balancing act between throughput and starvation — there is no free rule, only balance (p. 430).
- Locks are expensive, but critical sections must be guarded — the tension is resolved by minimizing, not eliminating, synchronization (pp. 431–432).
- Hand-coded instrumentation is a "shotgun approach": manual placement, unclear call choice, production slowdown, odds not with you (p. 436).
- The 2025 field report includes a deliberate **anti-case** — the deck-of-cards duplication was left unsolved because human recovery was cheap and the conflict discussion itself had value ("we chose to not solve the problem," pp. 439–440). The skill must allow "do nothing" as a legitimate answer.
- A Future Bob note recommends considering a functional language or functional style for concurrent modules (p. 428).

## Process prescriptions

- Get nonthreaded code working first; never chase both bug classes at once (p. 433).
- Think about startup and shutdown early and get them working early (p. 432).
- Write tests that can expose threading problems; run them frequently under varied configurations, platforms, and load; treat any failure as real (pp. 432–433).
- Make threaded code pluggable and tunable from the start; run with more threads than processors and on every target platform, early and often (pp. 433–434).
- Instrument (jiggle) code during testing — hand-coded for a thorny spot, automated for coverage — and keep instrumentation out of production (pp. 435–437).

## Open the PDF when

- You need the full execution-model definitions table or the Java library class descriptions verbatim (pp. 429–430).
- You are diagnosing a modern multiuser/serverless data-integrity issue and want the five 2025 field cases in full narrative detail (pp. 437–441).
- You need the exact ThreadJigglePoint/automated instrumentation discussion, including its JVM-preemption caveats (footnotes 9–10, pp. 434–436).
