# Keep User Decisions In Visible Worker Tasks

Status: Ready

Type: Defect

Provider: file

Work Item ID: keep-user-decisions-in-visible-worker-tasks

Completion: main-branch

## Summary

Correct the private Backlog Dispatcher contract so a canonical visible worker task owns its User Action Required question while the dispatcher continues unrelated eligible work.

## Context

The dispatcher currently lacks an explicit rule that keeps a user decision in the worker's visible conversation. Without that rule, the root dispatcher can become the waiting conversation and incorrectly hold unrelated capacity.

## Source Evidence

On 2026-08-13, the user explicitly required that the visible worker task enter User Action Required, receive a governed `Waiting for User` title, and ask the exact question with clear examples or options. The user also required the root Backlog Dispatcher to preserve that task while continuing unrelated eligible Work Items because User Action Required does not consume active execution capacity.

## Requirements

- Update `.agents/skills/backlog-dispatcher/SKILL.md` concisely.
- Require the canonical visible worker task to remain the user-facing decision context.
- Require a governed `Waiting for User` title and a clear worker-authored question with concrete examples or options.
- Prohibit the root Backlog Dispatcher from becoming the waiting conversation or replacing the preserved worker task.
- State that User Action Required releases active execution capacity while preserving the canonical task, candidate, provider evidence, and resumption context.
- Add directly focused regression coverage in `scripts/test_codex_task_control.py`.

## Acceptance Criteria

- The dispatcher contract assigns the question and waiting title to the canonical visible worker task.
- The dispatcher preserves and later resumes that same task after the answer.
- Unrelated eligible Work Items remain dispatchable while the item is User Action Required.
- Focused tests reject root-owned waiting, hidden-only questions, task replacement, and capacity retention.

## Dependencies

None.

## Verification

- Run the focused dispatcher contract tests in `scripts/test_codex_task_control.py`.
- Validate `.agents/skills/backlog-dispatcher/SKILL.md` with the configured skill validator.
- Run Git diff whitespace validation.
- Obtain fresh independent skill review and focused verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- `.agents/skills/backlog-dispatcher/SKILL.md`

### Allowed Dependent Artifacts

- `scripts/test_codex_task_control.py`

### Approval Resolution

The user explicitly authorized this exact concise dispatcher skill correction and focused tests on 2026-08-13.

## Notes

This item does not change provider lifecycle definitions or portable Dev Orchestrator authority. It corrects only the project-private dispatcher runtime contract.
