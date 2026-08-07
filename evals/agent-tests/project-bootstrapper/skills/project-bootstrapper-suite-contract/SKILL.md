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
- Ordinary project setup skips the final evidence audit. Whole-project reverse engineering assigns Wiki Ingester a read-only audit of the final integrated tree before Dev Verifier.
- Wiki Ingester reports exact stale, contradictory, or missing artifacts; Project Bootstrapper routes each result to the existing owner and obtains fresh independent review before a clear re-audit.
- Dev Documentation Writer creates or updates supported assigned non-wiki documents, including a missing module design, without owning the final cross-artifact audit.
- The same failed correction is attempted at most twice before BLOCKED.
- Repository mutation remains required, while resource-claim applies only when the project-selected resource coordination policy selects it.
- READY requires accepted configuration, complete documented scope, applicable independent reviews, final verification, a final direct or integration commit or explicit no-change result, clean worktrees, and released claims.
- The result includes status, project setup files, documentation, checks, and remaining questions.

## Failure Conditions

- Configuration or detection runs on a valid ordinary path without a stale or reconfiguration reason.
- Two dependency agents run concurrently.
- Same-owner review or verification substitutes for the required independent agent.
- One contribution is sent through merge coordination or multiple contributions bypass it.
- Integrated artifacts skip fresh post-integration review.
- Ordinary setup invokes the reverse-engineering evidence audit, Wiki Ingester mutates an audited artifact, an audit finding is routed to the wrong owner, or final verification runs before the re-audit is clear.
- A repeated correction loop exceeds the canonical cap.
- READY is reported with incomplete coverage, failed checks, dirty worktrees, active claims, or missing commit evidence.

## Semantic Dimensions

Judge state-branch accuracy, dependency routing, handoff completeness, independent-review integrity, integration choice, correction ownership, terminal-status integrity, and recovery cleanliness.

Do not return BLOCKED solely because runner-owned ordered target traces, loaded-instruction bindings, or nested parent bindings are unavailable at the Judge boundary. Record those items as conditionally pending the mandatory outer-runner post-audit and judge the supplied semantic and deterministic evidence. The outer runner invalidates the batch if its retained-session audit later fails.
