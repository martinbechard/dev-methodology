---
name: spring-boot
description: Use when implementing, testing, or reviewing Spring Boot controllers, services, repositories, configuration, validation, transactions, security boundaries, error handling, observability, or application tests.
metadata:
  category: stack-and-domain
---

# Spring Boot

## Coding Guidance

- Read the build, Spring Boot version, active configuration model, package boundaries, and established test slices before editing.
- Keep transport mapping in controllers, domain orchestration in services, and persistence behavior behind repository or data-access boundaries.
- Prefer constructor injection and explicit required dependencies. Avoid hidden service lookup and mutable global configuration.
- Validate request and configuration inputs at their owning boundary.
- Place transaction ownership around a coherent business operation. Do not rely on accidental proxy behavior, self-invocation, or lazy access outside the owned scope.
- Translate domain and infrastructure failures through the application's established exception and response contract.
- Preserve authentication and authorization at the correct method, route, and data boundary.
- Use the existing logging facade and configuration. Log decisions and identifiers needed for diagnosis without secrets or full sensitive payloads.
- Choose focused unit or slice tests first, then integration tests when wiring, serialization, security, persistence, or transactions are material.

## Review Evidence

Read references/review-checklist-spring-boot.md during code review. Use Code Review Evidence to extract and synthesize the results. Combine with Java Coding and SQL Coding when applicable.
