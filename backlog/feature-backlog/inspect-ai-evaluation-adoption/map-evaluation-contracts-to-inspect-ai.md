# Map Evaluation Contracts To Inspect AI

Status: Starting

Type: Analysis

Provider: file

Work Item ID: map-evaluation-contracts-to-inspect-ai

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Produce a source-backed mapping from every current governed evaluation responsibility to Inspect AI, a retained repository component, or an explicit unresolved gap before any live-model migration work begins.

## Context

The current runner combines ordinary evaluation infrastructure with repository-specific acceptance guarantees. Adoption is unsafe until task, dataset, agent, sandbox, scorer, Judge, evidence, report, status, cleanup, and publication responsibilities have explicit owners.

Estimated complexity is Medium. Estimated generation is 60,000–100,000 tokens, or 0.33–0.56 total agent-hours at the series planning rate, across 4–7 autonomous turns. Non-model runtime should remain below one hour.

## Source Evidence

The user authorized the Inspect-first phased adoption series on 2026-08-12 in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7. Phase 1 of the accepted proposal is contract mapping.

## Requirements

- Inventory current responsibilities from suite manifests, scenario catalogs, runner, reporting, tests, and protocol documentation.
- Map each responsibility to Inspect AI, a retained repository component, or an unresolved gap.
- Define categorical preservation for PASS, FAIL, BLOCKED, STALE, and INFRASTRUCTURE_FAILED.
- Identify candidate current code that could eventually be retired and code that must remain.
- Define evidence required for each later parity gate.
- Record current Inspect AI version, supported external Codex behavior, sandbox options, scorer APIs, multi-agent APIs, and log format from primary sources.
- Produce implementation recommendations without executing a paid live-model scenario.

## Acceptance Criteria

- Every governed status and evidence category has one explicit proposed owner.
- The mapping covers exact agent identity, topology, Judge independence, claims, Git mutation, containment, cleanup, and immutable reporting.
- Unknowns are explicit and routed to a later spike.
- An independent architecture review accepts the mapping as implementable and proportionate.
- The result states whether Phase 2 may proceed.

## Dependencies

None.

## Verification

- Compare the mapping against the current runner and protocol sources.
- Verify Inspect claims against current official documentation and pinned package APIs.
- Obtain independent architectural review.
- Run documentation and diff checks applicable to the produced artifact.

## Open Questions

- Which Inspect version should become the pilot baseline?
- Should governed status be represented as named scores, metadata, a retained result artifact, or a combination?

## Starting Handoff Evidence

- Reserved At: 2026-08-13T16:17:44Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `3e4a7b3c7e3dbeb8cdd86215fbc8f13ed8766e9b` on primary `main`.
- Series Position: First item in `backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md`; every later series child remains effective Holding.
- Priority: Oldest eligible ordered-series head after Offline staging reconciliation completed and released its evaluation and integration ownership.
- Capacity: Runs alongside `reconcile-project-organiser-filename-selection-regression-gaps`; Blocked, User Action Required, and later effective-Holding series children are excluded.
- Overlap: This Analysis may inspect evaluation sources read-only and must claim only its mapping artifact and directly required verification paths before mutation. It must not mutate Project Organiser's shared bundle-test surface or unrelated plan artifacts.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and assigns title and messaging responsibility to the visible root task.
- Transition Claims: Work Item `start-map-evaluation-contracts-work-item`; event `efb03db7-eff3-4716-b0b9-8ca920c696fb`. Provider `start-map-evaluation-contracts-provider`; event `7e9bbe1d-58c6-499a-8082-1e78d5692137`.
- Canonical Codex Task ID: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`.
- Canonical Conversation ID: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` (combined runtime identity).
- Runtime Host: `local`.
- Runtime Project: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Runtime Created At: `2026-08-13T16:18:30Z` (`1786637910`).
- Requested Title: `Starting — Map Evaluation Contracts To Inspect AI`; the runtime preview is ellipsized only.
- Runtime Creation Outcome: Unique success with no client or pending identity. Creation does not imply Running.
