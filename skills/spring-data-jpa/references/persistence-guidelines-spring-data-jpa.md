# Spring Data JPA Guidelines

## Entity Mapping

- Align table, column, constraint, precision, scale, temporal, enumeration, and converter mappings with the migration-owned schema.
- Choose identifier type and generation from database, API, batching, sharding, and lifecycle requirements. Do not impose UUID or numeric identifiers universally.
- Keep the required no-argument constructor no more visible than the framework needs.
- Avoid broad generated equality, hashing, string, and setter behavior on entities.
- Keep entity collections initialized and update both sides of bidirectional relationships through deliberate helper behavior.

## Relationships And Fetching

- Identify the owning side of every relationship and make cascade and orphan-removal behavior match lifecycle ownership.
- Select fetch behavior from use cases and query evidence. Do not rely on default eager behavior or make every relationship lazy without verifying callers.
- Prevent N plus one access with entity graphs, fetch joins, projections, batch fetching, or dedicated read queries selected for the result shape.
- Avoid combining collection fetch joins with pagination unless the provider and query shape prove correct results.
- Map entities to stable response or domain shapes before leaving the persistence context when lazy state must not escape.

## Repositories And Queries

- Use derived queries while their meaning remains clear; use explicit JPQL, criteria, specifications, or native SQL when the contract requires more control.
- Bind every external value as a parameter and keep dynamic sort or identifier fragments on an allowlist.
- Project only the data needed for large or read-only results.
- Bound list results and define deterministic ordering. Use keyset pagination when deep offsets are a demonstrated problem.
- Base indexes on real filters, joins, ordering, uniqueness, and query plans rather than indexing every mapped column.

## Persistence Context And Transactions

- Keep persistence-context scope aligned with the owning transaction and avoid depending on accidental lazy access after that scope.
- Understand when dirty checking is sufficient and avoid redundant saves that obscure ownership.
- Flush deliberately only when a database constraint, generated value, query ordering, or external boundary requires it.
- Use optimistic versioning where lost updates matter and define who retries or reports a conflict.
- Keep bulk updates and deletes consistent with the persistence context by clearing, refreshing, or isolating affected state as required.
- Use batching only after confirming identifier generation, statement shape, driver behavior, and memory limits support it.

## Schema Evolution And Testing

- Treat migration files as the production schema authority when the project uses migrations.
- Use expand, backfill, switch, and contract stages for changes that must remain compatible with running versions.
- Test against the production database engine when dialect, collation, generated values, constraints, locking, or migration behavior matters.
- Assert database outcomes and relationship behavior, not merely repository method invocation.
- Inspect SQL counts or plans when a fetch strategy or query-performance claim is part of acceptance.
