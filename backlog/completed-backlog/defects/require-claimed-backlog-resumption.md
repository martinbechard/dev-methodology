# Require Claimed Backlog Resumption

Status: Completed

Type: Defect

## Completion Outcome

The approved claimed blocked-work resumption contract is integrated on main at commit 5fc72048add03b71e8e1187fd442ec19723503c9. The steady-state procedure lives only in skills/manage-file-work-items/SKILL.md and its supported generated mirror. The retired skills/manage-backlog/SKILL.md remains a migration-only bridge with no resurrected lifecycle procedure.

Blocked handoff now commits Status: Blocked, Owner: Unowned, and Claim: None while preserving the blocker, unblock condition, evidence, and acceptance criteria before releasing prior ownership. Resumption passes through Ready, successful new exclusive claim acquisition, and a newly recorded owner before Running. WAIT, absent ownership, or another non-success restores the exact pre-attempt Blocked bytes.

## Completion Evidence

- The governed pre-mutation check for skills/manage-file-work-items/SKILL.md returned ALLOWED_APPROVED_DEFINITION_CHANGE using the user's direct replacement-scope answer “ok” from parent thread 019f77f4-c4bd-7c91-b197-c987a7beb838. Supported mirror validation returned ALLOWED_APPROVED_REGENERATION.
- Fresh independent methodology review passed candidate a019fbf84f0f4c365eb9e09860c2142220f87076 and passed the conflict-free current-main rebased candidate 5fc72048add03b71e8e1187fd442ec19723503c9.
- Focused deterministic verification passed four blocked-handoff and resumption contract tests, the targeted bundle regression, manage-file-work-items validation, generated skill-document freshness, four-selector validate-only, and Git diff validation.
- Live claimed resumption selectors passed for the direct-unowned rejection, successful Ready and newly claimed Running path, failed-claim byte restoration, and owned-to-unowned blocked handoff. The final handoff run exited 0 with no infrastructure errors, clean workspace, batch, and scenario cleanup, six catalog-matched deterministic receipts, a passed Judge with verified provenance, and identical checkpoint/final evidence. Its retained summary is /tmp/dev-backlog-steward-a019fbf-blocked-state-final.xyWDaH/summary.json.
- Exact-path integration ownership was acquired PRIMARY at event 8df323c9-497d-45d5-ae70-962eae3e6273 after coordinated resource release event 631438c5-f366-42a8-85df-aa295766868a. Main fast-forwarded from 0f312ed6d292cc7dd90a09ed9a7f392658ba1468 to 5fc72048add03b71e8e1187fd442ec19723503c9, post-integration focused checks passed, and the integration claim released cleanly at event df04528d-24d0-40ef-867d-6552247791e8.
- Separate terminal backlog ownership for only this active path and completed destination was acquired PRIMARY at event 318c6768-e0ce-4bf5-b523-87a527e2d929. Its release follows this committed terminal move from clean main.
- Canonical task 019f7f95-1242-7133-9033-a921c127df66 remains the delivery owner. Branch codex/claimed-backlog-resumption and worktree /Users/martinbechard/.codex/worktrees/3dd5/dev-methodology are cleanup-eligible after the terminal backlog claim is released and the parent confirms main ancestry and clean state.

## Approval Resolution

The user approved the exact governed definition scope after reviewing the prepared eval-only evidence.

## Approved Scope

Do you approve changing only skills/manage-backlog/SKILL.md to require that a blocked handoff releases prior ownership, preserves blocker/unblock/evidence/acceptance data, transitions through Ready, acquires a successful new exclusive claim and records the new owner before Running, and restores the byte-for-byte pre-attempt Blocked item when no claim or WAIT occurs?

Approval also permits supported regeneration of design/generated/skill-definitions.js from that source and integration with prepared non-governed eval/test commit 244efcd2aa26dc14d226ad33dc9be680cef6b95d. It does not authorize any other agent or skill definition.

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Yes”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, the user's direct reply on 2026-07-20 to the exact question above.

At approval time, delivery completion still required the governed pre-mutation check, implementation, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence. The completion evidence above records those finished gates.

## Replacement User Decision

The reviewed implementation cannot be integrated against current main under the original approval scope. Commit 60dbbd2 retired skills/manage-backlog/SKILL.md into a migration-only bridge that owns no lifecycle or recovery procedure. The replacement skills/manage-file-work-items/SKILL.md now owns file-work-item lifecycle and recovery behavior, and the bridge explicitly forbids adding new procedure there.

Do you approve changing only skills/manage-file-work-items/SKILL.md to carry the already reviewed claimed blocked-work resumption contract (blocked handoff commits Status: Blocked, Owner: Unowned, Claim: None with evidence preserved before release; resumption passes Ready → successful new exclusive claim/new owner → Running; absent/WAIT/rejected acquisition restores the exact pre-attempt Blocked bytes), together with only its supported generated skill-definition mirror and the already reviewed non-governed eval/test coverage? This supersedes the obsolete manage-backlog target and authorizes no other definition.

