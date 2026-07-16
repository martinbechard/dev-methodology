# Java Interface Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Adapter | An existing interface must satisfy a different caller contract | Translation and semantic mismatch |
| Bridge | Two dimensions vary independently | More types and delegation |
| Facade | A subsystem needs a stable, task-oriented entry point | Simplification can conceal required capabilities |

## Adapter

- Map names, values, nullness, exceptions, time, units, ownership, and lifecycle rather than merely matching method signatures.
- Keep the adaptee private unless callers intentionally need escape-hatch access.
- Prefer object composition; use inheritance only when the adaptee was designed for extension and class adaptation is required.
- Keep bidirectional translation explicit when identity or updates cross both ways.

## Bridge

- Identify the abstraction dimension and implementation dimension before introducing types.
- Keep the abstraction responsible for domain-facing operations and the implementation responsible for the platform or mechanism it owns.
- Avoid a bridge when only one dimension varies or ordinary dependency injection already expresses the relationship.
- Verify that either side can evolve without multiplying subclasses across both dimensions.

## Facade

- Design facade operations around complete caller tasks and owned transaction boundaries.
- Do not swallow errors or hide meaningful asynchronous, transactional, or performance behavior.
- Keep the underlying subsystem available only when bypass is part of the supported contract.
- Avoid turning the facade into a god object; delegate domain behavior to the subsystem owners.

## Java Verification

- Test adapters with boundary and failure values from both contracts.
- Test bridges across representative combinations of abstraction and implementation.
- Test facades as public workflows, including partial failure and cleanup.
- Preserve generic type safety, checked and unchecked failure contracts, resource ownership, and module visibility.

## Authoritative References

- [Adapter](https://refactoring.guru/design-patterns/adapter)
- [Bridge](https://refactoring.guru/design-patterns/bridge)
- [Facade](https://refactoring.guru/design-patterns/facade)
- [Head First: Adapter And Facade](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns)
