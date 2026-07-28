# Stop UX review from performing runtime technology routing

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/stop-ux-review-runtime-technology-routing.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-defects-019fa9bb

Normalized Objective: Stop UX review from performing runtime technology routing.

Dispatch Time: 2026-07-28T19:19:58Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending runtime creation

Root Agent Task: Pending runtime acceptance

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Stop UX review from performing runtime technology routing.

## Context

The primary affected skill is skills/user-experience-review/SKILL.md. The skill tells an ordinary UX reviewer to route specialized guidance from repository evidence even though Project Configurator owns setup routing and Dev UX Specialist consumes supplied active-scope guidance.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 15; agents/roles/dev-activities/dev-ux-specialist.role.yaml:6,64. Independent reviewer /root/confirm_new_routing_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use only technology guidance already supplied for the active folder and report a routing gap when required guidance is missing.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- UX review consumes active-scope guidance without ad hoc technology routing.
- A missing required route is reported rather than inferred.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Provide repository evidence for an un-routed skill and require no ad hoc load.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/user-experience-review/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
