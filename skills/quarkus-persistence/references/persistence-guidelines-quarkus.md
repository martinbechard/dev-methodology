# Quarkus Persistence Guidelines

## Stack Selection

- Read the owning extensions and datasource configuration before assuming standard Hibernate ORM, Hibernate Reactive, Panache, JDBC, or a reactive client.
- Use standard Hibernate ORM for ordinary blocking persistence unless a complete non-blocking data path and measured concurrency need justify Hibernate Reactive.
- Keep blocking entities and sessions off event-loop threads. Keep reactive entities and sessions inside the supported reactive execution and transaction context.
- Do not mix blocking and reactive transaction models inside one workflow without an explicit adapter and consistency design.

## Entity And Persistence-Unit Mapping

- Align table, column, constraint, precision, scale, temporal, enumeration, and converter mappings with the migration-owned schema.
- Choose identifiers from database, API, batching, sharding, and lifecycle requirements rather than framework convenience alone.
- Keep relationship ownership, cascades, orphan removal, and both sides of bidirectional associations deliberate and synchronized.
- Attach every entity and dependent mapped type consistently to the intended persistence unit. Panache entities belong to one persistence unit.
- Keep equality, hashing, string representation, and serialization safe across transient, managed, detached, proxied, and lazy-loaded states.

## Panache Style And Queries

- Choose active record when entity-owned persistence behavior fits the domain and static access is acceptable; choose repositories when injected persistence boundaries improve separation or testability.
- Keep one style consistent within a capability and avoid parallel DAO layers that duplicate Panache behavior.
- Bind external values as parameters and allowlist dynamic identifiers or sort fragments.
- Use projections and explicit fetch plans for large or read-only results and verify N plus one claims through executed SQL.
- Bound all list results, define deterministic ordering, and do not mix Panache range and page state accidentally.
- Close standard ORM streams within their transaction and session scope.

## Transactions And Concurrency

- Wrap writes and multi-query operations in the transaction mechanism owned by the selected stack.
- For Hibernate Reactive, use one consistent reactive transaction approach and keep the returned reactive value inside its session and transaction lifecycle.
- Flush only when a constraint, generated value, optimistic-lock failure, query ordering, or external boundary requires immediate feedback.
- Use optimistic versioning or pessimistic locks only with a defined contention, timeout, conflict, and retry contract.
- Keep remote calls and irreversible side effects outside local database transactions unless a durable coordination mechanism owns recovery.

## Schema And Verification

- Treat migrations as the production schema authority and avoid production automatic destructive schema generation.
- Configure the database version and dialect when inference cannot prove the production target.
- Use Dev Services for convenient development or test provisioning only when its image and configuration provide sufficient fidelity.
- Test mappings, queries, migrations, constraints, locking, transactions, and concurrency with the production database engine when those behaviors matter.
- Inspect executed SQL and query plans when fetch strategy, batching, indexing, or performance is part of acceptance.

## Authoritative References

- [Hibernate ORM With Panache](https://quarkus.io/guides/hibernate-orm-panache)
- [Hibernate Reactive With Panache](https://quarkus.io/guides/hibernate-reactive-panache)
- [Using Hibernate ORM And Jakarta Persistence](https://quarkus.io/guides/hibernate-orm)
- [Quarkus Transaction Guide](https://quarkus.io/guides/transaction)
- [Quarkus Dev Services](https://quarkus.io/guides/dev-services)
