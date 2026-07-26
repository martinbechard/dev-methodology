# Distinguish Coordination Notes From Unmet Dispatch Dependencies

Status: Running

Type: Defect

Owner: Root Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/distinguish-coordination-notes-from-unmet-dispatch-dependencies.md

Completion: direct-main

## Summary

Correct Coordinator inventory and file-provider lifecycle handling so coordination-only overlap notes do not make an otherwise Ready item ineligible for safe private-worktree dispatch.

## Context

The Coordinator left capacity idle after treating six Ready Defects as blocked by a referenced item. Each item said only to coordinate to avoid duplicate overlapping edits. The referenced item, backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md, is Blocked and Unowned, and the live claim registry had no matching claim. That wording is a scope and integration constraint, not a hard prerequisite for private-worktree implementation.

## Source Evidence

Direct user instruction in parent coordination task 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a on 2026-07-26: "add a workitem to fix the coordinator skill to avoid this kind of nonsense." The requested correction distinguishes hard prerequisites from coordination and overlap notes.

## Requirements

- Update codex-workitem-coordination and file-provider management behavior to classify a hard prerequisite separately from a coordination or overlap note.
- Keep an item with only coordination notes eligible for safe private-worktree implementation when the referenced item is Blocked or Unowned and has no live claim.
- Keep hard prerequisite dependencies ineligible until their prerequisite is satisfied.
- Prevent duplicate implementation and require scope and integration reconciliation for exact overlaps, serializing only the conflicting event when necessary.
- Report the distinction, eligibility decision, overlap constraint, and any deferred integration event clearly.
- Do not mutate governed definitions without the required exact path-specific user approval.

## Acceptance Criteria

- Focused regression coverage proves that an item with a hard unmet dependency remains ineligible for dispatch.
- Focused regression coverage proves that a coordination-only item remains eligible when its referenced item is Blocked or Unowned and has no live claim.
- Focused regression coverage proves exact overlap coordination occurs at integration without precluding private-worktree implementation.
- Focused regression coverage proves inventory and dispatch reporting clearly distinguish hard prerequisites from coordination notes.
- Focused tests and applicable file-provider lifecycle checks pass.
- Independent review confirms the implementation does not enable duplicate ownership or implementation.

## Dependencies

None.

## Verification

- Run focused codex-workitem-coordination regressions for hard prerequisites, coordination-only eligibility, exact-overlap integration, and reporting.
- Run focused manage-file-work-items or file-provider lifecycle regressions affected by the change.
- Run git diff --check.
- Obtain independent code and prompt review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Distinguish coordination notes from unmet dispatch dependencies.
- Dispatched At: 2026-07-26T17:08:29Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Current Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a (preserved from the Starting reservation).
- Canonical Work-Item Thread: 019f9f67-4487-75b3-89c4-3cbfbd83b640.
- Canonical Root Agent Task: /root.
- Root Dev Orchestrator: /root.
- Delivery Branch: Detached worktree base 7422fe5337f1b37cb9a1a6c1ec62580933db2e7c.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/6804/dev-methodology.
- Phase: Delivery accepted; this provider transaction contains no implementation artifact mutation.
- Started At: 2026-07-26T17:12:06Z.
- Claim Evidence: accept-running-distinguish-coordination-notes-019f95a9; acquire outcome SHARED_CHECKOUT_ACQUIRED; claim event 05d29f2c-e791-4a4a-a231-cd635a426cc1.

## Notes

This creation records requested Defect work only. It does not authorize implementation in this transaction.
