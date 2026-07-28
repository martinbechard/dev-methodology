# Align fix-explanation relationship examples with the six-type explanation model

Status: User Action Required

Type: Defect

Provider: file

Provider Reference: backlog/user-action-required/align-fix-explanation-item-taxonomy.md

Completion: direct-main

Owner: Root Dev Orchestrator 019fa9f9-33f0-7db3-90d5-2dc77dd89c06

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make fix-explanation relationship examples conform to the declared six-type structured-explanation model.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06

Root Agent Task: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06

Next Lifecycle Owner: Root Dev Orchestrator

## Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06.
- Canonical Root Agent Task: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06.
- Owner: Root Dev Orchestrator 019fa9f9-33f0-7db3-90d5-2dc77dd89c06.
- Branch: codex/align-fix-explanation-item-taxonomy.
- Worktree: /Users/martinbechard/.codex/worktrees/f57f/dev-methodology.
- Phase: Read-only source analysis and approval reconciliation.
- Started At: 2026-07-28T18:42:09Z.
- Started-At Evidence: The canonical root Dev Orchestrator accepted the parent reservation and authorized this distinct provider transition.
- Reservation Commit: 48bb5dd691c9763a1fff912ac1ff6200732b4814.
- Primary Main Reconciliation: main was clean at d794317a6cb4d47175522bb9df765bf654aace19 before this transaction.
- Initial Claim Status Evidence: The configured helper reported outcome STATUS with claims: [] before acquisition.
- Provider-Mutation Claim Evidence: running-acceptance-019fa9f9-33f0-7db3-90d5-2dc77dd89c06 acquired by dev-backlog-steward for this exact provider file; outcome SHARED_CHECKOUT_ACQUIRED; claim event 7c942f95-d112-45c5-8310-9557c9e387d3; claimed 2026-07-28T18:42:00.355710Z.
- Recovery History: An earlier claim attempt was refused with DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED; recovery event 335ebefc-8500-4e69-a6d4-6e58986e1e82. Independent recovery then reconciled primary main clean and the claim registry empty.
- Acceptance Evidence: Fresh independent exact-commit review was GOOD for batch-1 provider correction 1ef9018bf859607f161ff9a275c336c145b73b9a; promotion_complete: true.
- Dependencies: None.

## User Action Required

- Transition: Running -> User Action Required.
- Coordinator Decision: The required definition-change approval is a concrete user-owned decision.
- Canonical Work-Item Thread: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06, preserved for same-Thread resumption.
- Canonical Root Agent Task: 019fa9f9-33f0-7db3-90d5-2dc77dd89c06, preserved for same-Thread resumption.
- Running Lifecycle Commit: cde9160864182a00b5045bccc37a24b890a6f1f7.
- Exact User Question: “Do you approve changing exactly skills/fix-explanation/SKILL.md, limited to correcting its relationship examples so structured items use the six authorized item types—QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER—or so TEST, FIX, PROBLEM, and BENEFIT are clearly ordinary concepts rather than item types, while preserving the intended relationships? This does not authorize changing skills/structured-explanation/SKILL.md, skill metadata, or any other governed definition. Supported generated skill mirrors may be regenerated from this one approved source.”
- Why User Input Is Required: AGENTS.md and PROJECT.yaml require explicit scope-specific user approval for a governed definition change. The supported preflight returned BLOCKED_APPROVAL_REQUIRED, and the approval audit found no prior approval.
- Requested Approval Scope: skills/fix-explanation/SKILL.md only.
- Explicitly Excluded: skills/structured-explanation/SKILL.md, skill metadata, agents, and every other skill or governed definition.
- Prohibited Unattended Action: Do not mutate source, tests, or generated files; create an approval record; review; verify; integrate; or deliver until the user answers. Read-only evidence remains preserved.
- Resumption: Record the user's answer once, then preserve this canonical Thread and follow User Action Required -> Ready -> Starting -> Running through distinct authorized lifecycle transactions.

## Summary

Make fix-explanation relationship examples conform to the declared six-type structured-explanation model.

## Context

The primary affected skill is skills/fix-explanation/SKILL.md. Its relationship examples use TEST, FIX, PROBLEM, and BENEFIT as item types even though skills/structured-explanation/SKILL.md permits only QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER. The conflicting example makes the output contract unsatisfiable.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the conflicting examples at skills/fix-explanation/SKILL.md:152,191-196 and item-type authority at skills/structured-explanation/SKILL.md:30-37. Independent reviewer /root/confirm_critical_b accepted it as CONFIRMED_CRITICAL.

## Requirements

- Express relationship examples with permitted structured item types, or label those terms as ordinary concepts.
- Keep the six-type model authoritative.
- Preserve the intended fix-explanation relationships.

## Acceptance Criteria

- Every representative structured item uses one of the six declared item types.
- The relationship examples remain understandable without inventing additional types.
- The six-type model and fix-explanation examples no longer conflict.

## Dependencies

None

## Verification

- Produce a representative fix explanation.
- Assert that every structured item uses the declared six-type model.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/fix-explanation/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Discovery must separately justify any change to skills/structured-explanation/SKILL.md.
