# Enforce Agent-Claim Lifecycle Evidence In Runner Resource Scenarios

Status: Running

Type: Defect

Owner: Root Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/enforce-agent-claim-lifecycle-evidence-in-runner-resource-scenarios.md

Completion: direct-main

## Execution Acceptance

- Canonical Work-Item Thread: 019f981c-4fea-7b83-b8d2-0b254ff45f0c
- Canonical Task Id: 019f981c-4fea-7b83-b8d2-0b254ff45f0c
- Root Role: Dev Orchestrator
- Root Orchestrator Task: /root/resume_blocked_after_claim_publication/runner_lifecycle_recovery
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/e8bc/dev-methodology
- Delivery Branch: codex/enforce-agent-claim-lifecycle-evidence-019f981c
- Delivery Commit At Acceptance: 4778fd4435c50cc8a282a6a505eb41b061374278
- Phase: Fresh bounded recovery plan; not correction attempt 3 in the prior loop.
- Exact Implementation Scope: evals/agent-tests/runner.py and evals/agent-tests/test_runner.py.
- Reservation Commit: 94405248e0b73c38da0121f06b1d566fcece4577.
- Started At: 2026-07-26T11:06:09Z

## Execution Coordination Evidence

- Backlog Claim: runner-starting-to-running-019f981c-4fea-7b83-b8d2-0b254ff45f0c acquired on primary main at 2026-07-26T11:05:42.371076Z; acquisition journal event e7f0ccbc-1c10-47cc-90e8-38bbe4f8f843.
- Claim-Free Private-Lane Evidence: This transaction acquired only the exact primary backlog-file claim. The preserved delivery worktree is private, and no project-files or resource claim was acquired for source work during this lifecycle acceptance.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Enforce agent-claim lifecycle evidence in runner resource scenarios.
- Dispatched At: 2026-07-25T07:09:27Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.

## Reservation Coordination Evidence

- Backlog Claim: reserve-agent-claim-lifecycle-runner-defect-20260725 acquired on primary main at 2026-07-25T07:09:27.159466Z; acquisition journal event cf71e7da-e29c-45dd-bf1f-f3e30f6643c3.

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

## Candidate And Review Evidence

- Candidate: e437702d2c0119c6641caca52fb7561348086568 on `codex/enforce-agent-claim-lifecycle-evidence-019f981c`.
- Coder claim: released at journal event 1308c17c-e1a5-48db-9649-c919bc49bbfe.
- Candidate checks: 14 focused claim, handoff, and receipt checks passed; four provider-none checks passed; valid lifecycle evidence passed and was verified; absent activity was blocked and invalid; `py_compile` and `git diff --check` passed; 123 non-browser checks passed; 13 browser checks were unavailable because Playwright is absent.
- Fresh Dev Code Reviewer disposition: REJECT.

## Review Findings

- HIGH: Target-trace binding is token-only and does not bind repository, actor, claim, event, output, or success state.
- HIGH: Stale evidence commits are accepted when they are merely ancestors of a later unclaimed HEAD.
- HIGH: A truthful no-change release is incorrectly rejected.
- HIGH: An external symlinked `agent-claims.json` is accepted.
- MEDIUM: Duplicate successful lifecycle events and malformed journal lines do not fail closed.

## Replacement Candidate And Review Evidence

- Replacement candidate: 446371ff424d2ab2e3da53c72396dde356c36bcb.
- Correction claim: released at journal event b5c7f352-8fd0-4517-84ac-bde8c032b914.
- Replacement checks: seven focused checks passed; 126 non-browser runner checks passed; four provider-none checks passed; `py_compile`, `git diff --check`, catalog, generator, and project-wiki checks passed; 13 Playwright checks were unavailable; the scripts baseline failure is already tracked.
- Fresh Dev Code Reviewer disposition: REJECT.

## Replacement Candidate Review Findings

- HIGH: A counterfeit claim executable is accepted because suffix-only script identity can forge matched structured outputs instead of binding the configured trusted adapter.
- MEDIUM: Changed-state release accepts missing, null, or non-boolean `no_change` because it rejects only literal `True`.

## Final Correction Plan And Hard Stop

- Preserve rejected candidates e437702d2c0119c6641caca52fb7561348086568 and 446371ff424d2ab2e3da53c72396dde356c36bcb as review evidence.
- Reuse canonical task 019f981c-4fea-7b83-b8d2-0b254ff45f0c, the original Dev Coder, and the existing branch and worktree. The correction lane is exactly `evals/agent-tests/runner.py` and `evals/agent-tests/test_runner.py`; do not create a task or worktree or expand into governed, generated, unrelated, or newly discovered defect scope.
- Write red adversarial regressions before correction work.
- Bind executable identity for the evaluated target to the exact configured agent-claim command adapter path through canonical resolved identity plus containment and regular-file checks. Reject suffix lookalikes, sibling counterfeits, and symlink substitutions; basename and suffix are not authority.
- Treat release `no_change` as a required typed journal field bound exactly to the retained adapter result and scenario disposition. Reject missing, malformed, or contradictory values while preserving valid committed normal release and truthful normal no-change behavior.
- Complete the prior seven-finding adversarial matrix, provider-none checks, non-browser runner checks, `py_compile`, diff hygiene, and the cheapest disposable valid and invalid scenarios. Reconcile owned baseline failures without duplicates; Playwright absence may remain an unchanged omission.
- Produce one clean replacement commit and truthful claim release. Require a brand-new fresh independent full-candidate review, then independent verifier work only after review acceptance; do not integrate before both succeed.
- Hard stop: any material fresh-review finding, repeated evidence-binding bypass, or scope expansion after attempt 2 prohibits correction 3. Preserve the candidate and have Dev Backlog Steward transition this item from Running to Blocked with Owner: Unowned, the exact unblock condition, and complete evidence.

