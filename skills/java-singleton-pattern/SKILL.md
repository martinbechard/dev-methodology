---
name: java-singleton-pattern
description: Design, challenge, or review a Java Singleton when one process-wide instance and controlled access are explicit requirements, including lifecycle, concurrency, serialization, class-loader, dependency-injection, and test-isolation concerns.
metadata:
  category: stack-and-domain
---

# Java Singleton Pattern

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Require evidence that exactly one instance within a defined runtime boundary is part of the contract.
- Separate single-instance ownership from global access; dependency injection or explicit composition often satisfies the former without the latter.
- Define the boundary precisely: class loader, application context, process, cluster, tenant, or request.
- Prefer simple eager initialization or an enum only when their lifecycle and API semantics fit.
- Treat lazy initialization, serialization, reflection, cloning, shutdown, and test replacement as explicit compatibility concerns.
- Do not use Singleton as a default service locator, mutable global store, or substitute for owned dependency wiring.

Read [Java Singleton Guidelines](references/design-guidelines-java-singleton-pattern.md) when deciding whether Singleton is justified or reviewing its implementation.

## Verification

- Prove instance identity, thread safety, lifecycle, failure behavior, and isolation under the actual runtime boundary.
- Test serialization, reflection, class loaders, reset or replacement behavior only where those mechanisms are in scope.
- Report the simpler composition alternative considered and why it was insufficient.

## Review Evidence

Read references/review-checklist-java-singleton-pattern.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
