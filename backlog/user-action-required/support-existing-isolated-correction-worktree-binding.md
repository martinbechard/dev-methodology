# Support Existing Isolated Correction Worktree Binding

Status: User Action Required

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/user-action-required/support-existing-isolated-correction-worktree-binding.md

Completion: direct-main

## Resumption Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Reservation: One parent-owned same-task launch reservation; no new task is created.
- Normalized Objective: Deploy canonical Codex bundle to refresh stale agent-claim guidance.
- Dispatched At: 2026-07-25T12:33:09Z
- Intended Root Role: Dev Orchestrator
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch: codex/isolated-binding-019f976c at cc400d340638eb917c2184de19c1e8354f1aa897.
- Phase: Root lifecycle accepted; Starting-to-Running provider transition is recorded below.

## Resumption Coordination Evidence

- Backlog Claim: reserve-isolated-worktree-deployment-019f976c acquired on primary main at 2026-07-25T12:33:09.498977Z; acquisition journal event 917c1da2-1b74-4fb0-bcb5-b695400498ff.

## Launch Reservation

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Reservation: One parent-owned launch reservation.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch: codex/isolated-binding-019f976c at cc400d340638eb917c2184de19c1e8354f1aa897.
- Phase: Root lifecycle accepted; delivery proceeds in the canonical isolated correction worktree.
- Dispatched At: 2026-07-25T03:58:59Z

## Lifecycle Start

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Role And Owner: Dev Orchestrator
- Isolated Worktree Binding: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch State: codex/isolated-binding-019f976c at cc400d340638eb917c2184de19c1e8354f1aa897.
- Phase: Root lifecycle accepted; delivery proceeds only in the canonical isolated correction worktree.
- Started At: 2026-07-25T04:01:00.487775Z, after the root Dev Orchestrator accepted ownership.
- Coordination Claim: Dev Backlog Steward acquired short primary-main backlog claim support-existing-isolated-correction-worktree-binding-running-019f976c at event 41049fc1-bf18-453e-a663-7f7876efc28e from baseline commit ff63b40b46571f22fd5c5624c79d856ff9b243cf.
- Scope Boundary: This claim owns only the committed Starting-to-Running provider transition and must release immediately; delivery owns separate isolated project-artifact scope.

## Lifecycle Running

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Owner: Dev Orchestrator
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch State: codex/isolated-binding-019f976c at cc400d340638eb917c2184de19c1e8354f1aa897.
- Deployment Phase: Approved user-scope Codex bundle deployment is authorized and delivery may proceed only in the canonical isolated correction worktree.
- Started-At Evidence: 2026-07-25T04:01:00.487775Z, after the root Dev Orchestrator accepted ownership.
- Accepted Approval Scope: Only python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace, followed by runtime catalog refresh or new-session activation and installed-versus-canonical agent-claim byte verification; no engine change or broader user-home mutation.
- Backlog Claim: Dev Backlog Steward acquired short primary-main backlog claim support-isolated-binding-running-019f976c at 2026-07-25T12:41:26.036618Z; acquisition journal event d98ea91e-3207-45f4-a405-4c069f7f49f4; baseline commit 37a07d65720350516a81225c373ab2808f17d036.
- Scope Boundary: This claim owns only this committed Starting-to-Running provider transition and must release immediately; delivery remains under separate isolated project-artifact ownership.

## Summary

Make the claim transport and topology contract support explicit safe setup or reuse of a canonical correction task’s existing clean isolated worktree and branch even when no peer writer is active.

## Context

The current behavior can depend on an incidental competing claim to reach an isolated-worktree path. With an empty registry, a User Action Required correction received `SHARED_CHECKOUT_ACQUIRED` and released no-change event `0273f787-2f05-44a4-9b87-b96e9ac7858e`; a campaign correction likewise released no-change event `8d47aaf7-6f04-4267-9ced-6e473f8d9df9`. A durable-defect task received isolated setup events `a279c96b-ae93-4ce1-af04-dbaabbdafd63` and `405af7d3-cf11-4fec-9a59-cb00bdd22a1e` while another writer was active, but after the registry emptied, its explicit existing-worktree acquisition returned `SHARED_CHECKOUT_ACQUIRED` event `5bcd13c9-8d50-4258-ae22-72d4bfc3e4b2` and released no-change event `120a4e32-7a33-4b6c-9c59-8e8ae6eb37cb`.

## Source Evidence

Repeated confirmed coordination failure in canonical tasks `019f9722-61cb-7190-8a6d-21c5ab319339` and `019f96cf-226c-7f62-9d66-7d31cead822e`. Standing user direction requires every found defect to be durably logged and never ignored as a warning.

## Investigation Result

- Root investigation and a fresh independent review found no engine rebinding defect. Canonical agent-claim and codex-workitem-coordination already exempt private-worktree work that has no shared paths or resources.
- First-writer shared-checkout behavior is intentional. Two canonical tasks produced or resumed clean private candidates without claims, and no source or test mutation was needed.
- The causal issue is a coherent stale user-scope deployment: `/Users/martinbechard/.agents/skills/agent-claim/SKILL.md` has hash prefix `a3a487c3`, while the canonical source has hash prefix `8ec97bfe`. The stale installed guidance causes unnecessary acquisitions. README.md documents deployment as an explicit operation.

