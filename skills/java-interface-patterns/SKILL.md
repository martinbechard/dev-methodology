---
name: java-interface-patterns
description: Design or review Java Adapter, Bridge, or Facade patterns when integrating incompatible contracts, separating an abstraction from varying implementations, or exposing a deliberate simplified boundary over a subsystem.
metadata:
  category: stack-and-domain
---

# Java Interface Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Adapter to translate one existing contract into another without leaking the adaptee into callers.
- Use Bridge when two dimensions must vary independently and composition is preferable to a multiplied subclass hierarchy.
- Use Facade to expose a stable task-oriented boundary over a complex subsystem without pretending the subsystem has fewer semantics.
- Preserve error, lifecycle, transactional, concurrency, and performance semantics across every boundary.
- Keep translation one-way and owned where possible; avoid chains of wrappers with unclear responsibility.
- Prefer an ordinary interface and delegation when no named pattern adds decision clarity.

Read [Java Interface Pattern Guidelines](references/design-guidelines-java-interface-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove contract mapping, semantic equivalence, supported variation, failure translation, and caller independence from implementation details.
- Test boundary inputs and outputs rather than private delegation structure.
- Report which contract owns compatibility and which details remain intentionally exposed.

## Review Evidence

Read references/review-checklist-java-interface-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
