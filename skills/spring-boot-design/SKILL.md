---
name: spring-boot-design
description: Design or review Spring Boot application boundaries, package and module structure, transaction ownership, web and data stack choices, events, side effects, security boundaries, and operational architecture.
metadata:
  category: stack-and-domain
---

# Spring Boot Design

Combine with Spring Boot and Java Design when the selected design is implemented or reviewed in source code.

## Design Boundary

- Own application structure and responsibility placement, not annotation syntax or routine framework coding.
- Treat package-by-feature, package-by-layer, modular monolith, hexagonal architecture, and microservices as options whose costs require evidence.
- Preserve the existing application shape unless the requested behavior exposes a concrete boundary failure.

## Design Workflow

1. Identify user-visible workflows, domain responsibilities, consistency requirements, external systems, and operational constraints.
2. Define application modules and their public interactions before selecting controllers, services, repositories, events, or clients.
3. Place transaction, authorization, retry, caching, and side-effect ownership at boundaries that can enforce their guarantees.
4. Choose imperative or reactive execution from workload and dependency evidence, not fashion.
5. Verify dependencies, module APIs, AOT and native constraints, failure behavior, deployment form, and representative workflows with architecture and integration evidence.

Read [Spring Boot Design Principles](references/design-principles-spring-boot.md) when the task needs detailed decision criteria.

## Review Evidence

Read references/review-checklist-spring-boot-design.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
