# Require Server Components evidence before activating the RSC skill

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/react-server-components-detection-boundary.md

Completion: direct-main

Owner: Root Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Require Server Components evidence before activating the RSC skill.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fda6-7201-9e3a-6a1a8df4a19d

Root Agent Task: 019faa18-fda6-7201-9e3a-6a1a8df4a19d

Branch: codex/react-server-components-detection-boundary-019faa18

Worktree: /Users/martinbechard/.codex/worktrees/9ba1/dev-methodology

Phase: Analysis and implementation-boundary investigation

Started At: 2026-07-28T19:03:36Z

Claim Evidence: running-react-server-components-boundary-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:03:30.746799Z; claim event e498df89-684d-4091-b085-c7bb1862e058; exact file scope backlog/defect-backlog/react-server-components-detection-boundary.md; primary main baseline c41405babcc4b80ecc5404f1e6908d201373fede.

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

## Completion Evidence

Completion Selector: direct-main

Accepted Source Commit: 425a2bf6f65de341608641ef4a5a8ae58fe94fb1

Integration and Observed Main Commit: 54b8f357c2620275c5b1bd6f023052fcb85bae20

Main Before Integration: f8f7936e03fc2ad84847dc2d416e17087e21a2e8

Integration Strategy: conflict-free cherry-pick -x followed by ff-only main observation.

Source Reachability: The accepted source is intentionally non-ancestral. Patch ID 134fff176c06fedb112dcac9469a4fe27d4ca2a0 and the exact accepted four-path/content mapping prove the replayed content in integration commit 54b8f357c2620275c5b1bd6f023052fcb85bae20.

Independent Review: ACCEPTED with no findings.

Independent Verification: PASS.

Post-Integration Validation: Focused Python 3.11 test reported 1 OK; generator --check was current; diff and clean checks passed.

Definition Boundary: No governed definition changed. No definition approval was required.

Publication: No remote publication was required; no push was performed.

Prior Integration Claim Events: attempt 1 acquired fe4bdb5c and released 74b34621; attempt 2 acquired 04e52dea and released 156df97c; final attempt acquired b687d351 and released 001d2ad0.

Preserved Prior Evidence: Evidence tag retained for old integration commit 6436bedb.

Completed At UTC: 2026-07-28T19:52:15Z

Cleanup Eligibility: Eligible after this terminal provider closure commits and the exact completion claim is released.
