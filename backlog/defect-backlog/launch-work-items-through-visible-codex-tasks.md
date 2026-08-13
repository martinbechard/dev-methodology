# Launch Work Items Through Visible Codex Tasks

Status: Ready

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
