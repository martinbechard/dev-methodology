---
name: singleton-pattern
description: Design, challenge, or review Singleton when exactly one instance within a defined runtime boundary and controlled access are explicit requirements.
metadata:
  category: development-practice
---

# Singleton Pattern

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Require evidence that exactly one instance within a defined runtime boundary is part of the contract.
- Separate single-instance ownership from global access; explicit composition or dependency injection often satisfies the former.
- Define the boundary precisely: module, class loader, application context, process, cluster, tenant, or request.
- Define initialization, publication, failure, shutdown, replacement, serialization, and test isolation as applicable.
- Keep shared state immutable where possible and do not disguise a service locator or mutable global store as Singleton.
- Prefer an owned instance when uniqueness is not observable behavior.

Read [Singleton Pattern Guidelines](references/design-guidelines-singleton-pattern.md) before accepting or reviewing Singleton.

## Verification

- Prove identity, concurrency safety, lifecycle, failure behavior, and isolation under the actual runtime boundary.
- Test language runtime and framework mechanisms only where they can change the guarantee.
- Report the simpler composition alternative considered and why it was insufficient.

## Review Evidence

Read references/review-checklist-singleton-pattern.md during design or code review. Use Code Review Evidence to synthesize the results.
