# Keep User Decisions In Visible Worker Tasks

Status: Completed

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

## Starting Handoff Evidence

- Reserved At: 2026-08-13T11:36:41Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `ed426ee1a52b75038907dab97c4a61d8fd9ef4fa` on primary `main`.
- Dispatch Architecture: Create one user-visible Codex task whose initial reference-plus-delta prompt starts one Dev Orchestrator collaboration subagent for this provider record.
- Transition Claims: `start-visible-worker-uar-dispatcher-rule`; event `b636b7ab-11f2-4e23-b983-ae659017eea3`. `start-visible-worker-uar-provider`; event `6998554f-9a57-4dd2-aa6c-3317325a0c49`.
- Runtime Identity: Pending the caller-owned visible task creation result. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T11:42:03Z.
- Codex Task ID: `019ffaed-9208-7cb1-8564-b63317455fba`.
- Conversation ID: `019ffaed-9208-7cb1-8564-b63317455fba`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Keep User Decisions In Visible Worker Tasks`.
- Initial Action: Launch one Dev Orchestrator subagent for this authoritative provider record.
- Creation Outcome: Unique success with no client or pending ambiguity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-visible-worker-uar-rule-task`; event `6fb5f7f2-714b-4e4b-83a3-866c49ae1073`. `adopt-visible-worker-uar-rule-provider`; event `10c376cc-917f-4dce-8dab-13db7d3a5d54`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T11:43:16Z.
- Transition: `Starting -> Running`.
- Root Dev Orchestrator: `/root/keep_user_decisions_visible`.
- Canonical Codex Task ID: `019ffaed-9208-7cb1-8564-b63317455fba`.
- Work Claim: `keep-user-decisions-visible-work`; event `26adc248-6dfc-4369-bafc-2e62b0ad1b24`.
- Provider Mutation Claim: `keep-user-decisions-running-provider`; event `11b67e3a-d78b-4202-a12b-638161352ab0`.
- Complexity Gate: False. This is one routine source contribution lane with ordinary review, verification, and main-branch delivery only.

## Completion Evidence

- Completed At: 2026-08-13T13:04:44Z.
- Accepted Candidate: `e20cebf9ce84883262163489c18de6aeb284b6d7` on `candidate/keep-user-decisions-visible`.
- Integration Mapping: candidate commits `82b532a9ea777de3fe1f1e24c5bc023b052f8ce6`, `62b616ccddf01f155e5d8849a3f6d3982176ecd4`, and `e20cebf9ce84883262163489c18de6aeb284b6d7` were replayed as main commits `cdccd4c6`, `f6c31e8d`, and `bebf44d0`.
- Observed Main: `main` at `bebf44d0ebcabfce20b0143911acbdc3c4d42720`.
- Independent Source Review: PASS after two bounded correction cycles; final review found no blocking issue.
- Independent Verification: PASS; 38 focused tests, configured skill validation, diff whitespace, exact-path audit, ancestry, and clean candidate checks passed.
- Integrated Verification: PASS; 38 focused tests and configured skill validation passed on observed main. The integration changed only `.agents/skills/backlog-dispatcher/SKILL.md` and `scripts/test_codex_task_control.py`.
- Confirmed Issue Dispositions: outcome-classification and contradiction-test findings were corrected in this delivery. Coordinator-relay restoration was deliberately rejected because it contradicted the user-authorized project-private specialization and accepted architecture; it is not an excluded defect.
- Completion Disposition: READY through configured `main-branch` delivery with file Persistence terminal closure.
