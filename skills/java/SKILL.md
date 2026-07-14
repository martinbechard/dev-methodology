---
name: java
description: Implement, refactor, test, or review Java code using version-aware language rules for nullness, exceptions, resources, collections, concurrency, numeric behavior, time, and verification.
metadata:
  category: stack-and-domain
---

# Java

Combine with Java Design when the task chooses or changes public APIs, domain types, package boundaries, module relationships, or object ownership.

## Coding Boundary

- Treat the configured Java release, build, formatter, static analysis, and test conventions as the executable contract.
- Implement within the established design. Do not introduce a new architecture, pattern, package scheme, or public abstraction as a coding default.
- Use language features only when the configured source level, runtime support, and project conventions allow them.

## Coding Guidance

- Keep generic types checked and eliminate raw types, unsafe casts, and unjustified warning suppressions.
- Apply the project nullness convention consistently. Distinguish absent results, invalid input, and programmer errors instead of wrapping every nullable value in Optional.
- Preserve exception causes and translate failures only where recovery or the public contract is owned.
- Close resources deterministically and keep interruption, cancellation, and executor ownership observable when concurrency exists.
- Preserve collection mutability, iteration, equality, hashing, ordering, numeric scale, rounding, time-zone, locale, and charset semantics.
- Use the established logging facade without secrets, sensitive payloads, temporary output, or unbounded diagnostic data.
- Add focused tests and run the project-native compile, test, formatting, and configured analysis checks that cover the changed behavior.

Read [Java Coding Guidelines](references/coding-guidelines-java.md) when implementation or review needs the detailed language rules.

## Review Evidence

Read references/review-checklist-java.md during code review. Use Code Review Evidence to extract and synthesize the results.
