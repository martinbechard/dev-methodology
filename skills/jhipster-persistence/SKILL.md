---
name: jhipster-persistence
description: Use when implementing, reviewing, testing, or diagnosing JHipster SQL database profiles, JPA persistence, generated database changes, test-data contexts, or database parity in a Java and Spring Boot application.
metadata:
  category: stack-and-domain
---

# JHipster Persistence

Combine with JHipster Project, Java, Spring Boot, Liquibase, and SQL.

## Configuration Ownership

- Inspect .yo-rc.json, application profile files, the generated Liquibase root, and build-tool Liquibase wiring before changing database behavior.
- Keep development, test, and production database settings intentionally aligned. Document accepted differences such as an embedded development database or a Testcontainers test database.
- Keep credentials and environment-specific endpoints outside tracked defaults except for explicit non-secret local examples.

## Generated Persistence

- Use JDL or the entity generator when those inputs own the entity model. Use Liquibase directly for persistence changes outside generator ownership.
- Inspect generated JPA mappings, changelogs, fake data, tests, and client changes together before accepting entity regeneration.
- Separate development fake data from production migrations through the established Liquibase contexts.
- Coordinate JPA mappings and migration changes in one coherent change. Do not rely on schema auto-update as the migration contract.

## Verification

- Run affected JHipster persistence integration tests and use the Testcontainers profile when production database behavior is material.
- Verify startup, rollback or recovery expectations, and the health endpoint after configuration changes.
- Report any database reset required for local development and the exact data-loss boundary.
