# Java Design Principles

## Contracts And Valid States

- Start with observable behavior, invariants, failure semantics, lifecycle, and ownership rather than a preferred pattern.
- Represent materially different domain concepts with distinct types when that prevents invalid combinations or unit confusion.
- Keep constructors and factories responsible for establishing valid state. Do not require callers to remember a hidden initialization sequence.
- Expose the smallest public surface that supports current callers and preserve source, binary, serialization, and behavioral compatibility when those contracts matter.

## Cohesion And Dependency Direction

- Keep data and the behavior that protects its invariants together.
- Place a responsibility where its required knowledge already lives; avoid utility or common packages that accumulate unrelated behavior.
- Direct dependencies toward stable contracts and keep infrastructure details from leaking into domain-facing APIs unless the application intentionally couples them.
- Use package-private visibility to protect module internals when external callers do not require access.

## Interfaces, Inheritance, And Composition

- Introduce an interface for a real substitution boundary, independent implementation, external integration, or testing seam. Do not create one mechanically for every class.
- Prefer composition when behavior varies independently or inheritance would expose lifecycle details.
- Use inheritance only when subtype substitutability is valid for every public operation and the base contract owns the extension policy.
- Keep sealed hierarchies closed only when one owner can enumerate and evolve all valid variants.

## Ownership And Mutation

- Give each mutable value and resource one clear lifecycle owner.
- Prefer immutable values at module and thread boundaries, but do not copy large structures without a demonstrated ownership need.
- Make aggregate updates atomic from the caller perspective when partial state would violate invariants.
- Separate commands that change state from queries when combining them obscures side effects or failure behavior.

## Packages And Modules

- Organize packages around cohesive capabilities or modules when that makes ownership clearer than a global layer directory.
- Keep module APIs explicit and reject dependency cycles rather than hiding them behind service lookup or shared utility code.
- Do not introduce a multi-module build merely to mirror conceptual layers; require an independent build, release, ownership, or dependency-enforcement benefit.

## Patterns And Extensibility

- Apply a design pattern only when the forces it addresses are present and name the trade-off it introduces.
- Prefer direct code for one stable case. Introduce strategies, visitors, events, or plugin contracts when variants evolve independently.
- Avoid speculative extension points, configuration switches, factories, and generic frameworks without a current caller or expected variation.
- Keep concurrency, caching, persistence, and retry policies at boundaries that can own their lifecycle and failure semantics.