## Final Candidate And Review Evidence

- Final candidate: 4778fd4435c50cc8a282a6a505eb41b061374278 on `codex/enforce-agent-claim-lifecycle-evidence-019f981c`; its private worktree was clean.
- Coder claim: released at journal event 618bb101-5770-4227-8619-aaedea6e954d. The claim registry was empty after release.
- Fresh Dev Code Reviewer disposition: REJECT.
- HIGH: A different executable named `python` or `python3` can emit accepted results while the exact configured `claim.py` is only inert `argv[1]`; selected adapter execution is not proven.
- HIGH: Real acquire and release plus a later unclaimed commit and rewrite of the target-writable journal release `resulting_commit` is accepted because retained release output lacks independent commit identity.
- HIGH: Repository alias and contained journal symlink substitutions are accepted because relevant paths resolve without rejecting symlink components.
- Supported verification: exact HEAD and clean checks, unique ordered events, actor/claim/event matching, typed no-change, configured adapter path checks, provider-none checks, and headers; eight focused checks passed; runner checks passed 128 with 13 known Playwright checks unavailable; `git diff --check` passed; worktree was clean; no new baseline defect was identified.

## Blocked Handoff

- Exact blocker: The runner lacks runner-owned immutable proof that the configured interpreter and adapter actually executed, release commit identity cannot be rewritten, and repository and journal component symlinks are rejected.
- Next Action Owner: Dev Backlog Coordinator for future resumption routing. No active implementation owner exists.
- Unblock Condition: Explicit authorization and a fresh bounded design and implementation plan must provide trusted interpreter-and-adapter execution identity, runner-owned immutable release-to-commit binding or an authoritative adapter result field, and component-wise repository and journal symlink rejection, with red regressions for all three. Resume only through the normal Blocked -> Ready -> Starting -> Running lifecycle; correction attempt 3 in this canonical run is prohibited.

## Current-Main Recovery

- Reconciliation Date: 2026-07-26.
- Recovery Authority: Parent Coordinator previously explicitly authorized this runner lifecycle-evidence recovery among six named correction recoveries and now authorized this exact lifecycle resumption.
- Preserved Canonical Identity: Work-Item Thread and task 019f981c-4fea-7b83-b8d2-0b254ff45f0c remain authoritative; no replacement identity is created.
- Preserved Candidate Evidence: Rejected candidates e437702d2c0119c6641caca52fb7561348086568, 446371ff424d2ab2e3da53c72396dde356c36bcb, and 4778fd4435c50cc8a282a6a505eb41b061374278 remain review evidence only and are not integrated.
- Authorized Scope: A new bounded design-and-recovery plan, not correction attempt 3 in the prior loop. The plan remains exactly `evals/agent-tests/runner.py` and `evals/agent-tests/test_runner.py`; it must establish trusted interpreter-and-adapter execution identity, immutable release-to-commit binding, component-wise repository and journal symlink rejection, and red regressions before implementation.
- Current-Main Overlap Reconciliation: Decouple and OID candidates have no source integrated on current main. Before source mutation, reconcile any exact overlap against their current Blocked records and preserve their candidate evidence; no overlap authorizes taking or changing their work.
- Transition: Blocked -> Ready. Owner remains Unowned. This provider transition does not grant implementation ownership.
- Next Lifecycle Owner: the parent Dev Backlog Coordinator may separately reserve Ready -> Starting for this same canonical item.

## Current Starting Reservation

- Parent Coordination Thread: /root/resume_blocked_after_claim_publication.
- Canonical Thread/Task: 019f981c-4fea-7b83-b8d2-0b254ff45f0c; no replacement canonical identity is created.
- Reservation: One parent-owned Ready -> Starting launch reservation.
- Normalized Objective: Enforce agent-claim lifecycle evidence in runner resource scenarios.
- Intended Root Role: Dev Orchestrator.
- Codex Resumption Task: /root/resume_blocked_after_claim_publication/runner_lifecycle_recovery.
- Persistence And Completion: file provider; direct-main completion.
- Preserved Evidence: candidates e437702d2c0119c6641caca52fb7561348086568, 446371ff424d2ab2e3da53c72396dde356c36bcb, and 4778fd4435c50cc8a282a6a505eb41b061374278 remain rejected and unintegrated; their prior correction loop is not reopened.
- Authorized Bounded Scope: exactly `evals/agent-tests/runner.py` and `evals/agent-tests/test_runner.py`, with current-main overlap reconciliation before source mutation.
- Dispatched At: 2026-07-26T11:02:31Z.
- Launch Evidence: Parent Coordinator authorized this exact fresh recovery reservation. Runtime acceptance remains pending.
- Next Lifecycle Owner: the root Dev Orchestrator must record a distinct Starting -> Running acceptance for this same canonical identity before repository mutation.

## Notes

This item is ready for independently scoped implementation. It does not authorize unrelated runner changes or governed-definition mutation without required approval evidence.
