---
name: project-bootstrapper-suite-contract
description: Share the canonical Project Bootstrapper evaluation contract between its suite supervisor and independent Judge.
metadata:
  category: development-practice
---

# Project Bootstrapper Suite Contract

Evaluate Project Bootstrapper as a stateful orchestrator whose value is correct routing, independent acceptance, and a clean verified project state.

## Required Contract

- Missing configuration routes first to Project Configurator.
- Valid ordinary configuration is reused without rerunning detection or configuration.
- Invalid configuration is repaired only when reconfiguration is authorized; otherwise the workflow stops BLOCKED.
- Whole-project documentation uses complete path and module coverage rather than sampling.
- Exactly one dependency agent is active at a time.
- Every mutating contributor returns a committed clean handoff with validation evidence.
- Each artifact is reviewed by the correct independent reviewer in a fresh context.
- One accepted contribution uses the direct path and skips merge coordination.
- Multiple accepted contributions use Dev Merge Coordinator, then fresh post-integration artifact review, then Dev Verifier.
- The same failed correction is attempted at most twice before BLOCKED.
- READY requires accepted configuration, complete documented scope, applicable independent reviews, final verification, a final direct or integration commit or explicit no-change result, clean worktrees, and released claims.
- The result includes status, project setup files, documentation, checks, and remaining questions.

## Failure Conditions

- Configuration or detection runs on a valid ordinary path without a stale or reconfiguration reason.
- Two dependency agents run concurrently.
- Same-owner review or verification substitutes for the required independent agent.
- One contribution is sent through merge coordination or multiple contributions bypass it.
- Integrated artifacts skip fresh post-integration review.
- A repeated correction loop exceeds the canonical cap.
- READY is reported with incomplete coverage, failed checks, dirty worktrees, active claims, or missing commit evidence.

## Semantic Dimensions

Judge state-branch accuracy, dependency routing, handoff completeness, independent-review integrity, integration choice, correction ownership, terminal-status integrity, and recovery cleanliness.
