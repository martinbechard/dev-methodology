---
name: jhipster-security
description: Use when implementing, reviewing, testing, or diagnosing JHipster-generated authentication modes, user and authority conventions, Spring Security wiring, or gateway trust boundaries in a Java and Spring Boot application.
metadata:
  category: stack-and-domain
---

# JHipster Security

Combine with JHipster Project, Spring Boot, and Application Security.

## Generated Security Contract

- Inspect the authentication type in .yo-rc.json together with SecurityConfiguration, AuthoritiesConstants, the generated user model, and matching client authentication code.
- Preserve the generated user and authority invariants unless the task owns a complete identity-model change.
- Preserve generated reserved accounts, authority names, token claims, and login endpoints that upgrades or regeneration expect.
- Treat JHipster gateways, registries, microservices, and direct service access as separate trust boundaries. Do not assume gateway checks protect an independently reachable service.

## Change Workflow

- Decide whether an authentication-mode change belongs in generator configuration and regeneration or in project-owned Spring Security customization.
- Inspect the complete server and client diff after security regeneration because filters, routes, account flows, configuration, and tests change together.
- Keep custom access rules in the project-established extension points and preserve generated security anchors used by later upgrades.
- Review generated management and administration endpoint rules when the application type or authentication mode changes.

## Verification

- Verify login and account flows for the configured JHipster authentication mode and authority values.
- Verify direct-service and gateway behavior separately when the generated topology includes both paths.
- Confirm that regeneration preserves custom authorization behavior and does not duplicate generated security declarations.
- Report the generator version, authentication mode, generated files changed, and upgrade risk.
