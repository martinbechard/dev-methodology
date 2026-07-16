---
name: java-collaboration-patterns
description: Design or review Java Observer or Mediator patterns when state changes must notify subscribers or many peers need coordinated interaction without direct pairwise coupling.
metadata:
  category: stack-and-domain
---

# Java Collaboration Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Observer when one subject publishes defined changes to independently registered subscribers.
- Use Mediator when peer interactions require a central coordinator that owns collaboration rules.
- Define subscription, unsubscription, ordering, duplication, reentrancy, backpressure, thread, and failure semantics.
- Keep event payloads stable and avoid exposing mutable subject internals.
- Prevent the mediator from becoming an unbounded god object; keep domain behavior with the components that own it.
- Prefer direct dependencies when the participant set and interaction are stable and simple.

Read [Java Collaboration Pattern Guidelines](references/design-guidelines-java-collaboration-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove delivery, ordering, subscriber isolation, lifecycle cleanup, reentrancy, concurrency, and coordinator decisions as applicable.
- Test participants independently and verify collaboration through public events or mediator operations.
- Report synchronous versus asynchronous delivery and the owner of failures.

## Review Evidence

Read references/review-checklist-java-collaboration-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
