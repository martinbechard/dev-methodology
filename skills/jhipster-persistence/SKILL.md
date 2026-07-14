---
name: jhipster-persistence
description: Use when implementing, reviewing, testing, or diagnosing JHipster SQL database profiles, JPA persistence, Liquibase changelogs, generated migrations, test data, or development and production database parity.
metadata:
  category: stack-and-domain
---

# JHipster Persistence

Combine with JHipster Project, Java, Spring Boot, and SQL.

## Configuration Ownership

- Inspect .yo-rc.json, application profile files, the Liquibase master changelog, and build-tool Liquibase configuration before changing database behavior.
- Keep development, test, and production database settings intentionally aligned. Document accepted differences such as an embedded development database or a Testcontainers test database.
- Keep credentials and environment-specific endpoints outside tracked defaults except for explicit non-secret local examples.

## Migration Discipline

- Add a new ordered changelog for a schema evolution. Do not rewrite a changelog that may already have been applied.
- Use the entity generator, Liquibase diff support, or a manual changelog according to the project workflow, then review the resulting database operations before running them.
- Register every new changelog in the master file and keep constraints, indexes, nullability, defaults, and data backfills explicit.
- Separate development fake data from production migrations through the established Liquibase contexts.
- Coordinate JPA mappings and migration changes in one coherent change. Do not rely on schema auto-update as the migration contract.

## Verification

- Apply migrations to an empty database and to a representative pre-change database when compatibility matters.
- Run persistence integration tests against the normal test database and the production database engine through Testcontainers when engine behavior is material.
- Verify startup, rollback or recovery expectations, and the health endpoint after configuration changes.
- Report any database reset required for local development and the exact data-loss boundary.
