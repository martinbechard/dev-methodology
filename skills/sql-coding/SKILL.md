---
name: sql-coding
description: Use when writing, changing, testing, or reviewing SQL queries, schemas, migrations, transactions, indexes, constraints, data fixes, or persistence behavior without assuming a specific ORM or database vendor.
metadata:
  category: stack-and-domain
---

# SQL Coding

## Coding Guidance

- Read the schema, constraints, migrations, query callers, transaction ownership, supported database, and representative data shapes before editing.
- State expected input and output cardinality. Handle nulls, duplicates, empty sets, and missing relationships intentionally.
- Use parameters for untrusted values and allow-list identifiers that cannot be parameterized.
- Make join conditions, filters, grouping, ordering, and aggregation semantics explicit.
- Keep transactions as small as correctness allows. Account for isolation, locking, retries, idempotency, and partial failure where relevant.
- Prefer schema constraints for invariants the database owns.
- Add indexes only from observed access patterns and plan evidence; account for write and storage cost.
- Make migrations forward-safe, restartable when needed, and explicit about data conversion, locking, and rollback or recovery.
- Use the project's existing database and migration tools. Do not require a particular ORM, query builder, plan viewer, or logging format.

## Review Evidence

Read references/review-checklist-sql-coding.md during code review. Use Code Review Evidence to extract and synthesize the results.
