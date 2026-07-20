---
name: hibernate-orm-panache
description: Implement, test, diagnose, or review blocking Quarkus Hibernate ORM with Panache entities, repositories, identifiers, queries, paging, projections, transactions, flushing, locking, and persistence-unit behavior.
metadata:
  category: stack-and-domain
---

# Hibernate ORM With Panache

Combine with Quarkus Persistence, Quarkus, Java, and SQL. Use Java Design when choosing aggregate boundaries, persistence abstractions, identifier strategy, or transaction ownership.

## Blocking Persistence Boundary

- Apply this skill only when the owning build selects the quarkus-hibernate-orm-panache extension and a JDBC data path.
- Do not use this skill for Hibernate Reactive with Panache. A reactive HTTP endpoint alone does not select the persistence stack; inspect the owning extension and the complete execution path.
- Keep datasource, migration, schema, database-version, and persistence-unit decisions aligned with the shared Quarkus Persistence foundation.
- Attach each Panache entity to exactly one persistence unit and keep its mapped package and dependent mapped types within that unit's ownership.

## Model Style And Identifiers

- Choose active record when entity-owned persistence operations fit the domain and static access is acceptable. Choose repositories when an injected persistence boundary improves separation or testability, then keep the selected style consistent within a capability.
- Use PanacheEntity only when its generated Long identifier matches the schema and public contract. Use PanacheEntityBase with an explicit identifier, or PanacheRepositoryBase for repositories, when the identifier type or mapping differs.
- Treat Panache's generated accessor rewriting as part of runtime behavior. Keep custom accessors side-effect safe and verify that persistence, validation, and serialization observe the intended values.
- Preserve deliberate relationship ownership, cascades, orphan removal, equality, hashing, and lazy-state behavior in the underlying Hibernate ORM mapping.

## Queries And Result State

- Bind external values as parameters, use the required hash-prefixed form for named queries, and allowlist dynamic sort fields or query fragments.
- Bound list results and define deterministic ordering. Treat PanacheQuery paging and range selection as mutually exclusive state; use a fresh query when changing modes.
- Keep projections aligned with constructor and field requirements, and verify their executed select shape rather than assuming entity fetch behavior.
- Inspect executed SQL for fetch plans and N plus one behavior. Close stream results within the transaction and persistence context that own them.

## Transactions And Concurrency

- Put writes and multi-query state transitions inside a blocking transaction boundary. Do not rely on an HTTP method or entity operation to create an implicit transaction.
- Flush early only when a constraint, generated value, optimistic-lock result, or following query requires immediate database feedback.
- Use optimistic versioning or pessimistic locks only with explicit timeout, conflict, and retry behavior.
- Keep remote calls and irreversible side effects outside the local database transaction unless a durable coordination mechanism owns recovery.

## Verification

- Test active-record or repository behavior through the selected application boundary, including identifiers, mappings, named queries, projections, paging or ranges, transactions, flush behavior, and lock conflicts that are material to the change.
- Use the production database engine when dialect, constraints, locking, query plans, or migration behavior affects correctness.
- Verify generated accessors and executed SQL when correctness depends on build-time enhancement or query shape.

## Review Evidence

- Confirm that the owning extension is blocking Hibernate ORM with Panache and that no reactive persistence contract has been introduced.
- Confirm that model style, identifiers, query state, projections, transaction ownership, persistence units, and database-fidelity evidence match the implemented behavior.
