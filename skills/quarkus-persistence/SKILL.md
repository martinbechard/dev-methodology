---
name: quarkus-persistence
description: Implement, test, diagnose, or review Quarkus Hibernate ORM, Hibernate Reactive, Panache entities and shared persistence integration while limiting this skill to stack selection, datasource and persistence-unit alignment, schema ownership, database fidelity, and specialized companion routing.
metadata:
  category: stack-and-domain
---

# Quarkus Persistence

Combine with Quarkus, Java, and SQL. Use Quarkus Design or Java Design when choosing aggregate boundaries, persistence abstractions, or transaction ownership.

## Persistence Stack

- Inspect the owning extensions and datasource configuration before selecting standard Hibernate ORM with JDBC or Hibernate Reactive with reactive drivers.
- Do not introduce Hibernate Reactive only because the REST layer is reactive. Use it when the complete data path and workload justify non-blocking high concurrency.
- Route stack-specific entity, repository, query, and transaction work to the pertinent companion skill selected from source evidence.

## Shared Persistence Boundary

- Align datasources, entity packages, persistence units, mappings, constraints, and database versions with the migration-owned schema.
- Keep blocking and reactive execution and transaction models distinct across each workflow.
- Treat migrations as the production schema authority and avoid destructive automatic schema generation in production.
- Verify mappings, migrations, transaction boundaries, and database-specific behavior against a sufficiently faithful database engine.

Read [Quarkus Persistence Guidelines](references/persistence-guidelines-quarkus.md) when implementation or review needs detailed rules.

## Review Evidence

Read references/review-checklist-quarkus-persistence.md during code review. Use Code Review Evidence to extract and synthesize the results.
