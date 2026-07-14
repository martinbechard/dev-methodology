---
name: jhipster-security
description: Use when implementing, reviewing, testing, or diagnosing JHipster authentication, Spring Security configuration, route and method authorization, user identity, CORS, secrets, management endpoints, or gateway trust boundaries.
metadata:
  category: stack-and-domain
---

# JHipster Security

Combine with JHipster Project, Spring Boot, and Application Security.

## Identity And Authorization

- Inspect the generated authentication mode and security configuration before changing login, token, session, or OpenID Connect behavior.
- Keep public routes explicit and narrow. Enforce authorization at the route, method, and data boundary required by the use case.
- Preserve the generated user and authority invariants unless the task owns a complete identity-model change.
- Treat gateways, registries, microservices, and direct service access as separate trust boundaries. Do not assume gateway checks protect an independently reachable service.

## Configuration

- Keep signing keys, client secrets, passwords, and production endpoints out of tracked configuration.
- Keep permissive CORS behavior limited to an intentional development boundary. Configure production origins, methods, headers, credentials, and exposed headers explicitly.
- Review management, health, metrics, documentation, and administration endpoints separately from application APIs.
- Avoid logging tokens, credentials, authorization headers, personal data, or full sensitive request bodies.

## Verification

- Test anonymous, authenticated, unauthorized, and authorized behavior for every changed route.
- Test ownership and tenant boundaries with two distinct identities when data access depends on the caller.
- Verify token or session invalidation, expiry, and failure responses when authentication behavior changes.
- Verify production-profile CORS, secret injection, and management exposure rather than relying on development defaults.
