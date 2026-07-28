# Make Tailwind companion guidance conditional on active-scope routing

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-tailwind-companion-guidance-route-aware.md

Completion: direct-main

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

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/tailwind-design-system/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
