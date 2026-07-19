# Require Claimed Backlog Resumption

Status: Running

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: require-claimed-backlog-resumption-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T01:46:12.534961Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately before implementation.

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
