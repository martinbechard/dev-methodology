# Require Claimed Backlog Resumption

Status: Blocked

Type: Defect

## Blocked Outcome

- Preserved implementation commits: 25b93ba, 58b502b, and eb9826f.
- Independent review: fresh final review passed.
- Static verification: focused tests passed 5 of 5; repository scripts passed 399 of 399; project-wiki passed 17 of 17; bundle, skill, generated-output freshness, and diff checks passed.
- Integration: no implementation commit was integrated.
- Governed acceptance: incomplete. The original blocked-state run produced one clean target and Judge pass. The unowned and failed-claim runs produced standalone Judge passes, but runner timeout and cleanup prevented governed passes. The claimed path produced a correct target result but no Judge result and retained an active-claim cleanup conflict. The repeated original path produced no Judge result. Every standalone runner exited 124 and was classified as infrastructure-failed.
- Unblock condition: obtain Judge-complete, checkpoint-and-final-consistent, cleanup-clean governed passes for unowned, claimed, and failed-claim resumption, plus a second clean blocked-state pass with an empty claim registry after handoff.

## Summary

Prevent backlog handoffs from moving blocked work directly to running without explicit claim acquisition and an eligible lifecycle transition.

## Context

The Backlog Steward blocked-state scenario correctly moved active work from Running to Blocked, preserved the exact blocker and acceptance evidence, committed the handoff, released its claim, and left the repository clean. The handoff then prescribed Blocked to Running as the resumption path even though no agent owned the item.

The independent Judge returned FAIL because the proposed transition bypassed explicit claim acquisition and the eligible Queued and claimed path. Deterministic checks confirmed the committed state change and clean claim registry but did not reject the unsafe future handoff instruction. The complete evaluation did not edit the distributed backlog skills.

## Evidence

- evals/agent-tests/dev-backlog-steward/scenarios.yaml defines the blocked transition and claim lifecycle contract.
- evals/agent-tests/dev-backlog-steward/fixtures contains the frozen active backlog used by the scenario.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained claim evidence.
- The committed handoff named Blocked to Running without requiring a new owner to acquire a claim.

## Requirements

- Require blocked work to become eligible for ownership before it can return to Running.
- Require explicit successful claim acquisition by the resuming agent before any Running transition.
- Keep claim release on blocked handoff separate from future claim acquisition.
- Reject handoff instructions that imply ownership from state alone.
- Preserve the exact blocker, unblock condition, evidence, and acceptance criteria across the resumption transition.
- Add deterministic and Judge coverage for unowned Blocked to Running shortcuts.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A blocked handoff leaves the item unowned and does not authorize direct execution.
- Resumption records an eligible state, a successful new claim, the new owner, and only then Running.
- Failure to acquire the claim leaves the backlog item unchanged and not running.
- The prior blocker and acceptance evidence remain intact after resumption.
- The Backlog Steward blocked-state scenario passes repeatably with an empty registry after the original handoff.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for blocked handoff, eligibility, claim acquisition, and resumption transitions.
- Add a negative fixture that attempts direct unowned Blocked to Running and a positive claimed-resumption fixture.
- Run the Backlog Steward blocked-state scenario multiple times and inspect commit, handoff, claim journal, independent Judge verdict, and cleanup.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- The item may remain Blocked while the external unblock condition is unsatisfied.
- A state label never substitutes for ownership evidence.
