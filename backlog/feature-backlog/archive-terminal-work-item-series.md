# Archive Terminal Work-Item Series

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/archive-terminal-work-item-series.md

Completion: direct-main

## Summary

Define and enforce terminal archival for related work-item series so a completed or failed series no longer leaves its coordination folder under an active typed backlog.

## Context

The file-provider methodology defines how to create a related item series, derive its lifecycle from required children, keep its index current, and archive each child. It does not currently state when or how to archive the series folder and index after the derived series reaches a terminal state.

On 2026-07-29, four completed feature-series folders remained under backlog/feature-backlog after all of their children had been archived. Commit b5a48776d8dca621f4dc069e8805b4d924fe3abc moved those indexes under backlog/completed-backlog/features and repaired their links. That cleanup exposed the missing steady-state contract: terminal series maps must move out of active queues along with their terminal outcomes.

The implementation changes a governed distributed skill definition. The exact approved canonical source and dependent scope are recorded below. Before mutating the governed source, create the approval record named below and run the repository-supported definition-change precheck against the exact canonical path.

## Source Evidence

- On 2026-07-29 in Codex task 019faebe-b3cd-7ad0-b2b6-7a0abedf9787, the user stated: "this is not good, those folders should also be archived".
- After the methodology gap and the exact governed path skills/manage-file-work-items/SKILL.md were identified, the user directed: "ok create a workitem for this".
- Creation authority: the second statement explicitly requests this work item, and the combined statements authorize the exact series-archival outcome recorded here.
- Backlog creation claim: create-archive-terminal-series-item-019faebe; outcome SHARED_CHECKOUT_ACQUIRED; event 1dc83534-54e4-4604-9299-23cb8f8e5f21; exact destination backlog/feature-backlog/archive-terminal-work-item-series.md.

## Requirements

- Update the file-provider management contract so a series index remains in the active typed backlog only while the derived series is nonterminal.
- Define deterministic archive destinations for a terminal series folder and index:
  - a completed series goes under the matching backlog/completed-backlog type folder;
  - a failed or abandoned series goes under the matching backlog/failed-backlog type folder.
- Preserve the stable series slug and index.md coordination role at the archive destination.
- Require the terminal series transaction to keep the index links and every child Series reference aligned with the children’s canonical archive paths and the index’s canonical archive path.
- Define behavior for successful children, intentionally abandoned children, required terminal failures, and mixed nonterminal child states without collapsing mixed states prematurely.
- Require exact source and destination path ownership before moving a series index or updating child backlinks.
- Keep the series index non-runnable and do not add an independent lifecycle Status field to it.
- Update focused validation so active reports do not present a terminal series as active and archived series navigation remains complete.
- Regenerate only the supported distributed-skill mirror owned by the approved canonical source.
- Preserve the existing child-level terminal evidence and archive rules.

## Acceptance Criteria

- skills/manage-file-work-items/SKILL.md explicitly requires terminal series folders and indexes to leave active typed backlogs.
- The contract identifies the completed and failed archive destinations and the event that triggers the series move.
- The contract specifies how to update the archived index links and child Series references without changing child provider outcomes.
- A completed or failed series cannot leave an index-only folder under an active typed backlog.
- Nonterminal and mixed-state series remain in their appropriate nonterminal locations and retain exact child-state reporting.
- Focused tests cover completed-series archival, failed-series archival, mixed/nonterminal retention, link preservation, and prevention of orphaned active index folders.
- The supported generated skill-definition mirror matches the canonical source.
- The definition-change precheck accepts the approval record for exactly skills/manage-file-work-items/SKILL.md.
- Applicable focused tests and git diff --check pass.
- Independent review confirms the implementation does not broaden lifecycle authority or treat the index as a runnable work item.

## Dependencies

None.

## Verification

- Run the definition-change precheck:

```bash
python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change skills/manage-file-work-items/SKILL.md --approval-record approval-record-archive-terminal-series-manage-file-work-items.yaml
```

- Run focused manage-file-work-items contract assertions in scripts/test_bundle_content.py.
- Run focused backlog-report tests in scripts/test_generate_backlog_report.py.
- Regenerate the supported skill-definition mirror and verify source-to-generated freshness.
- Verify archived index links and child Series references with positive completed and failed cases plus negative nonterminal and mixed-state cases.
- Run git diff --check.
- Obtain fresh independent methodology review and verification before direct-main integration.

## Open Questions

- Determine whether the final child transition and series-index archival must be one atomic provider transaction or two serialized transactions with explicit recovery evidence.
- Determine the minimum child-backlink update set when children have already been archived across completed and failed type folders.

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-file-work-items/SKILL.md

