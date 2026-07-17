---
name: traversal-patterns
description: Design or review Iterator or Visitor when aggregate traversal must be encapsulated or stable object structures need independently evolving operations.
metadata:
  category: design-patterns
---

# Traversal Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Iterator when callers need sequential access without depending on aggregate representation.
- Use Visitor when a stable, closed element hierarchy needs multiple type-specific operations.
- Define traversal order, mutation, exhaustion, null, concurrency, recursion, resource, and failure semantics.
- Prefer language-native iteration before custom traversal machinery.
- Treat Visitor as a trade: adding operations becomes easier while adding element types becomes more expensive.
- Keep traversal state owned and avoid exposing collection internals.

Read [Traversal Pattern Guidelines](references/design-guidelines-traversal-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove order, completeness, exhaustion, mutation policy, dispatch coverage, recursion, and failure behavior.
- Test empty, singleton, nested, heterogeneous, cyclic, and modified structures where supported.
- Report the expected direction of future variation.

## Review Evidence

Read references/review-checklist-traversal-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
