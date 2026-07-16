---
name: quarkus-persistence
description: Implement, test, diagnose, or review Quarkus Hibernate ORM, Hibernate Reactive, Panache entities and repositories, queries, transactions, fetch plans, pagination, locking, schema integration, and database behavior.
metadata:
  category: stack-and-domain
---

# Quarkus Persistence

Combine with Quarkus, Java, and SQL. Use Quarkus Design or Java Design when choosing aggregate boundaries, active record versus repositories, persistence abstractions, or transaction ownership.

## Persistence Model

- Identify standard Hibernate ORM with JDBC or Hibernate Reactive with reactive drivers before selecting APIs, annotations, transaction behavior, and test support.
- Do not introduce Hibernate Reactive only because the REST layer is reactive. Use it when the complete data path and workload justify non-blocking high concurrency.
- Choose Panache active record or repository style from the application's ownership and testability needs, then use that style consistently within a capability.

## Persistence Coding

- Align entities, identifiers, relationships, converters, constraints, persistence units, and database versions with the migration-owned schema.
- Make fetch plans and projections explicit from use-case result shapes; prevent unbounded results and N plus one access with measured queries.
- Bound and deterministically order list queries. Choose paging, ranges, or keyset behavior from scale and public contract needs.
- Put writes and multi-query operations inside the transaction model owned by the selected blocking or reactive stack.
- Use locking, flushing, batching, and retries only with an explicit concurrency or immediate-validation contract.
- Verify mappings, queries, migrations, transactions, and concurrency against the production database engine when dialect behavior matters.

Read [Quarkus Persistence Guidelines](references/persistence-guidelines-quarkus.md) when implementation or review needs detailed rules.

## Review Evidence

Read references/review-checklist-quarkus-persistence.md during code review. Use Code Review Evidence to extract and synthesize the results.
