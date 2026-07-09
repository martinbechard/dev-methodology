---
name: postgres-drizzle
description: Use when coding, reviewing, or testing PostgreSQL persistence with Drizzle ORM, schemas, migrations, queries, transactions, indexes, relational models, or typed database access.
---

# Postgres Drizzle

Use this pack for typed PostgreSQL persistence through Drizzle.

## Routing

- Load with Coding Agent for schema, migration, query, transaction, repository, and persistence-layer changes.
- Load with Code Review Agent when a change affects data integrity, tenant boundaries, performance, or migration safety.
- Combine with TypeScript Strict, Next.js App Router, API Routes, Clerk Auth, and Jest.

## Guidance

- Keep schema definitions, domain types, and query results aligned.
- Prefer explicit transactions for multi-step writes.
- Treat tenant filters, ownership checks, and destructive operations as review-critical.
- Add indexes because a query needs them, not because they feel generally useful.

## Verification

- Run focused persistence tests and migration checks available in the project.
- Run build or typecheck after schema and query changes.
- Inspect generated SQL or query behavior when correctness depends on joins, filters, or transactions.
