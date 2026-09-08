---
chapter: 23
title: The Two Values of Software
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch23_The_Two_Values_of_Software.pdf
pages: 6
level: architecture
---

# Ch23 — The Two Values of Software

**Thesis:** Software has two values — the value of its behavior and the value of its structure — and structure is the greater of the two, because structure is what makes software *soft*. Software was invented so machine behavior could be changed quickly and easily; that flexibility depends critically on the shape of the system. You preserve it by separating policy from detail and leaving as many options open as possible, for as long as possible. (This PDF also carries the Part III "Architecture" opener, p. 443.)

## Named principles & rules

- **The Two Values of Software** — there is the value of software's behavior and the value of its structure; "The second of these is the greater of the two because it is this value that makes software *soft*" (p. 445).
- **Keeping Options Open** — the way you keep software soft is to leave as many options open as possible, for as long as possible; the options to keep open "are the details that don't matter" (p. 446).
- **[Policy vs. detail decomposition]** — all software systems decompose into two major elements: *policy* (all the business rules and procedures — where the true value of the system lives) and *detail* (IO devices, databases, Web systems, servers, frameworks, communication protocols — things that let humans and systems communicate with the policy but do not affect its behavior) (p. 446).
- **[A good architecture maximizes the number of decisions not made]** — the chapter's closing maxim, set off in italics: "A good architecture maximizes the number of decisions **not** made." (p. 447). (Unnamed in the text but functions as the chapter's law.)
- **[Purpose of architecture]** (Part III opener) — architecture's purpose is to facilitate development, deployment, operation, and maintenance; its role in behavior is "passive and cosmetic, not active or essential"; the ultimate goal is to minimize the lifetime cost of the system and maximize programmer productivity (p. 443).

## The argument

Architecture "has very little bearing on whether that system works. There are many systems out there, with terrible architectures, that work just fine. Their troubles are not in their operation; they are in deployment, maintenance, and ongoing development" (p. 443). So the value the architect can actually protect is structural.

The goal of architecture is to shape the system so policy is the essential element and details are irrelevant to it, allowing decisions about details to be *delayed* and *deferred* (p. 446). The chapter enumerates decisions that need not be made early: the database (relational, distributed, hierarchical, or flat files), the Web server — "you don't even have to decide *if* the system will be delivered over the Web" (p. 446) — REST vs. microservices vs. SOA frameworks, and dependency-injection frameworks.

Deferral pays twice: "the longer you wait to make those decisions, the more information you have with which to make them properly" (p. 446), and open options permit experiments — plugging one working policy into several databases or delivery mechanisms to compare (p. 447).

## Distilled example

No code. The central illustration is the list of four deferrable detail decisions (p. 446): database, Web server/Web-at-all, interface style (REST/microservices/SOA/React), and DI framework — each deferred for the same reason: *the high-level policy should not care*. The counterfactual close: even when the company has already committed to a database or framework, "pretend that those decisions have *not* been made, and give the system a shape that allows those decisions to be deferred for as long as possible. You never know when decisions like that might suddenly change" (p. 447).

## Smells & checklist

- High-level policy (business rules) that knows which database, Web framework, delivery mechanism, or DI container is in use (p. 446).
- Detail decisions (vendor, framework, protocol) made early in development without structural necessity (p. 446).
- A system shape in which policy cannot be exercised or tested apart from its details — no ability to run the experiment of swapping a database or dropping the Web (pp. 446–447).
- Structure sacrificed for present behavior: a system that works today but resists change — its trouble will be in deployment, maintenance, and ongoing development (p. 443).
- Corporate platform commitments allowed to leak into the system's shape rather than being treated as still-deferred decisions (p. 447).

## Trade-offs & exceptions

- Behavior still matters: "Certainly we want the system to work properly; and certainly the architecture of the system must support that as one of its highest priorities" (p. 443). The claim is only that architecture's leverage over behavior is small, not that behavior is unimportant.
- Architecture's role in behavior is real "and the role is critical," yet passive and cosmetic — there are few, if any, behavioral options architecture can leave open (p. 443).
- Deferral is not indefinite: options stay open only until "those decisions can no longer be deferred" (p. 447) — the point is to arrive at that moment with maximum information.
- The Part III opener flags itself as an overview and points to [Clean Arch] for the complete treatment (p. 443).

## Process prescriptions

None (beyond the standing posture: defer detail decisions, run experiments while options remain open, and pretend already-made platform commitments have not been made — pp. 446–447).

## Open the PDF when

- You need the exact wording of the deferrable-decision examples to argue against an early framework/database commitment (p. 446).
- You want the Part III "Architecture" opener's full framing of architecture's purpose and its passive role in behavior (p. 443).
