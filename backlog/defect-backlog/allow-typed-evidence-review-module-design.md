# Allow typed evidence in module-design review checklists

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/allow-typed-evidence-review-module-design.md

Completion: direct-main

Owner: Root Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Allow typed evidence in module-design review checklists.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-9a42-7e11-9c24-20a7a4264da3

Root Agent Task: 019faa83-9a42-7e11-9c24-20a7a4264da3

Phase: Implementation intake and governed-scope assessment

Started At: 2026-07-28T20:59:47Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim accept-running-module-design-019faa83; incarnation 8ad0f8bd-9fef-4949-bb1c-2c9fc4e9ca0c; claim journal event 2eae4bd2-7cda-4c60-8b5d-51591f3a33fc; exact provider path claimed in the primary main checkout.

Branch: codex/allow-typed-evidence-review-module-design-019faa83

Worktree: /Users/martinbechard/.codex/worktrees/e3a5/dev-methodology

## Summary

Allow typed evidence in module-design review checklists.

## Context

The primary affected skill is skills/review-module-design/SKILL.md. Conditional, operation-reconciliation, omission, and structural checks cannot all be supported by literal source quotations.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 31; skills/review-module-design/references/review-checklist-module-design.md:9-16,42-103; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use typed evidence in both the skill and direct checklist.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Conditional and omission findings retain their evidence type and explanation.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover an omitted operation, a non-applicable asynchronous boundary, and a resolved exact quotation.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-module-design/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
