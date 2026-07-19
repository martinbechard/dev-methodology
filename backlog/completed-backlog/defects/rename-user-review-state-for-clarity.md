# Rename User Review To User Action Required

Status: Completed

Type: Defect

## Completion Evidence

- Running transition: 0611437.
- Reviewed implementation: 349b27d with accepted correction 11c0fae.
- Integrated artifact contract: b7ec746 after fresh contribution review, pre-integration verification, fresh post-integration review, and complete post-integration verification.
- Active-state migration: 893c5f8 changed all 19 live Status: Proposed items to Status: Ready in a status-only primary commit.
- Queue migration: 5bc5cec moved the canonical guidance to backlog/user-action-required, updated remaining backlog-local references, and preserved the resolved analysis question and Resolution exactly.
- Installed bundle: refreshed transactionally to the user-scoped Codex skills and agents, verified byte-for-byte against the integrated sources, and refreshed the MCP catalog to revision edc027b489a9bab62971f17c4ffac90a4dcf53e087bee5e77068e50230327f53.
- Final verification: all 401 repository script tests, all 17 project-wiki script tests, focused migration tests, skill validation, generated-output freshness checks, OpenAI metadata alignment, OKF validation, and git diff checks passed; no active Proposed status or stale canonical queue reference remains.

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: rename-user-review-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T04:47:14.696958Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately before implementation.

## Summary

Replace the ambiguous User Review queue name with User Action Required so readers immediately understand that progress needs a decision, approval, action, authority grant, or information from the user.

## Context

The current queue uses backlog/user-review and Status: User Review. That wording can be mistaken for ordinary code review, document review, pull-request review, or a passive request to inspect something. The actual contract is narrower and more operational: the item is non-dispatchable because the next safe step requires user interaction.

[User Action Required queue guidance](../../user-action-required/README.md), [Create Backlog](../../../skills/create-backlog/SKILL.md), and [Manage Backlog](../../../skills/manage-backlog/SKILL.md) implement the intended boundary.

Use User Action Required as the canonical replacement. It covers the full interaction boundary more accurately than User Needed while remaining short enough for folder guidance, status fields, reports, badges, and operator summaries.

The [styled backlog report enhancement](../../feature-backlog/add-styled-backlog-report-with-user-input.md) depends on this terminology correction so it does not make the ambiguous name part of a new reporting contract.

## Requirements

- Rename the canonical queue from backlog/user-review to backlog/user-action-required.
- Rename the canonical status value from User Review to User Action Required.
- Preserve the underlying Type field as Feature, Defect, Analysis, or Investigation.
- Preserve the existing non-dispatchable lifecycle, exact user question, rationale, options and tradeoffs, resolution, unattended-work boundary, and post-answer routing behavior.
- Migrate every existing queue item and the queue guidance without losing content, history, or relative links.
- Update AGENTS.md, README guidance, create-backlog, manage-backlog, conceptual agent definitions, generated runtime definitions, Codex metadata, design documentation, regression tests, evaluation fixtures, and support data wherever they use the old canonical name or path.
- Keep ordinary code review, documentation review, pull-request review, and ready-for-review states distinct from User Action Required.
- Update report and operator language to use User Action Required as the machine-readable state and a plain-language heading such as Needs Your Input where a friendlier display label helps.
- Update inventory logic so the renamed queue guidance README remains excluded from work-item counts.
- Update claim and sparse-checkout guidance so the renamed primary-worktree-only queue remains available and governed with the rest of backlog.
- Sweep tracked source, generated artifacts, examples, tests, and installed-bundle documentation for stale backlog/user-review and Status: User Review references.
- Retain old terminology only in explicit migration tests or historical explanation where removing it would make the transition unverifiable.

## Acceptance Criteria

- A reader can identify from the folder and status names alone that the item requires user action before unattended work can continue.
- New user-interaction items are created under backlog/user-action-required with Status: User Action Required.
- Existing queued content is present under the new path with its underlying Type, exact question, resolution, and unattended-work boundary unchanged.
- Backlog inventory reports User Action Required separately from blocked, holding, runnable, and ordinary review work.
- Answered items still move deterministically to their underlying typed backlog folder, holding, or the matching archive according to the recorded resolution.
- No active instruction tells an agent to treat User Action Required as a work Type.
- No active instruction or generated runtime definition uses backlog/user-review or Status: User Review as the canonical contract.
- Pull-request readiness and code or artifact review terminology remain semantically distinct.
- Relative links resolve after the migration.
- Repository validation and generated-output freshness checks pass.

## Dependencies

None.

## Verification

- Add focused creation, inventory, dispatch-exclusion, resolution, move, archive, and invalid-item tests using the new folder and status.
- Add migration coverage that detects stale old-path or old-status references outside explicit compatibility fixtures.
- Verify the existing queued analysis retains its exact question and Resolution after migration.
- Run Agent Skill validation, metadata alignment, generated-output freshness checks, repository script tests, and project-wiki tests.
- Refresh installed bundle copies and confirm the loaded Create Backlog and Manage Backlog guidance uses the new contract.
- Run a repository-wide reference sweep and git diff --check.

## Notes

- User Needed is the motivating plain-language idea, but User Action Required is the canonical target because it states both the actor and the blocking condition.
- Needs Your Input remains acceptable display copy when the machine-readable User Action Required state is also visible or available to the reader.
