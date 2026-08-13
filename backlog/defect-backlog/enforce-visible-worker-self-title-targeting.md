# Enforce Visible Worker Self-Task Title Targeting

Status: Ready

Type: Defect

Provider: file

Work Item ID: enforce-visible-worker-self-title-targeting

Completion: main-branch

## Summary

Require each visible Work Item task to target only its own canonical Codex task and conversation identity for lifecycle and material-phase title operations.

## Context

Visible Work Item tasks sometimes target the delegation source or root Backlog Dispatcher task when synchronizing their own title. The root Dispatcher task `019ff2c3-1710-7aa1-89c4-9d6066f51fe4` has twice required correction back to `Backlog dispatcher`. The affected worker tasks retained their correct provider and runtime identities, so the incident is a title-target selection defect rather than a lifecycle mutation.

The visible task already owns its title and subagent messaging. Its title operation must use the exact canonical task and conversation identity recorded for that Work Item. The delegation source, runtime parent, `source_thread_id`, and root Dispatcher identity are evidence and routing fields only.

## Source Evidence

On 2026-08-13, the user requested a focused defect after a repeated root-title correction. The user required exact self-task title targeting, rejection of `source_thread_id` and root Dispatcher targets, preservation of current active work, and suppression evidence for repeated Watchdog alerts.

## Requirements

- Require a visible Work Item root task to use its own recorded canonical Task ID and Conversation ID for every self-title operation.
- Reject the delegation source, runtime parent, `source_thread_id`, root Dispatcher task, Coordinator task, nested Dev Orchestrator, and title-derived identities as self-title targets.
- Require an exact identity match before the title call and confirm the same identity afterward.
- Stop without mutation when the visible task cannot resolve its own canonical identity or when the target conflicts with provider evidence.
- Preserve the root Dispatcher title independently from worker lifecycle and material-phase titles.
- Add focused launch, title-target, and negative regression coverage for the visible-task architecture.

## Acceptance Criteria

- A visible worker task can synchronize its own governed title without changing the root Dispatcher title.
- Tests reject packets or runtime calls that use `source_thread_id`, runtime parent, or root Dispatcher identity as the worker's self-title target.
- Tests accept the exact canonical worker Task ID and Conversation ID recorded in the provider.
- Identity ambiguity produces zero title mutation and a specific Coordinator decision request.
- The repeated root-title incident has a durable suppression rule that distinguishes the corrected Dispatcher record from an unresolved worker-title mismatch.
- Changed skill sources validate and focused Codex task-control and dispatcher tests pass.

## Dependencies

None.

## Verification

- Run focused Codex task-control tests for exact self-identity targeting and rejected source/root identities.
- Run focused private Backlog Dispatcher launch and title-message contract tests.
- Validate each changed skill source.
- Regenerate only mechanically required projections and verify freshness.
- Run `git diff --check`.
- Obtain fresh independent review and verification.

## Open Questions

None.

## Governed Definition Approval

- Approved canonical sources: `.agents/skills/backlog-dispatcher/SKILL.md` and `skills/coordinate-codex-tasks/SKILL.md`.
- Allowed dependent artifacts: directly focused tests and mechanically required generated projections.
- Approval source: the user's explicit 2026-08-13 request to create and queue this focused enforcement defect.

## Notes

- This defect does not change provider lifecycle authority or permit title inference from text.
- Do not interrupt current Running work or rewrite historical runtime evidence.
- The existing corrected root Dispatcher title is terminal suppression evidence for this repeated alert; it is not an implementation candidate.