## Requirements

- Support explicit safe isolated-worktree setup or reuse independently of another active writer’s claim.
- Preserve the same canonical task, worktree, branch, and candidate bytes throughout correction setup and reuse.
- Treat supplied branch, base, and worktree intent as binding; do not silently ignore or replace it.
- Produce deterministic first-writer versus explicit-isolation outcomes.
- Keep primary main untouched until accepted delivery is ready for its authorized integration transaction.
- Reject dirty, stale, mismatched, or noncanonical existing worktrees.
- Preserve all existing overlap, primary-main, and dirty-owner safeguards.
- Journal the exact requested binding, resolved binding, and structured outcome.

## Acceptance Criteria

- A no-peer explicit-isolation request creates or binds the intended isolated worktree rather than acquiring the primary checkout.
- An active-peer explicit-isolation request preserves the same safe isolated behavior.
- A clean existing canonical worktree is reused with the exact task, branch, base, and candidate binding intact.
- Dirty, stale, branch-mismatched, base-mismatched, or worktree-mismatched requests are rejected without primary mutation.
- Tests prove exact base/branch binding, no primary mutation before accepted delivery, and overlap/dirty-owner safeguards.
- Registry, journal, and release evidence record the exact binding and outcome for success, rejection, and no-change release.

## Dependencies

None.

## Verification

- Run focused claim-engine and command-transport tests.
- Run focused lifecycle and coordination tests.
- Exercise exact real-Git worktree scenarios for no-peer isolation, active-peer isolation, existing reuse, binding mismatch, dirty state, and stale state.
- Run the full applicable shared-infrastructure regression and `git diff --check`.
- Obtain fresh independent review.

## Open Questions

- Which existing claim command fields and journal schema can express explicit reuse without widening the canonical worktree authority boundary?

## Notes

This record captures the defect only. Any governed-definition changes discovered during delivery require an exact canonical-path approval record before mutation.

## User Action Required

The approved exact installer command was attempted under shared-install acquisition event 61157224-fb22-4be0-b761-c74bd7544bb0, but stopped before mutation because the installer reported: customized owned skills require discrepancy analysis. The shared-install resource claim was released with no change at event 8a5e5b45-0c32-4984-b970-30b078eb7705. No installed or repository file changed.

Fresh independent three-way review compared the old deployed generic baseline at source commit 8a269a6c, 20 customized installed files across nine skill directories, and the current canonical source. It found that canonical source supersedes every meaningful customized intent. The documented replacement would discard only redundant wording, typos, and overbroad clauses, and it fixes the installed functional-spec template regression that removed the Related Code and Related Tests headings. The review also found that the removed preference-level literals -- brainstorming dependency, universal HTML-mockup instruction, and one-module/code-unit heuristic -- have more precise portable canonical replacements. Subset deployment is unsupported by the approved installer without a separate staged scope and approval.

The delivery remains associated with canonical task/thread 019f976c-6691-7a83-9df4-e73fc0baae73, canonical branch and worktree, prior approval, root-cause history, and running delivery commit e2e3627401406b13f3e53b3ab93afcb0b7055cc5. The separate telemetry-label follow-up remains out of scope.

## Question for the User

Do you approve rerunning the documented user-scope Codex deployment with the additional --replace-customized flag, accepting replacement of the 20 customized files after the three-way review found no meaningful semantic requirement would be lost?

## Why User Input Is Required

Prior approval covered only the exact installer command without destructive customized-owned replacement. The additional --replace-customized flag changes that authority boundary, so the user must decide whether the reviewed customized files may be replaced.

## Options and Tradeoffs

- A. Approve --replace-customized (recommended). Canonical source supersedes the customized content and fixes the structural regression.
- B. Identify exact clauses to preserve or merge. This requires separate canonical or staged-scope approval.
- C. Defer or decline. Installed agent-claim remains stale and deployment remains incomplete.

## Resolution

Approved on 2026-07-25 in canonical task 019f976c-6691-7a83-9df4-e73fc0baae73. Exact user answer: I approve. Provenance: direct answer to the recorded Question for the User.

Approved scope: only the documented user-scope Codex deployment `python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace`, followed by runtime catalog refresh or new-session activation and verification that installed agent-claim bytes match canonical source. No engine change or broader user-home mutation is authorized.

Resulting disposition: the exact approved command was attempted, but its customized-owned replacement safeguard stopped it before mutation. This new question is unresolved; the item is User Action Required with Owner: Unowned, preserving the same canonical task, branch, worktree, and evidence.

## Unattended Work Boundary

Do not run the installer, refresh the runtime catalog, mutate user-home paths, or make an engine change until the user answers the new question. After an answer, resume only through User Action Required -> Ready -> Starting -> Running lifecycle reconciliation.

## Follow-up Obligation

The distinct telemetry-label finding remains a separately logged follow-up obligation and is not part of this user-action-required question or transaction.
