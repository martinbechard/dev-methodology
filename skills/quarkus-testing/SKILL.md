---
name: quarkus-testing
description: Create, select, run, diagnose, or review Quarkus unit, component, QuarkusTest, integration, Dev Services, profile, security, persistence, JVM, container, and native tests.
metadata:
  category: stack-and-domain
---

# Quarkus Testing

Combine with Quarkus, Java, the detected persistence or security skills, and the project test framework.

## Test Selection

- Use plain unit tests when CDI, interception, configuration, extensions, and Quarkus runtime behavior are not part of the claim.
- Use Quarkus component or QuarkusTest support when injection, configuration, REST, security, persistence, transactions, or extension wiring must run inside Quarkus.
- Use a Quarkus integration test for the built artifact and run the native form when native delivery or compatibility-sensitive behavior is material.
- Use test profiles only for genuine configuration variants and group tests to avoid unnecessary application restarts.
- Use Dev Services or explicit test resources when the provisioned service and lifecycle provide sufficient production fidelity.

Read [Quarkus Testing Guidelines](references/testing-guidelines-quarkus.md) when test implementation or diagnosis needs detailed selection and isolation rules.

## Verification

- Keep tests deterministic and explicit about profiles, build-time settings, runtime overrides, ports, databases, external services, clocks, and mutable fixtures.
- Cover validation, authentication, authorization, translated failures, transaction outcomes, execution-thread assumptions, and side-effect timing at the relevant boundary.
- Report the test boundary, Quarkus launch mode, active profile, packaged form, database engine, Dev Services or external resources, and commands executed.

## Review Evidence

Read references/review-checklist-quarkus-testing.md during test review. Use Code Review Evidence to extract and synthesize the results.
