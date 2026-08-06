# Require Complete Terminal Task Reconciliation in Watchdog Cycles

Status: Running

Type: Defect

Provider: file

Work Item ID: require-complete-terminal-task-reconciliation-in-watchdog-cycles

Completion: direct-main

## Summary

Make every Dev Backlog Watchdog cycle reconcile all terminal tasks associated with the observed Coordinator campaign before it can report NO_ACTION, send one aggregate parent alert for every actionable terminal anomaly, and require Codex task archival by default after merged delivery and ordinary terminal gates pass.

## Context

Recent Watchdog cycles detected completed provider items while their clean worktrees, delivery or cleanup branches, task archival state, and archive-pause implications remained only partially reconciled. Individual alerts were delivered incrementally, requiring the user to identify additional completed tasks and clarify that pausing Codex task archival does not pause ordinary Git cleanup.

The Watchdog already observes provider, Git, claim, and Codex task state. Its terminal reconciliation must therefore evaluate the complete terminal set for the observed Coordinator campaign rather than stopping after the first anomaly or treating an archival pause as a blanket cleanup pause.

## Source Evidence

On 2026-08-06, in the dedicated Dev Backlog Watchdog conversation, the user challenged the incomplete terminal reconciliation:

> OK how come I have to point this out ? Do your instructions include checking for complete tasks to notify the dispatcher

The user then asked whether the durable Watchdog instructions needed correction:

> ok do we need to update skills for future instances of the watchdog?

After reviewing the exact proposal covering the three governed canonical sources listed below, the user explicitly authorized this defect:

> ok create the defect in the backlog

This direct request authorizes creation of this Ready Defect and modification of exactly the governed sources named in Governed Definition Approval.

## Requirements

- Require every Watchdog cycle to identify every terminal Codex task associated with the observed Coordinator campaign and reconcile each task independently.
- Evaluate provider terminal evidence, live and released claims, worktree disposition, delivery and cleanup branch disposition, deliberately preserved source branches, unresolved notifications, Codex archival state, and any explicit current user pause scoped to named Codex task archival.
- Archive each completed Codex task by default after its delivery is merged and its ordinary terminal reconciliation gates pass.
- Never infer, inherit, carry forward, or persist a campaign-wide archival pause from earlier conversation or another task. Treat a pause as valid only when current explicit user direction names its task-archival scope and the Watchdog can record and acknowledge that exact scope and evidence.
- Define a valid scoped archive pause as suppressing only the named Codex task archival. It must not suppress Git cleanup eligibility, worktree or branch cleanup alerts, provider closeout alerts, notifications, or other terminal reconciliation.
- Distinguish an ordinary cleanup-eligible branch from a deliberately preserved non-ancestral or non-equivalent source branch whose current evidence-backed disposition requires retention.
- Remove a clean terminal worktree when authorized even when its associated source branch must remain deliberately preserved.
- Send one aggregate parent alert covering every actionable terminal anomaly found in the cycle, with exact task, provider, worktree, branch, claim, archival, and next-action evidence.
- Do not repeatedly alert for a deliberately preserved resource while its current evidence-backed disposition remains unchanged. Alert again only when its evidence or required action changes.
- Prohibit NO_ACTION whenever any terminal task has an unacknowledged cleanup, closeout, notification, preservation, or archival action.
- Keep the Watchdog strictly read-only. The parent Coordinator remains responsible for cleanup, provider recovery, task archival decisions, and user archive-pause reconciliation.

## Acceptance Criteria

- A focused scenario with an explicit current pause scoped to one named Codex task and an otherwise cleanup-eligible terminal worktree or branch produces one actionable aggregate parent alert; it suppresses only that named task archival and does not suppress Git cleanup.
- A fully clean terminal task without an explicit current scoped pause produces an archival action when the Codex task remains unarchived after merged delivery and ordinary terminal gates pass.
- A prior conversational pause, an inherited campaign-wide pause, or a pause without current named-task scope and recorded evidence is invalid and cannot suppress the default archival action.
- A terminal task with a non-ancestral or non-equivalent source branch records that branch as deliberately preserved while still reporting its clean worktree as independently removable.
- A cycle containing multiple terminal anomalies emits one aggregate parent alert that names every anomaly and the smallest action for each, rather than stopping after the first finding or sending fragmented alerts.
- NO_ACTION is emitted only after every terminal task in the observed Coordinator campaign has complete provider, claim, worktree, branch, notification, preservation, and archival reconciliation, including exact acknowledgement of any valid current named-task archival pause.
- Unchanged evidence-backed preservation decisions do not generate repeat alerts, while changed evidence or a newly actionable cleanup condition does.
- The Watchdog remains read-only and no test or implementation grants it lifecycle, cleanup, claim, task archival, or repository mutation authority.

