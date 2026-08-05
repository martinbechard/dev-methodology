---
name: complete-work-item-direct-main
description: Complete a verified work item by deliberately integrating its accepted commit into the configured main branch, verifying the integrated state, and observing exact main reachability before any provider lifecycle closure. Use when the effective completion selector is direct-main.
metadata:
  category: development-practice
---

# Complete Work Item Direct Main

Complete delivery only after the accepted behavior is verified on the configured main branch. Direct main describes the observed final state; implementation may occur in the primary worktree or a private worktree.

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
2. Confirm the source worktree is clean.
3. Confirm every required review finding is resolved and every accepted source check names its command or provider check and outcome.
4. Record the source commit and changed paths before refreshing main so later evidence cannot silently substitute another contribution.

A branch name, pushed branch, patch file, detached checkout, pull request, merge request, or clean source worktree is not completion evidence.

## Claims

Follow the Claim Events table in agent-claim during integration. Provider closure remains a separate Persistence transaction.

## Main Reconciliation

From the intended integration checkout:

1. Confirm the checkout is the configured main branch. The globally clean route remains the normal route and continues to require a clean checkout.
2. Refresh configured remote references when remote observation or publication is required and authorized.
3. Compare local main, remote main, and the accepted source commit before changing history.
4. Preserve unrelated main advances. Never reset, force-update, overwrite, or discard them to make the candidate appear current.
5. Return BLOCKED with the observed commits when local and required remote state cannot be reconciled safely.

If the accepted source commit is already represented by current main, do not manufacture a topology-only merge. Continue to integrated verification and observation using the existing main commit.

## Unrelated Dirty Main Route

Use this route only when the configured-main checkout has pre-existing dirty state that is demonstrably unrelated to the accepted contribution. It is not a recovery route for uncertain state.

Before integration mutation:

1. Record the current main tip and the exact accepted-path set. Derive the complete source path set from the accepted commit or commits. Return BLOCKED when the source scope is unbounded, the accepted-path set is empty, or the two sets differ.
2. Record exact worktree and index path inventories, including staged, unstaged, untracked, unmerged, renamed, copied, and type-changed entries. Treat path names as exact repository-relative identities.
3. Reject any overlap between the accepted-path set and either inventory. An unmerged, renamed, copied, type-changed, or untracked collision is ambiguous and returns BLOCKED.
4. Return BLOCKED for any pre-existing staged entry. This route accepts only unrelated unstaged tracked or untracked state whose ownership and path identity are unambiguous.
5. Capture the byte content of every dirty path, binary-safe worktree diffs, and the exact index entries and blob identities for those paths. For an untracked path, capture a binary-safe comparison against its recorded absence from current main. Return BLOCKED when any path cannot be captured without interpretation.

Apply only the exact accepted files or exact accepted commits to the recorded current main tip. Record an exact source-to-integration mapping that names each source commit, its accepted paths, the integration strategy, and the resulting integration commit. The integration owner must not stash, reset, discard, overwrite, or otherwise normalize the pre-existing dirty state.

After integration mutation, recapture the same evidence. Prove the unrelated state is byte-for-byte and index-for-index identical, and compare the complete before and after path inventories. Classify the original paths as preserved unrelated dirt. Classify every additional staged, unstaged, untracked, unmerged, renamed, copied, or type-changed path as integration residue and return BLOCKED. This distinction replaces a global-cleanliness assertion only for the preserved paths; it does not excuse integration residue.

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

For the normal route, run checks and collect observations from the clean integration checkout. For the unrelated-dirty route, create or reuse a clean verification checkout at the resulting configured-main tip so pre-existing dirt cannot contaminate checks. Observe the configured-main branch and resulting tip from the authoritative integration checkout, and prove that the clean verification checkout is at that same full commit before running checks.

Then collect all of these observations:

- The authoritative integration checkout's branch exactly matches the configured main branch.
- The observed main tip is recorded with its full commit identity.
- The verification checkout is clean and resolves to the observed main tip.
- The integration commit is an ancestor of the observed main tip.
- The accepted source commit is an ancestor of main, or a recorded non-ancestral integration mapping proves that the observed integration commit contains the accepted change.
- The observed changed paths and focused check results match the integrated state.
- Required remote main contains the observed delivery when publication is configured and authorized.
- The normal-route worktree has no staged, unstaged, or untracked integration residue. The unrelated-dirty route reports its exact preserved paths separately and has no integration residue.

Use graph reachability for ancestral delivery, such as Git's merge-base ancestor check against the configured main reference. For a non-ancestral replay or squash, record the source commit, integration commit, chosen strategy, content-equivalence evidence, and the integration commit's reachability from main. Never accept branch labels or working-tree similarity in place of commit evidence.

## Lifecycle Handoff

When a provider is selected, prepare one terminal update containing:

- work-item identifier and provider reference;
- completion selector direct-main;
- accepted source commit and integration commit;
- observed main branch and tip;
- graph or non-ancestral integration evidence;
- review and source-check evidence;
- post-integration checks and any scoped omissions;
- required remote observation;
- clean verification evidence, preserved unrelated-dirt evidence when applicable, absence of integration residue, and applicable claim results; and
- completion disposition READY with requested lifecycle COMPLETED.

Return the prepared terminal handoff to the caller after integration is complete. The owning orchestrator decides whether and when to dispatch the selected provider manager. This skill neither performs that dispatch nor waits for its result. The provider-backed item remains nonterminal until the separate Persistence update succeeds. Do not report a provider-backed item as completed before that succeeds.

## Result

Return READY only when the complete direct-main delivery proof exists. Return:

- canonical work-item and provider references;
- source and integration commits;
- configured main branch and observed main tip;
- exact reachability or integration-mapping evidence;
- review, source-check, and post-integration verification evidence;
- required local and remote observations;
- clean-state or unrelated-dirty preservation evidence, exact source-to-integration mapping, applicable claim results; and
- the provider lifecycle update or provider-none terminal result.

Return BLOCKED with the preserved source commit, failed check, relevant claim result, recovery evidence, and one next action when integration, conflict resolution, verification, publication, main observation, or a claim operation cannot finish safely. A later provider recording failure is a Persistence failure and does not change Commit READY into BLOCKED.

An unmerged temporary branch can never return READY or cause lifecycle COMPLETED.
