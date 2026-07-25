# Require Durable Defect Logging And Direct-Main Work-Item Creation

Status: Ready

Type: Feature

Owner: Unowned

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Require durable defect logging and define safe claim-free primary-main work-item creation.
- Dispatched At: 2026-07-25T01:04:42Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Accepted as canonical work-item Thread 019f96cf-226c-7f62-9d66-7d31cead822e; canonical root task recorded below.

## Prior Execution Ownership

- Work-Item Thread: 019f96cf-226c-7f62-9d66-7d31cead822e
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96cf-226c-7f62-9d66-7d31cead822e
- Owner: Unowned
- Branch: Detached at 97e8e20761619518d37ca5a17310836b4f4bf3b6
- Worktree: /Users/martinbechard/.codex/worktrees/fa2b/dev-methodology
- Phase: Approval manifest ready; awaiting user approval.
- Started At: 2026-07-25T01:34:57Z
- Prior Coordination Release: require-durable-defect-logging-running-019f96cf; acquire event b67710d6-d249-46e4-a44f-1ff6625f1b14; release event d25f25bb-d408-41b5-9396-edfe6b3197b2 after commit 126ee9befb575c4ebd1d4ddd00444616a8a48808.

## User Action Required

Question: Do you approve mutation of exactly skills/create-file-work-item/SKILL.md and agents/roles/dev-activities/dev-orchestrator.role.yaml to require durable duplicate-reconciled logging of every confirmed defect, prohibit downgrading confirmed defects to warnings, and define safe claim-free work-item creation only on clean primary main?

Why Input Is Required: Repository definition authority requires exact scope-specific user approval; the Ready/Running item and general write authority are insufficient.

### Governed Canonical Approval Scope

- skills/create-file-work-item/SKILL.md
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Dependent Generated Mirrors (Not Approval Scope)

- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters/**, only where supported by the approved source categories

### Non-Governed Companion Scope (Not Approval Scope)

- skills/create-file-work-item/scripts/create.py
- skills/agent-claim-command/scripts/claim.py
- scripts/test_create_file_work_item.py
- scripts/test_agent_claim.py
- scripts/test_bundle_content.py
- README.md
- design/orchestrated-development-lifecycle.html
- design/work-item-provider-and-completion-contracts.md
- Applicable evaluation fixtures

Unattended Work Boundary: Do not mutate any governed definition, approval record, generated mirror, or dependent artifact until the parent reserves this same Thread for the Ready -> Starting transition, then records Starting -> Running before implementation.

Resolution: On 2026-07-25, the user answered exactly "approved" in canonical work-item Thread 019f96cf-226c-7f62-9d66-7d31cead822e. This authorizes mutation of exactly skills/create-file-work-item/SKILL.md and agents/roles/dev-activities/dev-orchestrator.role.yaml for the recorded defect-capture and safe primary-main creation policy. The answer does not authorize dependent generated mirrors or non-governed companion artifacts as governed definition scope; they remain implementation-dependent surfaces. Provenance: the user reply followed the exact recorded two-path approval question in that same canonical Thread.

## Summary

Make the methodology require every discovered defect to be logged durably rather than treated as an ignored warning, and make new file-backed work-item creation occur directly on primary main without a backlog claim or isolated worktree.

## Context

The user explicitly directed: when defects are found, always log them; do not ignore them or downgrade them to warnings. The user also directed that new work-item creation occur directly on primary main, never from an isolated worktree, and without a backlog claim. Current live policy still requires a short backlog-domain claim for file-provider creation, so this record does not alter the active policy.

Source Evidence: User direction in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a, including the message that expanded the defect-recording work into this explicitly requested feature.

## Requirements

- Require a durable file-provider record for each confirmed defect, including reproduction evidence and a runnable next action.
- Prohibit classifying a confirmed defect as an ignorable warning solely to avoid backlog creation.
- Define the direct-primary-main creation transaction and prohibit isolated-worktree creation for file-backed work items.
- Remove the backlog-claim requirement for creation only after the governing source, claim safety model, and concurrent-writer recovery behavior are reviewed.
- Preserve the exact canonical-path approval-manifest requirement before any governed agent or skill definition mutation.

## Acceptance Criteria

- The applicable backlog and agent guidance makes confirmed-defect recording mandatory and distinguishes it from unconfirmed observations.
- The file-provider workflow specifies direct primary-main creation with the required clean-state and concurrency safeguards.
- Tests cover defect capture, duplicate reconciliation, direct-main placement, and recovery from an interrupted creation transaction.
- Any governed-definition mutation is preceded by a successful exact-path approval-manifest check.

## Dependencies

None.

## Verification

- Run focused file-provider and claim/worktree lifecycle tests.
- Run the applicable generated-definition freshness checks if governed definitions change.
- Exercise the direct-main creation workflow in a disposable repository.
- Obtain fresh independent review.

## Notes

Until this feature is delivered, the current short backlog-domain claim requirement remains in force. This Ready item is not authorization to change a governed canonical definition without a user-approved exact scope and approval record.