## Dependencies

None.

## Verification

- Add focused Dev Backlog Watchdog scenarios and fixtures for default archival, rejection of inferred or inherited pauses, explicit current named-task pause scope and evidence, archival notification, independently removable worktrees, deliberately preserved non-equivalent branches, aggregate anomaly reporting, alert deduplication, and complete NO_ACTION reconciliation.
- Update the focused requirements matrix and executable Watchdog simulator or tests only where they directly consume the approved contract.
- Add exact bundle assertions for the terminal reconciliation, archive-pause, aggregate-alert, and NO_ACTION boundaries.
- Regenerate only affected design documentation and supported adapter outputs from the approved canonical sources.
- Validate each changed governed source, run the focused Watchdog suite and affected freshness checks, and run git diff --check.
- Obtain fresh independent review and verification of the read-only authority boundary and complete terminal-set behavior.

## Open Questions

None.

## Contract Correction Evidence

Recorded At: 2026-08-06T17:14:41Z.

Source: Direct user correction in canonical task 019fd80b-9089-78c0-9272-26ac6b7d47ff under parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Controlling Rule: Once code is merged and ordinary terminal reconciliation gates pass, archive the completed Codex task by default. Do not infer, carry forward, or persist a campaign-wide archival pause. A pause is valid only from explicit current user direction scoped to named task archival with exact scope and evidence recorded and acknowledged, and it suppresses no provider closeout, worktree cleanup, branch cleanup, notification, or other terminal reconciliation.

Scope Confirmation: This correction remains within the three already approved governed canonical sources and the bounded dependent artifacts listed below. It authorizes no additional governed definition.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-06T17:06:55Z

Coordinator: Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Normalized Objective: Require complete campaign-wide terminal reconciliation, aggregate every actionable terminal anomaly, scope archive pauses only to task archival, and prohibit NO_ACTION while unacknowledged terminal cleanup remains.

Launch Result: Started.

Canonical Conversation: 019fd80b-9089-78c0-9272-26ac6b7d47ff.

Last Contact At: 2026-08-06T17:10:29Z.

Next Reconciliation At: 2026-08-06T17:24:29Z.

Intended Root Role: Dev Orchestrator.

## Current Running Evidence

Transition: Starting -> Running.

Owner: Root Dev Orchestrator in task 019fd80b-9089-78c0-9272-26ac6b7d47ff.

Canonical Conversation: 019fd80b-9089-78c0-9272-26ac6b7d47ff.

Codex Task ID: 019fd80b-9089-78c0-9272-26ac6b7d47ff.

Root Agent Task: /root.

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Branch: codex/require-complete-terminal-reconciliation-019fd80b.

Worktree: /Users/martinbechard/.codex/worktrees/6db0/dev-methodology.

Phase: Independent focused verification.

Started At: 2026-08-06T17:10:29Z.

Accepted Execution Evidence: This canonical Root Dev Orchestrator task accepted the Coordinator handoff, established a clean work-item branch from main commit 654542af41884e28e340c0c1cb1bdcfa76931b48, and began the approved focused Watchdog correction under the exact governed-definition manifest.

Accepted Candidate Commit: 1f2ab0a3d71fe2a2c8a14c6ccdcd9035ff0cf391.

Candidate Checks: Watchdog simulator 31 tests passed; five exact bundle, design, and generated assertions passed; changed skills validated; Python compilation and generator freshness passed; diff checks passed. One unrelated broad catalog expected-count mismatch remains outside this item.

Next Action: Obtain the independent focused verifier verdict for candidate 1f2ab0a3d71fe2a2c8a14c6ccdcd9035ff0cf391, then prepare current-main direct-main integration only if verification passes.

## Active Execution Evidence

Condition Type: delegated-work.

Owner: Root Dev Orchestrator in task 019fd80b-9089-78c0-9272-26ac6b7d47ff.

Evidence: Independent Dev Verifier child /root/verify_terminal_reconciliation is verifying clean review-approved candidate 1f2ab0a3d71fe2a2c8a14c6ccdcd9035ff0cf391 through the bounded Watchdog simulator, exact bundle/design/generated assertions, supported validators and freshness checks, scope proof, and diff hygiene. Verification owns no mutation.

