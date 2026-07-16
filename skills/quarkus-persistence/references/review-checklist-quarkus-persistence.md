# Quarkus Persistence Review Checklist

- Question: Is the blocking Hibernate ORM or Hibernate Reactive stack identified and used consistently?
- Question: Are entity mappings, persistence units, dialect settings, and constraints aligned with the migration-owned schema?
- Question: Is the active-record or repository style deliberate and consistent within the capability?
- Question: Are relationship ownership, cascades, equality, hashing, serialization, and lazy state safe?
- Question: Are fetch plans, projections, parameters, pagination, ordering, SQL counts, and query plans suitable for expected volume?
- Question: Do transaction, session, and reactive pipeline boundaries prevent lost updates, stale state, and work outside the owning context?
- Question: Are locking, flush, timeout, conflict, and retry semantics explicit?
- Question: Do tests use sufficient database and packaged-runtime fidelity to prove mappings, migrations, queries, transactions, and concurrency?
