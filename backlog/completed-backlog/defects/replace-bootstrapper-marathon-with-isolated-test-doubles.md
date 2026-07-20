# Replace Bootstrapper Marathon With Isolated Test Doubles

Status: Completed

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: baton-1-bootstrapper-isolated-doubles-lifecycle.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T01:42:21.016690Z from clean baseline commit 54f8fa65dd840c2a5d529c6acff1080830c516bc.
- Scope boundary: this claim owns only the Running transition and primary index resource and is released after its clean commit. Project Bootstrapper suite-local scripted doubles, fixtures, tests, independent review, verification, and integration require a separate canonical isolated claim.

## Completion Evidence

- Accepted source lineage: 00741117821bc1304d2887bd6927c8ad9a334b6a, d47c7caee4044e381506a7480a3f6f4ff64ea7ed, and c347031d0be4ee27116fd5402cff6ab1c5175ff1; the cumulative source claim released normally in event 1037e4cd-14e1-4a3a-aad2-9de7a4ba37cd.
- Independent review accepted the exact six-file Project Bootstrapper suite-local contribution and its deterministic scripted orchestration boundary.
- Integrated on main as 4967f880e6aee0f9687729d55d0cb0585385e772 with all three Source-Commit records; the pinned generated Project Bootstrapper adapter digest was reconciled to the current-main generated adapter without widening scope.
- Focused verification passed twice with seven suite-local tests; global catalog validation passed; Codex validate-only for project-bootstrapper:missing-configuration-multi-contribution with jobs 1 passed; Git diff validation and clean status passed.
- Integration claim integrate-bootstrapper-isolated-test-doubles released normally in event 7890cebb-8cc7-49da-853c-940555e53e9d.
- The default required gate now uses bounded isolated scripted doubles; the variable live marathon remains optional and no broad or full agent-catalog run was used for this item.

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