### Allowed Dependent Artifacts

- approval-record-archive-terminal-series-manage-file-work-items.yaml
- design/generated/skill-definitions.js
- scripts/test_bundle_content.py
- scripts/generate-backlog-report.py only if report behavior must change to enforce the approved contract
- scripts/test_generate_backlog_report.py
- Directly related non-governed documentation only when required to keep the approved series-archival contract accurate

No other governed skill definition, conceptual agent definition, schema, model input, metadata definition, or generated definition family is approved.

### Approval Resolution

Approved at creation on 2026-07-29.

Exact user wording and provenance:

- "this is not good, those folders should also be archived" in Codex task 019faebe-b3cd-7ad0-b2b6-7a0abedf9787.
- "ok create a workitem for this" in the same task after the exact governed source skills/manage-file-work-items/SKILL.md and its supported generated mirror and focused tests were identified.

The approval covers exactly the governed canonical source listed above and only the allowed dependent artifacts listed separately. Additional governed paths require new explicit, scope-specific user approval.

## Notes

## Missed-Settlement Reconciliation

Transition: Starting -> Ready.
Reconciled At: 2026-07-29T17:38:47Z.
Settlement Deadline: 2026-07-29T17:36:38Z.
Canonical Conversation and Root Agent Task: 019faeef-e932-7352-a53d-fdb1535f5994.
Owner: Unowned.
Canonical Acceptance: None observed.
Source Mutation Evidence: None observed.
Required Resumption: Reuse the same canonical task through a new Ready -> Starting -> Running sequence.
Reconciliation: Ready.

## Historical Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: 019faeef-e932-7352-a53d-fdb1535f5994.
Launch Reservation: One synchronized bounded launch reservation in the adaptive-capacity batch.
Normalized Objective: Archive terminal work-item series.
Dispatch Time: 2026-07-29T17:35:38Z.
Intended Root Role: Root Dev Orchestrator.
Canonical Conversation and Root Agent Task: 019faeef-e932-7352-a53d-fdb1535f5994.
Direct Conversation-Title Handoff: Archive Terminal Work-Item Series.
Branch: codex/archive-terminal-work-item-series-019faeef.
Worktree: /Users/martinbechard/.codex/worktrees/2d69/dev-methodology.
Owner: Unowned pending accepted root.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T17:35:38Z to 2026-07-29T17:36:38Z (exactly 60 seconds; shared adaptive-capacity batch window).
Runtime Launch Result: Direct conversation-title handoff accepted for the synchronized batch.
Canonical Conversation: 019faeef-e932-7352-a53d-fdb1535f5994.
Owner Acceptance: Pending.
Reconciliation: Pending.

## Current Dispatch Reservation

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One parent-coordinator launch reservation; no runtime work-item Thread has been created by this reservation.

Normalized Objective: Archive terminal work-item series.

Dispatch Time: 2026-08-05T14:17:30.754473Z.

Intended Root Dev Orchestrator: Dev Orchestrator.

Runtime Launch Evidence: None. This provider transaction reserves capacity only and does not create or accept a runtime task.

Owner: Unowned.

Reconciliation: Starting reservation recorded by the parent Coordinator's Dev Backlog Steward.

## Running Acceptance

Transition: Starting -> Running.

Canonical Thread and Root Agent Task: 019faeef-e932-7352-a53d-fdb1535f5994.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Owner: Root Dev Orchestrator.

Branch: codex/archive-terminal-work-item-series-019faeef.

Worktree: /Users/martinbechard/.codex/worktrees/2d69/dev-methodology.

Observed HEAD at Acceptance: 2879c116fe637224ec181b93e966e5a1ee3022a6.

Phase: implementation / root-execution.

Started At and Acceptance Evidence: Root Dev Orchestrator accepted ownership at 2026-08-05T14:19:49Z.

Provider Mutation Claim: starting-running-archive-terminal-series-019faeef; outcome SHARED_CHECKOUT_ACQUIRED; event 77005449-442c-41f4-b4f4-2bfb16362592; exact path backlog/feature-backlog/archive-terminal-work-item-series.md.

Reconciliation: Canonical root ownership accepted; this transaction records the required provider lifecycle transition before governed-source mutation.

- Commit b5a48776d8dca621f4dc069e8805b4d924fe3abc is migration evidence, not a substitute for the steady-state contract and regression tests.
- Do not reintroduce a Status field on index.md merely to make terminal state visible; derive series state from required children and use archive location as terminal evidence.
