---
name: complete-work-item-direct-main
description: Complete a verified work item by deliberately integrating its accepted commit into the configured main branch, verifying the integrated state, and observing exact main reachability before any provider lifecycle closure. Use when the effective completion selector is direct-main.
metadata:
  category: development-practice
---

# Complete Work Item Direct Main

Complete delivery only after the accepted behavior is verified on the configured main branch. Direct main describes the observed final state; implementation may occur in an authorized primary or isolated worktree.

## Inputs

Resolve these inputs before integration:

- Canonical work-item identifier, provider selector, and provider reference when one exists.
- Effective completion selector and explicit configured main branch.
- Accepted source commit, source branch, worktree, changed paths, and clean-state evidence.
- Independent review result and the checks accepted for the source commit.
- Smallest credible post-integration verification for the changed surface.
- Required local main and, when configured, remote publication state.
- Terminal lifecycle evidence required by the selected provider, or explicit provider none.

Return BLOCKED when the completion selector is not direct-main, required evidence is missing, main is ambiguous, or the requested integration or publication lacks authority. Do not infer main from the current branch name, a remote default, a temporary branch, or provider metadata.

## Provider Independence

This skill owns Git delivery and main observation. It also owns terminal handoff preparation. It does not create, inventory, assign, close, move, or otherwise mutate provider records for file, GitHub, GitLab, Azure DevOps, or Jira providers. It must not dispatch a provider manager, Dev Backlog Steward, or any Persistence mutation.

- Preserve the canonical work-item identifier independently of the delivery branch and commit identifiers.
- After successful delivery, return the exact terminal evidence to the caller for the owning orchestrator to route through its Persistence phase.
- For provider none, record lifecycle COMPLETED in the task-local result before returning READY, together with the complete terminal evidence, because no provider manager exists.
- A provider-backed Persistence recording failure happens after this skill returns. It does not change Commit READY into BLOCKED or erase the delivery evidence; the provider-backed item remains nonterminal until the owning orchestrator reconciles Persistence.

## Evidence Gate

Before shared mutation:

1. Confirm the source commit exists and represents the reviewed, verified contribution.
2. Confirm the source worktree is clean. When resource coordination is enabled, confirm implementation ownership is released or explicitly handed to the integration owner.
3. Confirm every required review finding is resolved and every accepted source check names its command or provider check and outcome.
4. Record the source commit and changed paths before refreshing main so later evidence cannot silently substitute another contribution.

A branch name, pushed branch, patch file, detached checkout, pull request, merge request, or clean source worktree is not completion evidence.

## Integration Authority

When agent-claim is selected, apply that enabled resource-coordination implementation before touching shared main state and acquire one narrow integration claim covering:

- every main-worktree path that integration or conflict resolution may modify;
- the target-specific integration resource for the configured main branch; and
- only the shared test resources required by focused post-integration verification.

Do not include provider lifecycle surfaces in operational coordination ownership. Provider closure is a separate transaction owned by the Persistence phase. If enabled ownership is unavailable, preserve the accepted source commit and return or follow the selected coordination procedure's bounded wait state without mutating main. When none is selected, skip acquisition, wait, heartbeat, registry, handoff, and release evidence.

## Main Reconciliation

From the intended integration checkout:

1. Confirm the checkout is the configured main branch and is clean.
2. Refresh configured remote references when remote observation or publication is required and authorized.
3. Compare local main, remote main, and the accepted source commit before changing history.
4. Preserve unrelated main advances. Never reset, force-update, overwrite, or discard them to make the candidate appear current.
5. Return BLOCKED with the observed commits when local and required remote state cannot be reconciled safely.

If the accepted source commit is already represented by current main, do not manufacture a topology-only merge. Continue to integrated verification and observation using the existing main commit.

## Deliberate Integration

When the accepted commit is not yet represented on main, load and apply agent-work-merge or hand the commit to the repository's accepted integration owner while retaining the same evidence requirements.

- Use the repository-approved merge, cherry-pick, rebase-and-fast-forward, squash, or equivalent integration strategy.
- Record the source-to-integration commit mapping when the strategy changes commit identity.
- Resolve conflicts from source evidence and current-main intent, not by automatically choosing one side.
- Recheck every affected path after conflict resolution.
- If a conflict cannot be resolved safely, abort or preserve the repository's documented recoverable state, keep the accepted source commit, and return BLOCKED.
- Do not create a feature-branch pull request or merge request as a substitute for direct-main integration.

A successful Git command is intermediate evidence. It does not establish completion by itself.

## Integrated Verification And Main Observation

Run the smallest project-native post-integration checks that cover the changed behavior and credible regression risk. Expand only after a focused failure or evidence-backed shared impact. A failed required check returns BLOCKED and must not trigger provider lifecycle closure.

Then collect all of these observations from the clean integration checkout:

- The checked-out branch exactly matches the configured main branch.
- The observed main tip is recorded with its full commit identity.
- The integration commit is an ancestor of the observed main tip.
- The accepted source commit is an ancestor of main, or a recorded non-ancestral integration mapping proves that the observed integration commit contains the accepted change.
- The observed changed paths and focused check results match the integrated state.
- Required remote main contains the observed delivery when publication is configured and authorized.
- The worktree has no staged, unstaged, or untracked integration residue.

Use graph reachability for ancestral delivery, such as Git's merge-base ancestor check against the configured main reference. For a non-ancestral replay or squash, record the source commit, integration commit, chosen strategy, content-equivalence evidence, and the integration commit's reachability from main. Never accept branch labels or working-tree similarity in place of commit evidence.

## Release And Lifecycle Handoff

When resource coordination is enabled, release integration ownership only after main is clean, required checks pass, and all local and configured remote observations are recorded. A failed release returns BLOCKED until ownership is reconciled; do not hide live ownership behind READY. When coordination is none, main cleanliness and verification still apply without release evidence.

When a provider is selected, prepare one terminal update containing:

- work-item identifier and provider reference;
- completion selector direct-main;
- accepted source commit and integration commit;
- observed main branch and tip;
- graph or non-ancestral integration evidence;
- review and source-check evidence;
- post-integration checks and any scoped omissions;
- required remote observation;
- clean worktree and enabled integration-release evidence; and
- completion disposition READY with requested lifecycle COMPLETED.

Return the prepared terminal handoff to the caller after the integration claim is released. The owning orchestrator decides whether and when to dispatch the selected provider manager. This skill neither performs that dispatch nor waits for its result. The provider-backed item remains nonterminal until the separate Persistence update succeeds. Do not report a provider-backed item as completed before that succeeds.

## Result

Return READY only when the complete direct-main delivery proof exists. Return:

- canonical work-item and provider references;
- source and integration commits;
- configured main branch and observed main tip;
- exact reachability or integration-mapping evidence;
- review, source-check, and post-integration verification evidence;
- required local and remote observations;
- clean-state and enabled resource-coordination release evidence; and
- the provider lifecycle update or provider-none terminal result.

Return BLOCKED with the preserved source commit, exact failed gate, current ownership state, recovery evidence, and one next action when integration, conflict resolution, verification, publication, main observation, or enabled resource-coordination release cannot finish safely. A later provider recording failure is a Persistence failure and does not change Commit READY into BLOCKED.

An unmerged temporary branch can never return READY or cause lifecycle COMPLETED.
