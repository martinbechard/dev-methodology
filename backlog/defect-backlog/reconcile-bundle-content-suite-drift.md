# Reconcile Bundle Content Suite Drift

Status: Ready

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
