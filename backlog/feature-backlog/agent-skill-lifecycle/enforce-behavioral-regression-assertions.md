# Enforce Behavioral Regression Assertions

Status: Running

Type: Defect

## Current Resumption Ownership

- Canonical Dev Orchestrator task: 019f7e67-dfd1-7812-bb26-abb5cf14ea94.
- Parent task: 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Phase: post-restart current-main reconciliation, focused acceptance evidence, any bounded correction/review, completion, and cleanup without replaying rejected lineage.
- Superseded implementation commits b91eecde8d1daec285b749713db2d07efd4750e5, 938ea228d0275a3563c0ad01840dfb2b1bfed622, and 3f63321c36347ae4df68e181bd1fedec2e36d149 remain recovery evidence only.

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: enforce-behavioral-regression-assertions-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T03:16:50.695793Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately before implementation.

## Blocked Outcome

The Dev Orchestrator exhausted the bounded two-correction loop after fresh independent reviews. The clean, unintegrated implementation lineage remains preserved in commits b91eecde8d1daec285b749713db2d07efd4750e5, 938ea228d0275a3563c0ad01840dfb2b1bfed622, and 3f63321c36347ae4df68e181bd1fedec2e36d149. These commits are recovery evidence, not accepted or integration-ready contributions.

No implementation was integrated. Generated skill documentation and adapters were not regenerated or integrated, the live Dev Coder TypeScript suite was not run, and no dev-verifier acceptance occurred.

## Blocked Evidence

The final HIGH provenance defect is in scripts/agent_skill_evals/validation.py. The behavior-regression-sensitivity gate derives phase outcomes from supervisor-copied transitions[*].exitCode, while the retained command evidence is validated only for marker presence. An adversarial probe claimed the JSON exit sequence 1/0/1/0 while its referenced command evidence reported 0/1/0/1; _validate_judges returned errors: []. A false PASS therefore remains possible for this critical deterministic gate.

## Unblock Condition

A separately authorized implementation must resolve structured evaluator-owned command records for every phase, derive or cross-check each transition exit code from retained command evidence rather than supervisor JSON, and add a rejection regression test for conflicting JSON and command outcomes. The corrected contribution must then restart fresh independent review and independent verification, perform serialized generation and bundle integration, run the live TypeScript scenario, and complete terminal lifecycle evaluation. Until all of that evidence passes, the preserved commits must not be treated as accepted or ready to integrate.

## Summary

Require implementation agents to prove that focused regression tests detect removal of the requested behavior, not merely that the edited test suite passes with the implementation present.

## Context

The Dev Coder executable TypeScript scenario requested a non-negative order total and required focused regression coverage. The target added the implementation clamp and left seven passing tests, but no assertion exercised a negative pre-clamp total or verified the resulting non-negative value. The independent Judge removed the clamp conceptually and confirmed that every added and existing test would still pass.

The target loaded test-driven-development, careful-coding, TypeScript, and the other declared implementation skills. The deterministic harness gates passed because a test-state transition occurred and the required commands succeeded; those gates did not establish that the changed assertion protected the requested behavior.

The complete conceptual-agent suite rollout records this as a target FAIL rather than a test-infrastructure failure. The evaluation did not edit the distributed skills.

## Evidence

- evals/agent-tests/dev-coder/scenarios.yaml requires the requested behavior to be expressed through focused regression tests.
- evals/projects/typescript-order-pricing contains the executable fixture used to remove network and dependency uncertainty.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The focused run completed with clean custom-agent identity, claim lifecycle, allowed-path, test-transition, command-outcome, and cleanup audits.

## Requirements

- Make the implementation workflow require at least one assertion that directly observes each requested behavior change.
- Require a red-state demonstration that fails for the missing behavior before accepting the green implementation, when the fixture and task make that demonstration safe and practical.
- Treat a test that passes both with and without the behavior change as insufficient regression protection.
- Keep the guidance technology-neutral while allowing technology skills to name native mutation checks, focused test selectors, or assertion patterns.
- Add deterministic or Judge coverage that distinguishes a meaningful behavioral regression test from an unrelated passing test edit.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- The relevant implementation and test-driven-development source contracts explicitly require behavior-sensitive assertions.
- Generated Codex implementation adapters contain the aligned requirement without contradictory guidance.
- A fixture patch that changes tests without protecting the requested behavior is rejected.
- A fixture patch with an observed red state and focused behavior assertion can pass.
- The Dev Coder TypeScript behavior scenario passes on a repeatable run with clean identity and cleanup evidence.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for the changed skill and generated adapter content.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Dev Coder TypeScript behavior scenario and inspect the target patch, pre-implementation failure, post-implementation pass, independent Judge verdict, and cleanup evidence.
- Remove or reverse the implementation behavior in a disposable fixture and prove that the focused regression assertion fails.
- Run repository unit tests and Git diff validation.

## Notes

- Do not require broad mutation-testing infrastructure for every task; require the narrowest reliable proof that the requested behavior is protected.
- Do not weaken the existing requirement to keep implementation changes small and scoped.