The user approved this exact replacement scope with the direct answer “ok” in parent thread 019f77f4-c4bd-7c91-b197-c987a7beb838 on 2026-07-20. The approval supersedes only the obsolete governed target; all behavioral, mirror, and non-governed coverage boundaries above remain unchanged.

## Historical Preserved Candidate

- Candidate 0579356 is clean and independently methodology-reviewed PASS.
- Focused verification passed four deterministic tests, two bundle tests, source/mirror freshness, and the four required live selector outcomes with clean claim release and rollback evidence.
- No integration claim was acquired and no obsolete bridge procedure was restored.
- Branch and private worktree remain clean and preserved under canonical task 019f7f95-1242-7133-9033-a921c127df66.

## Current Resumption Ownership

- Canonical Dev Orchestrator task: 019f7f95-1242-7133-9033-a921c127df66.
- Parent task: 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Worktree: /Users/martinbechard/.codex/worktrees/3dd5/dev-methodology.
- Branch/ref: codex/claimed-backlog-resumption, integrated candidate 5fc72048add03b71e8e1187fd442ec19723503c9.
- Started from approved Ready commit 78441b34f6e2df68d38e61d048d8d0d3f0bc0a81.
- Phase: completed after approved governed source implementation, semantic current-main reconciliation, focused resumption verification, fresh review, direct integration, and terminal backlog closeout.
- Replacement-scope resumption: user-approved skills/manage-file-work-items/SKILL.md authority recorded at bf18ae8; canonical task resumed under the same preserved candidate and evidence.
- Preserved commits 25b93bad57e1ee2ffe445de29421aa5bf80c5c9a, 58b502bcfd3d79666b190b3db192da5007c22391, and eb9826f4c87e6b3ed30b1068841cc357898fe531 remain historical recovery evidence superseded by the integrated current-main candidate.
- Superseded archived claimed-resumption tasks, including 019f7e67-dfdf-74f0-ac17-e6d06b63828e, are not canonical ownership.

## Historical Blocked Outcome

- Preserved implementation commits: 25b93ba, 58b502b, and eb9826f.
- Independent review: fresh final review passed.
- Static verification: focused tests passed 5 of 5; repository scripts passed 399 of 399; project-wiki passed 17 of 17; bundle, skill, generated-output freshness, and diff checks passed.
- Integration: no implementation commit was integrated.
- Governed acceptance: incomplete. The original blocked-state run produced one clean target and Judge pass. The unowned and failed-claim runs produced standalone Judge passes, but runner timeout and cleanup prevented governed passes. The claimed path produced a correct target result but no Judge result and retained an active-claim cleanup conflict. The repeated original path produced no Judge result. Every standalone runner exited 124 and was classified as infrastructure-failed.
- Unblock condition: obtain Judge-complete, checkpoint-and-final-consistent, cleanup-clean governed passes for unowned, claimed, and failed-claim resumption, plus a second clean blocked-state pass with an empty claim registry after handoff.

## Summary

Prevent backlog handoffs from moving blocked work directly to running without explicit claim acquisition and an eligible lifecycle transition.

## Context

The Backlog Steward blocked-state scenario correctly moved active work from Running to Blocked, preserved the exact blocker and acceptance evidence, committed the handoff, released its claim, and left the repository clean. The handoff then prescribed Blocked to Running as the resumption path even though no agent owned the item.

The independent Judge returned FAIL because the proposed transition bypassed explicit claim acquisition and the eligible Queued and claimed path. Deterministic checks confirmed the committed state change and clean claim registry but did not reject the unsafe future handoff instruction. The complete evaluation did not edit the distributed backlog skills.

## Evidence

- evals/agent-tests/dev-backlog-steward/scenarios.yaml defines the blocked transition and claim lifecycle contract.
- evals/agent-tests/dev-backlog-steward/fixtures contains the frozen active backlog used by the scenario.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained claim evidence.
- The committed handoff named Blocked to Running without requiring a new owner to acquire a claim.

## Requirements

- Require blocked work to become eligible for ownership before it can return to Running.
- Require explicit successful claim acquisition by the resuming agent before any Running transition.
- Keep claim release on blocked handoff separate from future claim acquisition.
- Reject handoff instructions that imply ownership from state alone.
- Preserve the exact blocker, unblock condition, evidence, and acceptance criteria across the resumption transition.
- Add deterministic and Judge coverage for unowned Blocked to Running shortcuts.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A blocked handoff leaves the item unowned and does not authorize direct execution.
- Resumption records an eligible state, a successful new claim, the new owner, and only then Running.
- Failure to acquire the claim leaves the backlog item unchanged and not running.
- The prior blocker and acceptance evidence remain intact after resumption.
- The Backlog Steward blocked-state scenario passes repeatably with an empty registry after the original handoff.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for blocked handoff, eligibility, claim acquisition, and resumption transitions.
- Add a negative fixture that attempts direct unowned Blocked to Running and a positive claimed-resumption fixture.
- Run the Backlog Steward blocked-state scenario multiple times and inspect commit, handoff, claim journal, independent Judge verdict, and cleanup.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- The item may remain Blocked while the external unblock condition is unsatisfied.
- A state label never substitutes for ownership evidence.
