---
name: interface-patterns
description: Design or review Adapter, Bridge, or Facade when integrating incompatible contracts, separating independently varying dimensions, or exposing a deliberate boundary over a complex subsystem.
metadata:
  category: stack-and-domain
---

# Interface Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Adapter to translate one existing contract into another without leaking the adaptee into callers.
- Use Bridge when two dimensions must vary independently without multiplying subclasses.
- Use Facade to expose a stable task-oriented boundary over a complex subsystem.
- Preserve values, errors, lifecycle, transactions, concurrency, and performance semantics across boundaries.
- Keep translation and compatibility ownership explicit.
- Prefer ordinary delegation when no named pattern adds decision clarity.

Read [Interface Pattern Guidelines](references/design-guidelines-interface-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove contract mapping, semantic equivalence, supported variation, failure translation, and caller independence.
- Test boundary inputs and outputs rather than private delegation structure.
- Report which contract owns compatibility and which details remain exposed.

## Review Evidence

Read references/review-checklist-interface-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
