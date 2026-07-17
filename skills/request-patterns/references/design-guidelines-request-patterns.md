# Request And History Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Command | A request needs independent identity or lifecycle | Command types and dispatch infrastructure |
| Chain of Responsibility | Ordered handlers decide whether and how processing continues | Control flow and ownership become indirect |
| Memento | State must be restored without exposing representation | Snapshots consume storage and can become stale or unsafe |

## Command

- Define the command as intent and stable input, not a bag of mutable references to ambient state.
- Separate command creation, validation, authorization, execution, persistence, retry, and result ownership.
- Make idempotency and deduplication explicit before commands are queued or retried.
- For undo, capture the minimum state needed to compensate and define what happens after partial failure.
- Avoid one class per trivial local method call when no scheduling, history, transport, or policy is gained.

## Chain Of Responsibility

- Define handler order and whether a handler consumes, transforms, rejects, enriches, or passes the request.
- Make termination explicit: first match, all handlers, accumulated result, or error.
- Keep handlers independently testable and avoid hidden coupling through mutable shared context.
- Define failure policy, cleanup, retries, and whether earlier side effects are compensated.
- Prefer an explicit list or pipeline function when handler objects add no independent lifecycle or configuration.

## Concurrency And Transactions

- Identify the thread, executor, transaction, security identity, trace context, and cancellation token used for execution.
- Keep asynchronous submission failure distinct from eventual command failure.
- Do not retry non-idempotent commands without a durable key or explicit compensation contract.

## Memento

- Keep snapshot creation and restoration under the originator so caretakers do not depend on private representation.
- Define deep versus shallow capture, identity, version compatibility, retention, security, and resource ownership.
- Use immutable snapshots and bound history growth with an explicit retention or eviction policy.
- Prefer event history or compensating actions when replay or business reversal is the actual requirement.

## Verification

- Test command serialization or persistence compatibility when requests cross process or time boundaries.
- Test chain ordering, short-circuiting, all-pass, rejection, exception, and cleanup behavior.
- Test memento capture, restoration, version mismatch, retained mutable state, and history eviction.

## Authoritative References

- [Command](https://refactoring.guru/design-patterns/command)
- [Chain Of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility)
- [Memento](https://refactoring.guru/design-patterns/memento)
- [Head First: Command](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
