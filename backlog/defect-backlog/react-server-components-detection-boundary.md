# Require Server Components evidence before activating the RSC skill

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/react-server-components-detection-boundary.md

Completion: direct-main

Owner: Unowned pending root acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Require Server Components evidence before activating the RSC skill.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending canonical child Thread creation after this durable reservation.

Root Agent Task: Pending canonical root Dev Orchestrator acceptance.

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Narrow React Server Components skill activation so it requires Server Components evidence rather than broad application TypeScript files.

## Context

The primary affected provider identity is skills/react-server-components. Its activation boundary is broad enough to select the RSC skill for application TSX without evidence that Server Components are present. The smallest accepted correction is detection.yaml-only.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the false-positive activation finding for skills/react-server-components. Independent reviewer /root/confirm_critical_d accepted it as CONFIRMED_CRITICAL.

## Requirements

- Require concrete Server Components evidence before activating the RSC skill.
- Preserve activation for projects that actually use Server Components.
- Keep detection metadata and its tests aligned.

## Acceptance Criteria

- Plain application TSX without Server Components evidence does not activate the RSC skill.
- A fixture with Server Components evidence activates it.
- Detection remains deterministic and documented.

## Dependencies

None

## Verification

- Cover plain application TSX and a Server Components fixture.
- Run focused technology-detection tests and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected provider identity, or overlapping accepted outcome.

This record has one primary affected provider identity: skills/react-server-components. The accepted smallest correction is skills/react-server-components/detection.yaml only, which is not presently a governed definition surface. No governed-definition approval is required unless later discovery changes skills/react-server-components/SKILL.md or skills/react-server-components/agents/openai.yaml; either change would require explicit scope-specific user approval, a provenance approval record, and the supported pre-mutation definition-change check.
