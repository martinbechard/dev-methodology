---
name: test-strategy
description: Select, execute, and report technology-neutral unit, integration, contract, system, and regression verification from changed behavior and risk. Use when implementing tests, planning verification, reviewing coverage, diagnosing failures, or deciding which project-native checks establish confidence.
metadata:
  category: development-practice
---

# Test Strategy

Choose tests from behavior and risk, then use routed specialized test guidance when available.

## Workflow

1. Identify the changed contract, user-visible outcome, state transition, failure modes, and affected boundaries.
2. Select the smallest useful test boundary for each risk.
3. Route applicable specialized test skills from repository evidence.
4. Run focused checks first, then broader checks when the blast radius requires them.
5. Preserve failing evidence. Do not weaken assertions, disable checks, or relabel failures to obtain a pass.
6. Report exact commands, outcomes, skipped checks, environment blockers, and residual risk.

## Coverage Principles

- Test observable behavior rather than implementation arrangement.
- Cover success, invalid input, dependency failure, authorization, state transitions, and recurrence risk when applicable.
- Use doubles only at owned external or nondeterministic boundaries.
- Keep fixtures readable and restore mutated global state.
- Distinguish a product failure from an unavailable environment or dependency.

## Review Evidence

Read references/review-checklist-test-strategy.md during verification or code review.
