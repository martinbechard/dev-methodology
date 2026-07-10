---
name: python-coding
description: Implement, refactor, test, or review Python source with explicit module boundaries, type-aware interfaces, predictable resource handling, and project-native tooling. Use for Python files and Python package work.
metadata:
  category: stack-and-domain
---

# Python Coding

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
