# Define Functional Specification UX Mockup Criteria

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/define-functional-specification-ux-mockup-criteria.md

Completion: direct-main

## Execution / Ownership

- Owner: Unowned
- Canonical task: /root/process_backlog/orch_functional_spec_ux
- Proposed artifact claim: define-functional-spec-ux-mockup-criteria
- Claim: None
- Branch: codex/define-functional-spec-ux-mockup-criteria
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/define-functional-spec-ux-mockup-criteria
- Phase: Exact approval recorded; Ready for fresh dispatch.
- Starting main: af0a3fe63404a793f2bf7dcf40dd2a3de563109e
- Accepted candidate: None.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Open issues: None for lifecycle dispatch; implementation must remain within the recorded approval.
- Next owner: Dev Backlog Coordinator.
- Delivery evidence: Approval recorded; implementation and candidate remain pending.

## Read-Only Discovery

- Completed: Current functional-specification guidance and companion surfaces were inspected without artifact mutation.
- Artifact claim: None acquired.
- Candidate: None accepted.
- Artifact mutation: None performed.

## User Action Required

### Question For The User

Do you explicitly approve changing skills/create-functional-spec/SKILL.md to require a proportionate UX mockup only when documented interaction/layout complexity triggers defined criteria, while requiring a concrete no-mockup rationale for simple or non-visual specifications, with supported generated skill mirrors regenerated from that approved source?

### Why User Input Is Required

The completed read-only discovery identified one governed skill-definition path. Repository policy requires explicit scope-specific approval before its mutation.

### Non-Governed Companion Surfaces

- skills/development-methodology/assets/templates/functional-spec-template.md
- skills/review-functional-spec/references/review-checklist-functional-spec.md
- scripts/test_bundle_content.py

### Options And Tradeoffs

- Approve the exact governed path: permit the criteria change and supported generated mirror regeneration.
- Narrow the scope: preserve excluded behavior as unresolved work.
- Defer: retain the discovery evidence without implementation.

### Resolution

Approved on 2026-07-22. The user answered "ok" directly after the exact Question For The User in the parent turn. Provenance: parent coordination conversation for /root/process_backlog/orch_functional_spec_ux.

The approval covers exactly the governed path skills/create-functional-spec/SKILL.md and regeneration only of its supported generated mirrors.

The only ordinary non-governed companion surfaces covered by this direction are:

- skills/development-methodology/assets/templates/functional-spec-template.md
- skills/review-functional-spec/references/review-checklist-functional-spec.md
- scripts/test_bundle_content.py

The answer does not authorize changes to skills/review-functional-spec/SKILL.md or any other governed path.

### Unattended Work Boundary

The item is Ready for a fresh dispatch but is not Running. No artifact claim has been acquired. Work must stay within skills/create-functional-spec/SKILL.md, its supported generated mirrors, and the three ordinary non-governed companion surfaces recorded in the Resolution. Changes to skills/review-functional-spec/SKILL.md or any other governed path remain prohibited without separate approval.

## Summary

Define deterministic, evidence-based criteria for when a functional specification requires UX mockups.

## Context

Functional specifications describe user-visible behavior, actor workflows, entry points, states, permissions, acceptance behavior, and verification. A mockup is useful only when supported interaction or layout complexity makes it necessary to communicate the contract; it must not become mandatory HTML for every functional specification.

## Source Evidence

- Direct user authorization in the 2026-07-22 parent coordination request to create this Ready Feature item.
- Current functional-specification guidance in skills/create-functional-spec/SKILL.md, skills/review-functional-spec/SKILL.md, and skills/development-methodology/assets/templates/functional-spec-template.md.

## Requirements

- Define deterministic criteria based on evidence-backed interaction and layout complexity for requiring a UX mockup.
- Do not require HTML or a visual mockup for every functional specification.
- Require an explicit no-mockup rationale for simple or non-visual specifications.
- Keep creation guidance, functional-specification template, and review checklist contracts compatible.
- Add focused tests that distinguish mockup-required and no-mockup cases.
- Before mutating any governed skill definition, obtain exact scope-specific user approval and run the supported pre-mutation approval check.

## Acceptance Criteria

- Criteria can be applied consistently from documented interaction and layout evidence.
- A simple or non-visual specification can pass with a concrete no-mockup rationale.
- A specification with qualifying interaction or layout complexity identifies the required mockup form and its contract role.
- The compatible template and review checklist make the same requirement observable.
- Focused tests cover positive and negative criteria cases.
- Any governed definition mutation has durable exact scope-specific approval evidence and passes the supported pre-mutation check.

## Dependencies

None.

## Verification

- Inspect the canonical functional-specification creation, template, review, and checklist contracts before implementation.
- Run focused tests and bundle checks for every approved changed surface.
- Run git diff --check and obtain independent review of the exact change.

## Notes

Mockup can mean a proportionate visual artifact; this work item does not prescribe HTML unless the approved criteria and evidence require it.
