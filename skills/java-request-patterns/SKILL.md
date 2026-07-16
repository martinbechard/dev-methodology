---
name: java-request-patterns
description: Design or review Java Command or Chain of Responsibility patterns when requests must be represented, queued, retried, undone, logged, or passed through an ordered sequence of independently owned handlers.
metadata:
  category: stack-and-domain
---

# Java Request Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Command when a request needs identity, data, lifecycle, scheduling, retry, undo, audit, or transport independent of its invoker.
- Use Chain of Responsibility when ordered handlers may process, transform, reject, or pass a request without the sender choosing the receiver.
- Define whether handlers stop, continue, aggregate, transform, or compensate after success and failure.
- Make ordering, idempotency, concurrency, retry, cancellation, and transaction boundaries explicit.
- Keep command payloads stable and avoid capturing mutable ambient context unintentionally.
- Prefer a direct call or simple loop when request objects or handler indirection add no operational capability.

Read [Java Request Pattern Guidelines](references/design-guidelines-java-request-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove routing, ordering, short-circuiting, retry, cancellation, failure, and compensation behavior that the contract supports.
- Test requests and handlers independently, then verify the assembled pipeline.
- Report which component owns execution and durable request state.

## Review Evidence

Read references/review-checklist-java-request-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
