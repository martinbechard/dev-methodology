# Launch Work Items Through Visible Codex Tasks

Status: Starting

Type: Defect

Provider: file

Work Item ID: launch-work-items-through-visible-codex-tasks

Completion: main-branch

## Summary

Make every dispatched Work Item start through one user-visible Codex task before that task launches its Dev Orchestrator collaboration subagent.

## Source Evidence

On 2026-08-13, the user corrected the Backlog Dispatcher launch architecture. The root Dispatcher must create a visible Codex task in the project list. The task's initial prompt must instruct it to launch the Dev Orchestrator subagent for the authoritative provider record. The root Dispatcher must not directly launch that hidden collaboration execution as the Work Item launch.

## Requirements

- Update `.agents/skills/backlog-dispatcher/SKILL.md` concisely.
- Define the canonical Work Item runtime identity as the user-visible Codex task created by the root Dispatcher.
- Require that task's initial reference-plus-delta prompt to launch one Dev Orchestrator collaboration subagent for the authoritative provider record.
- Prohibit the root Dispatcher from directly spawning the Dev Orchestrator collaboration execution as the Work Item launch.
- Keep lifecycle and phase titles on the visible Codex task.
- Preserve exact task-creation reconciliation, duplicate prevention, and the distinction between task creation and Starting -> Running acceptance.
- Add focused contract tests in `scripts/test_codex_task_control.py`.
- Do not expand this correction into design, role, generated-output, or broad bundle-documentation updates; route those dependent artifacts separately when required.

## Acceptance Criteria

- Focused tests reject direct hidden collaboration launch by the root Dispatcher.
- Focused tests require visible Codex task creation before the nested Dev Orchestrator launch.
- The initial task prompt remains strict reference-plus-delta and names the authoritative provider locator.
- The visible Codex task owns lifecycle and phase title synchronization.
- Existing live hidden executions are preserved without duplicate implementation.
- Fresh independent skill review and focused verification pass.

## Dependencies

None.

## Verification

- Validate `.agents/skills/backlog-dispatcher/SKILL.md` through the configured skill validator.
- Run focused `scripts.test_codex_task_control` tests.
- Run Git diff whitespace validation.
- Obtain fresh independent skill review and verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- `.agents/skills/backlog-dispatcher/SKILL.md`

### Allowed Dependent Artifacts

- `scripts/test_codex_task_control.py`

### Approval Resolution

Approved at creation. On 2026-08-13, the user explicitly requested the concise Backlog Dispatcher skill correction and focused tests for this launch architecture.

## Notes

- Existing `/root/document_external_cleanup` and `/root/parse_nested_uar_report_fields` executions remain their Work Items' preserved owners until they stop or complete. Do not create visible replacement tasks while either execution is live.
- Apply the corrected architecture to every new dispatch after this item is delivered.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T01:59:39Z.
- Parent Runtime Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Intended Visible Task Role: runtime launch wrapper for one Dev Orchestrator collaboration subagent.
- Baseline: `73af4876cfddc725ad1599f8d2f7c3a3e04b2587` on primary `main`.
- Dispatch Reservation: Exactly one user-visible Codex task in the saved dev-methodology project. Its initial reference-plus-delta prompt launches the nested Dev Orchestrator collaboration subagent for this provider record.
- Capacity and Overlap: Immediate policy correction is authorized alongside the two preserved live executions. Its exact source and focused-test paths do not overlap their mutation scope.
- Transition Claim: `start-visible-codex-task-dispatch-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `11915b40-70c9-45e5-8e46-b445dee56fa9`.
- Next Reconciliation: Reconcile the exact visible task-creation result. Task creation does not establish Running; the nested Dev Orchestrator records Starting -> Running before mutation.
