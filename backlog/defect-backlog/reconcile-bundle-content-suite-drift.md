# Reconcile Bundle Content Suite Drift

Status: Starting

Type: Defect

Provider: file

Owner: Unowned

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

Starting Recorded At: 2026-08-08T17:44:34Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Resume the preserved six-path partial evaluation candidate, apply the approved suite-local eight-path correction under the user's evaluation-only authority protocol, complete focused and one aggregate verification, and deliver only after fresh review and verification accept an immutable candidate.

Launch Result: Started

Canonical Execution: 019fda10-8f12-7ae0-8d71-9b8678c17451

Last Contact At: 2026-08-08T17:44:34Z

Next Reconciliation At: 2026-08-08T17:58:00Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: The user answered the recorded question in the preserved canonical conversation. UAR -> Ready is durable at `b94cdfc39af8001600357ff412293dde920c3997`; the same canonical task remains active with the preserved six-path partial worktree, and no duplicate launch is authorized.

## Prior Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Coder producer `/root/bundle_content_coder` under the canonical Root Dev Orchestrator.

Evidence: Dev Coder holds exact path claim `reconcile-bundle-content-test-path-019fda10`, acquired 2026-08-07T02:49:41.766714Z, and `scripts/test_bundle_content.py` is currently modified in the isolated worktree. The exact claim manifest now also covers four proven ordinary eval-source defects required by the Agent-suite reconciliation; no governed skill or Agent definition path is included.

Observed At: 2026-08-07T03:01:50Z

Started At: 2026-08-07T02:49:41.766714Z

Deadline or Expires At: 2026-08-07T05:01:50Z

Next Action: Dev Coder will finish the exact five-path correction, rerun only newly affected focused checks, run the single aggregate bundle-content suite once after focused acceptance, and commit one immutable candidate for independent review and verification.

Next Reconciliation At: 2026-08-07T03:16:50Z

Codex Task ID: 019fda10-8f12-7ae0-8d71-9b8678c17451.

Conversation ID: 019fda10-8f12-7ae0-8d71-9b8678c17451.

Root Role: Dev Orchestrator.

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Branch: Detached HEAD at 9bbbb27692d4e1f73b8434fc85cfcd1bb0cd64cc.

Worktree: /Users/martinbechard/.codex/worktrees/6e5c/dev-methodology.

Phase: Delegated test and exact ordinary eval-fixture correction before candidate freeze.

Conversation Title Evidence: Implementing — Reconcile Bundle Content Suite Drift synchronized at 2026-08-07T02:41:09Z.

Provider Evidence Refresh Claim: reconcile-bundle-content-delegated-update-019fda10; activity update; acquire outcome SHARED_CHECKOUT_ACQUIRED; acquisition event 1b9a6dc0-7e3f-43ea-aba7-90db4d21ea4c. Exact provider path claim reconcile-bundle-content-delegated-path-019fda10 acquired with event 13046410-8040-4a91-8776-6002125d630c.

## User Action Required

Recorded At: 2026-08-07T03:08:00Z

### Question for the User

Do you approve expanding reconcile-bundle-content-suite-drift to modify exactly these three governed Dev Orchestrator evaluation definitions: evals/agent-tests/dev-orchestrator/skills/dev-orchestrator-suite-contract/SKILL.md, evals/agent-tests/dev-orchestrator/agents/supervisor.toml, and evals/agent-tests/dev-orchestrator/agents/judge.toml; and the five directly implicated ordinary fixture/test paths already identified, solely to remove the retired dev-backlog-steward fixed-dependency contract and align the suite with the canonical Dev Orchestrator role?

### Why User Input Was Requested

The earlier workflow treated the three suite-local skill/Agent evaluation definitions as governed paths and the current item explicitly forbade changing them without new exact authority. The user's answer below approves the current change and corrects that protocol for future non-distributed evaluation-only artifacts.

### Approved Ordinary Fixture/Test Paths

- evals/agent-tests/dev-orchestrator/scenarios.yaml
- evals/agent-tests/dev-orchestrator/fixtures/dependency-routing/fixture-contract.yaml
- evals/agent-tests/dev-orchestrator/test_fixtures.py
- evals/agent-tests/dev-orchestrator/fixtures/skill-under-test-defect-routing/README.md
- evals/agent-tests/dev-orchestrator/fixtures/skill-under-test-defect-routing/expected-finding.yaml

### Explicit Exclusions

No distributed skill, distributed Agent definition, broad suite, simulator, framework, production methodology, canonical production source, design source, generated artifact, or unrelated repository path is approved.

### Current Recovery Evidence

Six modified unstaged paths remain in isolated worktree /Users/martinbechard/.codex/worktrees/6e5c/dev-methodology at detached baseline 9bbbb27692d4e1f73b8434fc85cfcd1bb0cd64cc. The diff has 94 insertions and 42 deletions. Binary diff SHA-256: 670604590700aa464d669cc8af4d176c299f78369085adaf043132ecb4478000. All ten focused methods are green. py_compile, YAML parse, and diff check are green. The aggregate suite was deliberately not run. Producer exact path release event: 6dcce931-d738-4009-a9e7-8a8be3892c91. Root outcome blocked release event: 928e0573-e7e9-4d04-89bc-83392843424e.

### Unattended Work Boundary

No further source edit, candidate commit, aggregate bundle-content run, review, verification, integration, or provider completion may proceed. Preserved six-path isolated-worktree bytes remain untouched.

### Resolution

Approved on 2026-08-08 in canonical conversation `019fda10-8f12-7ae0-8d71-9b8678c17451`. The user's exact answer was: `1) the current change is approved 2) future protocol: changes to test artifacts / judges/ skills etc not distributed to users don't need special approval.` The current eight-path evaluation correction is therefore authorized. Preserve the existing six-path partial candidate and resume through Ready -> Starting -> Running before further mutation.

## Evaluation-Only Authority Protocol

Authority Source: Direct user instruction in canonical conversation `019fda10-8f12-7ae0-8d71-9b8678c17451` on 2026-08-08 America/Toronto.

Standing Boundary: Evaluation-only test artifacts that are not installed or distributed to users or projects do not require special governed-definition approval merely because they are named skills, supervisors, Judges, scenarios, fixtures, or suite-local Agent definitions.

Covered Examples: Suite-local supervisors and Judges, evaluation-only skills and contracts, scenarios, fixtures, expected findings, test data, and test-harness instructions under the non-distributed evaluation surface.

Unchanged Governance: Distributed skills, distributed Agent definitions, generated user-facing adapters, canonical production sources, and other artifacts installed or published to users or projects retain their normal authority and scope requirements.

Integrity Boundary: This protocol does not authorize weakening tests to hide a real defect, expanding into an unrelated framework or broad suite, or changing distributed/canonical behavior merely to make a private evaluation pass. Evidence must still show that an evaluation-only correction aligns the suite with the current canonical contract.
