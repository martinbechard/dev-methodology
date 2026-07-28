# Allow typed evidence in architecture review checklists

Status: User Action Required

Type: Defect

Provider: file

Provider Reference: backlog/user-action-required/allow-typed-evidence-review-architecture.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-defects-019fa9bb

Normalized Objective: Allow typed evidence in architecture review checklists.

Dispatch Time: 2026-07-28T19:19:58Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa2d-2ffa-75c0-80d5-e3bd4f7a31fa

Root Agent Task: 019faa2d-2ffa-75c0-80d5-e3bd4f7a31fa

Phase: Waiting for exact scope-specific user approval before any governed-definition mutation.

Started At: 2026-07-28T19:26:56.856080Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim starting-to-running-review-architecture-019faa2d; incarnation 01c1ae9d-5532-4613-8a93-08d5199f3ea7; claim journal event 7dd8c4f3-0e63-47a4-b627-d6762eaa290c; exact provider path claimed in the primary main checkout.

Recovery Evidence: Initial lifecycle claim attempt returned DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED because the unrelated backlog/defect-backlog/detect-typescript-esm-in-bundler-only-projects.md was modified. Coordinator recovery confirmed that record committed as f0f5c17a6af52fdcf332fc7cf48e7c0b49ee98ef and released claim event 1828d51c-d8e3-416a-a26a-22a8ac029a6a before this clean-primary retry.

Running Evidence: Running transition committed as f7d41dbaa54112b211de1657bd4d2d011b93c9ea. The Running claim acquire event was 7dd8c4f3-0e63-47a4-b627-d6762eaa290c and release event was ebc5b5ff-9c8c-4ad7-a8f4-3690ed426438.

Branch: codex/allow-typed-evidence-review-architecture-019faa2d

Worktree: /Users/martinbechard/.codex/worktrees/9954/dev-methodology

Next Lifecycle Owner: Dev Backlog Coordinator

## User Action Required Evidence

Question: Do you approve modifying exactly the governed canonical definition skills/review-architecture/SKILL.md so architecture reviews use the existing shared typed-evidence model—exact quotation, summary, assessment, or not applicable—and allow explained not-applicable results without invented quotation?

Why User Owns It: Repository governance requires explicit exact-scope user approval.

Approved Governed Scope Requested: skills/review-architecture/SKILL.md only.

Ordinary Companion Scope After Approval: skills/review-architecture/references/review-checklist-architecture.md and focused assertions in scripts/test_bundle_content.py.

Exclusions: No other skill or agent definition; never hand-edit generated mirrors.

Preflight Evidence: python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change skills/review-architecture/SKILL.md returned classification governed-definition, outcome BLOCKED_APPROVAL_REQUIRED.

Unattended Work Boundary: All definition, companion test/reference, regeneration, review, verification, and delivery work stops; read-only inspection only.

Resumption: Record the answer, then complete User Action Required -> Ready -> Starting -> Running in this same canonical Thread before any mutation.

## Summary

Allow typed evidence in architecture review checklists.

## Context

The primary affected skill is skills/review-architecture/SKILL.md. The package requires exact quotation for every applicable result, including absence-based and derived structural conclusions that have no literal target text.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 30; skills/review-architecture/references/review-checklist-architecture.md:9-16; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use the shared typed-evidence model and allow explained not-applicable results without quotation.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Literal quotation, absence-based findings, and explained not-applicable results are represented truthfully.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover a literal quotation, an absence-based failure, and a conditional not-applicable result.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-architecture/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
