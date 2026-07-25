# Align Module Design Template And Bundle Test Contract

Status: Running

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

Ready Disposition: This approved defect is active in backlog/defect-backlog with Status: Ready and Owner: Unowned. Preserve candidate db82828f8e240a3014eb87635b6f7135362934af and the existing review and verification evidence. The parent Coordinator owns the later same-Thread Ready -> Starting transition; this record does not start or run implementation.
