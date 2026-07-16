---
name: java-creation-patterns
description: Design or review Java object creation using Factory Method, Abstract Factory, Builder, or Prototype when construction varies, related product families must stay consistent, assembly is staged, or copying is the owned creation mechanism.
metadata:
  category: stack-and-domain
---

# Java Creation Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Start from construction variability, invariants, ownership, and lifecycle rather than a preferred pattern name.
- Use Factory Method when a creator owns a stable workflow but subclasses or implementations select the product.
- Use Abstract Factory when callers must create a compatible family without depending on its concrete types.
- Use Builder when construction is staged, optional, or must prevent exposure of an invalid intermediate product.
- Use Prototype when copying a configured object is clearer and safer than reconstructing it from public state.
- Keep creation contracts small and do not add a hierarchy when a constructor or static factory already proves sufficient.

Read [Java Creation Pattern Guidelines](references/design-guidelines-java-creation-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove product invariants, family compatibility, ownership, failure behavior, and caller independence from concrete construction.
- Test every supported variation and reject invalid or incomplete construction explicitly.
- Report why the selected pattern is simpler than the nearest alternative.

## Review Evidence

Read references/review-checklist-java-creation-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
