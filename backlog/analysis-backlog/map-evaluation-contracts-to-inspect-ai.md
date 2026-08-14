# Map Evaluation Contracts To Inspect AI

Status: Ready

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

The user authorized one exceptional fourth correction and fresh independent review in canonical Task and Conversation `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`.

The final correction is limited to:

- one-to-one required `Responsibility-ID` metadata for `R-001` through `R-062`; and
- explicit retirement-evidence traceability for every retirement row and every Phase 2 through Phase 8 gate.

Use conservative defaults. Retain repository authorities, require explicit parity evidence, retire nothing without proof, and stop later phases when required evidence is missing.

### Answered User Action And Ready Transition

- Transition: `User Action Required -> Ready`.
- Recorded At: `2026-08-14T21:37:25Z`.
- Decision Provenance: Exact user authorization supplied to the Dev Backlog Coordinator for the preserved canonical task.
- Preserved Canonical Task and Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` on host `local`.
- Preserved Dev Orchestrator: `/root/map_evaluation_contracts_to_inspect_ai`.
- Preserved Candidate: `33d6a25350f5230cb359c1ad76397fea4dda44fc`.
- Preserved Evidence: Existing plan, three consumed review/correction cycles, series evidence, and the two unresolved findings.
- Final-Cycle Boundary: This is the fourth and final correction cycle. No fifth cycle or unrelated methodology work is authorized.
- Scheduling Boundary: The item remains Ready and unexecuted while the High-priority Defect `require-explicit-user-approval-for-new-infrastructure` owns the sole local crisis slot.
- Coordination Boundary: Claim-free crisis transition. No claim operation occurred. Preserve the post-reset draft and claim evidence until crisis exit reconciliation.
- Required Runtime Title: `Ready — Map Evaluation Contracts To Inspect AI` when the canonical runtime record is loaded and title mutation is available.
- Next Action: After the High-priority Defect becomes terminal or truthfully non-active, reserve this same canonical execution through `Ready -> Starting -> Running` and perform only the authorized final correction, fresh independent review, and focused verification.

### Unattended Work Boundary

Do not modify, review, verify, deliver, or close this Work Item before the preserved Dev Orchestrator accepts the Starting reservation. Preserve the canonical execution and candidate. Unrelated eligible Work Items may continue only as crisis policy permits.

## Final-Cycle Crisis Reservation

- Transition: `Ready -> Starting`.
- Reserved At: `2026-08-14T22:32:22Z`.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Baseline: `35555d916c0ed615bad17953bb246a2f5cbe9349` on configured primary branch `main`.
- Canonical Task and Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` on host `local`.
- Preserved Dev Orchestrator: `/root/map_evaluation_contracts_to_inspect_ai`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Capacity: Sole local dev-methodology crisis execution after `require-explicit-user-approval-for-new-infrastructure` entered User Action Required.
- Preserved Candidate: `33d6a25350f5230cb359c1ad76397fea4dda44fc` with existing plan, review history, series evidence, and all accepted content.
- Authorized Scope: The fourth and final correction cycle is limited to the two ledgers recorded in the Resolution. No fifth cycle, unrelated methodology work, or later-series implementation is authorized.
- Coordination Boundary: Claim-free crisis reservation. No claim operation occurred; preserve the post-reset draft and claim evidence until crisis exit reconciliation.
- Required Runtime Title: `Starting — Map Evaluation Contracts To Inspect AI`.
- Required Acceptance: The same Dev Orchestrator records `Starting -> Running` claim-free before correction, review, verification, or delivery work resumes.
- Next Action: Resume the preserved canonical task and existing nested execution. After accepted Running evidence, complete only the authorized ledgers, obtain fresh independent review and focused verification, and return a terminal result or one truthful exhausted-boundary disposition.

## Final-Cycle Running Acceptance

