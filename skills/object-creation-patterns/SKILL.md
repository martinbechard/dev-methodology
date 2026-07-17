---
name: object-creation-patterns
description: Design or review Factory Method, Abstract Factory, Builder, or Prototype when construction varies, product families must stay compatible, assembly is staged, or copying is the owned creation mechanism.
metadata:
  category: development-practice
---

# Object Creation Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Start from construction variability, invariants, ownership, and lifecycle rather than a preferred pattern name.
- Use Factory Method when a creator owns a stable workflow but an extension point selects the product.
- Use Abstract Factory when callers must create a compatible product family without concrete dependencies.
- Use Builder when construction is staged, optional, representation-specific, or must hide invalid intermediate state.
- Use Prototype when copying a configured exemplar is clearer and safer than reconstructing public state.
- Prefer a constructor or simple factory when it already proves the contract.

Read [Object Creation Pattern Guidelines](references/design-guidelines-object-creation-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove product invariants, family compatibility, ownership, failure behavior, and caller independence from concrete construction.
- Test every supported variation and reject invalid or incomplete construction explicitly.
- Report why the selected pattern is simpler than the nearest alternative.

## Review Evidence

Read references/review-checklist-object-creation-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
