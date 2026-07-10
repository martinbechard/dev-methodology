---
name: create-unit-test-plan
description: Use when creating or substantially rewriting a durable unit test plan from a design, source code, defect, or behavior contract before or alongside test implementation.
metadata:
  category: artifact-creation
---

# Create Unit Test Plan

Use skills/development-methodology/assets/templates/unit-test-plan-template.md as the starting asset.

Copy the template when a local editable artifact is needed. Replace every TODO instruction with source-backed content.

## Workflow

1. Read the behavior contract, design, implementation, callers, dependencies, existing tests, defects, and project test guidance.
2. Identify the unit boundary, observable responsibilities, invariants, inputs, outputs, state transitions, errors, and external boundaries.
3. Record discrepancies between intended behavior and current code instead of silently choosing one.
4. Define concrete scenarios with setup, action, expected result, and source traceability.
5. Describe doubles by boundary contract and purpose without mandating a mocking library.
6. Mark non-applicable failure cases honestly and explain material omissions.
7. Map every important responsibility and risk to one or more scenarios.
8. Use review-unit-test-plan and documentation-page-verifier before finishing.

The plan is optional for small changes. Create it when a durable coverage artifact will help implementation, review, handoff, or audit.
