---
chapter: 12
title: Objects and Data Structures
pdf: /media/ajay/gdrive/_reference_vault/programming/clean_code_by_martin_2nd_ed_Chapters/Ch12_Objects_and_Data_Structures.pdf
pages: 18
level: class | surface | architecture
---

# Ch12 — Objects and Data Structures

**Thesis:** Objects and data structures are virtual opposites: an object hides its data behind abstractions and exposes behavior; a data structure exposes its data and has no meaningful behavior. Neither is superior — each makes one axis of change cheap and the other expensive — so the clean designer chooses deliberately per part of the system, hiding whatever is volatile behind whatever is static, instead of reflexively making everything an object or blithely bolting getters and setters onto everything.

## Named principles & rules

- **Data Abstraction** (pp. 251–252): Hiding implementation "is not just a matter of putting a layer of functions between the variables. Hiding implementation is about abstractions!" A class exposes abstract interfaces that let users manipulate the *essence* of the data without knowing its form. The worst option is to blithely add getters and setters.
- **Data/Object Antisymmetry** (pp. 252–255): Objects hide data behind abstractions and expose functions; data structures expose data and have no meaningful functions. Consequence: procedural code makes it easy to add new functions without changing data structures; OO code makes it easy to add new data structures without changing functions — and each makes the opposite change hard.
- **The Law of Demeter** (p. 255): A method *f* of class *C* should only call methods of: *C* itself; an object created by *f*; an object passed as an argument to *f*; an object held in an instance variable of *C*. It should not invoke methods on objects returned by any allowed call. "Be shy, talk to friends, and don't talk to strangers."
- **Trainwrecks** (p. 256): Chains of calls like `ctxt.getOptions().getScratchDir().getAbsolutePath()` — sloppy style, usually best split up. Whether a chain violates Demeter depends on whether the links are objects (violation) or data structures (Demeter does not apply).
- **Hybrids** (pp. 256–257): Structures half object, half data structure — significant functions plus public accessors/mutators that effectively expose the variables. Hard to add functions *and* hard to add data structures: "the worst of both worlds." Indicative of muddled design. (Footnote: sometimes called *feature envy* [Refactoring].)
- **Tell the Other Guy** (p. 257): Fix trainwrecks and Demeter violations by telling objects to do what we want (`ctxt.createScratchFileStream(classFileName)`) instead of traversing a network of objects to gather resources. From Thomas & Hunt's "OO in One Sentence: Keep it DRY, Shy, and Tell the Other Guy" (p. 258); connects to Alan Kay's message passing and command/query separation (CQS).
- **Data Transfer Objects (DTOs)** (p. 258): The quintessential data structure — a class/struct with public variables and no functions. Useful for databases, socket messages, and as the first stage translating raw data into objects. The Java "bean" form (private fields plus getters/setters) is quasi-encapsulation that "usually provides no other benefit."
- **The Object/Relational "Impedance Mismatch"** (p. 259): Databases contain data structures; objects are about functions; "data structures and objects are orthogonal." There is no way to map a table to an object — ORMs don't create objects, "they just load data structures."
- **[Hide the volatile, expose the static]** (pp. 259–260): The choice between the two forms comes down to which is more likely to grow and change. Hide volatile behavior behind static data structures, or hide volatile data structures behind static behavior: "We hide the volatile so that the changes don't affect the static."
- **The OO/Procedural Trade-off** (pp. 264–265): If the design interprets requirement changes as new *types*, OO is best; if as new *functions*, the procedural switch is best — "we use OO when we want to add new data types to existing functions, and we use procedural switch statements when we want to add new functions to existing data types."
- **[Switch-at-the-periphery rule]** (p. 265): Martin's general rule for `switch`/`if-else` chains: locate them at the periphery of the system (e.g., `main`); at most one per switchable type; their cases must create the polymorphic objects the rest of the system uses.
- **Single Responsibility Principle (SRP), Open–Closed Principle (OCP), Dependency Inversion Principle (DIP)** (pp. 261–262): Scattered switch statements violate SRP and OCP and make a design *rigid* (many changes required) and *fragile* (breaks easily). A design whose parts cannot be separated and deployed independently violates DIP and is *immobile*.

