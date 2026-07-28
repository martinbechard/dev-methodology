# Resolve the project-wiki template from the installed skill catalog

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/make-project-wiki-template-resolution-install-portable.md

Completion: direct-main

Owner: Completed / Root Dev Orchestrator / canonical task 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Prior Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Resolve the project-wiki template from the installed skill catalog.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Canonical Branch: codex/project-wiki-template-resolution-portable-019faa18

Assigned Worktree: /Users/martinbechard/.codex/worktrees/c5e3/dev-methodology

Current Phase: Completed and archived after verified direct-main delivery.

Started At: 2026-07-28T19:03:10Z

Claim Evidence: running-project-wiki-template-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:03:10.486935Z; claim event a7ae62a2-3ac9-411b-bb9a-21601bd1c398.

Completed At: 2026-07-28T23:19:45Z

Next Lifecycle Owner: None; terminal archive

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

## Starting Reservation

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Launch Reservation: reserve-four-approved-ready-starting-project-wiki-template-019fa9bb.

Dispatch Time: 2026-07-28T22:09:28Z.

Normalized Objective: Resolve the project-wiki template from the installed skill catalog.

Intended Root Role: Dev Orchestrator.

Canonical Runtime Thread and Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf.

Observed Launch Evidence: Existing canonical work-item Thread is preserved for resumption; no replacement Thread is authorized.

Starting -> Running Requirement: The preserved root Dev Orchestrator must accept this same Thread and atomically record Starting -> Running with the canonical identity, branch, worktree, and accepted ownership evidence before repository mutation.

## Running Acceptance Evidence

Accepted Owner: Root Dev Orchestrator / canonical task 019faa18-fde1-7690-ba81-7eb1a23bf4cf.

Accepted Runtime Thread and Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf.

Accepted Branch and Worktree: codex/project-wiki-template-resolution-portable-019faa18; /Users/martinbechard/.codex/worktrees/c5e3/dev-methodology.

Required Pre-Implementation Gate: Create the delegated-user-direction approval record for skills/project-wiki-create/SKILL.md only and run the exact definition-change preflight before any governed-definition mutation.

No-Mutation-Before-Preflight Evidence: The approved scope and exclusions remain recorded in Resumption Evidence; no governed definition, approval record, test, generated file, or unrelated path was mutated by this acceptance transaction.

Acceptance Claim Evidence: running-project-wiki-template-approved-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T22:59:00.533782Z; claim event 565fba33-65de-4547-bda7-36aeb816855e.

## Completion Evidence

Completion Disposition: READY for direct-main provider closure.

Accepted Source Commit: 4568e98fbd05b69b5aadfe6510eec4b173e5f28c.

Integration and Observed Main Commit: d2aecb0a6216786f105aed7a7dd8e13930724dae on local configured main.

Integration Strategy: cherry-pick -x then fast-forward.

Non-Ancestral Mapping Evidence: The accepted source is non-ancestral. Exact four-path byte mapping was proven, and d2aecb0a6216786f105aed7a7dd8e13930724dae is reachable from main.

Delivered Paths: approval-record-project-wiki-template-resolution.yaml; skills/project-wiki-create/SKILL.md; scripts/test_install_skills.py; design/generated/skill-definitions.js.

Definition Preflight: ALLOWED_APPROVED_DEFINITION_CHANGE.

Independent Review: APPROVED with no findings.

Independent Verification: VERIFIED. Focused source and clean-install regression, single-skill validation, build-skill-docs freshness, and diff checks passed. The reviewer additionally ran the full installer module: 81 tests passed.

Post-Integration Verification: Focused regression, freshness, diff, reachability and content mapping, and clean-state checks passed on primary main.

Remote Publication: No remote push was required; local configured main is the delivery authority.

Integration Claim Evidence: Acquired as SHARED_CHECKOUT_ACQUIRED, event 23b99e11-f146-4334-a23c-bb80f95e53a9; released as RELEASED, event 6abb32c8-5935-4156-9148-1e5c0e4bb5f5.

Cleanup Eligibility: Integration branch and worktree codex/project-wiki-template-resolution-integration-019faa18 at /Users/martinbechard/dev/dev-methodology/.worktrees/project-wiki-template-resolution-integration-019faa18 are cleanup-eligible after provider closure.

Terminal Provider Claim Evidence: complete-project-wiki-template-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T23:19:45.407453Z; claim event ff92ebe6-f51b-4457-bbdd-7b182e89ff02.

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
