# Spring Data JPA Review Checklist

- Question: Do entity mappings and constraints agree with the migration-owned database schema?
- Question: Are relationship ownership, cascades, orphan removal, and bidirectional synchronization correct for the lifecycle?
- Question: Are equality, hashing, and string representation safe across entity and proxy states?
- Question: Does each use case have an intentional fetch plan without N plus one access or unsafe lazy-state escape?
- Question: Are query parameters, projections, pagination, ordering, indexes, and query plans aligned with expected data volume?
- Question: Do transaction and persistence-context boundaries prevent lost updates, stale state, and accidental flush behavior?
- Question: Are locking and retry semantics explicit for concurrent updates?
- Question: Do tests use sufficient database fidelity to prove mappings, constraints, queries, migrations, and concurrency behavior?
