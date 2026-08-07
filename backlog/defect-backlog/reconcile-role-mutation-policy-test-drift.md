# Reconcile Role Mutation Policy Test Drift

Status: Starting

Type: Defect

Provider: file

Owner: Unowned

Work Item ID: reconcile-role-mutation-policy-test-drift

Completion: main-branch

## Summary

Update three stale assertions in `scripts/test_role_mutation_policy.py` so the focused role-mutation suite validates the current conceptual Agent definitions and role schema.

## Context

The focused role-policy suite still expects a removed Dev Backlog Steward phrase, exactly 28 roles, and role schema version 5. The authoritative sources now contain 30 roles and role schema version 7, and the Steward definition expresses its project-guidance boundary with different wording. These stale assertions produce three failures while current Agent generation and schema parsing succeed.

## Source Evidence

On 2026-08-06, the command `/opt/homebrew/bin/python3.11 -m unittest scripts.test_role_mutation_policy` failed in `test_backlog_steward_leaves_resource_coordination_to_project_guidance`, `test_repository_mutation_does_not_load_resource_coordination`, and `test_role_schema_requires_repository_mutation`. The first two stale assertions were also recorded as unrelated baseline evidence in completed work item `align-documentation-methodology-skills`. The user instructed: “don't forget to log defects for corrections.”

## Requirements

- Replace the removed Steward phrase assertion with a current source-backed boundary assertion.
- Derive or update the expected conceptual Agent count without weakening repository-mutation coverage.
- Update the role schema version assertion to the current authoritative version.
- Keep the tests focused on the intended policy rather than unrelated wording or historical inventory values.

## Acceptance Criteria

- `scripts.test_role_mutation_policy` passes against the current role definitions and schema.
- The Steward test still proves that project guidance owns resource-coordination selection.
- The repository-mutation test still evaluates every conceptual Agent definition.
- The schema test still requires `repositoryMutation` and validates the current schema version.
- No production role definition or role schema is changed merely to satisfy stale tests.

## Dependencies

None.

## Verification

- Run `/opt/homebrew/bin/python3.11 -m unittest scripts.test_role_mutation_policy`.
- Run the Agent generation and role-schema focused tests.
- Run `git diff --check`.

## Open Questions

None.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T03:40:09Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Reconcile the stale focused role-mutation policy test assertions with the current conceptual Agent definitions and role schema while retaining the tests' intended policy coverage.

Dispatch Time: 2026-08-07T03:40:09Z

Intended Root Role: Dev Orchestrator

Launch Result: Not attempted

Canonical Execution: None

Last Contact: None

Next Reconciliation At: 2026-08-07T03:55:09Z
