# Make agent-claim reset recover invalid JSON registry shapes

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/agent-claim-reset-invalid-json-shapes.md

Completion: direct-main

Owner: Root Dev Orchestrator task 019fa9f9-33f9-72f3-bbda-e18bbdea4bb5

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make the agent-claim reset operation recover every invalid JSON registry shape that its contract promises to repair.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-33f9-72f3-bbda-e18bbdea4bb5

Root Agent Task: 019fa9f9-33f9-72f3-bbda-e18bbdea4bb5

Branch: codex/agent-claim-reset-invalid-json-shapes-019fa9f9

Worktree: /Users/martinbechard/.codex/worktrees/8eed/dev-methodology

Phase: Root Dev Orchestrator accepted delivery ownership; implementation has not started.

Started At: 2026-07-28T18:44:20.209181Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim running-acceptance-agent-claim-reset-invalid-json-shapes-019fa9f9; incarnation 922ba317-8b4c-40ae-a083-d9f001d343a1; claim journal event 82780823-6fb1-4e00-82f2-3dc843eccfe2; exact provider path claimed in the primary main checkout.

Replacement / Re-home Evidence: The original acceptance Steward made no mutation because claim running-acceptance-agent-claim-reset-invalid-json-shapes-019fa9f9 returned DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED; recovery journal event cd02e4ee-d90b-4168-9c9a-b879b294f926. Parent Coordinator authorized this re-home after primary main was reconciled clean at 12f90c126d0bc6ea7d3ad5ab05792d35eb9d02a7.

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make the agent-claim reset operation recover every invalid JSON registry shape that its contract promises to repair.

## Context

The primary affected skill is skills/agent-claim-command/SKILL.md. Its reset contract promises recovery when the claim registry contains malformed contents. Independent review found that valid JSON with a non-object top-level value reaches a get call in skills/agent-claim-command/scripts/claim.py and can raise AttributeError instead of restoring a valid empty registry.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records this finding at skills/agent-claim-command/SKILL.md:153 and implementation confirmation at skills/agent-claim-command/scripts/claim.py:1999-2008. Independent reviewer /root/confirm_critical_a accepted it as CONFIRMED_CRITICAL.

## Requirements

- Define one recovery path for malformed JSON and valid JSON values that are not registry objects.
- Make reset return a valid empty registry for every supported invalid registry shape.
- Keep valid claim-registry behavior unchanged.

## Acceptance Criteria

- Reset succeeds for missing, malformed, non-object, and invalid claims-shape registries.
- Each supported reset leaves a valid empty registry.
- Existing valid registry reset behavior remains documented and tested.

## Dependencies

None

## Verification

- Exercise missing, malformed, non-object, and invalid claims-shape registry inputs.
- Confirm a valid empty registry after each supported reset.
- Run focused command-helper tests and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/agent-claim-command/SKILL.md. It does not authorize a skill-definition mutation. If the correction changes that governed SKILL.md, later implementation requires explicit scope-specific user approval naming the exact definition, a provenance approval record, and the supported pre-mutation definition-change check. A code-only correction to skills/agent-claim-command/scripts/claim.py remains subject to ordinary implementation review and verification.

## Completion Evidence

- Completed At: 2026-07-28T19:32:27Z.
- Accepted candidate: 0a005efbf36d446c1c8ce70c15c5cc6661e9b167.
- Direct-main integration: dfab50ca1b6bd4c1a6c956a3dae42baefbed6d1a. It changes only skills/agent-claim-command/scripts/claim.py and scripts/test_agent_claim.py, and its bytes were proven equivalent to the accepted candidate.
- Main observation: integration commit dfab50ca1b6bd4c1a6c956a3dae42baefbed6d1a is an ancestor of observed primary main e1aefd26240c2c343e154a462a76b05cc38b2565. The primary checkout was clean before this provider transaction.
- Review and verification: independent review GOOD; candidate and integration verification PASS, including focused command-helper tests and diff validation.
- Lifecycle and integration claims: acceptance acquire and release events 82780823-6fb1-4e00-82f2-3dc843eccfe2 and 8cd19f2d-037d-482d-83a2-a2d4c0145ae1; integration acquire and release events d68398af-22a9-4296-9204-f44a4d19aa2e and 0b523e08-e03a-4fec-b6fd-a10c1de3d168.
- Terminal provider claim: complete-agent-claim-reset-invalid-json-shapes-019fa9f9 acquired for the source and destination paths as SHARED_CHECKOUT_ACQUIRED, event de29ab34-24a1-4efe-a379-f4edbaa62d36.
- Source-to-integration mapping: candidate 0a005efbf36d446c1c8ce70c15c5cc6661e9b167 -> integration dfab50ca1b6bd4c1a6c956a3dae42baefbed6d1a.
