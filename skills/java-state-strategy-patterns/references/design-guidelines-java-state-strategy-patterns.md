# Java State And Strategy Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Strategy | One algorithm varies independently from its context | More configuration and objects |
| State | Behavior and allowed transitions depend on current state | Distributed transition logic |
| Template Method | A stable inherited workflow owns customizable steps | Tight inheritance and hook coupling |

## Strategy

- Keep the strategy contract about one coherent algorithm and make required context explicit in parameters or construction.
- Prefer stateless strategies and Java functional interfaces when one operation is sufficient.
- Define selection ownership, fallback, configuration errors, and whether strategies may change at runtime.
- Test all strategies through the shared contract with the same conformance cases.

## State

- Model states and transitions explicitly before extracting classes.
- Keep transition authorization and invariant checks with one clear owner.
- Decide whether states initiate transitions or return transition decisions to the context; avoid mixing both casually.
- Use an enum and transition table when behavior is small and closed; add state objects when state-specific behavior and evolution justify them.

## Template Method

- Keep the template operation final when subclasses must not reorder invariant steps.
- Minimize protected hooks and document which are required, optional, idempotent, or allowed to fail.
- Avoid calling overridable methods from constructors.
- Prefer Strategy when variation must change per instance or evolve independently from the base class.

## Java Verification

- Test strategies for substitutability, state machines for every allowed and rejected transition, and templates for invariant step order.
- Verify thread safety when contexts change strategy or state concurrently.
- Preserve exception, cancellation, transaction, and resource semantics across variation points.

## Authoritative References

- [Strategy](https://refactoring.guru/design-patterns/strategy)
- [State](https://refactoring.guru/design-patterns/state)
- [Template Method](https://refactoring.guru/design-patterns/template-method)
- [Java Comparator](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Comparator.html)
- [Head First Design Patterns, Second Edition](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns)
