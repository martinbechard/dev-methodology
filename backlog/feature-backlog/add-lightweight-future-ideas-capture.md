# Add Lightweight Future Ideas Capture

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-lightweight-future-ideas-capture.md

Completion: direct-main

## Discovery Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f85c8-6274-7593-b073-dd8b12b7b079
- Worktree: /Users/martinbechard/.codex/worktrees/ceb0/dev-methodology
- Branch: codex/add-lightweight-future-ideas-capture
- Starting main: 2624b5b25ba6e5548051d7b9953933b1e57b3f87
- Phase: Bounded storage, scanner, promotion, and exact governed-scope discovery completed; the recorded exact approval permits Ready-state dispatch within the stated scope.
- Started: 2026-07-21
- Running-record claim: start-future-ideas-019f85c8, acquired event e227f815-0a32-41f5-9753-606238d66788.
- Open issues: No user-action issue remains. Implementation must stay within the approved exact scope.
- Accepted candidate: Pending.

## Delivery Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: /root/process_backlog/orch_future_ideas
- Artifact claim: future-ideas-implementation-20260722
- Branch: codex/future-ideas-implementation-20260722
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/future-ideas-implementation-20260722
- Starting main: 13ea3ffe92fe7a8352f33b4f618f39f212322ba3
- Phase: Lifecycle Running committed; ARTIFACT GO pending.
- Candidate: Pending.
- Accepted commit: Pending.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Delivery evidence: Pending.
- Claim pressure: README.md is currently owned by deploy-explicit-project-20260722. Start on proven non-overlapping scopes; serialize any later README.md or scripts/test_bundle_content.py extension rather than waiting idle or polling.

## User Action Required

### Question For The User

Do you approve changes to exactly these four governed canonical files for this work item, with regeneration only of their supported mirrors?

1. skills/create-file-work-item/SKILL.md
2. skills/manage-file-work-items/SKILL.md
3. skills/codex-workitem-coordination/SKILL.md
4. agents/roles/dev-activities/dev-backlog-steward.role.yaml

### Why User Input Is Required

The evidence-backed Future Ideas design changes three governed skill definitions and one governed conceptual agent definition. Repository policy requires exact path-specific approval before mutation.

### Options And Tradeoffs

- Approve the exact four-file scope: implement lightweight non-dispatchable ideas, opt-in listing, and explicit promotion provenance.
- Narrow the scope by naming allowed paths: preserve excluded behavior as blocked follow-up work.
- Defer: retain the resolved design without implementation.

### Resolution

Approved on 2026-07-22. The user answered "ok authorized" immediately after the exact Question For The User recorded above in the parent conversation. Provenance: parent coordination conversation for this backlog transition. The approval covers exactly the four governed canonical files listed in that question and regeneration only of their supported mirrors.

### Unattended Work Boundary

Ready-state work may proceed only within the exact approved scope. Any governed path or related surface outside the recorded question requires separate scope-specific approval. Future Ideas remain outside normal backlog scans and dispatch.

### Discovery Evidence

- Canonical task: 019f85c8-6274-7593-b073-dd8b12b7b079.
- Clean branch/worktree: codex/add-lightweight-future-ideas-capture at /Users/martinbechard/.codex/worktrees/ceb0/dev-methodology, based on 2624b5b25ba6e5548051d7b9953933b1e57b3f87.
- Storage decision: backlog/future-ideas is outside the ordinary scanner folder set.
- Listing decision: Future Ideas appear only through an explicit opt-in report operation.
- Promotion decision: retain the source idea in place with a durable Promoted To reference.
- Revisit decision: keep revisit triggers free text so ideas do not become routine machine-scheduled work.
- Supported generated mirrors: design/generated skill and role definitions, Dev Backlog Steward native adapters, and the agent-generation manifest emitted by the supported generator.
- Directly related non-governed scope: scripts/generate-backlog-report.py, scripts/test_generate_backlog_report.py, scripts/test_bundle_content.py, README.md, design/work-item-provider-and-completion-contracts.md, and focused Dev Backlog Steward scenario coverage if needed.
- UAR routing claim: route-future-ideas-approval, acquired event 60e626ac-6c5e-4f53-b074-c9028d906779.

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

## Delivery Evidence Update — 2026-07-22

- Current phase: Implementation and disjoint validation continue; candidate pending.
- Artifact claim: future-ideas-implementation-20260722 acquired, event 71163a6f-decc-45af-856b-21d9e061c6a3.
- Approval-record extension: Succeeded, event c060c39d-93fa-4180-8fb4-d36187339de8.
- Governed approval checks: All four exact pre-mutation checks returned ALLOWED before mutation.
- Generated-scope extension: Returned CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, event dcc8d3e4-6e74-46ce-a727-0d1e65a92aa7, against project-skill-extensions-20260722 on design/generated/skill-definitions.js and generated/adapters/agent-generation-manifest.json.
- Claim wait started at: 2026-07-22T14:25:09Z.
- Claim wait attempts: 1.
- Current claim: Unchanged.
- Wait behavior: No polling; disjoint validation continues.
- Sequencing: README.md and scripts/test_bundle_content.py remain sequenced behind the project-extension lane and deploy README correction.
- Candidate commit: Pending.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Delivery evidence: Pending.
- Next owner: Dev Orchestrator.
