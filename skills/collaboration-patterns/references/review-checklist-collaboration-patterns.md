# Collaboration Patterns Review Checklist

- Question: Does the collaboration require independent subscribers or coordination among many peers?
- Question: Are subscription ownership, unsubscription, payload, ordering, duplication, and delivery mode explicit?
- Question: Are reentrancy, backpressure, concurrency, subscriber failure, and context propagation handled?
- Question: Are listener leaks and mutable publisher-state exposure prevented?
- Question: Does the mediator own collaboration policy without absorbing participant-owned domain behavior?
- Question: Is mediator scope, state, transaction, and thread safety explicit?
- Question: Do tests cover no subscribers, multiple subscribers, failing subscribers, reentrancy, and coordinator decisions?
- Question: Are direct dependencies insufficient for a documented reason?
