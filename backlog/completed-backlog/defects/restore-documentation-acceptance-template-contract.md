# Restore Documentation Acceptance Template Contract

Status: Completed

Type: Defect

Owner: Completed by canonical root Dev Orchestrator

Completion: direct-main

Completed At: 2026-07-25T03:49:35Z

Provider Reference: backlog/completed-backlog/defects/restore-documentation-acceptance-template-contract.md

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One same-task resumption launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Restore or evidence-correct the Documentation Acceptance template contract.
- Dispatched At: 2026-07-25T03:18:55Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Existing canonical work-item Thread 019f96ce-fb8b-7e51-9e26-c8b7617bf7b5 and root task /root are retained; no replacement task was created.
- Approval Provenance: Shared approval commit 154a4c491d82ac0f5cd15ab19776a003c87c3679 recorded the exact `Amend it to skip over any note.` answer for the approved five-path scope before this same-task resumption reservation.

## Delivery Ownership

- Canonical Work-Item Thread: 019f96ce-fb8b-7e51-9e26-c8b7617bf7b5
- Canonical Root Task: /root
- Root Role: Dev Orchestrator
- Current Delivery Checkout: /Users/martinbechard/.codex/worktrees/3e54/dev-methodology
- Current Branch State: Detached at 97e8e20761619518d37ca5a17310836b4f4bf3b6
- Phase: Source Reconciliation
- Started At: 2026-07-25T01:14:02Z
- Coordination Evidence: SHARED_CHECKOUT_ACQUIRED backlog claim 019f96ce-backlog-running; journal event 4391771e-568e-4baa-9ee5-780db88ed049.

## Running Resumption

- Resumed Phase: Approved Governed Contract Correction.
- Preserved Candidate Branch: codex/restore-documentation-acceptance-template-contract-correction.
- Preserved Candidate Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/restore-doc-acceptance-template-correction-019f96ce.
- Preserved Candidate Tip: 7f97d242b4facde4e19727179a08a8bcb4111258.
- Shared Approval Answer: 'Amend it to skip over any note.'
- Approval Commit: 154a4c491d82ac0f5cd15ab19776a003c87c3679.
- Exact Approved Governed Paths: skills/create-architecture/SKILL.md; skills/create-functional-spec/SKILL.md; skills/create-high-level-design/SKILL.md; skills/create-module-design/SKILL.md; skills/review-module-design/SKILL.md.
- Enabled Claim Evidence: SHARED_CHECKOUT_ACQUIRED backlog claim 019f96ce-doc-acceptance-running-resume; journal event 243b9fd7-0653-4430-a79e-3c56029885d5.

## Summary

Restore the Documentation Acceptance section required by the reverse-engineering contract across the relevant documentation templates, or correct the test only if evidence proves the section is intentionally obsolete.

## Context

`python3 -m unittest scripts.test_bundle_content` fails in `test_reverse_engineering_separates_pass_acceptance_and_readiness`. The test expects exactly one `## Documentation Acceptance` heading in each relevant template and currently finds zero. The failure reproduces on baseline commit 4fe3c217 and current main.

Source Evidence: The user directed durable logging of confirmed defects in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a. The assertion is in scripts/test_bundle_content.py. The contract covers the templates under skills/development-methodology/assets/templates, including module-design-template.md, high-level-design-template.md, architecture-template.md, and functional-spec-template.md.

## Requirements

- Reconcile the template headings with the bottom-up reverse-engineering acceptance contract.
- Preserve a distinct Documentation Acceptance decision beginning with ACCEPTED or BLOCKED and a distinct Implementation Readiness decision beginning with READY or BLOCKED.
- Do not silently remove the test expectation without evidence that the documented contract changed intentionally.
- Obtain exact canonical-path approval before changing governed distributed-skill definitions.

## Acceptance Criteria

- `test_reverse_engineering_separates_pass_acceptance_and_readiness` passes using the project-supported Python interpreter.
- Each contract template contains exactly one Documentation Acceptance heading and exactly one Implementation Readiness heading.
- The template instructions and create/review skill checks agree on the leading decision markers and current-pass semantics.

## Dependencies

None.

## Verification

- Run `python3 -m unittest scripts.test_bundle_content` and retain the result.
- Run the narrow affected test before the full module.
- Run the governed-definition approval check before changing a canonical template or distributed skill definition.
- Obtain fresh independent review.

## Notes

This is a baseline-reproduced defect. The implementation must preserve the distinction between accurate documentation acceptance and downstream implementation readiness.

## User Action Required

