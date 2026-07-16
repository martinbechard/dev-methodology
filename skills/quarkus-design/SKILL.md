---
name: quarkus-design
description: Design or review Quarkus application boundaries, extension use, CDI ownership, blocking and reactive execution, transaction scope, events, security boundaries, build-time augmentation, and deployment architecture.
metadata:
  category: stack-and-domain
---

# Quarkus Design

Combine with Quarkus and Java Design when the selected design is implemented or reviewed in source code.

## Design Boundary

- Own application structure, responsibility placement, execution models, transaction ownership, extension strategy, and deployment constraints, not routine annotation syntax.
- Treat simple layering, package-by-feature, modular monoliths, ports and adapters, and services as options whose costs require evidence.
- Preserve the existing application shape unless the requested behavior exposes a concrete boundary, execution, augmentation, or deployment failure.

## Design Workflow

1. Identify user-visible workflows, domain responsibilities, consistency needs, external systems, workload characteristics, and deployment targets.
2. Define module responsibilities and public interactions before selecting REST resources, CDI beans, repositories, events, messaging channels, or clients.
3. Choose blocking, reactive, or virtual-thread execution for the complete dependency chain and place transitions at explicit boundaries.
4. Place transaction, authorization, retry, caching, and side-effect ownership where their guarantees can be enforced and observed.
5. Verify build-time augmentation, runtime configuration, extension compatibility, native-image constraints, failure behavior, and representative workflows.

Read [Quarkus Design Principles](references/design-principles-quarkus.md) when the task needs detailed decision criteria.

## Review Evidence

Read references/review-checklist-quarkus-design.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
