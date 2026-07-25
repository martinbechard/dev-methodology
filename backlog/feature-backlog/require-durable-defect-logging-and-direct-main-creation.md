# Require Durable Defect Logging And Direct-Main Work-Item Creation

Status: Running

Type: Feature

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Require durable defect logging and define safe claim-free primary-main work-item creation.
- Dispatched At: 2026-07-25T01:04:42Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Accepted as canonical work-item Thread 019f96cf-226c-7f62-9d66-7d31cead822e; canonical root task recorded below.

## Execution Ownership

- Work-Item Thread: 019f96cf-226c-7f62-9d66-7d31cead822e
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96cf-226c-7f62-9d66-7d31cead822e
- Owner: Dev Orchestrator
- Branch: Detached at 97e8e20761619518d37ca5a17310836b4f4bf3b6
- Worktree: /Users/martinbechard/.codex/worktrees/fa2b/dev-methodology
- Phase: Approval manifest ready; awaiting user approval.
- Started At: 2026-07-25T01:34:57Z
- Coordination: Enabled; agent-claim short backlog transaction completed before this provider mutation.
- Claim Evidence: require-durable-defect-logging-running-019f96cf; agent-claim event b67710d6-d249-46e4-a44f-1ff6625f1b14; resource backlog:mutation:require-durable-defect-logging-and-direct-main-creation.

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
