# Explain User Action Required Requests With Examples

Status: Completed

Type: Feature

Owner: Unowned

Claim: None.

Provider: file

Provider Reference: backlog/completed-backlog/features/explain-user-action-required-with-examples.md

Completion: direct-main

## Summary

Require a clear user-facing explanation after the Coordinator selects User Action Required and the provider records that state.

## Requirements

- Ask one plain-language question.
- Explain why the user owns the answer.
- Give evidence-backed options or an illustrative example when useful.
- State the practical consequence of each option.
- State exactly what unattended work stops and what independent work may continue.
- Keep technical dependencies, missing tools, implementation failures, and agent-resolvable questions out of User Action Required.
- Preserve the same canonical task and do not repeat a recorded answer.

## Authority

The user approved changes to exactly these governed sources:

- agents/roles/dev-activities/dev-orchestrator.role.yaml
- skills/manage-file-work-items/SKILL.md

Supported generated mirrors and focused dependent documentation and tests were permitted.

## Superseded Recovery

Rejected candidates 31e52b0e, 0aa3d90f, and aec92b11 are historical only. Their natural-language semantic evaluator was not reused.

## Completion Evidence

- Implementation commit: 93446a49.
- Two focused User Action Required contract tests passed.
- Two existing focused bundle contract tests passed.
- Skill validation, role and skill generation freshness, evaluation-document freshness, Python compilation, and diff checks passed.
- The Codex user installation was refreshed.
- The installed manage-file-work-items skill and Dev Orchestrator agent match the committed source bytes.
