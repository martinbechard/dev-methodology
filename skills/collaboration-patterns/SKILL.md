---
name: collaboration-patterns
description: Design or review Observer or Mediator when state changes notify independent subscribers or many peers need coordinated interaction without direct pairwise coupling.
metadata:
  category: development-practice
---

# Collaboration Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Observer when one subject publishes defined changes to independently registered subscribers.
- Use Mediator when peer interactions require a central coordinator that owns collaboration rules.
- Define subscription, unsubscription, ordering, duplication, reentrancy, backpressure, execution context, and failures.
- Keep event payloads stable and avoid exposing mutable subject internals.
- Prevent the mediator from becoming an unbounded god object.
- Prefer direct dependencies when participants and interactions are stable and simple.

Read [Collaboration Pattern Guidelines](references/design-guidelines-collaboration-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove delivery, ordering, subscriber isolation, cleanup, reentrancy, concurrency, and coordinator decisions as applicable.
- Test participants independently and collaboration through public events or mediator operations.
- Report delivery mode and failure ownership.

## Review Evidence

Read references/review-checklist-collaboration-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
