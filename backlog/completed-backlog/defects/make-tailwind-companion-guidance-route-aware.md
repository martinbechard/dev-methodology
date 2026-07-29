# Make Tailwind companion guidance conditional on active-scope routing

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/make-tailwind-companion-guidance-route-aware.md

Completion: direct-main

Owner: Dev Orchestrator

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Launch Reservation: reserve-six-approved-ready-starting-019fa9bb.
- Dispatch Time: 2026-07-28T22:42:49Z.
- Normalized Objective: Make Tailwind companion guidance conditional on active-scope routing.
- Intended Root Role: Dev Orchestrator.
- Canonical Runtime Thread and Root Agent Task: 019faa83-d3c4-7962-b3f8-f4b1a9845d94.
- Observed Launch Evidence: The existing canonical work-item Thread is preserved for resumption. No replacement Thread is authorized.
- Starting -> Running Requirement: The preserved root Dev Orchestrator must accept this same Thread and atomically record Starting -> Running with canonical identity, branch, worktree, and accepted ownership evidence before repository mutation.

## Running Acceptance

- Transition: Starting -> Running.
- Accepted Owner: Dev Orchestrator.
- Canonical Runtime Thread and Root Agent Task: 019faa83-d3c4-7962-b3f8-f4b1a9845d94.
- Branch: codex/tailwind-companion-route-aware-019faa83.
- Worktree: /Users/martinbechard/.codex/worktrees/41ca/dev-methodology.
- Phase: Running acceptance complete; approved Tailwind guidance correction is pending the separate governed-source approval-record and pre-mutation check.
- Approved Governed Scope: skills/tailwind-design-system/SKILL.md only.
- Repository Mutation Boundary: No source mutation occurred before this Running acceptance became durable. Any later source mutation remains gated on the exact-scope approval record and successful supported pre-mutation check.

## Completion Evidence

- Completed At: 2026-07-29T00:11:23Z.
- Completion Selector: direct-main.
- Accepted Source Candidate: 5f149c41ead5edf668617d76b675563c823352b8; source paths: skills/tailwind-design-system/SKILL.md, scripts/test_tailwind_design_system.py, and design/generated/skill-definitions.js.
- Independent Review: ACCEPT with no actionable findings.
- Independent Verification: VERIFIED PASS.
- Integration: fresh current-main cleanup branch codex/tailwind-companion-route-aware-integration-019faa83; merge commit b5c77cf1abe9127ae303eb91ab8a16ad0487221e; current-main reconciliation commit and observed primary-main tip d6ea790d90238b1efb0bcf04fb47cd624191afb0.
- Main Reachability: source candidate 5f149c41ead5edf668617d76b675563c823352b8 and integration tip d6ea790d90238b1efb0bcf04fb47cd624191afb0 are ancestors of primary main.
- Primary-Main Checks: Python 3.11 focused unittest, 3 tests OK; skill validation passed; build-skill-docs --check passed; py_compile passed; governed source preflight ALLOWED_APPROVED_DEFINITION_CHANGE; mirror preflight ALLOWED_APPROVED_REGENERATION; and git diff --check passed.
- Approval Scope and Provenance: user approval from Parent Dev Backlog Coordinator task 019fa9bb-1423-7e80-bcde-3caa765e3758 approved only skills/tailwind-design-system/SKILL.md; no other governed definition was approved.
- Scoped Omission: an initial Apple Python 3.9 invocation failed only because an existing test_bundle_content import requires standard-library tomllib; the configured Python 3.11 rerun passed all checks.
- Delivery Authority: local primary main; no remote publication is configured or required.
- Cleanup Eligibility: codex/tailwind-companion-route-aware-integration-019faa83 is fully merged; cleanup is eligible under the direct-main completion process.

## User Action Required Resolution

