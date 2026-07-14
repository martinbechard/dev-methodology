---
name: spring-data-jpa
description: Implement, test, diagnose, or review Spring Data JPA entities, relationships, repositories, queries, fetch plans, pagination, locking, batching, persistence contexts, and database integration.
metadata:
  category: stack-and-domain
---

# Spring Data JPA

Combine with Spring Boot, Java, and SQL. Use Spring Boot Design or Java Design when choosing aggregate boundaries, persistence abstractions, identifier strategy, or transaction ownership.

## Persistence Coding

- Map identifiers, columns, enumerations, converters, generated values, and constraints to the actual database and migration contract.
- Keep relationship ownership and both sides of bidirectional associations synchronized deliberately.
- Make fetch behavior explicit from use-case query needs; prevent N plus one behavior with measured fetch plans, entity graphs, projections, or targeted queries.
- Keep entity equality, hashing, and string representation safe across transient, managed, detached, proxied, and lazy-loaded states.
- Bound list queries and choose offset or keyset pagination from scale and ordering requirements.
- Use optimistic or pessimistic locking only with a defined conflict and retry contract.
- Coordinate schema changes with SQL, Liquibase, Flyway, or the project's migration owner rather than relying on production automatic DDL.

Read [Spring Data JPA Guidelines](references/persistence-guidelines-spring-data-jpa.md) when implementation or review needs detailed persistence rules.

## Verification

- Use the production database engine when dialect, locking, constraints, migrations, or query plans are material.
- Test mapping, query result shape, relationship changes, transaction behavior, and concurrent updates at the narrowest useful boundary.
- Inspect generated SQL or query plans when correctness or performance depends on the executed statement.

## Review Evidence

Read references/review-checklist-spring-data-jpa.md during code review. Use Code Review Evidence to extract and synthesize the results.
