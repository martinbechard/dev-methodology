# Enforce Methodology Review Checklist Completion

Owner: Unowned

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: enforce-methodology-review-checklist-completion

Completion: main-branch

## Summary

Require Methodology Artifact Reviewer results to complete and save the existing structured-review checklist before returning findings.

## Context

The reviewer loaded the required checklist but returned NEEDS_CORRECTION findings without saving a completed checklist. Its findings also omitted the checklist question, authority, evidence, correction, and impact required by the existing template. The checklist already defines the required review method; this defect must enforce it without redesigning or expanding the checklist.

## Source Evidence

The user identified the incomplete Methodology Artifact Review on 2026-08-10 and clarified: “I only want it to use the existing checklist.”

## Requirements

- Clarify that read-only review prohibits changing the candidate, not writing the authorized checklist and findings artifacts.
- Add the completed existing checklist to the Methodology Artifact Reviewer output contract.
- Require every NEEDS_CORRECTION finding to reference its checklist question and retain the existing authority, evidence, correction, and impact fields.
- Treat a missing or incomplete saved checklist as an invalid review result.
- Do not add, redesign, or expand checklist questions.

## Acceptance Criteria

- A Methodology Artifact Reviewer cannot return a valid verdict before saving the completed existing checklist.
- Focused contract coverage rejects findings that are not derived from the saved checklist or omit its required fields.
- The existing structured-review checklist questions remain unchanged.

## Dependencies

None.

## Verification

- Run focused Methodology Artifact Reviewer role and evaluation-contract tests.
- Regenerate affected role projections through the repository-authorized generator and check freshness.
- Run Git diff checks.

## Open Questions

None.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T02:24:31Z

Coordinator: Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Normalized Objective: Enforce completion and saving of the existing Methodology Artifact Reviewer checklist before a verdict, without changing or expanding the checklist.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-11T02:39:31Z

Intended Root Role: Dev Orchestrator

## Running Evidence

Started At: 2026-08-11T02:26:58Z

Canonical Conversation: 019feea3-4792-7991-89c8-bcf35f814f25

Root Agent Task: 019feea3-4792-7991-89c8-bcf35f814f25

Parent Coordination: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: detached at 8ef7a1c45aa0bac1da17cad5fdec21d63a028235

Worktree: /Users/martinbechard/.codex/worktrees/f43a/dev-methodology

Phase: implementation

Accepted Execution Evidence: This canonical Root Dev Orchestrator accepted the Starting reservation and acquired the exact file-provider Work Item ID for outcome delivery.

## User Action Required

The initial review plus two correction retries are exhausted. The preserved candidate remains undelivered because its path validation accepts Windows-style parent escapes and drive-absolute paths for checklist artifacts.

## Question for the User

Do you authorize one additional bounded correction limited to rejecting Windows-style parent-escape and absolute checklist paths, adding focused negative tests, and then performing one final re-review and verification?

Asked At: 2026-08-11T03:47:04Z

Asked In: Parent coordination task 019fb057-1767-7ef2-b5fa-41f4417b20b3

## Why User Input Is Required

The agreed three-strikes review rule requires user action after the third failed review. Continuing would otherwise create an unauthorized fourth correction cycle.

## Resolution

Pending.

## Preserved Recovery State

Candidate: 795b3616

Exact blocker: Q012-Q016:runner-safe-relative-file-accepts-windows-path-escape.

Required correction: reject paths such as ..\\escape.md and C:/escape.md before resolving checklist or findings artifact locations.
