---
name: spring-boot-testing
description: Create, select, run, diagnose, or review Spring Boot unit, slice, context, security, persistence, Testcontainers, and application integration tests using version-aware test support.
metadata:
  category: stack-and-domain
---

# Spring Boot Testing

Combine with Spring Boot, Java, JUnit, Mockito, and the detected persistence or security skills. This skill owns Spring test boundaries and application-context behavior; JUnit and Mockito own their respective test-framework and test-double mechanics.

## Test Selection

- Use plain unit tests when Spring configuration and proxies are not part of the behavior.
- Use the narrow MVC, WebFlux, JSON, persistence, client, or security slice that owns the framework boundary under test.
- Use a complete application context only when auto-configuration, cross-layer wiring, transactions, security, serialization, or startup behavior must be proved together.
- Use the Spring test annotations available in the configured framework line. Do not copy deprecated mock-bean annotations from another version.
- Use Testcontainers or another production-compatible service when dialect or external-service behavior is material.
- Keep container lifecycle aligned with the cached application context; use service connections or explicit dynamic properties supported by the configured Spring Boot line.
- Test the packaged application or native image when launch behavior, resources, AOT processing, or deployment configuration is part of the claim.

Read [Spring Boot Testing Guidelines](references/testing-guidelines-spring-boot.md) when test implementation or diagnosis needs detailed selection and isolation rules.

## Verification

- Keep tests deterministic, isolated, and explicit about profiles, properties, clocks, ports, databases, and external services.
- Test successful behavior, validation, authorization, translated failures, and transaction outcomes at the relevant boundary.
- Report which test layer, application context, database engine, and external services ran.
- Report whether evidence came from the test JVM, packaged JAR, container, AOT-processed application, or native image.

## Review Evidence

Read references/review-checklist-spring-boot-testing.md during test review. Use Code Review Evidence to extract and synthesize the results.
