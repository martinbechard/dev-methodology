# Enforce Agent-Claim Lifecycle Evidence In Runner Resource Scenarios

Status: Ready

Type: Defect

Owner: Unassigned

Provider: file

Provider Reference: backlog/defect-backlog/enforce-agent-claim-lifecycle-evidence-in-runner-resource-scenarios.md

Completion: direct-main

## Summary

Make the evaluation runner prove that an agent-claim resource-coordination scenario performed the required claim lifecycle, rather than accepting envelope-shaped receipts with no actual repository, registry, journal, acquisition, or release activity.

## Context

In `evals/agent-tests/runner.py`, the resource-coordination scenario path, handoff audit, and deterministic receipt validation accept a direct agent-claim scenario when its target trace is blank and it has no repository, claim registry, journal, acquisition, or release activity. The generic claim-lifecycle receipt checks validate the receipt envelope only; they do not bind its contents to the scenario actor or commit. This defect is distinct from candidate-only none-audit bypasses and records current-main behavior only.

## Source Evidence

- Canonical user direction in task `019f979e-5330-7501-8340-92dfd593f6ef` requires every additional confirmed distinct defect to be logged durably.
- Fresh code review of candidate `75390715` examined `_scenario_resource_coordination`, the handoff audit, and deterministic receipt validation in `evals/agent-tests/runner.py`.
- A direct reproducer was accepted despite absent claim activity and a blank target trace.

## Requirements

- For scenarios that select `resource_coordination: agent-claim`, require lifecycle evidence from the scenario execution rather than generic receipt shape alone.
- Bind required claim evidence to the scenario actor and the relevant committed execution state.
- Preserve distinct behavior for scenarios that select a different coordination provider or none.
- Do not treat candidate-only none-audit observations as current-main defects.

## Acceptance Criteria

- A selected agent-claim scenario retains contained registry and journal evidence for an acquisition and a normal release.
- The retained lifecycle evidence is bound to the scenario actor and commit used by the audited scenario.
- A scenario with no claim activity, an absent registry or journal record, a blank target trace, or a missing normal release is rejected deterministically.
- A negative regression test proves that envelope-valid generic receipts cannot satisfy the lifecycle requirement when claim activity is absent.

## Dependencies

None.

## Verification

- Run focused runner resource-coordination, handoff-audit, and deterministic-receipt tests.
- Run direct disposable scenario reproductions for valid acquisition-and-release evidence and absent claim activity.
- Run `git diff --check` and obtain fresh independent review.

## Open Questions

- Which existing receipt field can carry the contained registry and journal references without duplicating the claim engine's durable event model?

## Coordination Evidence

- Backlog claim `record-runner-review-defects-019f979e` acquired on primary main at 2026-07-25T05:39:43.871470Z; acquisition journal event `29dc95c6-c2ba-473b-8034-3420d7eecd6b`.

## Notes

This item is ready for independently scoped implementation. It does not authorize unrelated runner changes or governed-definition mutation without required approval evidence.
