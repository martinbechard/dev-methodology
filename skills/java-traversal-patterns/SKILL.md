---
name: java-traversal-patterns
description: Design or review Java Iterator or Visitor patterns when aggregate traversal must be encapsulated or stable object structures need new operations without placing those operations on every element type.
metadata:
  category: stack-and-domain
---

# Java Traversal Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Iterator when callers need sequential access without depending on aggregate representation.
- Use Visitor when a stable, closed element hierarchy needs multiple operations with type-specific behavior.
- Define traversal order, mutation, exhaustion, null, concurrency, recursion, and failure semantics.
- Prefer Iterable, Iterator, streams, or ordinary polymorphic methods before introducing custom traversal machinery.
- Treat Visitor as a trade: adding operations becomes easier while adding element types becomes more expensive.
- Keep traversal state owned and avoid exposing collection internals through cursor shortcuts.

Read [Java Traversal Pattern Guidelines](references/design-guidelines-java-traversal-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove order, completeness, exhaustion, mutation policy, dispatch coverage, recursion, and failure behavior.
- Test empty, singleton, nested, heterogeneous, and concurrently modified structures where supported.
- Report the expected direction of future variation: new operations or new element types.

## Review Evidence

Read references/review-checklist-java-traversal-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
