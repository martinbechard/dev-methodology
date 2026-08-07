# Reconcile Bundle Content Suite Drift

Status: Running

Type: Defect

Provider: file

Work Item ID: reconcile-bundle-content-suite-drift

Completion: main-branch

## Summary

Restore the complete scripts.test_bundle_content suite by reconciling stale assertions and missing fixture references with the current methodology sources and completed migrations.

## Context

A broad verification run during the design/agents documentation move completed 168 bundle-content tests with ten failures and two errors. The two focused tests that consume the moved design paths passed, so the failures are outside that documentation rename.

The failed assertions span several completed repository changes: document-topic skills were renamed and retired, new Agent evaluation suites were added, delivery fixtures changed their required skills, active-capacity vocabulary moved from task to execution, review routing changed, lifecycle documentation ownership moved, and the harness-loading prose check reports current design text. The suite still encodes earlier expectations for those surfaces.

## Source Evidence

On 2026-08-07, scripts.test_bundle_content reported ten failures and two errors after the focused provider-family and resource-coordination design tests passed. The errors referenced missing .agents/skills/create-document-outline/SKILL.md and .agents/skills/improve-document-outline/SKILL.md. The failures named Agent suite inventory, delivery-fixture skill lists, documentation topic ownership, Starting-plus-Running terminology, documentation-writer model coverage, Orchestrator review routing, and harness-instruction prose checks.

The repository rule requiring every confirmed incorrect state to be logged authorizes this defect record. This item does not authorize changing governed skill or Agent definitions merely to satisfy a stale test.

## Requirements

- Classify every one of the twelve observed results as a stale test expectation, missing generated or fixture artifact, or current source defect before changing behavior.
- Replace references to retired create-document-outline and improve-document-outline project-local skills with the current document-topic contracts, or remove obsolete assertions when the completed migration intentionally retired those files.
- Reconcile expected Agent evaluation suite and model-profile inventories with the current registered roles, including document-topic editing and skill-lint review.
- Reconcile delivery-fixture required-skill assertions with the current separation among coding, work-item management, delivery, and resource coordination.
- Update active-capacity assertions to the current canonical execution vocabulary without weakening the Starting-plus-Running capacity invariant.
- Reconcile Dev Orchestrator review-routing expectations with the current role-owned review and backlog-steward boundaries.
- Correct the harness-instruction prose check or the implicated design prose according to the actual harness-loading contract; do not silence legitimate duplicate-loading instructions.
- Preserve valid negative tests and contract boundaries while removing expectations made obsolete by completed migrations.
- Add focused regression evidence for each corrected expectation before accepting a green aggregate suite.

## Acceptance Criteria

- All twelve recorded failures or errors have an evidence-backed disposition and a focused correction.
- scripts.test_bundle_content passes without restoring retired identifiers or weakening current Agent, skill, delivery, capacity, review, or harness contracts.
- Focused tests prove the current document-topic skill identities, Agent suite inventory, model-profile coverage, delivery-fixture skill ownership, capacity vocabulary, review routing, and harness-loading prose boundary.
- Source behavior changes only where evidence proves the source is wrong; stale tests are corrected without changing valid production or methodology contracts.
- Generated outputs are regenerated from canonical sources when a correction changes a generator input.
- Git diff checks and the directly affected documentation or YAML validations pass.

## Dependencies

None.

## Verification

- Run each formerly failing scripts.test_bundle_content test independently while correcting its owning expectation.
- Run scripts.test_bundle_content as one aggregate suite after all focused cases pass.
- Run the directly affected generator freshness, YAML, Markdown, skill, or Agent evaluation checks identified by each correction.
- Search for the retired document-outline identifiers and classify every remaining historical or compatibility occurrence.
- Run git diff --check.

## Open Questions

- Determine whether the harness-instruction failures identify over-broad sentence matching or genuinely duplicated loading instructions.
- Determine whether any missing document-topic fixture should be generated from the current analyze-document-topics and revise-document-topics definitions rather than removed.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T02:30:14Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Classify and correct the twelve recorded bundle-content failures or errors against current methodology sources, preserving valid contracts and changing source behavior only when evidence proves it wrong.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-07T02:45:14Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: No Starting or Running provider item, no finish-lane work, clean main at `d2c72418e8f69855737c684f0b74d4ee1a8f729d`, empty resource-claim registry, and no duplicate canonical task. The User Action Required item remains non-dispatchable and untouched.

## Active Execution Evidence

Condition Type: root-execution

Owner: Root Dev Orchestrator.

Evidence: Canonical root task 019fda10-8f12-7ae0-8d71-9b8678c17451 is actively executing this work item. All twelve formerly failing results were reproduced individually under Python 3.11 and classified against current sources; the next bounded action is a test-only correction delegated to one Dev Coder.

Observed At: 2026-08-07T02:41:09Z

Started At: 2026-08-07T02:34:30.318691Z.

Deadline or Expires At: 2026-08-07T04:41:09Z

Next Action: Commit this corrected provider evidence, reacquire exact outcome work, delegate scripts/test_bundle_content.py to one Dev Coder, and obtain one immutable candidate.

Next Reconciliation At: 2026-08-07T02:56:09Z

Codex Task ID: 019fda10-8f12-7ae0-8d71-9b8678c17451.

Conversation ID: 019fda10-8f12-7ae0-8d71-9b8678c17451.

Root Role: Dev Orchestrator.

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Branch: Detached HEAD at 9bbbb27692d4e1f73b8434fc85cfcd1bb0cd64cc.

Worktree: /Users/martinbechard/.codex/worktrees/6e5c/dev-methodology.

Phase: Test-only correction after evidence-backed classification of all twelve recorded results.

Conversation Title Evidence: Implementing — Reconcile Bundle Content Suite Drift synchronized at 2026-08-07T02:41:09Z.

Provider Evidence Refresh Claim: reconcile-bundle-content-evidence-update-019fda10; activity update; acquire outcome SHARED_CHECKOUT_ACQUIRED; acquisition event 3a64a9c3-d695-4148-9dfe-44f499e5a57b. Exact provider path claim reconcile-bundle-content-evidence-path-019fda10 acquired with event 3a912c64-f449-43a8-9cf0-2636d43df53b.
