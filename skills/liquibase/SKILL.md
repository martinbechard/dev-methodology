---
name: liquibase
description: Use when implementing, reviewing, testing, or diagnosing Liquibase changelogs, changesets, includes, contexts, labels, preconditions, checksums, updates, or rollback and recovery behavior.
metadata:
  category: stack-and-domain
---

# Liquibase

Combine with SQL and the database-specific skills detected for the affected scope.

## Changeset Ownership

- Identify the root changelog, include chain, changelog format, target database, contexts, labels, and existing DATABASECHANGELOG state before editing.
- Treat id, author, and file path as changeset identity. Add a new changeset for an applied schema evolution instead of modifying, moving, or renaming an executed changeset without an explicit compatibility plan.
- Keep constraints, indexes, nullability, defaults, and data backfills explicit. Separate schema and data work when their failure, locking, or recovery boundaries differ.
- Use preconditions only for a deliberate compatibility decision. Do not hide unexpected schema drift with permissive execution or mark-ran behavior.
- Define rollback or forward-recovery expectations for destructive and data-changing operations. Do not assume every change type has a safe automatic rollback.

## Change Workflow

1. Follow the project's established changelog format and naming order.
2. Add the changeset to the root include chain and inspect the SQL generated for the target database.
3. Run Liquibase validation before applying the change.
4. Apply pending changes to an empty database and a representative pre-change database when compatibility matters.
5. Test declared rollback behavior or document the forward-recovery procedure and exact data-loss boundary.

## Verification

- Confirm the update succeeds twice without unintentionally replaying completed changesets or leaving a stale lock.
- Run database and persistence integration tests against every materially different supported engine.
- Report the changelog path, changeset identity, contexts or labels, database engine, commands used, rollback evidence, and remaining deployment risk.
