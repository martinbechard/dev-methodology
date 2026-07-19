# Specify Deterministic Dev Orchestrator Dependency Routing Fixtures

Status: Running

Type: Feature

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: deterministic-dev-orchestrator-routing-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T11:51:35.871715Z from clean baseline commit ee278e2f7e17f8f8c6b22bd44531111edaab859a.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Evaluation fixtures, runner source, tests, generated outputs, verification, and integration remain gated on a later ARTIFACT GO.

## Summary

Provide a fully specified, deterministic fixture for the Dev Orchestrator dependency-routing scenario so every contribution, review, verification, integration, and closeout gate can execute without invented work.

## Context

The dependency-routing scenario names an API source lane and an operator runbook lane, but its frozen fixture supplies no target files, requested behavior, or acceptance criteria. Both producing agents therefore returned BLOCKED without commits. The runner correctly stopped before review, verification, integration, or backlog closeout because the committed-handoffs gate could not pass.

This is a test-harness specification gap rather than a product authority question. The classification is recorded in [Classify Agent Suite Blocking Resources](../completed-backlog/analyses/classify-agent-suite-blocking-resources.md), and the authoritative run evidence is preserved in [Complete Agent Suite Results](../../evals/agent-tests/results/2026-07-17-complete-agent-suites.md).

## Requirements

- Give the dependency-routing fixture concrete source and documentation target files inside its disposable workspace.
- State one bounded requested behavior, source contract, documentation obligation, acceptance criteria, and verification expectation for each contribution lane.
- Provide deterministic dependency inputs and receipts for the producing agents, independent source and artifact reviews, contribution verification, integration, post-integration reviews, final verification, and backlog closeout.
- Require clean committed handoffs with claim evidence before downstream gates execute.
- Preserve the declared sequential dependency bound and prohibit concurrent nested dependency execution.
- Keep the fixture isolated from real project artifacts and external product decisions.
- Preserve the bounded-correction and terminal-status-integrity scenarios as separate safety-boundary evidence.
- Make runner failures identify the missing lane input or handoff field rather than collapsing into an unexplained BLOCKED result.

## Acceptance Criteria

- The dependency-routing target can complete both producing lanes without requesting unspecified product behavior.
- Every declared dependency is invoked through the expected identity and order.
- Both contribution handoffs contain clean commits, review evidence, verification evidence, and released source claims.
- Integration occurs only after contribution review and verification, followed by fresh post-integration review and complete verification.
- The scenario reaches its expected semantic result without a test-infrastructure BLOCKED classification.
- The disposable fixture, claims, dependency slot, and worktrees close cleanly.
- Existing bounded-correction and unavailable-dependency scenarios retain their expected safe BLOCKED behavior.

## Dependencies

None.

## Verification

- Run the focused Dev Orchestrator dependency-routing scenario and inspect the ordered target and dependency traces.
- Assert the committed-handoffs, dependency-identity-and-order, claim-lifecycle, output-contract, and readiness-consistency gates.
- Remove each required lane input and handoff field in focused fixture tests and confirm the runner reports the exact missing evidence.
- Run the Dev Orchestrator suite repeatedly and compare deterministic fixture identities, call order, terminal status, and cleanup.
- Run the agent-test runner unit tests, applicable bundle validation, and Git diff validation.

## Notes

- The fixture must test orchestration contracts, not the prose quality or implementation creativity of live child agents.
- Do not weaken committed-handoff or gate-order requirements to obtain a passing scenario.
