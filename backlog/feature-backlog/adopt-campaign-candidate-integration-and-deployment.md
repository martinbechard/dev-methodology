# Adopt Campaign Candidate Integration And Deployment

Status: Running

Type: Feature

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Adopt reviewed private candidates with one final campaign integration/deployment transaction.
- Dispatched At: 2026-07-25T01:04:58Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

## Execution Ownership

- Work-Item Thread: 019f96cf-48ef-7c41-bef1-ca69d574526c
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96cf-48ef-7c41-bef1-ca69d574526c
- Owner: Dev Orchestrator
- Branch: detached at reservation commit 97e8e20761619518d37ca5a17310836b4f4bf3b6
- Worktree: /Users/martinbechard/.codex/worktrees/1c8b/dev-methodology
- Phase: Persistence acceptance / canonical-manifest discovery
- Started At: 2026-07-25T01:09:02Z
- Coordination: Enabled; agent-claim short backlog transaction completed before this provider mutation.
- Claim Evidence: 019f96cf-48ef-7c41-bef1-ca69d574526c-backlog-running; agent-claim event ef24e4c8-e833-4434-a69b-94ebd69d2846; backlog scope on canonical primary main.

## Summary

Adopt a campaign delivery model in which overlapping work items produce reviewed and verified candidate commits in private worktrees, followed by one final integration and deployment work item that updates shared outputs once on primary main.

## Context

The user requested a model where overlapping work does not repeatedly regenerate or deploy shared outputs on main. Individual work items should keep their own implementation, independent review, verification, and candidate-commit evidence in private worktrees. A final campaign integration/deployment item should combine accepted candidates, reconcile conflicts, regenerate shared outputs once, validate integrated canonical skill paths, and complete the final primary-main transaction.

Source Evidence: The user message in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a beginning `I see that we have tasks waiting for each other...` and directing that file updates be completed first, followed by a final deployment work item.

## Requirements

- Define candidate-commit eligibility: scoped ownership, clean private worktree, fresh independent review, focused verification, and traceable acceptance evidence.
- Keep shared generated outputs, deployment, and primary-main integration out of overlapping item delivery unless the item is the designated campaign finalizer.
- Define one final campaign integration/deployment work item that selects accepted candidates, reconciles semantic conflicts, regenerates shared outputs once, validates integrated canonical skill paths, and commits the resulting primary-main state.
- Define stale-candidate handling: rebase or replay only after comparing canonical paths and rerunning affected review and verification; reject obsolete candidates with durable evidence.
- Preserve per-item review and verification evidence rather than substituting campaign-level acceptance for it.

## Acceptance Criteria

- The workflow identifies the only role and work item allowed to regenerate shared outputs and deploy on main for a campaign.
- Two overlapping candidate items can complete review and verification without touching shared generated outputs on main.
- The finalizer can integrate accepted candidates, resolve a semantic conflict with documented decisions, regenerate once, and pass integrated canonical-path validation.
- A stale candidate is either refreshed through the defined checks or rejected with a recoverable record.

## Dependencies

None.

## Verification

- Add focused workflow and lifecycle tests covering accepted candidates, semantic conflict reconciliation, stale-candidate rejection or refresh, and one-time generated-output regeneration.
- Exercise a multi-item disposable-repository campaign.
- Run applicable generated-output freshness checks and the final campaign validation gate.
- Obtain fresh independent review of per-item and finalizer behavior.

## Notes

This feature changes delivery coordination, not the authority of canonical definitions. Any governed definition mutation still requires an exact canonical-path approval manifest before editing.
