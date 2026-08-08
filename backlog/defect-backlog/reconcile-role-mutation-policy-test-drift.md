# Reconcile Role Mutation Policy Test Drift

Status: Ready

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

Launch Result: Started

Canonical Execution: 019fda4f-3b3e-71d0-83c2-e277aa4bec68

Last Contact: 2026-08-07T03:42:39Z

Next Reconciliation At: 2026-08-07T03:57:39Z

## Running Execution

Canonical Conversation: 019fda4f-3b3e-71d0-83c2-e277aa4bec68

Codex Task ID: 019fda4f-3b3e-71d0-83c2-e277aa4bec68

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/reconcile-role-mutation-policy-test-drift

Worktree: /Users/martinbechard/.codex/worktrees/d0e3/dev-methodology

Phase: Preparing the focused stale-assertion correction

Started At: 2026-08-07T03:42:39Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator (019fda4f-3b3e-71d0-83c2-e277aa4bec68)

Evidence: The canonical Codex task is active, its clean private worktree is on the dedicated branch, and it is accepting this exact bounded work item.

Observed At: 2026-08-07T03:42:39Z

Started At: 2026-08-07T03:42:39Z

Deadline or Expires At: 2026-08-07T04:27:39Z

Next Action: Acquire outcome-work ownership and assign the focused three-assertion correction to Dev Coder.

Next Reconciliation At: 2026-08-07T03:57:39Z

## Holding Evidence

Deferral Authority: User-directed immediate stop for token-conservation pause.

Pause Evidence: User-directed token-conservation pause; preserve every current modified byte, commit, branch, worktree, and evidence without continuing implementation or delivery.

Canonical Task and Conversation: 019fda4f-3b3e-71d0-83c2-e277aa4bec68

Parent Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Preserved Branch: codex/reconcile-role-mutation-policy-test-drift

Preserved Worktree: /Users/martinbechard/.codex/worktrees/d0e3/dev-methodology

Preservation State: Clean at 1db807768d696c3aa2813d3824b5bbd298b3d9ae; no modified bytes and no immutable candidate commit.

Stopped Child Inventory: Exactly /root/candidate (Dev Coder), interrupted while running before edits/tests/commit, now stopped; zero other child executions.

Prior Task-Owned Claims Released: Provider-path release event 391beb03-0c67-405f-a49e-32d08080476c; Running-update release event 70d8d1d9-fcf0-4066-b5a5-c91841343406; outcome-work release event a49d5c3e-1c92-439f-b4df-f5d737cdf503.

Pre-Transaction Claim State: No task-owned live claim remained before this transaction.

Resumption Condition: Holding -> Ready -> Starting -> Running in this same canonical task before source work resumes.

## Ready Resumption Evidence

Transition: Holding -> Ready

Resumption Authority: Explicit user directive received by parent Coordinator on 2026-08-08.

Owner: Unowned

Canonical Task: 019fda4f-3b3e-71d0-83c2-e277aa4bec68

Next Action: Parent Coordinator records Ready -> Starting for the preserved canonical task; all Holding evidence remains history.
