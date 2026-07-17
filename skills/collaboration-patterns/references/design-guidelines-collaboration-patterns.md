# Collaboration Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Observer | One publisher has independently registered subscribers | Delivery and lifecycle are indirect |
| Mediator | Many peers need coordinated interaction rules | The mediator can accumulate too much behavior |

## Observer

- Define the event contract, publisher, subscription owner, and unsubscribe lifecycle.
- Choose push, pull, or hybrid payloads intentionally and avoid exposing mutable publisher state.
- Define synchronous versus asynchronous delivery, ordering, duplicate delivery, reentrancy, and subscriber failure isolation.
- Prevent listener leaks with explicit ownership; use weak references only when their nondeterministic lifecycle is acceptable.
- Prefer direct callbacks when there is one stable listener and no independent subscription lifecycle.

## Mediator

- Put collaboration policy in the mediator while keeping participant-owned domain behavior in participants.
- Keep participant-to-mediator messages explicit and avoid a generic string or object message bus.
- Split mediators by cohesive workflow before one coordinator owns every interaction in the subsystem.
- Define whether the mediator is stateful, thread-safe, transactional, replaceable, or scoped.
- Prefer direct dependencies when pairwise interaction is stable and does not form a dependency web.

## Execution And Concurrency

- Use the configured event or reactive API when it already defines backpressure, cancellation, and failure semantics.
- Do not block publisher threads unexpectedly.
- Preserve security identity, diagnostic context, transaction timing, and happens-before relationships across asynchronous delivery.

## Verification

- Test subscription, unsubscription, empty subscriber sets, reentrant publication, failing subscribers, and ordering guarantees.
- Test mediator decisions from public participant interactions and verify that participants remain independently usable where promised.

## Authoritative References

- [Observer](https://refactoring.guru/design-patterns/observer)
- [Mediator](https://refactoring.guru/design-patterns/mediator)
- [Head First: Observer](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
