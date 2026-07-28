# Route E2E evidence delivery through Commit authority

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/end-to-end-verification-commit-authority.md

Completion: direct-main

Owner: Unowned pending acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make end-to-end verification deliver evidence through the selected Commit workflow instead of unconditionally creating a commit.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending

Root Agent Task: Pending

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make end-to-end verification deliver evidence through the selected Commit workflow instead of unconditionally creating a commit.

## Context

The primary affected skill is skills/end-to-end-verification/SKILL.md. It unconditionally requires a commit before handoff even where the selected Commit workflow or request grants evidence-only authority. That exceeds the verifier's ownership boundary.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records this finding at skills/end-to-end-verification/SKILL.md:22. Independent reviewer /root/confirm_critical_a accepted it as CONFIRMED_CRITICAL.

## Requirements

- Route evidence delivery through the selected Commit workflow.
- Preserve read-only verification when mutation authority is absent.
- Do not create commits outside the selected workflow.

## Acceptance Criteria

- Direct-main and feature-branch contexts use only their selected delivery route; UNSET creates no commit and requires an explicit Commit-selection question/stop before delivery.
- Evidence-only verification produces a handoff without a verifier-created commit.
- The skill states the verifier and delivery-owner boundaries unambiguously.

## Dependencies

None

## Verification

- Exercise direct-main, feature-branch, UNSET, and evidence-only contexts.
- Confirm only the selected workflow can create commits.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/end-to-end-verification/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
