# Require Durable Defect Logging And Direct-Main Work-Item Creation

Status: Ready

Type: Feature

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
