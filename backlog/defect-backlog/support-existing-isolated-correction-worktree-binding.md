# Support Existing Isolated Correction Worktree Binding

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/support-existing-isolated-correction-worktree-binding.md

Completion: direct-main

## Starting Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Reservation: One parent-owned same-task reservation; no replacement task is created.
- Normalized Objective: Deploy canonical Codex bundle with approved customized replacement and verify catalog.
- Dispatched At: 2026-07-25T16:01:43Z
- Intended Root Role: Dev Orchestrator
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch: codex/isolated-binding-019f976c at 570a0271870e96abcb5c0ddf01428fd749b238f3.
- Approved Override Scope: python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace --replace-customized, followed by catalog refresh or new-session activation and installed-byte verification; limited to the nine reviewed customized bundle-owned skill trees and normal bundle-owned outputs.
- Phase: Awaiting root lifecycle acceptance. Owner remains Unowned until the root Dev Orchestrator accepts the reservation.

## Current Lifecycle Running

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Owner: Dev Orchestrator
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch: codex/isolated-binding-019f976c at stable source commit 570a0271870e96abcb5c0ddf01428fd749b238f3.
- Accepted Approval Scope: python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace --replace-customized, followed by catalog refresh or new-session activation and installed-byte verification; no engine mutation.
- Started At: 2026-07-25T16:06:41Z, after root lifecycle acceptance.
- Sequencing Variance And Adoption: The Ready -> Starting transaction completed in the canonical task at commit e1572f96 before the parent STOP message arrived. The parent subsequently adopted that immutable same-task reservation as valid; no duplicate identity or mutation exists.
- Phase: Root accepted. Deployment retry may proceed only after this provider transition is committed and its short backlog claim is released.

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

## Deployment Discrepancy Evidence

The approved exact installer command exited 1 at its customization safety boundary before mutation. The shared-install claim was acquired at event 3fb1a956-d56f-410f-8e99-4877b4cfd45e and released no-change at event 82d30f3e-f58a-4402-9f0f-9c5a0be5b6f3. It changed no installed, repository, or provider bytes. Installed agent-claim remains stale.

Fresh independent discrepancy review compared the common manifest baseline commit 8a269a6c612a1e9b22f6ecf5d4877020cf974e7b, 20 changed installed files with no installed-added files, and current canonical source. The nine customized owned skill trees are create-architecture, create-functional-spec, create-high-level-design, create-module-design, development-methodology, review-architecture, review-functional-spec, review-high-level-design, and review-module-design. One canonical-only file-work-item template is also present.

The review found that useful proposition, ledger, diagram, and path-tree intent is already integrated canonically; installed-only directives are obsolete or overbroad; canonical source fixes missing Related Code and Related Tests sections; and no installed-only sensitive indicators were detected. It classified all nine customized trees safe to replace as one decision, while noting that 19 exact byte origins are not recoverable from Git.

The delivery remains associated with canonical task/thread 019f976c-6691-7a83-9df4-e73fc0baae73, parent 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a, canonical branch codex/isolated-binding-019f976c at stable deployment source commit 570a0271870e96abcb5c0ddf01428fd749b238f3, and canonical worktree /Users/martinbechard/.codex/worktrees/0311/dev-methodology. The separate telemetry-label follow-up remains out of scope.

## Approval Record

Approved on 2026-07-25 in canonical task/thread 019f976c-6691-7a83-9df4-e73fc0baae73. Exact user answer: I approve. Provenance: direct answer to the recorded --replace-customized Question for the User.

Approved scope: python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace --replace-customized, followed by catalog refresh or new-session activation and installed-byte verification. The approval is limited to the existing reviewed nine customized bundle-owned skill trees and normal bundle-owned outputs of that command. No engine source change or unrelated user-home mutation is authorized.

## Resolution

Approval is recorded. Deployment has not yet been rerun. The item is Running with Owner: Dev Orchestrator, preserving the same canonical task, branch, worktree, investigation, discrepancy-review, and approval evidence. Root acceptance is recorded; deployment remains outside this provider transition.

## Ready Lifecycle Boundary

Do not run the installer, refresh the runtime catalog, edit user-home files, or make an engine change in this provider transition. Deployment retry is permitted only after this commit and backlog-claim release.

## Follow-up Obligation

The distinct telemetry-label finding remains a separately logged follow-up obligation and is not part of this user-action-required question or transaction.
