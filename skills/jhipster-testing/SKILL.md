---
name: jhipster-testing
description: Use when creating, selecting, running, reviewing, or diagnosing JHipster backend, frontend, integration, architecture, Testcontainers, end-to-end, performance, or production-build verification.
metadata:
  category: stack-and-domain
---

# JHipster Testing

Combine with JHipster Project and the test framework skills detected for the affected stack.

## Test Selection

- Start with focused Java unit or Spring integration tests for the changed backend behavior.
- Use the Testcontainers profile when production database semantics, migrations, queries, or transaction behavior matter.
- Preserve and extend ArchUnit rules when the change affects package or layer boundaries.
- Run frontend unit tests for client logic and end-to-end tests for workflows that cross the browser, API, security, and database boundaries.
- Use performance or behavior tests only when their generated surface is part of the change or acceptance criteria.

## Generated Test Care

- Treat generated tests as a working baseline, not disposable scaffolding.
- Update generated sample values when domain validation makes the generic fixtures invalid.
- Do not weaken assertions, disable a profile, or remove a quality gate merely to make regenerated code pass.
- Keep test data isolated and deterministic across reused Spring contexts and parallel execution.

## Verification Sequence

1. Run the narrow affected tests.
2. Run the project-native backend verification task.
3. Run the frontend unit checks when client code changed.
4. Run the relevant end-to-end workflow when user-visible behavior changed.
5. Exercise the production build when build profiles, packaging, or production configuration changed.

Report which layers ran, which database engine was used, and any generated test limitation that remains.
