# Decouple Dev Orchestrator Suite From Agent Claim When Resource Coordination Is None

Status: Starting

Type: Defect

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Decouple Dev Orchestrator evaluation from agent-claim when resource coordination is none.
- Dispatched At: 2026-07-25T01:03:56Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

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
