# Assert Strengthened Fixture Root Prompt Boundary

Status: Completed

Type: Defect

Owner: Dev Orchestrator (/root)

Provider: file

Provider Reference: backlog/completed-backlog/defects/assert-strengthened-fixture-root-prompt-boundary.md

Completion: direct-main

## Summary

Align the focused prompt regression with the strengthened fixture-root boundary so the full clause cannot silently regress.

## Context

The strengthened prompt requires every suite-owned path below fixtureRoot, but the focused test asserts only the pre-existing never-under-/tmp phrase. A regression could revert the strengthened clause unnoticed.

## Source Evidence

Fresh review of candidate 1eab8bb66c2eb24d841d53c4b136f0638527c1c3 in canonical task 019f978e-28b7-7561-be38-b535ab26850f confirmed this distinct defect on 2026-07-25. Standing user direction requires each additional confirmed defect to be logged durably.

## Requirements

- Assert the full strengthened fixture-root prompt boundary in the focused regression.
- Keep the existing never-under-/tmp boundary assertion where it remains applicable.
- Do not weaken the established boundary.
- Do not mutate governed definitions without required exact approval evidence.

## Acceptance Criteria

- The focused regression distinguishes and asserts the full strengthened fixtureRoot clause.
- The focused prompt contract passes.
- The resulting contract does not weaken the established boundary.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle correction edits.

## Verification

- Run the focused fixture-root prompt contract regression.
- Run relevant runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Assert strengthened fixture-root prompt boundary.
- Dispatched At: 2026-07-26T16:58:35Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: 019f9f5e-0150-7832-aaf4-a2eaa5c6b58c.
- Coordination Classification: The Dependencies entry is a coordination-only overlap note. Its referenced item is Blocked and Unowned, and the preflight registry has no live claim. Private-worktree implementation may begin; exact overlap scope and integration must be reconciled before the conflicting integration event.
- Next Lifecycle Owner: The root Dev Orchestrator owns delivery and must preserve this canonical Thread.

## Current Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-Item Thread: 019f9f5e-0150-7832-aaf4-a2eaa5c6b58c.
- Canonical Root Agent Task: 019f9f5e-0150-7832-aaf4-a2eaa5c6b58c.
- Root Dev Orchestrator: /root.
- Delivery Branch: codex/assert-strengthened-fixture-root-prompt-boundary-019f9f5e.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/b21d/dev-methodology.
- Phase: Delivery accepted; implementation has not started in this provider transaction.
- Started At: 2026-07-26T17:01:46Z.
- Claim Evidence: running-assert-strengthened-fixture-root-prompt-boundary-019f9f5e; acquire event c670a918-1b6b-42b8-ac28-35da9dd7f65c.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.

## Completion Evidence

- Completed At: 2026-07-26T17:16:12Z.
- Completion Disposition: READY for direct-main closure.
- Accepted Delivery Source Commit: 75557788bf7315034b7aa47a9a25ef9a528d9241.
- Direct-Main Integration Commit: 9ce6fd7c72f157f143a4ca159f3380f1452d0263.
- Source-To-Integration Mapping: Direct cherry-pick replay. Both commits contain the same six-line addition to evals/agent-tests/test_runner.py, and the integration commit message records the source commit.
- Main Observation: primary main was observed at 503a8f9ebcd1efa922c452e2a1dd492eed023ef7 before closure. It has since advanced cleanly to 0157f063bb3d95b7eece985b6f02baade46d310c, which retains 9ce6fd7c72f157f143a4ca159f3380f1452d0263 as an ancestor.
- Independent Review: GOOD.
- Independent Verifier: PASS.
- Candidate Verification: focused unittest PASS using Python 3.11.
- Post-Integration Verification: focused unittest PASS using Python 3.11; git diff --check PASS.
- Governed Definition Changes: none.
- Integration Claim: acquired at journal event 64733c7d-2f8e-47a4-b7a8-0d66d663a429 and released at journal event a69453e4-999a-4a5d-86e2-725374e96bd2.
- Running Claim: acquired at journal event c670a918-1b6b-42b8-ac28-35da9dd7f65c and released at journal event fe8068e9-f6b0-4e40-9639-e95f90929455.
- Terminal Provider Claim: complete-assert-strengthened-fixture-root-prompt-boundary-019f9f5e acquired at journal event e3761867-2c14-43b4-a1e1-5ffd396cedbd and extended to the exact archive path at event 9a3a7dad-2f4c-46e6-a5e4-a6a34b4e84a2. Release evidence follows this archive commit.
- Completed Archive Path: backlog/completed-backlog/defects/assert-strengthened-fixture-root-prompt-boundary.md.
