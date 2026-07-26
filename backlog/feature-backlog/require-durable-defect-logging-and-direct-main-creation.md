# Require Durable Defect Logging And Direct-Main Work-Item Creation

Status: Blocked

Type: Feature

Owner: Unowned

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One same-task resumption launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Require durable defect logging and define safe claim-free primary-main work-item creation.
- Dispatched At: 2026-07-25T02:35:39Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Existing canonical work-item Thread 019f96cf-226c-7f62-9d66-7d31cead822e is retained; no replacement task was created.

## Prior Execution Ownership

- Work-Item Thread: 019f96cf-226c-7f62-9d66-7d31cead822e
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96cf-226c-7f62-9d66-7d31cead822e
- Owner: Unowned
- Branch: Detached at 97e8e20761619518d37ca5a17310836b4f4bf3b6
- Worktree: /Users/martinbechard/.codex/worktrees/fa2b/dev-methodology
- Phase: Approved definition implementation / pre-mutation checks.
- Started At: 2026-07-25T01:34:57Z
- Prior Coordination Release: require-durable-defect-logging-running-019f96cf; acquire event b67710d6-d249-46e4-a44f-1ff6625f1b14; release event d25f25bb-d408-41b5-9396-edfe6b3197b2 after commit 126ee9befb575c4ebd1d4ddd00444616a8a48808.

## Blocked Handoff

- Status: Blocked
- Owner: Unowned
- Operational Claim: None
- Delivery Claim: None
- Canonical Work-Item Thread And Root Task: 019f96cf-226c-7f62-9d66-7d31cead822e
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Preserved Delivery Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/durable-defect-creation-coder-019f96cf
- Preserved Delivery Branch: codex/durable-defect-creation-coder-019f96cf
- Preserved Historical Branch HEAD: 32212af7d6751e3dd89d43485e2a355c1b3e3288
- Preserved Commits: 4f47fea91dc6f49b4f36d5c1360bf414fce2d852 and 957c93370c476bb3296151f979b5f1407362e7be
- Preserved Untracked Approval Records: approval-record-durable-defect-create-file-work-item.yaml and approval-record-durable-defect-dev-orchestrator.yaml remain only in the preserved private worktree.
- Superseded Claim-Free Portion: The four-path claim-free net behavior is superseded and must not be integrated, discarded, or carried forward. Its exact cumulative paths are skills/create-file-work-item/scripts/create.py, scripts/test_create_file_work_item.py, skills/agent-claim-command/scripts/claim.py, and scripts/test_agent_claim.py.
- Delivery Boundary: No primary integration occurred. No governed source mutation, generated mutation, test-policy mutation, or documentation-policy mutation occurred. Methodology Maintainer was interrupted before governed mutation.

### Exact Blocker And Dependency

Historical exact-file lifecycle task 019f9783-31a0-7e91-9704-08cde7886b3a is no longer User Action Required. Its canonical record is archived at backlog/completed-backlog/features/use-exact-work-item-claims-for-lifecycle-updates.md as Completed — superseded; that record identifies published policy/install evidence at main commit 6e59985b8cd0280e729f56eb8d2d362adf3f4ab6 and preserves its unaccepted candidate separately. The archive expressly transfers no accepted delivery, implementation, review, or completion baton to this item. This item's required direct current-main path mapping, semantic compatibility review, verification, release, and integration baton for its durable-defect/direct-main policy remain absent. Do not classify this technical dependency as User Action Required and do not log a duplicate defect for the already-recorded policy conflict.

### Unblock And Resumption

The parent Coordinator must reconcile the published policy at 6e59985b8cd0280e729f56eb8d2d362adf3f4ab6 with this item's exact requirements and supply a distinct current-main path mapping, supersession decision, semantic review, verification, release, and integration baton. Resume only through the same-task provider sequence Blocked -> Ready -> Starting -> Running; no direct Blocked -> Running transition is authorized. Retain this item's acceptance criteria and original exact user approval history as recovery context while the claim-free portion remains superseded.

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
