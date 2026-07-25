# Align Module Design Template And Bundle Test Contract

Status: Completed

Type: Defect

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One same-task resumption launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Align module design template and bundle test Implementation Readiness contract.
- Dispatched At: 2026-07-25T03:11:39Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Existing canonical work-item Thread 019f96ce-dd33-7bf2-bbe1-73e2af07da52 is retained; no replacement task was created.
- Approval Provenance: The canonical Thread recorded the user's exact `Amend it to skip over any note.` answer for the five-path scope before this same-task resumption reservation.

## Lifecycle Start

- Owner: root Dev Orchestrator
- Canonical Runtime Identity: 019f96ce-dd33-7bf2-bbe1-73e2af07da52
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/1e75/dev-methodology
- Canonical Branch: codex/align-module-template-test-contract
- Phase: approved-governed-definition-correction
- Coordination Evidence: The parent reserved this same-task resumption in Starting, and the Dev Backlog Steward recorded this atomic Starting-to-Running acceptance on primary main under claim align-module-template-start-running-019f96ce (event 23c0d8ea-d338-43d3-bc8d-6b74b1db269d).

## Execution Ownership

- Work-Item Thread: 019f96ce-dd33-7bf2-bbe1-73e2af07da52
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96ce-dd33-7bf2-bbe1-73e2af07da52
- Owner: root Dev Orchestrator
- Branch: codex/align-module-template-test-contract
- Worktree: /Users/martinbechard/.codex/worktrees/1e75/dev-methodology
- Phase: approved-governed-definition-correction
- Started At: 2026-07-25T01:08:24Z
- Coordination: Enabled; agent-claim short backlog transaction completed before this provider mutation.
- Claim Evidence: backlog-starting-running-019f96ce-dd33-7bf2-bbe1-73e2af07da52; agent-claim event a731c430-1b5e-4da7-b30d-5999f2942bea; resource backlog:mutation:align-module-template-test-contract.

## Summary

Align the create-module-design bundle-content test with the maintained module-design template contract for the Implementation Readiness section.

## Context

`python3 -m unittest scripts.test_bundle_content` fails in `test_planned_hld_and_module_creation_contracts`. The test expects the exact phrase `Begin this section with **READY.** or **BLOCKED.**`, while `skills/development-methodology/assets/templates/module-design-template.md` currently begins the instruction with `TODO: Immediately after the retained blockquote note, begin the authored section content with **READY.** or **BLOCKED.**`. The mismatch reproduces on baseline commit 4fe3c217 and current main.

Source Evidence: The user directed durable logging of confirmed defects in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a. The failing assertion is in scripts/test_bundle_content.py; the affected canonical template is skills/development-methodology/assets/templates/module-design-template.md.

## Requirements

- Determine whether the executable assertion or the intended template wording is authoritative.
- Make the test and canonical template contract agree without weakening the requirement that Implementation Readiness begins with READY or BLOCKED.
- Preserve the parallel Documentation Acceptance distinction and the required heading structure.
- Obtain exact canonical-path approval before changing any governed distributed skill definition.

## Acceptance Criteria

- `test_planned_hld_and_module_creation_contracts` passes using the project-supported Python interpreter.
- The module template still instructs authors to put READY or BLOCKED first in the Implementation Readiness content.
- The test verifies the intended semantic contract rather than an obsolete formatting fragment.

## Dependencies

None.

## Verification

- Run `python3 -m unittest scripts.test_bundle_content` and retain the result.
- Run the narrow affected test before the full module.
- Run the governed-definition approval check if the canonical template or a distributed skill is changed.
- Obtain fresh independent review.

## Notes

This is a baseline-reproduced regression, not a current-main-only failure. Do not implement a template or skill-definition change without the required approval manifest.

## Delivery And Review Evidence

