---
name: composition-patterns
description: Design or review Composite, Decorator, Proxy, or Flyweight when clients need uniform trees, stackable behavior, controlled access, or shared intrinsic state across many logical objects.
metadata:
  category: development-practice
---

# Composition Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Composite when leaves and containers share meaningful operations and recursive structure belongs to the domain.
- Use Decorator when responsibilities compose per instance without changing the wrapped contract.
- Use Proxy when access, location, lifecycle, security, or loading must be controlled while preserving subject semantics.
- Use Flyweight when many logical objects can safely share immutable intrinsic state while callers supply extrinsic state.
- Define ownership, identity, equality, ordering, recursion, failure, lifecycle, and concurrency through every layer.
- Prefer a direct object graph when sharing or wrappers add no demonstrated value.

Read [Composition Pattern Guidelines](references/design-guidelines-composition-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove substitutability, composition order, recursive termination, access policy, sharing boundaries, failure propagation, and cleanup.
- Test representative leaf, composite, wrapped, proxied, pooled, and unshared cases as applicable.
- Report every intentional semantic difference introduced by indirection.

## Review Evidence

Read references/review-checklist-composition-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
