# Request And History Patterns Review Checklist

- Question: Does the request require identity or lifecycle, or an independently configured handler chain?
- Question: Are command validation, authorization, execution, persistence, retry, and result ownership separated clearly?
- Question: Are command payloads stable and free of unintended mutable ambient state?
- Question: Are idempotency, deduplication, cancellation, retry, undo, and compensation defined where applicable?
- Question: Is chain ordering and termination behavior explicit?
- Question: Do mementos hide representation while defining snapshot depth, compatibility, retention, and restoration ownership?
- Question: Are handler side effects, failures, cleanup, and shared context controlled?
- Question: Do tests cover routing, ordering, short-circuiting, rejection, failure, retry, and compensation contracts?
- Question: Is a direct call or explicit loop insufficient for a documented reason?