- Transition: `Starting -> Running`.
- Accepted At: `2026-08-14T22:34:10Z`.
- Canonical Task and Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` on host `local`.
- Owner: `/root/map_evaluation_contracts_to_inspect_ai` under the Dev Orchestrator Role.
- Branch and Worktree: configured primary branch `main` in `/Users/martinbechard/dev/dev-methodology`.
- Preserved Candidate: `33d6a25350f5230cb359c1ad76397fea4dda44fc` with all previously accepted mapping content.
- Accepted Scope: One exceptional fourth correction cycle limited to the two user-authorized ledgers, followed by fresh independent review and focused verification.
- Coordination Boundary: Claim-free crisis execution. No claim operation occurred before or during this acceptance.

## Fifth-Cycle Snapshot Decision

### Question for the User

Do you authorize one fifth and final correction cycle to establish a new frozen source snapshot, semantically review the nine changed authoritative sources, refresh their completion digests, and correct `SRC-L041` to the current analysis-backlog provider path and digest?

### Why User Input Is Required

The authorized fourth cycle completed both required traceability ledgers, and their focused checks pass. Fresh independent review then found that nine frozen completion digests changed after the original snapshot and that `SRC-L041` still points to the former feature-backlog location rather than the current authoritative analysis-backlog Work Item. These findings affect source authority and cannot be corrected or excluded safely within the exhausted fourth-cycle authorization.

### Options and Tradeoffs

- **Authorize one fifth and final cycle (recommended):** Freeze a new current-main source snapshot, semantically review the nine changed sources, refresh only the affected digests, correct `SRC-L041` path and digest, then obtain fresh independent review and focused verification. No sixth cycle is authorized.
- **Do not authorize and abandon successful delivery:** Preserve candidate `86b158051ada82cca2891d484f7a32cd6c68541c` and all review evidence as incomplete. This Work Item will not complete, and later ordered Inspect AI phases remain unable to proceed.

### Preserved Evidence And Unattended Boundary

- Transition: `Running -> User Action Required`.
- Recorded At: `2026-08-14T22:50:10Z`.
- Canonical Task and Conversation: `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` on host `local`.
- Preserved Dev Orchestrator: `/root/map_evaluation_contracts_to_inspect_ai`.
- Preserved Candidate: `86b158051ada82cca2891d484f7a32cd6c68541c` on current main.
- Fourth-Cycle Result: Both user-authorized traceability checks pass.
- Review Result: Fresh independent review fails only on nine drifted frozen completion digests and the stale `SRC-L041` provider path/digest.
- Verification State: Focused verification correctly did not start after review failure.
- Coordination Boundary: Claim-free crisis transition. No claim operation occurred.
- Required Runtime Title: `Waiting for User — Map Evaluation Contracts To Inspect AI`.
- Unattended Work Boundary: Do not correct, review, verify, deliver, replace the execution, start later Inspect AI phases, or infer approval until the user answers in this canonical task. Preserve the candidate, plan, review history, and all accepted content.

### Fifth-Cycle Resolution And Ready Transition

- Exact User Answer: `A - I authorize`.
- Decision Provenance: Exact answer supplied by the user in canonical Task and Conversation `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` and handed to the preserved Dev Orchestrator by the visible root runtime.
- Transition: `User Action Required -> Ready`.
- Recorded At: `2026-08-14T22:53:24Z`.
- Preserved Candidate: `86b158051ada82cca2891d484f7a32cd6c68541c` with all accepted content and review evidence.
- Authorized Scope: One fifth and final correction cycle limited to a new current-main frozen snapshot, semantic review of the nine changed authoritative sources, refresh of only affected completion digests, and correction of `SRC-L041` to the current analysis-backlog provider path and digest.
- Hard Boundary: No sixth cycle, replacement execution, claim operation, unrelated methodology work, later Inspect series item, or scope expansion is authorized.
- Next Action: Reserve and accept this same canonical execution through separate `Ready -> Starting -> Running` transitions before correction begins.
