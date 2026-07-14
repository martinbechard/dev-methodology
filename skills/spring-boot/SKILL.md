---
name: spring-boot
description: Implement, refactor, diagnose, or review Spring Boot code using version-aware framework rules for dependency injection, configuration, validation, web behavior, transactions, security, and observability.
metadata:
  category: stack-and-domain
---

# Spring Boot

Combine with Spring Boot Design when the task chooses application boundaries, packages, modules, transaction ownership, communication style, or architectural patterns. Load Spring Data JPA and Spring Boot Testing when their concern-specific evidence applies.

## Framework Baseline

- Read the owning build for the Spring Boot, Spring Framework, Java, Security, Data, Hibernate, and test versions before selecting APIs.
- Identify whether the affected path uses Spring MVC or WebFlux and JDBC or JPA or R2DBC. Do not mix imperative and reactive assumptions.
- Preserve dependency management from the Spring Boot parent or platform. Do not pin managed versions without a demonstrated compatibility need.

## Coding Guidance

- Prefer constructor injection and explicit required dependencies. Avoid hidden service lookup and mutable global configuration.
- Bind related configuration through the established type-safe configuration model and validate required values at startup.
- Validate transport input before trusted behavior and translate failures through the established HTTP or messaging error contract.
- Apply transaction annotations with explicit awareness of proxy interception, rollback rules, thread boundaries, and reactive context.
- Preserve framework-provided authentication, authorization, CSRF, CORS, and token validation behavior unless the application contract intentionally replaces it.
- Keep Actuator exposure, logging, metrics, and tracing bounded and free of secrets or full sensitive payloads.
- Use focused unit or slice tests first and integration tests when wiring, serialization, security, persistence, or transactions are material.

Read [Spring Boot Coding Guidelines](references/coding-guidelines-spring-boot.md) when implementation or review needs detailed framework rules.

## Review Evidence

Read references/review-checklist-spring-boot.md during code review. Use Code Review Evidence to extract and synthesize the results. Combine with Java and SQL when applicable.
