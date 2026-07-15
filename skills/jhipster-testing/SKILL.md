---
name: jhipster-testing
description: Use when maintaining or running JHipster-generated test profiles, fixtures, architecture rules, Testcontainers wiring, frontend checks, or end-to-end scaffolding in a Java and Spring Boot application.
metadata:
  category: stack-and-domain
---

# JHipster Testing

Combine with JHipster Project, Test Strategy, and the test framework skills detected for the affected stack.

## Generated Test Contract

- Inspect the generator version, build profiles, package scripts, and generated test directories before selecting JHipster-specific checks.
- Use the generated Testcontainers profile when the project provides it and production database behavior is material.
- Preserve generated ArchUnit rules and their JHipster package conventions when regeneration or structural changes affect them.
- Use the checked-in frontend, end-to-end, and performance commands only when those surfaces were generated and remain part of the project contract.

## Regeneration Care

- Treat generated entity and integration tests as a working baseline, not disposable scaffolding.
- Update generated sample values when domain validation makes the generic fixtures invalid.
- Inspect test changes together with regenerated server, client, and migration files.
- Preserve project-specific tests outside generator-owned files or in established extension points so regeneration does not erase them.

## Verification

- Run the generated backend profile and client or end-to-end commands affected by the change.
- Confirm that regeneration does not remove custom coverage or invalidate generated fixtures.
- Report the generator version, generated profiles used, database engine, and any generated-test limitation that remains.
