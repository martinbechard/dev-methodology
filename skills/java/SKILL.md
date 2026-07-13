---
name: java
description: Use when implementing, refactoring, testing, or reviewing Java code, including type contracts, nullability, exceptions, resources, concurrency, collections, side effects, and review evidence.
metadata:
  category: stack-and-domain
---

# Java

## Coding Guidance

- Read the build files, configured Java version, module boundaries, formatter, and test conventions before editing.
- Use domain types and interfaces that express ownership and valid states. Avoid raw types and unchecked casts.
- Make nullability explicit through project conventions and validate external inputs at the boundary.
- Use exceptions for exceptional conditions, preserve causes, and translate them only at a boundary that owns the public contract.
- Close files, streams, database handles, and other resources deterministically.
- Prefer immutable values and narrow mutation. Make thread ownership and shared-state synchronization explicit when concurrency exists.
- Keep collections, equality, hashing, ordering, and numeric behavior aligned with domain semantics.
- Use the project's existing logging facade. Use temporary language-native output only when no logging facility exists, and remove it before completion.
- Add focused tests and run the project-native compile, test, static-analysis, and formatting checks that cover the change.

## Review Evidence

Read references/review-checklist-java.md during code review. Use Code Review Evidence to extract and synthesize the results.
