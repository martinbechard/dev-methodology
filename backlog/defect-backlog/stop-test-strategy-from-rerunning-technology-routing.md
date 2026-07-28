# Stop test-strategy from rerunning technology-skill routing

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/stop-test-strategy-from-rerunning-technology-routing.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-defects-019fa9bb

Normalized Objective: Keep test-strategy work within the setup-selected technology-skill routing rather than rerunning detection during ordinary work.

Dispatch Time: 2026-07-28T19:19:58Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending runtime creation

Root Agent Task: Pending runtime acceptance

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Keep test-strategy work within the setup-selected technology-skill routing rather than rerunning detection during ordinary work.

## Context

The primary affected skill is skills/test-strategy/SKILL.md. It directs work to rerun technology-skill routing even though the project configuration assigns that detection responsibility to Project Configurator. This can create inconsistent routing and exceeds ordinary-work authority.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the routing conflict for skills/test-strategy/SKILL.md. Independent reviewer /root/confirm_critical_e accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use the setup-selected technology skillset during ordinary test-strategy work.
- Remove ordinary-work directions to rerun technology detection.
- Preserve a defined escalation route for genuine configuration changes.

## Acceptance Criteria

- Test-strategy does not rerun detector routing during ordinary work.
- It follows the project-configured skillset.
- A configuration-change route remains explicit and owned by Project Configurator.

## Dependencies

None

## Verification

- Exercise ordinary test-strategy work with configured routing.
- Confirm no detector rerun occurs.
- Verify the configuration-change escalation route remains available.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/test-strategy/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
