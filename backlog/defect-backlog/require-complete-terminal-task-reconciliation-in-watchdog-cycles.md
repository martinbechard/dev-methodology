# Require Complete Terminal Task Reconciliation in Watchdog Cycles

Status: Ready

Type: Defect

Provider: file

Work Item ID: require-complete-terminal-task-reconciliation-in-watchdog-cycles

Completion: direct-main

## Summary

Make every Dev Backlog Watchdog cycle reconcile all terminal tasks associated with the observed Coordinator campaign before it can report NO_ACTION, and send one aggregate parent alert for every actionable terminal anomaly.

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
- Evaluate provider terminal evidence, live and released claims, worktree disposition, delivery and cleanup branch disposition, deliberately preserved source branches, unresolved notifications, Codex archival state, and any current user archive pause.
- Define an archive pause as suppressing only Codex task archival. It must not suppress Git cleanup eligibility, worktree or branch cleanup alerts, provider closeout alerts, or other terminal reconciliation.
- Distinguish an ordinary cleanup-eligible branch from a deliberately preserved non-ancestral or non-equivalent source branch whose current evidence-backed disposition requires retention.
- Remove a clean terminal worktree when authorized even when its associated source branch must remain deliberately preserved.
- Send one aggregate parent alert covering every actionable terminal anomaly found in the cycle, with exact task, provider, worktree, branch, claim, archival, and next-action evidence.
- Do not repeatedly alert for a deliberately preserved resource while its current evidence-backed disposition remains unchanged. Alert again only when its evidence or required action changes.
- Prohibit NO_ACTION whenever any terminal task has an unacknowledged cleanup, closeout, notification, preservation, or archival action.
- Keep the Watchdog strictly read-only. The parent Coordinator remains responsible for cleanup, provider recovery, task archival decisions, and user archive-pause reconciliation.

## Acceptance Criteria

- A focused scenario with an active archive pause and an otherwise cleanup-eligible terminal worktree or branch produces one actionable aggregate parent alert; it does not suppress Git cleanup because task archival is paused.
- A fully clean terminal task without an archive pause produces an archival notification when the Codex task remains unarchived.
- A terminal task with a non-ancestral or non-equivalent source branch records that branch as deliberately preserved while still reporting its clean worktree as independently removable.
- A cycle containing multiple terminal anomalies emits one aggregate parent alert that names every anomaly and the smallest action for each, rather than stopping after the first finding or sending fragmented alerts.
- NO_ACTION is emitted only after every terminal task in the observed Coordinator campaign has complete provider, claim, worktree, branch, notification, preservation, and archival reconciliation, including any acknowledged archive pause.
- Unchanged evidence-backed preservation decisions do not generate repeat alerts, while changed evidence or a newly actionable cleanup condition does.
- The Watchdog remains read-only and no test or implementation grants it lifecycle, cleanup, claim, task archival, or repository mutation authority.

## Dependencies

None.

## Verification

- Add focused Dev Backlog Watchdog scenarios and fixtures for archive-pause scope, archival notification, independently removable worktrees, deliberately preserved non-equivalent branches, aggregate anomaly reporting, alert deduplication, and complete NO_ACTION reconciliation.
- Update the focused requirements matrix and executable Watchdog simulator or tests only where they directly consume the approved contract.
- Add exact bundle assertions for the terminal reconciliation, archive-pause, aggregate-alert, and NO_ACTION boundaries.
- Regenerate only affected design documentation and supported adapter outputs from the approved canonical sources.
- Validate each changed governed source, run the focused Watchdog suite and affected freshness checks, and run git diff --check.
- Obtain fresh independent review and verification of the read-only authority boundary and complete terminal-set behavior.

## Open Questions

None.

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
