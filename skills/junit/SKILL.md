---
name: junit
description: Create, run, diagnose, or review JUnit tests using version-aware lifecycle, assertions, parameterization, extensions, timeouts, temporary resources, tags, and parallel-execution rules.
metadata:
  category: stack-and-domain
---

# JUnit

Combine with Java and with the detected application-framework testing skill. JUnit owns test-framework mechanics; the application skill owns runtime, container, context, persistence, and delivery-specific test boundaries.

## JUnit Boundary

- Read the configured JUnit, Java, build-tool, and test-engine versions before selecting annotations or features.
- Test observable behavior through the smallest fixture that proves the contract.
- Keep each test independent under the configured instance lifecycle and execution order.
- Use parameterized tests for meaningful input partitions, not to conceal unrelated scenarios.
- Use extensions for reusable lifecycle integration; keep ordinary setup in fixtures and helpers.
- Use bounded timeouts for genuine liveness contracts and account for the execution thread used by the timeout mode.
- Treat parallel execution as opt-in. Identify shared resources and isolate or lock them explicitly.

Read [JUnit Testing Guidelines](references/testing-guidelines-junit.md) when implementation or diagnosis needs detailed assertion, lifecycle, extension, timeout, or parallel-execution rules.

## Verification

- Run the narrow affected tests, then the owning module or project suite.
- Cover successful behavior, meaningful boundaries, invalid inputs, expected failures, and state transitions.
- Report the test engine, lifecycle or execution settings that matter, selected scope, and exact commands executed.

## Review Evidence

Read references/review-checklist-junit.md during test review. Use Code Review Evidence to extract and synthesize the results.