## The argument

Objects come from Dahl and Nygaard's Simula and Alan Kay's biology analogy — cells collaborating by messages, never asking questions: "They send messages but do not expect answers" (p. 250). Relational databases are the opposite tradition: the structure of the data is critical and visible, and programs are subservient to it (pp. 250–251). Both traditions are legitimate, and the antisymmetry between them runs deep.

The practical stakes are change-cost. In the ShapeManager parable (pp. 260–264), duplicated switch statements over shape types mean a new `Triangle` forces edits across many modules — and the CEO's plan to ship shapes separately is "dead on arrival" because `Circle` and `Square` are woven through the fabric of the system. "Mature programmers know that the idea that everything is an object is a myth. Sometimes you really do want simple data structures with procedures operating on them" (p. 255). And the payoff of the whole chapter: "Good software developers understand these issues without prejudice and choose the approach that is best for the job at hand" (p. 266).

## Distilled example

Procedural Shapes vs OO Shapes (pp. 253–254):

```java
// Procedural: dumb data structures + one Geometry class
public class Square { public Point topLeft; public double side; }
public class Geometry {
  public double area(Object shape) {
    if (shape instanceof Square) { ... }
    else if (shape instanceof Rectangle) { ... }
    else if (shape instanceof Circle) { ... } ...
```

Adding `perimeter()` touches only `Geometry`; adding a shape touches every function.

```java
// OO: polymorphic area(), no Geometry class
public class Square implements Shape {
  private Point topLeft; private double side;
  public double area() { return side*side; }
}
```

Adding a shape touches nothing existing; adding a function touches every shape. The "Not So Fast, Johnson" twist (p. 264): when customers ask for `renderDropShadow` instead of new shapes, the switch version wins — only `ShapeManager` changes.

## Smells & checklist

- Getters/setters added automatically, exposing private variables as if public (pp. 251–252). Prefer abstract expressions of the data (e.g., `getPercentFuelRemaining()` over `getGallonsOfGasoline()`, p. 252).
- Trainwreck call chains navigating through multiple objects (p. 256) — split them, or better, Tell the Other Guy.
- Method calls on objects returned from allowed calls — Law of Demeter violation, *if* the intermediates are objects rather than data structures (pp. 255–256).
- Hybrid classes: significant behavior plus public/quasi-public data (pp. 256–257). Avoid creating them.
- Beans: private fields plus mechanical getters/setters — might as well have public fields (p. 258).
- Duplicated switch/if-else chains over the same type tag across many methods or modules (pp. 261–262).
- Switch statements away from the system periphery, or more than one per switchable type (p. 265).
- Mixed levels of detail in one function (dots, slashes, file extensions mixed with intent, p. 257).

## Trade-offs & exceptions

- Neither form is wrong: things hard for OO are easy for procedures and vice versa (p. 255). Expect both kinds of components in one complex system; the decision "may have to be made differently in different parts of a system" (p. 260).
- Whether Demeter applies at all depends on object vs data structure status; accessor functions on data structures merely confuse the issue (p. 256).
- Visitor/dual-dispatch can work around the OO side of the dichotomy but "carry costs of their own and generally return the structure to that of a procedural program" (p. 254 fn5).
- Martin's personal preference is OO — interpret changes as new data types — but he "won't force an OO round peg into a procedural square hole" where behavior is overwhelmingly more volatile than data (p. 265).
- Performance: switch statements can beat polymorphic dispatch by nanoseconds; if that matters, abandon OCP/DIP *only* in the critical loops — "Don't abandon OO design throughout the entire system because a few time-critical inner loops must use switches" (p. 265).

## Process prescriptions

None.

## Open the PDF when

- You need the full ShapeManager/CEO parable (pp. 260–264) to argue deployment-independence (DIP) consequences in detail.
- You need the exact Demeter analysis of the `ctxt.getOptions()` example and its data-structure rewrite (pp. 256–257).
- Debating ORM architecture — the impedance-mismatch section (p. 259) has more historical texture than captured here.
