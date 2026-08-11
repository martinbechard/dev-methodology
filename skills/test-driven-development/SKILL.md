---
name: test-driven-development
description: Use when implementing behavior through a framework-neutral red-green-refactor loop, especially for regressions, domain rules, boundary contracts, or incremental design changes.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 20be5019-a369-407b-a620-bb880c21b03f
Created-UTC: 2026-07-10T03:47:10Z
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: git-derived
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->

# Test-Driven Development

## Run Red-Green-Refactor Loop

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
- Derive valid, boundary, and invalid cases from accepted contract authority. Do not encode implementation conveniences or inferred restrictions as invalid-input expectations.
- Exercise representative values across every authorized domain; an inclusive numeric range does not imply whole numbers. Test internal rounding through observable outputs without rejecting permitted fractional inputs.
- Keep a materially ambiguous validity rule as an explicit decision or blocker when the broader authorized behavior cannot be implemented safely.
- When a test fails unexpectedly, switch to Root Cause Analysis before changing production behavior.

## Substantial Test Infrastructure Gate

Ordinary unit tests, small local fixtures, framework-native doubles, and routine TDD helpers remain inside the normal coding loop. They do not require separate architectural review.

Before implementing substantial custom helpers, service simulators, fake services, harnesses, runners, test stubs, or equivalent test infrastructure, pause the coding loop. Dev Coder updates the plan with:

- the behavior that needs proof;
- why focused existing tools, fixtures, mocks, or adapters are insufficient;
- the smallest viable test approach;
- reuse alternatives; and
- the scope and maintenance cost of the proposed infrastructure.

Dev Architect reviews necessity, reuse, scope, and proportionality before implementation. A disproportionate proposal returns for correction. A technically justified larger approach proceeds only after the user explicitly confirms its documented scale through Dev Orchestrator. The original implementation request does not imply that approval.
