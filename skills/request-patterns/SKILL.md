---
name: request-patterns
description: Design or review Command, Chain of Responsibility, or Memento when requests need independent lifecycle, ordered handlers, undo, or controlled snapshots of object state.
metadata:
  category: design-patterns
---

# Request And History Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Command when a request needs identity, lifecycle, scheduling, retry, audit, transport, or undo independent of its invoker.
- Use Chain of Responsibility when ordered handlers may process, transform, reject, or pass a request without sender-selected receivers.
- Use Memento when an originator must capture and later restore state without exposing its representation to caretakers.
- Define ordering, termination, idempotency, cancellation, transactions, snapshot ownership, retention, and compensation.
- Keep commands and mementos stable and free of unintended mutable ambient references.
- Prefer direct calls, explicit loops, or domain events when no independent lifecycle or history is required.

Read [Request And History Pattern Guidelines](references/design-guidelines-request-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove routing, ordering, short-circuiting, retry, failure, undo, snapshot fidelity, restoration, and compensation as applicable.
- Test requests, handlers, originators, and caretakers independently before assembled workflows.
- Report who owns execution and retained history.

## Review Evidence

Read references/review-checklist-request-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