Question: Do you approve mutation only of these governed canonical source paths: skills/create-architecture/SKILL.md; skills/create-functional-spec/SKILL.md; skills/create-high-level-design/SKILL.md; skills/create-module-design/SKILL.md; skills/review-module-design/SKILL.md?

Why Input Is Required: The independent reviewer found that retained blockquote notes precede authored decisions while the existing creation and review gates require the first nonblank content under the heading. Therefore the acceptance criterion is not met, and changing any governed canonical source requires explicit, scope-specific user approval.

Authorized Scope If Approved: Align the wording to first authored decision after the retained blockquote note, preserving ACCEPTED/BLOCKED versus READY/BLOCKED independence and current-pass semantics. The ordinary companion correction will align four review checklists, strengthen scripts/test_bundle_content.py ordering assertions, and regenerate only policy-supported mirrors. No other governed source is authorized.

Prohibited Until Approval: Do not perform further artifact or integration work.

Permitted Resumption: User Action Required -> Ready after the answer, then the parent Starting reservation and the same canonical Thread Running transition.

## Handoff Evidence

- Preserved candidate commits: 3159c5bf63e25c71df8a264f925bac02a2c76541 and 7f97d242b4facde4e19727179a08a8bcb4111258.
- Released implementation claim events: cb048e7b-e975-487b-b607-0e0488e5e42d and 3d50e8b9-5361-4aa0-80be-48ed748564a5.
- Verifier gates: GOOD.
- Independent reviewer finding: HIGH. Retained blockquote notes precede authored decisions while existing creation and review gates demand the first nonblank content under the heading, so the acceptance criterion is not met.

## Resolution

- User answer: 'Amend it to skip over any note.'
- Provenance: Shared canonical module-contract Thread 019f96ce-dd33-7bf2-bbe1-73e2af07da52; durable approval commit 154a4c491d82ac0f5cd15ab19776a003c87c3679; delegated into this same canonical Documentation Acceptance Thread 019f96ce-fb8b-7e51-9e26-c8b7617bf7b5.
- Approved governed scope: skills/create-architecture/SKILL.md; skills/create-functional-spec/SKILL.md; skills/create-high-level-design/SKILL.md; skills/create-module-design/SKILL.md; skills/review-module-design/SKILL.md.
- Approved meaning: Evaluate the first authored decision after skipping any retained explanatory note or notes, preserving ACCEPTED/BLOCKED versus READY/BLOCKED independence and current-pass semantics.
- Resulting disposition: User Action Required -> Ready. No artifact mutation, integration work, task creation, or Running transition occurred in this provider transaction.
- Next step: Parent same-task Starting reservation, followed only by the same canonical Thread Running transition after its root Dev Orchestrator accepts ownership.

## Completion Evidence

- Accepted delivery and integration commit: dfbd1542ade8bd8a705ea0396562146fbaa21af6.
- Delivery parent: 1d909c76062e8235b64f649124c2898f9fa6557a.
- Delivery tree: ad57cbe37d5bf34b5fbdefcad068a5305175c541.
- Completion process: direct-main.
- Main observation: main was observed at dfbd1542ade8bd8a705ea0396562146fbaa21af6; ancestry and reachability were confirmed.
- Reviewed scope: exactly 21 paths; committed content manifest: 6541a5d6f3f8e4c3f959be18fc52c294cb5beb8bdff9d5d7a609426415ed4087; no generated/adapters changes.
- Approval evidence: user answer 'Amend it to skip over any note'; shared approval commit 154a4c491d82ac0f5cd15ab19776a003c87c3679; all five exact approval records and checks ALLOWED for skills/create-architecture/SKILL.md; skills/create-functional-spec/SKILL.md; skills/create-high-level-design/SKILL.md; skills/create-module-design/SKILL.md; skills/review-module-design/SKILL.md.
- Independent review: corrected fresh methodology review GOOD with no findings.
- Independent verification: GOOD.
- Precommit gates: focused 8/8, full scripts.test_bundle_content 118/118, skill validation, generator, hierarchy, support, and diff gates PASS.
- Committed-main gates: narrow 1/1, generator freshness, skill validation, diff, and clean checks PASS.
- Delivery ownership release: source/project claim restore-doc-acceptance-governed-019f96ce released at event f4d84f3c-2a92-40bb-8901-868d934ce9c7; primary main was clean.
- Earlier candidate commits 3159c5bf63e25c71df8a264f925bac02a2c76541 and 7f97d242b4facde4e19727179a08a8bcb4111258 remain superseded evidence, together with the reviewer correction history.
- Residual risk: none.
