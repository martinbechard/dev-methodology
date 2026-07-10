---
name: end-to-end-verification
description: Verify complete user or system workflows across real boundaries without assuming a particular automation framework. Use for end-to-end tests, acceptance workflows, authenticated or stateful journeys, runtime coordination, visible failure states, or reproducible system-level evidence.
metadata:
  category: development-practice
---

# End To End Verification

Prove the complete workflow with explicit environment ownership and observable assertions.

## Workflow

1. Identify the authoritative workflow, actors, starting state, dependencies, and expected result.
2. Route specialized automation guidance when the project provides it.
3. Make service, process, session, identity, data, and cleanup ownership explicit.
4. Exercise success and material failure paths through real public boundaries.
5. Prefer stable user-visible or contract-level observations over timing assumptions.
6. Capture reproducible steps, assertions, runtime errors, and diagnostic artifacts.
7. Distinguish product failures from environment, identity, data, or runtime setup blockers.

## Review Evidence

Read references/review-checklist-end-to-end-verification.md during verification or review.
