# Java Creation Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Factory Method | A creator owns a stable operation but product selection varies | Subclass or implementation coupling |
| Abstract Factory | A complete family of related products must vary together | Family interfaces expand when product kinds change |
| Builder | Construction is staged, optional, validated, or representation-specific | Extra construction API and mutable assembly state |
| Prototype | A configured exemplar is the authoritative basis for new instances | Copy depth, identity, and ownership ambiguity |

## Factory Method And Abstract Factory

- Keep factory results behind the narrowest useful product contract.
- Put selection policy with the component that owns configuration and lifecycle.
- For Abstract Factory, verify that every factory creates a compatible family and that callers cannot accidentally mix families.
- Do not hide arbitrary service location behind a factory name.
- Prefer a static factory when product selection is local and no replaceable factory object is required.

## Builder

- Distinguish a fluent convenience API from the Builder pattern. The pattern earns its cost when assembly stages, representations, or validation are meaningful.
- Keep required inputs unmistakable and reject incomplete products at build time.
- Decide whether builders are reusable, thread-confined, or single-use and whether build returns an immutable snapshot.
- Avoid duplicating domain invariants between builder and product; choose one authoritative validation boundary.

## Prototype

- Define deep versus shallow copying for every owned reference.
- Preserve or replace identity, version, timestamps, listeners, caches, and external handles deliberately.
- Prefer copy constructors or named copy methods over Cloneable when they make ownership and type guarantees clearer.
- Never duplicate resources such as locks, threads, sockets, transactions, or persistence identities accidentally.

## Java Verification

- Test factories through product contracts and builders through complete and incomplete construction cases.
- Test prototypes with mutable nested state so aliasing failures are observable.
- Verify generic types, nullness, exceptions, resource ownership, concurrency, serialization, and module visibility under the configured Java release.

## Authoritative References

- [Classic Design Pattern Catalog](https://refactoring.guru/design-patterns/catalog)
- [Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)
- [Builder](https://refactoring.guru/design-patterns/builder)
- [Prototype](https://refactoring.guru/design-patterns/prototype)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns)
- [Java ServiceLoader](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/ServiceLoader.html)