- Resolved At: 2026-07-28T22:40:09Z.
- User Answer: `Approve - it should contail all tailwind guidance and not load other skills`.
- User-Message Provenance: Parent Dev Backlog Coordinator task 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Result: Treat `contail` as `contain`. Approved only skills/tailwind-design-system/SKILL.md. It must contain the Tailwind guidance it needs and must not instruct the reader to load companion or other skills. No other governed definition is approved.
- Approval Gate: Before any governed-source mutation, create the exact-scope approval record from this provenance and pass the supported pre-mutation check.
- Ready Resumption: Preserve canonical Thread and root task 019faa83-d3c4-7962-b3f8-f4b1a9845d94, branch, worktree, and history. The parent alone may separately reserve Ready -> Starting; the preserved root alone must separately accept Starting -> Running before repository mutation.

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Make Tailwind companion guidance conditional on active-scope routing.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-d3c4-7962-b3f8-f4b1a9845d94

Root Agent Task: 019faa83-d3c4-7962-b3f8-f4b1a9845d94

Branch: codex/tailwind-companion-route-aware-019faa83

Worktree: /Users/martinbechard/.codex/worktrees/41ca/dev-methodology

Phase: Completed; verified direct-main delivery observed on primary main.

Started At: 2026-07-28T21:00:12Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim complete-tailwind-route-aware-019faa83; acquisition journal event 7a438165-cae7-4675-ab2a-dcaa3151a555. Integration claim integrate-tailwind-route-aware-019faa83: SHARED_CHECKOUT_ACQUIRED journal 6e43b041-a07e-42d0-9487-c60b8b75da78 and RELEASED journal 82dbbef9-128a-480e-987c-3c5b2df16d3e. Preserved Running acceptance evidence: SHARED_CHECKOUT_ACQUIRED claim accept-running-tailwind-approved-019faa83; acquisition journal event 416a53f5-f73b-4f2d-bb5b-fc662ccc9462. Preserved User Action Required transition evidence: SHARED_CHECKOUT_ACQUIRED claim move-user-action-tailwind-019faa83; acquisition journal event 08db59f8-b414-418e-b747-92e3a7ded6ef. Preserved prior Running acceptance evidence: provider commit 48ec224dbc8a7981a0ea234990d3de1c599f0bad; SHARED_CHECKOUT_ACQUIRED claim accept-running-tailwind-019faa83, acquisition journal event bafae64e-bed6-4c26-aa1d-32a9a005094a, and release journal event 1f9c568f-a28e-48bf-a47a-fe4bbfd2e084. Preserved Starting reservation evidence: SHARED_CHECKOUT_ACQUIRED claim reserve-six-ready-refill-tailwind-019fa9bb-retry; acquisition journal event d7b2246e-4e09-43df-a8f7-a5a04455a0d9.

## Summary

Make Tailwind companion guidance conditional on active-scope routing.

## Context

The primary affected skill is skills/tailwind-design-system/SKILL.md. The unconditional five-skill combination can require unavailable tools and combine alternative Next.js and Vite runtime models even though Tailwind detection declares no companions.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 16; companion metadata for React Server Components, React Vite Renderer, Next.js App Router, Jest, and Playwright. Independent reviewer /root/confirm_new_routing_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use only framework, renderer, and test guidance supplied for the active scope.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Tailwind guidance uses only active-scope companion guidance.
- Alternative framework and renderer models are not combined.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover Tailwind with Vite and Next.js.
- Include a negative case where an un-routed test skill is not loaded.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

Do you explicitly approve changing exactly the governed skill definition skills/tailwind-design-system/SKILL.md so its Tailwind companion guidance uses only framework, renderer, and test skills already routed into the active scope?

## User Action Required

Why The User Owns This: The requested correction changes exactly one governed skill definition. Project policy requires explicit, scope-specific user approval before that canonical source may be changed. The supported pre-mutation check returned BLOCKED_APPROVAL_REQUIRED with exit 3.

Approve: Permits an exact provenance approval record, the supported pre-mutation check, a narrow canonical source correction, supported same-category regeneration, and focused Tailwind Vite, Next.js, and unrouted-test verification.

Defer: Moves or keeps this recognized work non-dispatchable until the user is ready, with no source mutation.

Decline: Leaves the definition unchanged and routes the item to an authorized terminal abandonment or failure disposition.

Unattended Stop: No source, generated mirror, test, candidate, review, verification, integration, or completion mutation may continue. Only lifecycle recording and read-only preservation are permitted.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/tailwind-design-system/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
