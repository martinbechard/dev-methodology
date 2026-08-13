# Map Evaluation Contracts To Inspect AI

Status: User Action Required

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

## Running Acceptance Evidence

- Accepted At: 2026-08-13T16:19:59Z.
- Owner: `/root/map_evaluation_contracts_to_inspect_ai` under the Dev Orchestrator Role.
- Canonical Codex Task: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`.
- Canonical Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`.
- Branch and Worktree: primary `main` at `/Users/martinbechard/dev/dev-methodology`.
- Phase: source inspection and bounded implementation planning.
- Acceptance: The dispatched root accepted execution ownership after acquiring the exact Work Item ID and provider path.

## Exhausted Correction Disposition

- Recorded At: 2026-08-13T17:53:55Z.
- Transition: `Running -> User Action Required`.
- Canonical Task and Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` on host `local`.
- Preserved Dev Orchestrator: `/root/map_evaluation_contracts_to_inspect_ai`.
- Preserved Candidate: `33d6a25350f5230cb359c1ad76397fea4dda44fc` on primary `main`.
- Attempt History: Three artifact-review correction cycles are consumed. A fourth cycle requires explicit user authority.
- Unresolved Finding 1: Responsibilities `R-001` through `R-062` require one-to-one metadata keyed by `Responsibility-ID`.
- Unresolved Finding 2: Every retirement row and each Phase 2–8 gate require explicit retirement-evidence traceability.
- Preserved State: The mapping artifact is clean and committed; all Map claims are released. Preserve the canonical execution, plan pair, candidate, review history, and series evidence.
- Series Effect: Later Inspect AI adoption children remain effective `Holding` while this first ordered item is nonterminal.
- Transition Claim: `map-inspect-ai-exhausted-review-uar-019ff2c3`; event `5866571d-9dc4-40b3-87eb-c19f081b1824`.

## User Action Required

### Question for the User

Do you authorize one exceptional fourth correction and fresh independent review cycle, limited exactly to adding one-to-one `Responsibility-ID` metadata for `R-001` through `R-062` and retirement-evidence traceability for every retirement row and the Phase 2–8 gates?

### Why User Input Is Required

The normal correction limit is exhausted. Both omissions affect required mapping completeness, so the Coordinator cannot authorize another cycle or silently exclude them.

### Options and Tradeoffs

- **Authorize one exceptional fourth cycle (recommended):** Complete only the two missing ledgers, obtain fresh independent review and focused verification, and preserve the existing candidate and all accepted content.
- **Do not authorize and abandon this delivery:** Preserve candidate `33d6a253` as incomplete evidence, end this Work Item without successful delivery, and keep later Inspect AI adoption phases from proceeding because their ordered prerequisite remains unsatisfied.

### Resolution

Pending in canonical Task and Conversation `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`.

### Unattended Work Boundary

Do not modify, review, verify, deliver, or close this Work Item until the user answers in its canonical visible task. Unrelated eligible Work Items may continue.
