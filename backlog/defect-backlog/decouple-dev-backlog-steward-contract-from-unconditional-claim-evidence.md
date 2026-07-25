# Decouple Dev Backlog Steward Contract From Unconditional Claim Evidence

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/decouple-dev-backlog-steward-contract-from-unconditional-claim-evidence.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Decouple Dev Backlog Steward contracts from unconditional claim evidence.
- Dispatched At: 2026-07-25T01:42:15Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

## Summary

Make Dev Backlog Steward’s canonical and generated contracts honor resource_coordination none without requiring claim calls or claim evidence, while preserving strict claim behavior when agent-claim is selected.

## Context

Candidate cb5c7725 reproduced five broad scripts-gate failures that map to one distinct unrecorded defect: Dev Backlog Steward canonical and generated contracts use unconditional claim-evidence wording even when resource_coordination is none. This conflicts with the project-selected resource-coordination contract, which requires provider-none flows to make zero claim calls and require no claim evidence.

## Source Evidence

The candidate cb5c7725 broad scripts gate reproduced the five related failures. The user policy in parent Thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a requires every confirmed defect to be durably logged rather than treated as a warning.

## Requirements

- Identify the exact canonical and generated Dev Backlog Steward contract surfaces that unconditionally require claim evidence.
- When resource_coordination is none, require zero claim calls, registry mutations, releases, and claim-specific lifecycle evidence.
- When agent-claim is selected, preserve strict short backlog-claim acquisition, committed mutation, and truthful release evidence.
- Keep file-provider lifecycle ownership and resource-coordination selection independent.
- Obtain an exact canonical-path approval record before mutating any governed definition source.

## Acceptance Criteria

- Provider-none scenarios for Dev Backlog Steward complete with zero claim calls and no claim-specific evidence requirement.
- Agent-claim-selected scenarios retain required acquisition, commit, and release evidence.
- Canonical source, generated adapter, and applicable scripts/evaluation/bundle surfaces agree on the selected behavior.
- The focused reproducer for the five related gate failures passes or is replaced by evidence-backed equivalent coverage.

## Dependencies

None.

## Verification

- Refine and run a focused reproducer across the affected scripts, evaluation, and bundle surfaces.
- Run focused resource-coordination-none and agent-claim-selected lifecycle tests.
- Run generated-definition freshness and applicable broad scripts gate checks.
- Obtain fresh independent review.

## Open Questions

- Which exact canonical Dev Backlog Steward definitions and derived adapters are implicated by the candidate’s five failures?

## Notes

This record preserves the current confirmed scope for implementation discovery. Do not change a governed canonical definition without a successful exact-path approval-manifest check.
