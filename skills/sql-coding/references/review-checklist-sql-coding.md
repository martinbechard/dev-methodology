# SQL Coding Review Checklist

- Question: Are expected input and output cardinality, null, duplicate, and empty-set semantics correct?
- Question: Are joins, filters, grouping, ordering, and aggregation aligned with the intended behavior?
- Question: Are untrusted values parameterized and dynamic identifiers constrained safely?
- Question: Do constraints enforce the invariants owned by the database without conflicting with existing data?
- Question: Are transaction scope, isolation, locking, retries, idempotency, and partial failures handled where relevant?
- Question: Are indexes justified by access-pattern and plan evidence with write and storage trade-offs considered?
- Question: Are migrations ordered, forward-safe, recoverable, and explicit about conversion and lock risk?
- Question: Do tests use representative data and cover missing relationships, duplicates, concurrent behavior, and failure paths where applicable?
- Question: Is database-specific behavior identified instead of presented as portable SQL?
- Question: Do migration, query, and integration checks provide evidence for the changed scope?
