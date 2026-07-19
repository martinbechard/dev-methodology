# Replace Bootstrapper Marathon With Isolated Test Doubles

Status: Ready

Type: Defect

## Summary

Replace the Project Bootstrapper multi-contribution marathon scenario with deterministic test doubles over isolated copies of the agents and skills under test.

## Context

The missing-configuration-multi-contribution scenario exercised a complete live bootstrap workflow: Project Configurator creation and repeated review, five documentation contributions and reviews, integration, final review, and final verification. One governed attempt ran for 4,936 seconds before returning BLOCKED. A later recovery was stopped after another 21 minutes while still correcting the first configuration contribution.

This is too broad for a required suite gate. It makes agent latency and review nondeterminism part of the test result, obscures which orchestration contract failed, and encourages a long-lived repository-wide claim even though the behavior can be tested against an isolated snapshot.

## Evidence

- evals/agent-tests/project-bootstrapper/scenarios.yaml defines the missing-configuration-multi-contribution scenario.
- evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution contains the frozen fixture.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the stopped recovery and terminal FAIL classification.
- /private/tmp/dev-methodology-agent-suite-bootstrapper-20260718-v1/summary.json records the 4,936-second governed attempt and clean BLOCKED checkpoint.

## Requirements

- Copy the exact agents, skills, contracts, and fixture inputs under test into an isolated temporary workspace before execution.
- Do not require a repository-wide claim while the isolated test runs.
- Replace live Project Configurator, documentation writer, reviewer, merger, and verifier dependencies with deterministic scripted test doubles for orchestration-contract coverage.
- Let each double return controlled PASS, FAIL, NEEDS_CORRECTION, BLOCKED, timeout, and malformed-handoff responses.
- Assert ordered delegation, contribution acceptance, correction caps, integration choice, final review, final verification, claim closeout, and cleanup directly from recorded calls.
- Apply a strict wall-clock timeout measured in minutes, with immediate owned-process cleanup and a terminal infrastructure result.
- Keep any live multi-agent bootstrap exercise as an optional integration smoke test that does not gate the repository or hold a long-lived claim.
- Split semantic Project Configurator and documentation quality checks into their owning focused suites.

## Acceptance Criteria

- The required Bootstrapper suite completes deterministically in a bounded local test run.
- The orchestration test uses scripted agents and does not launch a full live documentation pipeline.
- Every dependency outcome and correction branch is reproducible without model variance.
- The test operates on an isolated copy and holds no repository-wide claim during execution.
- Timeout cleanup leaves no process, fixture, worktree, claim, credential, or browser residue.
- A separate optional command can run the live integration smoke test without being part of the default gate.
- Runner unit tests, bundle tests, generated-output checks, and Git diff validation pass.

## Dependencies

None.

## Verification

- Run the deterministic Bootstrapper suite repeatedly and compare call traces and verdicts.
- Force every scripted correction and failure branch and verify the terminal checkpoint.
- Trigger the wall-clock limit and verify immediate cleanup.
- Verify the primary repository remains available and unclaimed while the isolated test runs.
- Run the optional live smoke command once without promoting its variable latency into the required gate.

## Notes

- The live 4,936-second attempt is retained as evidence that this test boundary is unsuitable.
- Test doubles should preserve the Bootstrapper protocol, not imitate documentation quality or model prose.
