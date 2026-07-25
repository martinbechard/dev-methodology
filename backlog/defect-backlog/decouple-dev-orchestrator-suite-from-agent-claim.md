# Decouple Dev Orchestrator Suite From Agent Claim When Resource Coordination Is None

Status: Blocked

Type: Defect

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Decouple Dev Orchestrator evaluation from agent-claim when resource coordination is none.
- Dispatched At: 2026-07-25T01:03:56Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

## Execution Ownership

- Work-Item Thread: 019f96ce-b1a0-7633-97ab-336ba7d188e4
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96ce-b1a0-7633-97ab-336ba7d188e4
- Owner: Unowned
- Branch: Detached at reservation commit 97e8e20761619518d37ca5a17310836b4f4bf3b6; implementation claim and branch are pending.
- Worktree: /Users/martinbechard/.codex/worktrees/e5ea/dev-methodology
- Phase: BLOCKED
- Started At: 2026-07-25T01:11:22Z
- Coordination: Enabled; agent-claim is selected. The claim registry was empty when root acceptance began; this short lifecycle backlog transaction is recorded separately from delivery ownership.
- Claim Evidence: backlog-starting-running-019f96ce-b1a0-7633-97ab-336ba7d188e4; agent-claim acquire event 42904e24-7b4e-4ba5-ae67-71c793ab25ec. No implementation claim is recorded.
- Claim: None after release of the short blocked-handoff backlog transaction.

## Blocked Handoff

- Blocker: The bounded two-attempt correction loop is exhausted for the same resource-coordination acceptance criterion.
- Final Review: The prompt reviewer approved real adapter execution. The code reviewer returned FINDINGS: (1) a release journal event can drift in claim id, baseline, scope, or resource from the retained adapter result, while audit accepts the wrong claim; (2) the provider-none helper commits agent-claim PROJECT configuration, allowing a scenario-none/candidate-agent-claim mismatch to pass.
- Candidate Evidence: cb5c7725 and fb7ee1f5 are unaccepted candidate commits on main. Correction commit 2be3274a869355a9078d81b918700909006db652 is on branch codex/decouple-dev-orchestrator-eval-correction2-019f96ce in the clean worktree /Users/martinbechard/dev/dev-methodology/.worktrees/decouple-dev-orchestrator-eval-correction2-019f96ce.
- Released Delivery Ownership: The implementation claim was released under agent-claim event c6756ff6-fe90-4a66-8b51-9e227c38048e.
- Delivery State: No Commit READY disposition, integration, or terminal closure exists.
- Unblock Condition: A fresh authorized dispatch after the parent reconciles this exhausted-loop evidence, with a new bounded correction owner to bind release-journal identity and preserve provider-none fixture configuration; then obtain fresh code and prompt review, verification, direct-main delivery, and terminal closure.
- Permitted Resumption: Blocked to Ready through the parent Dev Backlog Coordinator, followed by a new Starting to Running acceptance transaction. This record grants no implementation ownership.

## Summary

Make the Dev Orchestrator evaluation suite honor the independent resource-coordination selection so a project that selects none does not require or load agent-claim.

## Context

The Dev Orchestrator suite currently declares agent-claim as a required skill in evals/agent-tests/dev-orchestrator/suite.yaml and its scenarios target that skill. A suite run produces 16 errors when the native Dev Orchestrator is required to load or use agent-claim despite the project resource_coordination selection being independent and set to none. This contradicts the completed Select Resource Coordination Per Project contract, which states that selecting none renders no resource-coordination procedure and requires no claim lifecycle or evidence.

Source Evidence: The user explicitly directed durable defect logging in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a. The confirmed failure concerns evals/agent-tests/dev-orchestrator/suite.yaml, evals/agent-tests/dev-orchestrator/scenarios.yaml, evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/PROJECT.yaml, agents/roles/dev-activities/dev-orchestrator.role.yaml, and generated/adapters/codex/agents/dev-orchestrator.toml.

## Requirements

- Preserve the independent meaning of resource_coordination and repository mutation.
- When a fixture or project selects resource_coordination none, Dev Orchestrator must not be required to load, invoke, or emit agent-claim lifecycle evidence.
- Keep agent-claim behavior available and testable when the project selects agent-claim.
- Correct the suite contract, fixture, canonical source, generated adapter, and focused tests only after required governed-definition approval is recorded.

## Acceptance Criteria

- A focused reproducer for the dependency-routing fixture with resource_coordination none completes without the 16 agent-claim-related errors.
- A companion agent-claim-selected case still requires the configured claim behavior.
- The full Dev Orchestrator suite reports the intended verdicts without resource-coordination cross-coupling.
- Generated native-agent output is regenerated only from an approved canonical source and passes the relevant freshness checks.

## Dependencies

None.

## Verification

- Run the focused Dev Orchestrator suite command against evals/agent-tests/dev-orchestrator/suite.yaml and preserve its report.
- Run the focused fixture tests in evals/agent-tests/dev-orchestrator/test_fixtures.py.
- Run the relevant bundle and generated-adapter freshness checks.
- Obtain a fresh independent review of the canonical and generated changes.

## Notes

This item records a confirmed defect only. Do not weaken the independent resource-coordination contract or change governed definition sources without an exact canonical-path approval manifest.
