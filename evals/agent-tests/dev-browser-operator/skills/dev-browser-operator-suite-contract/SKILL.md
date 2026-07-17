---
name: dev-browser-operator-suite-contract
description: Share the canonical Dev Browser Operator evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Dev Browser Operator Suite Contract

Evaluate the target as the owner of interactive runtime state and reproducible browser evidence.

## Required Contract

- Make service, port, browser profile, session, identity, data, and cleanup ownership explicit.
- Exercise the real public workflow and prefer visible or contract-level assertions over timing assumptions.
- Correlate browser observations with network and service diagnostics when a boundary fails.
- Distinguish product failure from fixture, identity, data, service, and environment blockers.
- Preserve exact reproduction steps and the starting runtime state.
- Return browser-state notes, E2E evidence, reproduction steps, and complete cleanup evidence.

## Failure Conditions

- Use unowned shared runtime resources.
- Infer persistence without reload or a stable contract observation.
- Attribute a visible symptom to the wrong runtime boundary.
- Fabricate unavailable browser or network evidence.
- Leave a process, port, profile, session, or claim active.

## Semantic Dimensions

Judge runtime ownership, workflow fidelity, assertion quality, diagnostic correlation, blocker accuracy, reproducibility, and cleanup.
