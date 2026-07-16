---
name: java-composition-patterns
description: Design or review Java Composite, Decorator, or Proxy patterns when clients need uniform tree operations, stackable behavior, or controlled access to another object while preserving its contract.
metadata:
  category: stack-and-domain
---

# Java Composition Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Composite when leaves and containers share meaningful operations and recursive structure is part of the domain.
- Use Decorator when responsibilities must be composed per instance without changing the wrapped contract.
- Use Proxy when access, location, lifecycle, security, or loading must be controlled while preserving subject semantics.
- Define ownership, identity, equality, ordering, recursion, exception, and lifecycle behavior through wrapper layers.
- Keep type promises honest; unsupported leaf operations and decorators that change core semantics weaken substitutability.
- Avoid wrapper stacks whose order or side effects cannot be understood and tested locally.

Read [Java Composition Pattern Guidelines](references/design-guidelines-java-composition-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove transparent behavior, composition order, recursive termination, access policy, failure propagation, and cleanup.
- Test representative leaf, composite, wrapped, unwrapped, local, and proxied cases as applicable.
- Report any semantic difference intentionally introduced by a wrapper.

## Review Evidence

Read references/review-checklist-java-composition-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
