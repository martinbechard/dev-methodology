# Replace the structured-design chain-of-thought output contract

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/replace-structured-design-chain-of-thought-output-contract.md

Completion: direct-main

Owner: Root Dev Orchestrator task 019faa19-2538-7cd0-832e-62b428886363

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Replace the structured-design chain-of-thought output contract.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa19-2538-7cd0-832e-62b428886363

Root Agent Task: 019faa19-2538-7cd0-832e-62b428886363

Branch: codex/replace-structured-design-cot-contract-019faa19

Worktree: /Users/martinbechard/.codex/worktrees/3d44/dev-methodology

Phase: Lifecycle accepted; implementation authorization and source analysis pending.

Started At: 2026-07-28T19:05:44.790829Z

Claim Evidence: Initial exact-file acquisition was refused with DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED while three other primary backlog transactions were uncommitted. Parent Coordinator recovery committed those transactions through clean primary main 41e61c0a92fd8fe1d6bfbb696923a4abef8376d8 and reconciled claims as STATUS with claims []. Claim running-replace-structured-design-cot-contract-019faa19 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:05:44.790829Z; claim journal event 28c352c9-c935-4650-9b87-23c41d6a2e8e.

## Summary

Replace the public chain-of-thought output contract in structured-design with concise observable design evidence.

## Context

The primary affected skill is skills/structured-design/SKILL.md. It requires public chain-of-thought output, which is not an appropriate durable artifact contract. The review companion may also need alignment if its instructions change.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the output-contract finding for skills/structured-design/SKILL.md; skills/review-structured-artifact/SKILL.md is directly cited as the companion CHAIN-OF-THOUGHT review surface. Independent reviewer /root/confirm_critical_e accepted it as CONFIRMED_CRITICAL.

## Requirements

- Replace chain-of-thought output requirements with concise decision, evidence, and uncertainty artifacts.
- Preserve structured-design usefulness without requiring hidden reasoning disclosure.
- Align the review companion only if its contract actually conflicts.

## Acceptance Criteria

- Structured-design output contains observable design conclusions and supporting evidence without requiring chain-of-thought.
- The revised contract remains reviewable.
- Any changed review companion uses the same safe output boundary.

## Dependencies

None

## Verification

- Produce a representative structured-design artifact.
- Confirm it includes conclusions, evidence, and uncertainty without chain-of-thought.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/structured-design/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. If skills/review-structured-artifact/SKILL.md changes, it requires separate exact-path approval and a separate accepted pre-mutation check.
