# Define Functional Specification UX Mockup Criteria

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/define-functional-specification-ux-mockup-criteria.md

Completion: direct-main

## Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: /root/process_backlog/orch_functional_spec_ux
- Proposed artifact claim: define-functional-spec-ux-mockup-criteria
- Branch: codex/define-functional-spec-ux-mockup-criteria
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/define-functional-spec-ux-mockup-criteria
- Phase: Lifecycle Running committed; artifact claim pending ARTIFACT GO.
- Starting main: af0a3fe63404a793f2bf7dcf40dd2a3de563109e
- Accepted candidate: Pending.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Open issues: Artifact work must not begin until ARTIFACT GO is issued.
- Next owner: Dev Orchestrator.
- Delivery evidence: Pending.

## Summary

Define deterministic, evidence-based criteria for when a functional specification requires UX mockups.

## Context

Functional specifications describe user-visible behavior, actor workflows, entry points, states, permissions, acceptance behavior, and verification. A mockup is useful only when supported interaction or layout complexity makes it necessary to communicate the contract; it must not become mandatory HTML for every functional specification.

## Source Evidence

- Direct user authorization in the 2026-07-22 parent coordination request to create this Ready Feature item.
- Current functional-specification guidance in skills/create-functional-spec/SKILL.md, skills/review-functional-spec/SKILL.md, and skills/development-methodology/assets/templates/functional-spec-template.md.

## Requirements

- Define deterministic criteria based on evidence-backed interaction and layout complexity for requiring a UX mockup.
- Do not require HTML or a visual mockup for every functional specification.
- Require an explicit no-mockup rationale for simple or non-visual specifications.
- Keep creation guidance, functional-specification template, and review checklist contracts compatible.
- Add focused tests that distinguish mockup-required and no-mockup cases.
- Before mutating any governed skill definition, obtain exact scope-specific user approval and run the supported pre-mutation approval check.

## Acceptance Criteria

- Criteria can be applied consistently from documented interaction and layout evidence.
- A simple or non-visual specification can pass with a concrete no-mockup rationale.
- A specification with qualifying interaction or layout complexity identifies the required mockup form and its contract role.
- The compatible template and review checklist make the same requirement observable.
- Focused tests cover positive and negative criteria cases.
- Any governed definition mutation has durable exact scope-specific approval evidence and passes the supported pre-mutation check.

## Dependencies

None.

## Verification

- Inspect the canonical functional-specification creation, template, review, and checklist contracts before implementation.
- Run focused tests and bundle checks for every approved changed surface.
- Run git diff --check and obtain independent review of the exact change.

## Notes

Mockup can mean a proportionate visual artifact; this work item does not prescribe HTML unless the approved criteria and evidence require it.
