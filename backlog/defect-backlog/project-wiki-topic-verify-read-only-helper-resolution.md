# Keep topic verification read-only and make helper checks executable

Status: Blocked

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-topic-verify-read-only-helper-resolution.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Keep topic verification read-only and make helper checks executable.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fde3-7d20-ad68-77bfcf160fbd

Root Agent Task: 019faa18-fde3-7d20-ad68-77bfcf160fbd

Next Lifecycle Owner: Dev Backlog Coordinator

Branch: codex/project-wiki-topic-verify-helper-resolution-019faa18

Worktree: /Users/martinbechard/.codex/worktrees/5cd1/dev-methodology

Phase: Blocked — validation-root configuration authority required

Started At: 2026-07-28T19:03:33Z

Claim Evidence: running-project-wiki-topic-verify-helper-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED on primary main at 2026-07-28T19:03:26.668254Z; claim journal event 9df147d9-db17-41a7-a86d-bc5923f35672.

Running Acceptance Time: 2026-07-28T21:53:54Z

Resumed Running Claim Evidence: running-resumed-project-wiki-topic-verify-helper-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED on primary main at 2026-07-28T21:53:49.399159Z; claim journal event 0c1f90d5-0391-42c5-a22a-7fc48b95448e.

Running Lifecycle Commit: 41e61c0a92fd8fe1d6bfbb696923a4abef8376d8

## User Action Required

Question: Do you approve changing the governed definition skills/project-wiki-topic-verify/SKILL.md to keep verification strictly read-only and resolve its project-wiki helper commands from the loaded installed/source skill location?

Why User Owns It: root AGENTS.md requires explicit exact scope-specific approval for every skill-definition change.

Approval Scope: skills/project-wiki-topic-verify/SKILL.md only.

Exclusions: No approval for any other skill or agent definition, no hand edits to generated mirrors, no cross-family regeneration, and no implementation before approval. Ordinary non-governed test or checklist corrections are not part of this approval grant.

Preflight Evidence: Lines 51-52 and 104 use unresolved project-wiki-skill-root. Line 51 authorizes okf-migrate despite the read-only contract on lines 3, 10, and 53. skills/project-wiki/scripts/test_setup_guidance.py currently codifies these defects; its focused 8-test run passed, proving test drift rather than acceptance.

Unattended Stop: No governed definition mutation, candidate production, integration, or completion may continue until approval is recorded and the supported pre-mutation check passes. Read-only evidence already collected is preserved.

Resolution: Approved on 2026-07-28. Exact user answer: ok I approve.

## Resumption Evidence

Transition: User Action Required to Ready recorded on 2026-07-28.

Answer Provenance: Exact answer ok I approve in preserved canonical Runtime Thread 019faa18-fde3-7d20-ad68-77bfcf160fbd directly after the recorded User Action Required question; routed to Parent Coordination Thread 019fa9bb-1423-7e80-bcde-3caa765e3758.

Approved Scope and Semantics: skills/project-wiki-topic-verify/SKILL.md only. Keep verification strictly read-only and resolve helper commands from the loaded installed or source skill location. Preserve existing exclusions. No other governed definition scope is approved.

Preserved Execution Identity: Runtime Thread and Root Agent Task 019faa18-fde3-7d20-ad68-77bfcf160fbd; branch codex/project-wiki-topic-verify-helper-resolution-019faa18; worktree /Users/martinbechard/.codex/worktrees/5cd1/dev-methodology; prior lifecycle history remains intact.

Pre-Mutation Requirement: Before any governed definition mutation, create the exact approval record from this user direction and pass the supported definition-change preflight for skills/project-wiki-topic-verify/SKILL.md.

## Blocked Evidence

Blocker: Required mcp-agent-ops skill_validate returned structured root-policy rejection: Path is outside configured skill roots: /Users/martinbechard/dev/dev-methodology/skills/project-wiki-topic-verify. skill-authoring forbids repository fallback after structured rejection.

Blocker Owner: Project Configurator / validator-root configuration authority.

Coordinator Action: Provide an authorized configured skill_validate route for repository source packages or route a governing validation-contract change through its own authority. Do not retry unchanged integration.

Unblock Condition: Configured validation supports this repository source package through an authorized root, or governing authority changes the validation contract.

Candidate and Delivery Preservation: Accepted candidate 77416fc3fde142b57d3addc676efa5986a852b08; preserved integration branch codex/integrate-topic-verify-read-only-helper-019faa18-77416fc3; preserved exact replay stash 6085a8100d81b3e11f4aaac1476e67582177bbb5; last unchanged main observation 3fbbd092055e4a3344b66d4a6b2c7db093d86345. No integration commit or main update occurred. Source worktree is clean.

Preflight, Review, and Verification Evidence: ALLOWED_APPROVED_DEFINITION_CHANGE and ALLOWED_APPROVED_REGENERATION prechecks; independent review APPROVED; verification VERIFIED PASS; focused tests 1/1; project-wiki tests 19/19; build-skill-docs --check and git diff --check passed; exact replay hashes and generated-delta equivalence confirmed.

Integration Claim Evidence: Integration claim acquired event e2adfc5a-982e-4644-aa11-12e05664be97 and released event 90850a74-484b-49f1-9ff9-ad207ef6b8bc.

Provider Claim Evidence: blocked-project-wiki-topic-verify-helper-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED on primary main at 2026-07-28T22:27:36.741385Z; claim journal event 69037ae4-07e9-48de-bce5-036c9934a4b5.

Permitted Resumption: Blocked to Ready only after Dev Backlog Coordinator verifies the unblock condition. Then require Ready to Starting to Running using the same canonical task before a new attempt.

## Starting Reservation Evidence

Transition: Ready to Starting recorded by Parent Dev Backlog Coordinator on 2026-07-28.

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Launch Reservation: resume-project-wiki-topic-verify-019faa18-fde3-7d20-ad68-77bfcf160fbd.

Reservation Time: 2026-07-28T21:49:12Z.

Canonical Execution Identity: Runtime Thread and Root Agent Task 019faa18-fde3-7d20-ad68-77bfcf160fbd; branch codex/project-wiki-topic-verify-helper-resolution-019faa18; worktree /Users/martinbechard/.codex/worktrees/5cd1/dev-methodology.

Required Next Acceptance: The existing sole Root Dev Orchestrator must separately accept Starting to Running through its Dev Backlog Steward before any governed-definition mutation. No replacement Thread is authorized.

## Summary

Keep project-wiki topic verification read-only and make its helper commands resolve from an executable installed location.

## Context

The primary affected skill is skills/project-wiki-topic-verify/SKILL.md. Its verification guidance invokes an operation that can mutate state despite the role’s read-only boundary and references an unresolved project-wiki-skill-root helper location.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the read-only and helper-resolution finding for skills/project-wiki-topic-verify/SKILL.md. Independent reviewer /root/confirm_critical_d accepted it as CONFIRMED_CRITICAL.

## Requirements

- Remove or redirect mutating helper operations from the read-only verification route.
- Resolve all required helper paths from a documented executable skill location.
- Preserve topic verification coverage.

## Acceptance Criteria

- Topic verification completes without mutating wiki state.
- Every documented helper command resolves in source and installed contexts.
- Verification findings remain reportable without an implicit repair action.

## Dependencies

None

## Verification

- Run the topic-verification route against a fixture and confirm no mutation occurs.
- Resolve each documented helper command from source and installed contexts.
- Run focused verification tests and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki-topic-verify/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
