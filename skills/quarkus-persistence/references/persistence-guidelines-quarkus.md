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
- Attach every entity and dependent mapped type consistently to the intended persistence unit.
- Keep equality, hashing, string representation, and serialization safe across transient, managed, detached, proxied, and lazy-loaded states.

## Specialized Persistence Guidance

- Load the focused companion selected by the owning extension before applying entity, repository, query, paging, projection, flush, or locking rules.
- Use Hibernate ORM With Panache only for the blocking quarkus-hibernate-orm-panache extension. Keep other persistence-stack behavior with its matching companion.
- Keep shared datasource, persistence-unit, migration, schema, and database-fidelity decisions in this foundation rather than duplicating them across companions.

## Transaction Model

- Wrap writes and multi-query operations in the transaction mechanism owned by the selected stack.
- Keep blocking and reactive transaction models distinct within each workflow and route their detailed behavior to the matching companion.
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