- Clean candidate: db82828f8e240a3014eb87635b6f7135362934af.
- Candidate scope: scripts/test_bundle_content.py only; no governed definition path changed.
- Independent review: approved with no findings.
- Verifier: PASS for the focused test, structural readiness check, candidate scope audit, and whitespace gate.
- Known concurrent baseline warning: the full bundle-content module still has the separately tracked, baseline-reproduced Documentation Acceptance failure. It was not introduced by this candidate.
- Implementation and integration claims are released. No integration occurred.

## Canonical Decision Dependency

- Canonical decision owner Thread: 019f96ce-fb8b-7e51-9e26-c8b7617bf7b5.
- Durable canonical decision: backlog/user-action-required/restore-documentation-acceptance-template-contract.md at commit ab02f64a0718d47bd2da356890f09ab217b1eb45.

## User Decision Record

Question: Do you approve aligning only these governed canonical sources — skills/create-architecture/SKILL.md; skills/create-functional-spec/SKILL.md; skills/create-high-level-design/SKILL.md; skills/create-module-design/SKILL.md; skills/review-module-design/SKILL.md — so Documentation Acceptance and Implementation Readiness mean the first authored decision after skipping any retained explanatory note(s), preserving ACCEPTED/BLOCKED versus READY/BLOCKED and current-pass semantics?

Why User Input Is Required: This item shares the canonical governed-definition decision recorded by Thread 019f96ce-fb8b-7e51-9e26-c8b7617bf7b5. Explicit, scope-specific user approval is required before any governed canonical source may change.

Resolution: Approved on 2026-07-25. The canonical Thread 019f96ce-dd33-7bf2-bbe1-73e2af07da52 current user message answered: "Amend it to skip over any note." This is explicit approval for only the five canonical sources named in the Question. Documentation Acceptance and Implementation Readiness must evaluate the first authored decision after skipping any retained explanatory note(s), preserving ACCEPTED/BLOCKED versus READY/BLOCKED and current-pass semantics.

Ready Disposition: This approved defect was resumed by the canonical work-item Thread after the parent Coordinator recorded the later same-Thread Ready -> Starting transition. Preserve candidate db82828f8e240a3014eb87635b6f7135362934af and the existing review and verification evidence.

## Completion Evidence

- Completed At: 2026-07-25T03:53:04Z.
- Accepted source candidate: db82828f8e240a3014eb87635b6f7135362934af. It is non-ancestral, but its intended contract is superseded and reconciled by the stronger semantic integration at dfbd1542ade8bd8a705ea0396562146fbaa21af6; no stale candidate bytes were reapplied.
- Integration and main delivery: dfbd1542ade8bd8a705ea0396562146fbaa21af6 was the delivery observation commit and is reachable from main. At terminal handoff, main later advanced through descendant eedb7117d4f698dea100516542136f078c379e82; the current primary-main observation is eb2accc2ead24fbb4074a1fd628e51cb962899cc.
- Resumption and approval: the same canonical Thread 019f96ce-dd33-7bf2-bbe1-73e2af07da52 recorded the user-approved five-path correction to skip leading retained explanatory note(s). The earlier terminal backlog claim 019f96ce-doc-acceptance-complete was released (event 4538ebe7-1e37-4d24-b6ae-79423bf66a33). The implementation candidate claim and shared governed integration claim were released; the integration release event is f4d84f3c-2a92-40bb-8901-868d934ce9c7.
- Contract evidence: both assertion sites now skip leading retained explanatory note(s), require the exact READY or BLOCKED marker for Implementation Readiness, preserve mandatory Documentation Acceptance before Implementation Readiness, and cover multiple-note and swapped-section mutants.
- Review and verification: source review for db82828f8e240a3014eb87635b6f7135362934af approved with no findings; its focused verifier passed. Fresh shared-governed-correction review and verifier were GOOD. The full affected module passed 118/118, and validation, generator freshness, and diff gates passed.
- Independent post-integration observation: under Python 3.11.13, the two focused tests passed, scripts.test_bundle_content passed 118/118, and the dfbd1542 diff check passed. An initial Python 3.9 run failed before discovery because tomllib is unavailable; the supported Python 3.11 run supplied the final evidence.
