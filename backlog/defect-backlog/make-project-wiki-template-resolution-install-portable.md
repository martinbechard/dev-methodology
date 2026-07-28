# Resolve the project-wiki template from the installed skill catalog

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Prior Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Resolve the project-wiki template from the installed skill catalog.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Canonical Branch: codex/project-wiki-template-resolution-portable-019faa18

Assigned Worktree: /Users/martinbechard/.codex/worktrees/c5e3/dev-methodology

Current Phase: Ready for parent dispatch reservation; preserved canonical root must accept Starting -> Running before repository mutation.

Started At: 2026-07-28T19:03:10Z

Claim Evidence: running-project-wiki-template-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:03:10.486935Z; claim event a7ae62a2-3ac9-411b-bb9a-21601bd1c398.

Next Lifecycle Owner: User approval authority

## Resumption Evidence

User Answer: approved

Answered At: 2026-07-28

Answer Provenance: Canonical work-item Thread 019faa18-fde1-7690-ba81-7eb1a23bf4cf; exact user message immediately after the recorded User Action Required question.

Disposition: User Action Required -> Ready.

Approved Scope: skills/project-wiki-create/SKILL.md only.

Approved Semantics: Its Template section resolves project-wiki-template.md through the installed development-methodology catalog entry and the same catalog-root mechanism in a source checkout.

Exclusions Preserved: No review-routing change, other skill or agent definition, hand-edited generated mirror, or unrelated change.

Approval-Record and Preflight Requirement: Before any governed-definition mutation, create a delegated-user-direction approval record covering skills/project-wiki-create/SKILL.md and run scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change for that path using the record.

Preserved Canonical Thread and Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf.

## Summary

Make project-wiki creation resolve its template from the installed skill catalog instead of a dev-methodology source-checkout path.

## Context

The primary affected skill is skills/project-wiki-create/SKILL.md. It names a template location that exists only in the source checkout, so an installed skill cannot reliably locate the template. The separately proposed review-routing subfinding was rejected and is excluded from this item.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the non-portable template finding for skills/project-wiki-create/SKILL.md. Independent reviewer /root/confirm_critical_c accepted the template-resolution defect as CONFIRMED_CRITICAL and rejected the separate review-routing subfinding.

## Requirements

- Resolve the template from the installed project-wiki skill catalog.
- Keep source-checkout and installed-target paths supported without hard-coded repository assumptions.
- Do not alter review-routing behavior under this item.

## Acceptance Criteria

- A source checkout and installed target both resolve a valid template.
- No dev-methodology-only absolute or source-root template path is required.
- Review-routing text remains out of this correction scope.

## Dependencies

None

## Verification

- Resolve the template from a source checkout and an installed target fixture.
- Confirm both resolve the same required template artifact.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## User Action Required

Blocker: Definition-change approval is absent for the governed definition skills/project-wiki-create/SKILL.md.

Blocker Owner: User

Question: Do you approve changing the governed definition skills/project-wiki-create/SKILL.md only, so its Template section resolves project-wiki-template.md through the available installed development-methodology skill catalog entry (and the same catalog-root mechanism in a source checkout), without changing review routing or any other skill/agent definition?

Why User Input Is Required: Project guidance requires explicit scope-specific user direction before a governed skill definition can be changed. No prior authorization covers this exact definition and change scope.

Unattended Boundary: No governed definition mutation, implementation, generation, integration, or delivery may proceed until the exact approval is recorded. Read-only evidence remains preserved.

Exclusions: No review-routing changes; no other skill or agent definitions; no generated mirrors; no unrelated changes.

Preserved Canonical Identity: Runtime Thread and Root Agent Task 019faa18-fde1-7690-ba81-7eb1a23bf4cf; Parent Coordination Thread 019fa9bb-1423-7e80-bcde-3caa765e3758; Launch Reservation reserve-seven-batch2-defects-019fa9bb.

Preserved Delivery Context: Branch codex/project-wiki-template-resolution-portable-019faa18; worktree /Users/martinbechard/.codex/worktrees/c5e3/dev-methodology; lifecycle commit 31b48bb6b69941fef0ba8c698ea637bc9d47a78c.

Preserved Fixture Evidence: Clean fixture /tmp/project-wiki-portability.77vEwM. Installed template SHA-256 888d610236da436fd4c0bb4175a50e0313e65c75406788984ff83e682979a604 is present at installed-skills/development-methodology/assets/templates/project-wiki-template.md. The documented target-repository/skills/development-methodology/assets/templates/project-wiki-template.md is missing.

Recovery Evidence: The first claim attempt was rejected as DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED, event 368be21e-f62c-4242-8c25-e37cd27a1e9e. The Coordinator authorized recovery after the interfering transactions settled.

Transition Claim Evidence: user-action-project-wiki-template-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:10:46.660203Z; claim event fda0e1e9-704d-45e1-bfa1-8e10938f8fe3.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki-create/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
