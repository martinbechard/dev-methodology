# Make Tailwind companion guidance conditional on active-scope routing

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-tailwind-companion-guidance-route-aware.md

Completion: direct-main

Owner: Unowned

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

Phase: Ready for parent dispatch reservation; preserved canonical root must accept Starting -> Running before repository mutation.

Started At: 2026-07-28T21:00:12Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim move-user-action-tailwind-019faa83; acquisition journal event 08db59f8-b414-418e-b747-92e3a7ded6ef. Preserved Running acceptance evidence: provider commit 48ec224dbc8a7981a0ea234990d3de1c599f0bad; SHARED_CHECKOUT_ACQUIRED claim accept-running-tailwind-019faa83, acquisition journal event bafae64e-bed6-4c26-aa1d-32a9a005094a, and release journal event 1f9c568f-a28e-48bf-a47a-fe4bbfd2e084. Preserved Starting reservation evidence: SHARED_CHECKOUT_ACQUIRED claim reserve-six-ready-refill-tailwind-019fa9bb-retry; acquisition journal event d7b2246e-4e09-43df-a8f7-a5a04455a0d9.

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
