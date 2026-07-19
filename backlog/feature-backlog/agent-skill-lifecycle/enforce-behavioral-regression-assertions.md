# Enforce Behavioral Regression Assertions

Status: Running

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: enforce-behavioral-regression-assertions-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T03:16:50.695793Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately before implementation.

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
