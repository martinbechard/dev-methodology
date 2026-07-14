---
name: java-design
description: Design or review Java APIs, domain types, object ownership, package cohesion, module boundaries, dependency direction, extensibility, and compatibility before implementation details are chosen.
metadata:
  category: stack-and-domain
---

# Java Design

Combine with Java when the design is implemented, refactored, tested, or reviewed in source code.

## Design Boundary

- Own structural decisions: public contracts, valid states, ownership, mutation boundaries, dependency direction, packages, modules, and extension points.
- Do not own formatting, routine syntax, build commands, exception mechanics, or other language-level coding rules.
- Preserve the established architecture unless evidence shows that the requested behavior cannot fit it safely.

## Design Workflow

1. Identify callers, observable behavior, lifecycle, compatibility constraints, and the code that currently owns the responsibility.
2. Model valid states and invariants before selecting classes, records, interfaces, inheritance, or patterns.
3. Keep dependencies directed toward stable contracts and keep related behavior and data cohesive.
4. Choose the smallest public surface and extension mechanism that satisfies demonstrated variation.
5. Verify the design through representative callers, dependency checks, focused tests, and compatibility evidence.

Read [Java Design Principles](references/design-principles-java.md) when the task needs detailed decision criteria.

## Review Evidence

Read references/review-checklist-java-design.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
