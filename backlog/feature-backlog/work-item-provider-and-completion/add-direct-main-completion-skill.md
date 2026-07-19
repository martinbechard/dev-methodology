# Add Direct-Main Completion Skill

Status: Proposed

Type: Feature

## Summary

Add complete-work-item-direct-main so a verified contribution reaches completion only after its final commit is deliberately integrated into main and observed there.

## Context

This item is a completion lane in the [Work-Item Provider And Completion Contracts series](index.md). The current simple-workitem prototype ends with a verified local commit, which is a useful handoff but does not guarantee that the commit is on main. A temporary isolation branch may be required for safe claim ownership, but that branch is an implementation mechanism rather than the terminal delivery state.

## Requirements

- Add the complete-work-item-direct-main skill with a provider-independent work-item input and explicit target main branch.
- Acquire the appropriate implementation and integration ownership through agent-claim.
- Permit implementation in the clean primary worktree or a canonical isolated worktree according to claim outcomes.
- Require a coherent verified commit before integration.
- When work was produced on an isolated or temporary branch, use agent-work-merge or the repository's accepted integration owner to integrate that commit into current main deliberately.
- Refresh and reconcile the configured main branch before integration without overwriting unrelated work.
- Resolve conflicts through explicit source-backed decisions and rerun affected verification after integration.
- Require the final commit or an integration commit containing it to be reachable from and checked out on main.
- Observe the local and, when publication is part of the configured contract and authority exists, remote main state before returning completion.
- Release implementation and integration claims only from clean committed worktrees.
- Return READY only with the work-item reference, source and integration commits, main reachability evidence, checks, clean state, and required provider lifecycle update.
- Return BLOCKED when main integration, required publication, conflict resolution, verification, ownership, or authority cannot complete safely.
- Do not create a feature branch pull request as a substitute for direct-main integration.

## Acceptance Criteria

- A commit created directly on an authorized current main branch can complete after verification and observed reachability.
- A commit created in an isolated worktree does not complete until it is integrated into main.
- A temporary branch name or pushed branch without main reachability never produces READY.
- An integration conflict triggers explicit resolution and post-integration verification.
- A failed or unauthorized main update returns BLOCKED with the preserved commit and no false lifecycle closure.
- The result identifies exactly which main commit contains the delivered behavior.
- File, GitHub, and GitLab work-item providers can all use the same completion skill independently of their queue lifecycle.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add disposable-repository tests for direct primary commit, isolated commit integration, stale main, unrelated main advance, clean conflict resolution, unresolved conflict, failed verification, missing publication authority, and claim release.
- Assert graph reachability from main rather than accepting branch-name or working-tree claims.
- Add negative tests proving an unmerged temporary branch cannot return READY or close the configured work item.
- Verify provider lifecycle updates receive the final observed main commit.
- Run Agent Skill validation, generated-output checks, focused Git and claim tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- Direct-main describes the final state, not necessarily the worktree used during implementation.
- Repositories that prohibit direct integration to main should select feature-branch completion instead of weakening this contract.
