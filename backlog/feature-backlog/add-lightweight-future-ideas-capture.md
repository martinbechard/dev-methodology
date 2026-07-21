# Add Lightweight Future Ideas Capture

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-lightweight-future-ideas-capture.md

Completion: direct-main

## Current Execution

- Owner: Dev Orchestrator
- Canonical task: 019f85c8-6274-7593-b073-dd8b12b7b079
- Worktree: /Users/martinbechard/.codex/worktrees/ceb0/dev-methodology
- Branch: codex/add-lightweight-future-ideas-capture
- Starting main: 2624b5b25ba6e5548051d7b9953933b1e57b3f87
- Phase: Bounded storage, scanner, promotion, and exact governed-scope discovery.
- Started: 2026-07-21
- Running-record claim: start-future-ideas-019f85c8, acquired event e227f815-0a32-41f5-9753-606238d66788.
- Open issues: Exact governed-definition approval scope remains to be established from discovery evidence.
- Accepted candidate: Pending.

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Add a lightweight Future Ideas area for potentially useful thoughts that should be remembered but are not yet actionable, approved, scheduled, or part of normal backlog dispatch.

## Context

The user distinguished Future Ideas from Holding during the design dialogue on 2026-07-21. Holding represents recognized work intentionally paused. A future idea should require less structure and no routine attention unless someone deliberately begins ideation or promotion.

Future Ideas must not become another actionable lifecycle state and must not be counted or dispatched as ordinary backlog work.

## Source Evidence

- On 2026-07-21, the user proposed an official Future Ideas area for potentially interesting future work.
- The user clarified that it should be less structured than Holding and need no routine attention unless deliberate ideation begins.
- On 2026-07-21, the user explicitly requested creation of work items based on those conversations.

## Requirements

- Define one lightweight, non-dispatchable Future Ideas storage area outside normal typed active queues.
- Require only a title, short synopsis, origin or rationale, and optional notes or revisit trigger.
- Do not require Status, Owner, Dependencies, Acceptance Criteria, Verification, or a user decision merely to capture an idea.
- Exclude Future Ideas from ordinary backlog scans, runnable counts, dispatch, lifecycle transitions, and unattended work.
- Define deliberate promotion into a normal typed work item with complete required fields and provenance back to the source idea.
- Keep Holding for already-recognized work intentionally paused.
- Define whether promotion preserves, archives, links, or removes the original idea without losing provenance.
- Update file-work-item guidance, backlog reporting, examples, tests, and user-facing documentation consistently.
- Obtain exact, scope-specific approval before changing governed skill definitions.

## Acceptance Criteria

- An idea can be captured without pretending it is approved work.
- Normal inventory and dispatch ignore Future Ideas unless an explicit ideation or promotion operation includes them.
- Promoting an idea creates a valid typed work item and retains a durable source link.
- Holding and Future Ideas have distinct documented meanings and deterministic routing.
- Tests demonstrate that idea files do not affect runnable or unattended backlog counts.

## Dependencies

None.

## Verification

- Inspect every backlog scanner, report, dispatcher, template, and lifecycle rule before choosing the storage path.
- Test minimal idea validation, ordinary-scan exclusion, explicit listing, promotion, provenance, and Holding separation.
- Verify documentation and examples use the same terminology and fields.
- Run focused backlog tests, Git diff validation, and independent methodology review.

## Open Questions

- Should promotion archive the source idea or retain it in place with a promoted-to reference?
- Should revisit triggers be free text only or optionally machine-readable without making ideas part of routine dispatch?
