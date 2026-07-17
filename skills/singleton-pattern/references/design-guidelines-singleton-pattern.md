# Singleton Pattern Guidelines

## Decision Test

- Name the resource or invariant that requires one instance and the exact boundary within which one means one.
- Compare explicit composition, dependency injection, application-context scope, a module-owned instance, and an ordinary static function before selecting Singleton.
- Reject Singleton when the real goal is convenient access, hidden service location, or mutable global state.

## Construction Choices

- Prefer module or runtime initialization when construction is cheap and startup failure is acceptable.
- Use language-native single-instance mechanisms only when their identity, serialization, inheritance, and initialization semantics match the contract.
- For lazy construction, prove safe publication, failure retry behavior, and reentrancy under the configured runtime.
- Avoid locking on every access unless measured cost is acceptable and lifecycle simplicity is more important.

## Runtime Boundaries

- A module-level or static reference is normally scoped to one loaded module or runtime, not one host, cluster, tenant, or deployment.
- Framework application contexts can create more than one supposedly singleton bean and tests may construct multiple contexts.
- Serialization, reflection or metaprogramming, copying, instrumentation, process models, and ahead-of-time initialization can change instance guarantees.
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
