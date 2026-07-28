# Allow typed evidence in unit-test-plan review checklists

Status: User Action Required

Type: Defect

Provider: file

Provider Reference: backlog/user-action-required/allow-typed-evidence-review-unit-test-plan.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Allow typed evidence in unit-test-plan review checklists.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-d3aa-7c61-a6fb-aec4584086bb

Root Agent Task: 019faa83-d3aa-7c61-a6fb-aec4584086bb

Branch: codex/allow-typed-evidence-review-unit-test-plan

Worktree: /Users/martinbechard/.codex/worktrees/9beb/dev-methodology

Phase: Waiting for User - definition approval

Started At: 2026-07-28T21:00:28Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim accept-running-unit-test-plan-019faa83; acquisition journal event e34a3ba4-2923-49f2-a37b-5f71cee17153. Live claim status immediately before acceptance also showed the unrelated recovery claim document-outline-skill-file-019fa9bf owning only .agents/skills/create-document-outline/skill.md and no overlapping path; separate claim accept-running-module-design-019faa83 owns only backlog/defect-backlog/allow-typed-evidence-review-module-design.md and also does not overlap this provider file.

Running Provider Commit: 496c00920a559c11c4b498fa2b833b7c3d7215c0

Running Claim Release: RELEASED claim accept-running-unit-test-plan-019faa83; release journal event 86e95205-d90e-4a43-92ea-3f8c0f51fabb.

User Action Required Transition Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim user-action-required-unit-test-plan-019faa83; acquisition journal event 96e9b513-95b8-486c-ae30-220245a5b721.

## User Action Required

Do you explicitly approve changing the governed skill definition skills/review-unit-test-plan/SKILL.md so its unit-test-plan review workflow accepts typed evidence—exact quotation, summary, derived assessment, or not applicable—instead of requiring quoted evidence for every applicable checklist result?

Why Input Is Required: root AGENTS.md and PROJECT.yaml require explicit scope-specific user approval for skills/*/SKILL.md. The supported preflight command below returned {"classification":"governed-definition","outcome":"BLOCKED_APPROVAL_REQUIRED"} with exit 3.

```text
python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change skills/review-unit-test-plan/SKILL.md
```

Smallest Correction: The governed SKILL.md must change because Workflow step 3 mandates “status, quoted evidence, and assessment” for every applicable question, while the acceptance criteria require the skill and checklist to accept typed evidence.

Concrete Example:

- Before: a missing source conflict or non-applicable failure case must manufacture or force a quotation even though its conclusion is derived or not applicable.
- After: the checklist item identifies Evidence type as exact quotation, summary, assessment, or not applicable; names Evidence source; records the appropriate evidence or reason; and grounds Assessment in that typed evidence.

Consequences:

- Approve: after the answer is durably recorded, the parent routes User Action Required -> Ready -> Starting for this same canonical Thread; the same root Orchestrator accepts Running; an exact-scope approval record citing the user message is created; the supported preflight must return ALLOWED_APPROVED_DEFINITION_CHANGE before mutation. Only then may the exact governed SKILL.md change, with ordinary non-governed direct-checklist/test corrections and only supported distributed-skill regeneration handled within the resumed item.
- Defer: move to Holding, preserve identities and evidence, and make no definition, checklist, test, or generated changes until deliberately resumed.
- Decline: end the item through the authorized Abandoned or failed archive path, preserving the decision and evidence, with no definition, checklist, test, or generated changes.

Blocker Owner: User

Unblock Condition: Explicit approval of exactly skills/review-unit-test-plan/SKILL.md, followed by the durable answer and resumption sequence and a successful supported preflight.

Next-Action Owner: User for the answer, then parent Dev Backlog Coordinator and sole Dev Backlog Steward for lifecycle routing.

Unattended Stop: Do not mutate skills/review-unit-test-plan/SKILL.md, its direct checklist, tests, generated mirrors, or other implementation artifacts. Do not perform unsupported or cross-family regeneration.

## Summary

Allow typed evidence in unit-test-plan review checklists.

## Context

The primary affected skill is skills/review-unit-test-plan/SKILL.md. Conflict absence, coverage gaps, duplicate-test assessment, and non-applicable failure cases require derived or not-applicable evidence, but the package requires quotations for every result.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 14; skills/review-unit-test-plan/references/review-checklist-unit-test-plan.md:5-10,15-31; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Apply the shared typed-evidence model across the skill and checklist.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Derived, not-applicable, and quotation-backed cases remain distinguishable.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover a missing source conflict, a non-applicable failure case, and a quotation-backed scenario.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-unit-test-plan/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
