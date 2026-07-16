# Java Singleton Pattern Guidelines

## Decision Test

- Name the resource or invariant that requires one instance and the exact boundary within which one means one.
- Compare explicit composition, dependency injection, application-context scope, a module-owned instance, and an ordinary static function before selecting Singleton.
- Reject Singleton when the real goal is convenient access, hidden service location, or mutable global state.

## Java Construction Choices

- Prefer eager static initialization when construction is cheap and failure during class initialization is acceptable.
- Consider an enum only when enum identity, serialization, inheritance limits, and eager initialization match the public contract.
- Use an initialization-on-demand holder when lazy class initialization is required and its failure semantics are acceptable.
- Use volatile and correct publication if double-checked locking is unavoidable under the configured Java memory model.
- Avoid synchronized access on every call unless measured cost is acceptable and lifecycle simplicity is more important.

## Runtime Boundaries

- A static field is normally one per defining class loader, not one per host, cluster, tenant, or deployment.
- Framework application contexts can create more than one supposedly singleton bean and tests may construct multiple contexts.
- Serialization, reflection, cloning, instrumentation, and native-image initialization can change instance guarantees.
- Define startup, failed initialization, shutdown, resource cleanup, and reinitialization behavior.

## Testability And State

- Keep the singleton immutable where possible.
- Inject the singleton into consumers instead of letting consumers discover it globally.
- Do not add a public reset method solely for tests; that usually exposes unsafe production state transitions.
- Test concurrent first access when lazy creation is part of the contract.
- Test the actual class-loader or application-context topology when that boundary matters.

## Authoritative References

- [Singleton](https://refactoring.guru/design-patterns/singleton)
- [Head First Design Patterns, Second Edition](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
- [Java Language Specification: Class Initialization](https://docs.oracle.com/javase/specs/jls/se25/html/jls-12.html#jls-12.4)
- [Java Enum](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Enum.html)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns/tree/master/singleton)
