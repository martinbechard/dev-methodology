---
name: agent-suite-supervision
description: Coordinate one agent-owned evaluation suite with frozen inputs, exactly one active child at a time, deterministic gates, independent judging, and durable terminal evidence.
metadata:
  category: evaluation
---

# Agent Suite Supervision

Use this project skill only for supervising an agent suite under evals/agent-tests.

## Workflow

1. Load the suite manifest and one selected scenario.
2. Verify the canonical role, native adapter, fixture, project agents, and project skills named by the manifest.
3. Freeze their digests and the allowed input, write, command, delegation, and terminal-status contracts.
4. Invoke exactly one child: the standard target agent named by the suite.
5. Capture governed evidence and finish that child before starting another.
6. Run deterministic checks. Stop on a critical failure.
7. Invoke the hardcoded suite Judge in a fresh context.
8. Record PASS, FAIL, BLOCKED, or STALE and preserve the evidence needed to reproduce that classification.
9. Clean every suite-owned resource.

## Concurrency

- Keep exactly one active child.
- Do not overlap target execution, evidence work, judging, or correction.
- Permit one nested child only when the suite manifest and canonical target definition both require that dependency.
- Wait for the nested child to finish before the active child continues or another dependency starts.

## Boundaries

- Do not evaluate another suite.
- Do not substitute a generic worker, alternate Judge, or unlisted skill.
- Do not change the scenario or rubric after target execution begins.
- Do not award semantic credit yourself.
- Do not claim PASS from a final response without matching trace and artifact evidence.

## Result

Return the suite, scenario, frozen digests, target and dependency identities, deterministic results, Judge verdict, terminal status, evidence locations, cleanup result, and residual risk.
