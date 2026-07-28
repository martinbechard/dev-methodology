# Allow typed evidence in high-level-design review checklists

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/allow-typed-evidence-review-high-level-design.md

Completion: direct-main

Owner: Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Allow typed evidence in high-level-design review checklists.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-9a42-7e11-9c24-207fde14359b

Root Agent Task: 019faa83-9a42-7e11-9c24-207fde14359b

Phase: Starting -> Running accepted by the root Dev Orchestrator before implementation.

Started At: 2026-07-28T21:00:15Z

Claim Evidence: Reservation claim SHARED_CHECKOUT_ACQUIRED reserve-six-ready-refill-high-level-design-019fa9bb-retry, acquisition journal event 969dc859-f1ca-4b19-8ced-ae084cbca933. Acceptance claim SHARED_CHECKOUT_ACQUIRED accept-running-high-level-design-019faa83, acquisition journal event 7dc68740-6349-428b-bb6d-5f235b8aba09; backlog-mutation:primary extension journal event e4c5e9b4-40c2-47cc-86f1-fc1bf6d2812c.

## Summary

Allow typed evidence in high-level-design review checklists.

## Context

The primary affected skill is skills/review-high-level-design/SKILL.md. The package forces quotation for derived coverage, missing contracts, diagram-trigger analysis, and mode-dependent not-applicable questions.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 30; skills/review-high-level-design/references/review-checklist-high-level-design.md:9-16,32-47,71-85; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Align the skill and checklist with typed evidence and explanation-backed not-applicable results.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Mode-dependent not-applicable results carry an explanation instead of fabricated quotation.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover a mode-dependent not-applicable result, a missing-contract failure, and a literal quotation.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-high-level-design/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
