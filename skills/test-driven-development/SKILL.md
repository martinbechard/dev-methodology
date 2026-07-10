---
name: test-driven-development
description: Use when implementing behavior through a framework-neutral red-green-refactor loop, especially for regressions, domain rules, boundary contracts, or incremental design changes.
metadata:
  category: development-practice
---

# Test-Driven Development

## Workflow

1. State one observable behavior and the smallest useful test boundary.
2. Write or select one focused test that fails for the expected reason.
3. Make the minimum implementation change that satisfies that behavior.
4. Run the focused test and confirm the failure became a pass for the intended reason.
5. Refactor only after the behavior is green, preserving the test contract.
6. Add relevant negative, boundary, state-transition, or regression cases.
7. Run broader tests and build checks in proportion to the change.

## Boundaries

- Use the project's existing test framework and commands.
- Prefer observable behavior over implementation detail.
- Mock only real external or nondeterministic boundaries.
- Do not introduce a new test library, tracing API, logger, fixture system, or command convention.
- When a test fails unexpectedly, switch to Root Cause Analysis before changing production behavior.