Observed At: 2026-08-06T17:51:56Z.

Started At: 2026-08-06T17:10:29Z.

Deadline or Expires At: 2026-08-06T18:51:56Z.

Next Action: Independent verifier returns PASS/READY or FAIL/BLOCKED with exact focused commands and evidence; no broad suite or live Codex cycle is permitted.

Next Reconciliation At: 2026-08-06T18:05:56Z.

Conversation Title Evidence: The canonical conversation is Verifying — Require Complete Terminal Reconciliation.

## Correction History

Attempt 1 Started At: 2026-08-06T17:33:36Z.

Reviewer Verdict: NEEDS_CORRECTION on candidate 1b07440ec4b875e6586c1da3921038ebc9d6c0c9.

Confirmed Finding 1: Failed and Abandoned tasks incorrectly required merged delivery, preventing truthful terminal reconciliation and NO_ACTION.

Confirmed Finding 2: A terminal Codex record without canonical task identity could incorrectly return NO_ACTION.

Residual Review Question: Reconcile whether the existing evidence model distinguishes no applicable claim from missing required released-claim evidence; add the smallest focused boundary when supported or preserve the exact residual risk.

Disposition: Both confirmed findings are returned to the original Dev Coder for correction in this delivery. No finding is excluded or deferred.

Correction Commit: 9cde838a3099dbbcfef235bd9f5bc86601d0cbe9.

Correction Result: Both confirmed findings are implemented in focused simulator coverage. The claim-evidence question is resolved through an explicit claim-applicability field so required release evidence is never fabricated or silently omitted.

Attempt 2 Started At: 2026-08-06T17:42:35Z.

Re-review Verdict: NEEDS_CORRECTION on candidate 9cde838a3099dbbcfef235bd9f5bc86601d0cbe9.

Confirmed Finding 3: Canonical skill and role language still imposed merged delivery on Failed and Abandoned even though the corrected simulator restricted that gate to Completed.

Confirmed Finding 4: Claim applicability defaulted to non-applicable, so missing applicability evidence could still allow NO_ACTION.

Residual Risk To Resolve: Changed-preservation alerts must expose enough acknowledged prior and current evidence to verify why the alert recurred.

Disposition: Both confirmed findings and the bounded residual risk are returned to the original Dev Coder for correction attempt 2. No finding is excluded or deferred. A later material failure of this same correction boundary will be handed to the parent Coordinator with preserved evidence rather than entering a third attempt.

Correction Attempt 2 Commit: 1f2ab0a3d71fe2a2c8a14c6ccdcd9035ff0cf391.

Correction Attempt 2 Result: Canonical and generated status-aware wording now matches the simulator; claim applicability is explicit tri-state; recurring preservation alerts retain acknowledged prior and current evidence; all focused candidate checks pass.

Final Independent Review: APPROVED candidate 1f2ab0a3d71fe2a2c8a14c6ccdcd9035ff0cf391 with no material findings, no open questions, exact approved scope, clean worktree, and deterministic simulator/source/generated coverage. No live Codex runtime cycle was run because the bounded read-only review scope prohibits it.

## Governed Definition Approval

### Governed Canonical Sources

- skills/coordinate-work-items/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml

### Allowed Dependent Artifacts

- Focused Dev Backlog Watchdog suite scenarios, fixtures, and requirements matrix entries that exercise terminal reconciliation.
- Focused Watchdog simulator and test files that directly consume the approved contract.
- Exact bundle-content assertions for terminal cleanup, archive-pause scope, aggregate alerts, deliberate preservation, and NO_ACTION.
- Affected hand-authored design documentation that explains the approved Watchdog behavior.
- Supported generated documentation and adapter outputs derived only from the three approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-06. The user accepted the immediately preceding exact proposal to update the Watchdog workflow and then directed, “ok create the defect in the backlog”. That request authorizes only the three governed canonical sources listed above and their bounded dependent artifacts. Any additional governed definition requires new exact-path approval.

## Notes

- Creation authority is the direct 2026-08-06 user request recorded in Source Evidence.
- Creation transaction timestamp: 2026-08-06T16:59:35Z.
- This item corrects future Watchdog behavior only. It does not itself authorize cleanup or archival of any current Codex task, worktree, or branch.
