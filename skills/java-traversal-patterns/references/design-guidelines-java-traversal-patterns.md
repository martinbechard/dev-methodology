# Java Traversal Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Iterator | Traversal must be independent from aggregate representation | Cursor lifecycle and mutation rules |
| Visitor | A stable element hierarchy needs many external operations | Adding element types changes every visitor |

## Iterator

- Implement Iterable when repeatable iteration is part of the aggregate contract.
- Define encounter order, exhaustion, removal, concurrent modification, null elements, and whether multiple iterators are independent.
- Prefer standard Iterator, Spliterator, streams, and collection views unless a custom cursor has additional domain semantics.
- Keep resource-backed iteration closeable through an explicit owning API; Iterator alone does not own resource cleanup.
- Avoid returning internal mutable collections as a substitute for traversal abstraction.

## Visitor

- Use Visitor when the element hierarchy is comparatively stable and operations change more often than element types.
- Keep double dispatch exhaustive and make fallback behavior explicit for unknown or future types.
- Decide where traversal lives: the object structure, the visitor, or a separate traversal component.
- Use generic result and context types when operations return values or need explicit state.
- Prefer ordinary polymorphic methods when the operation is core element behavior, and prefer pattern matching when the hierarchy and configured Java release make it simpler and sufficiently extensible.

## Recursion And Performance

- Protect recursive traversals from cycles and unbounded depth where the structure is not guaranteed to be a tree.
- Define lazy versus eager evaluation and short-circuit behavior.
- Keep parallel traversal opt-in and preserve ordering, thread safety, and side-effect rules.

## Verification

- Test empty, singleton, nested, heterogeneous, cyclic, exhausted, and concurrently modified structures as supported.
- Run one visitor conformance suite across every element type and test every visitor across representative structures.

## Authoritative References

- [Iterator](https://refactoring.guru/design-patterns/iterator)
- [Visitor](https://refactoring.guru/design-patterns/visitor)
- [Java Iterator](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Iterator.html)
- [Java Spliterator](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Spliterator.html)
- [Head First: Iterator And Composite](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns)
