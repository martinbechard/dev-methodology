# Add Structured Commit Disposition To Orchestrator Evaluation Contract

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/add-structured-commit-disposition-to-orchestrator-evaluation-contract.md

Completion: direct-main

## Current Running Acceptance

- Owner: root Dev Orchestrator.
- Current Root Dev Orchestrator Agent Task: /root/resume_blocked_after_claim_publication/structured_commit_recovery.
- Parent Coordination Thread: /root/resume_blocked_after_claim_publication.
- Historical Canonical Work-Item Thread/Task: 019f970d-1e68-7563-b840-a18765cfb70a remains preserved and is not replaced.
- Branch: main.
- Primary Worktree: /Users/martinbechard/dev/dev-methodology.
- Phase: Current-main semantic reconciliation and read-only acceptance audit.
- Started At: 2026-07-26T07:23:02Z.
- Parent Reservation: One parent-owned launch reservation recorded at 2026-07-26T07:19:53Z under claim structured-commit-ready-starting-20260726 (acquisition event c007a46a-01d7-4b3e-8c26-ca8e352499fe).
- Claim-Free Private-Lane Evidence: No implementation lane exists yet; the live claim registry was empty before dispatch, and implementation has no active claim.
- Provider Mutation Claim: Exact-file lifecycle mutation acquired under structured-commit-disposition-running-20260726 (event 3002fe60-720e-4040-87bf-4a64ea2a1d9e); it protects only this provider record and does not grant implementation ownership.

## Recovery Resumption

- Transition: Blocked -> Ready.
- Recovery Authority: The user's explicit restart-blocked request for a fresh bounded recovery.
- Preserved Canonical Work-Item Thread/Task: 019f970d-1e68-7563-b840-a18765cfb70a. Retain all candidate, review, blocker, and approval history.
- Authority Boundary: Existing exact governed-definition approvals and User Action Required boundaries remain unchanged; this resumption grants no expanded definition authority.
- Required Sequence: Reconcile current-main semantics first, then make a bounded correction only if necessary; obtain fresh independent review and focused verification before direct-main delivery and provider closure. No full repository regression is required.
- Next Lifecycle Owner: Parent Dev Backlog Coordinator reserves Ready -> Starting; root Dev Orchestrator acceptance remains required before Running.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Add structured Commit disposition to the Dev Orchestrator evaluation contract.
- Dispatched At: 2026-07-25T02:12:50Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: 019f970d-1e68-7563-b840-a18765cfb70a

## Lifecycle Start

- Owner: root Dev Orchestrator
- Canonical Runtime Identity: 019f970d-1e68-7563-b840-a18765cfb70a
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/f18e/dev-methodology
- Canonical Branch State: detached at 930261abea315b05c167a426d6e8729453b88a71
- Phase: Diagnosis complete; the supported classifier returned ALLOWED_ORDINARY_CHANGE for evals/agent-tests/dev-orchestrator/suite.yaml and its suite-contract skill, so no governed-definition mutation is proposed; implementation waits only for distinct active claim-audit repair release of overlapping runner, test, and fixture paths.
- Coordination Evidence: The parent reserved this item in Starting, and the Dev Backlog Steward recorded this atomic Starting-to-Running acceptance on primary main under claim structured-commit-disposition-start-019f970d (event 14c1785e-ef75-43f0-a445-c72ebb0c9efc).

## Summary

Make the Dev Orchestrator evaluation contract represent the structured effective-Commit disposition that its suite skill promises, rather than binding final verification directly to Dev Backlog Steward closeout without a Commit receipt.

## Context

The Dev Orchestrator suite skill promises a structured effective-Commit disposition. Its scenario and report schema contain no Commit receipt, however, and deterministically bind final verification directly to Dev Backlog Steward closeout. This makes the evaluated contract unable to demonstrate the promised Commit decision boundary.

## Source Evidence

Fresh independent prompt-review finding from canonical task 019f96ce-b1a0-7633-97ab-336ba7d188e4. Read-only search found no matching active or completed record. This item records the finding only and authorizes no unrelated fix.

## Requirements

- Identify the suite skill, scenario, report schema, and judge/supervisor surfaces that promise or consume the effective-Commit disposition.
- Add an explicit structured Commit receipt or equivalent evidence boundary before final verification and Dev Backlog Steward closeout.
- Preserve the existing separation between implementation, review, verification, Commit application, and provider lifecycle mutation.
- Keep closeout blocked when the required effective-Commit disposition is absent or inconsistent.
- Obtain exact canonical-path approval before changing any governed definition source.

## Acceptance Criteria

- The Dev Orchestrator evaluation can observe and judge a structured effective-Commit disposition.
- Final verification and Dev Backlog Steward closeout are ordered after the recorded Commit disposition.
- A missing, rejected, or inconsistent Commit receipt produces an evidence-backed non-success verdict.
- Focused scenarios and report-schema checks cover the receipt and ordering contract.

## Dependencies

None.

## Verification

- Run focused Dev Orchestrator suite scenarios and report-schema tests.
- Run the relevant evaluator, bundle-content, and generated-definition freshness checks.
- Obtain fresh independent review.

## Open Questions

- Which existing structured handoff schema is the narrowest authoritative representation for the effective-Commit disposition?

## Notes

Do not implement this finding as part of unrelated candidate work. Governed-definition changes require a successful exact-path approval-manifest check before mutation.

## Blocked Handoff

- Owner: Unowned
- Claim: None (released)
- Canonical Runtime Identity: 019f970d-1e68-7563-b840-a18765cfb70a
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a (recovery identity only)
- Disposition: The bounded correction loop is exhausted. Do not integrate the preserved candidate as-is.
- Candidate History: Rejected candidates a04493177067abc3f40bc5bb49dcf91a601b0c65 and 3352102081b85c3dcda4c23a22bb238c84b2062b; final preserved candidate 9f0aafce2281519b5d35dbffe0cba72561e50ed9.
- Released Candidate Ownership: All candidate claims are released. The final release event is 905da8cd-f1f5-4cf5-9148-36b19f6670ad. The preserved candidate worktree and branch are clean: codex/add-structured-commit-disposition-correction2-019f970d.
- Fresh Code And Prompt Review Blockers:
  - The file-provider Persistence receipt is self-asserted because the runner does not verify the configured backlog item's committed lifecycle state and archive path, and the positive fixture commits closeout.txt.
  - The coordinator prompt contradicts the parser by requiring every sessionIds value to be non-empty while provider-none and BLOCKED dispositions require empty arrays.
  - The promised AWAITING_REVIEW-to-READY same-delivery continuity is not executable across distinct nonterminal and terminal provider updates.
- Recorded Checks: 38/38 fixtures passed; staging 2/2 passed; schema, bundle, skill, validate, py_compile, and diff checks passed. The broad runner result was 107/120, with the same 13 baseline Playwright environment failures.
- Unblock Condition: Authorize and resume a fresh bounded correction that evidence-binds file-provider state and archive bytes to retained Dev Backlog Steward execution, fixes the prompt empty-session rule, and adds executable phase continuity. It must then receive fresh independent code and prompt review plus verification.
