# Log Every Confirmed Incorrect State Before Closeout

Status: Running

Type: Defect

Provider: file

Work Item ID: log-every-confirmed-incorrect-state-before-closeout

Completion: direct-main

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Require a durable, duplicate-reconciled record for every confirmed incorrect state before closeout, including correction of the stale completed skill-group series index.
Dispatch Time: 2026-08-05T22:37:35Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Effective Commit Selector: complete-work-item-direct-main.
Canonical Runtime Evidence: None at reservation time. The parent Coordinator must reconcile this reservation before creating one canonical work-item Thread.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-confirmed-defect-closeout-019fb4 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 61488f73-df6a-49ee-a76e-8622bb304cc4.
Required Next Lifecycle Transition: The canonical root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

## Current Execution Ownership

Transition: Starting -> Running.
Canonical Thread: 019fd414-a82c-75e3-b8e3-98af21bb06bd.
Root Agent Task: /root.
Owner: Dev Orchestrator.
Branch: codex/log-every-confirmed-incorrect-state-closeout-019fb057.
Worktree: /Users/martinbechard/.codex/worktrees/589e/dev-methodology.
Phase: Discovery.
Started At: 2026-08-05T22:41:15.338523Z.
Claim Evidence: Exact-file claim record-running-confirmed-defect-closeout-019fb057 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 88535e40-1e2c-4b82-83a7-53773d92f1e9.

## Summary

Require every confirmed incorrect state to receive a durable, duplicate-reconciled record before a task closes. A task must not merely mention a confirmed defect as a residual issue and leave it untracked.

## Context

The Dev Orchestrator already requires durable recording of defects confirmed by independent review, verification, runtime evidence, or an accepted reproduction. That rule did not govern a direct documentation task closeout on 2026-08-05.

The task confirmed that backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md remained under the active feature backlog even though all ten required child work items had been archived as Completed. This contradicts the Terminal Series Archive contract in skills/manage-file-work-items/SKILL.md, which requires a completed series index to move to backlog/completed-backlog/features/apply-object-oriented-skill-group-design/index.md and prohibits an index-only series folder from remaining active.

The final task response reported the stale index but did not reconcile it with an existing durable defect or create a new defect. The incorrect state was therefore acknowledged and ignored by the work-item workflow.

## Source Evidence

- On 2026-08-05, after the direct task verified the completed skill-group work and updated the grouping documentation, current repository evidence showed one active index at backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md and ten corresponding child records under backlog/completed-backlog/features.
- The same task explicitly reported that the active index contained obsolete links and statuses, but created no durable defect before closing.
- The user then directed in the same Codex conversation: "create a defect - when something incorrect is detected, we must always log it rather than ignoring it".
- This direct request authorizes creation of this active defect. It authorizes logging and later correction of the recorded behavior; it does not start implementation in the creation transaction.

## Requirements

- Establish one shared closeout rule that applies whenever an agent confirms an incorrect state, including direct tasks that do not run through the Dev Orchestrator workflow.
- Before closeout, reconcile the finding with an existing durable provider record or create one new defect through the effective Persistence-selected creation procedure.
- Record the reproduction evidence, affected artifact or behavior, impact, and runnable next action so another task can act without the originating conversation.
- Keep a confirmed defect visible even when it can be corrected within the current authorized scope. The durable record may be the current authoritative work item when it preserves the finding and correction evidence; otherwise create or reconcile a distinct defect item.
- Never downgrade, omit, or leave a confirmed defect only in conversational prose to avoid durable recording.
- Preserve duplicate detection. Reuse the canonical Work Item ID when the same defect is already tracked rather than creating another item.
- Distinguish confirmed incorrect behavior from suspicion, an open question, expected behavior, an accepted limitation, or an already tracked issue with no new outcome.
- When the effective provider is unavailable, UNSET, or cannot persist the record, report the closeout as Blocked with the preserved finding instead of silently completing.
- Reconcile the concrete stale apply-object-oriented-skill-group-design series index with the terminal-series archival contract, including its index links and every explicit child Series backlink.
- Update the applicable agent, shared skill, project-directive, generated, documentation, and evaluation surfaces from their authoritative sources after discovery identifies the smallest coherent contract owner.

## Acceptance Criteria

- A direct task that confirms an incorrect state cannot report successful closeout until the finding has a canonical durable record or the inability to create that record is reported as Blocked.
- The Dev Orchestrator and direct-task closeout paths use the same definition of a confirmed defect and the same duplicate-reconciled recording obligation.
- A confirmed defect corrected within the current task still has durable finding and correction evidence; a confirmed out-of-scope defect has a separate runnable record.
- An unconfirmed observation, expected state, accepted limitation, or exact duplicate does not create a misleading new defect.
- The final user-facing closeout identifies the canonical Work Item ID for every confirmed defect that was not already visible through the current work item.
- backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md no longer remains as an active index-only terminal series. The archived index and all explicit child backlinks resolve to canonical terminal paths without changing child completion evidence.
- Focused evaluations reproduce the missed direct-task case, duplicate reconciliation, current-scope correction, provider-unavailable blocking, and the unconfirmed-observation boundary.
- Supported generated artifacts are current, the affected skill and agent definitions validate, focused tests pass, and independent review confirms that the rule does not manufacture defects from uncertainty.

## Dependencies

None.

## Verification

- Add a focused regression scenario in the evaluation surface that owns direct task closeout and rerun its individual evaluation.
- Rerun the Dev Orchestrator confirmed-defect scenarios to prove the existing path remains coherent with the shared rule.
- Add or update focused contract assertions in scripts/test_bundle_content.py for the authoritative source and supported generated outputs.
- Run the terminal-series reporter tests that cover completed-series archival, reciprocal links, and prevention of active index-only folders.
- Validate every changed skill package and conceptual agent source, regenerate only their supported artifacts, and run freshness checks.
- Run git diff --check and obtain fresh independent review and verification.

## Open Questions

- Identify the smallest shared contract owner that governs both direct task closeout and Dev Orchestrator closeout without duplicating the rule across unrelated skills or agent definitions.
- Determine whether the direct-task evaluation belongs to an existing general communication or maintenance contract or requires a focused root-task closeout fixture.

## Notes

- This item records a regression and coverage gap in the completed durable-defect policy; it does not reopen or duplicate backlog/completed-backlog/features/require-durable-defect-logging-and-direct-main-creation.md.
- The stale series index is the accepted reproduction for this defect and is not a separate dependency.
- Creation of this item does not authorize mutation of a newly discovered governed skill or agent-definition path. Record the smallest exact manifest and obtain any scope-specific approval required by the governing workflow before such mutation.
