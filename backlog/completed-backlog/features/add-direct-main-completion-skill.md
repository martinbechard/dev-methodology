# Add Direct-Main Completion Skill

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7f8c-e53a-7f23-9920-9df843d3b5d9.
- Branch: codex/add-direct-main-completion-skill.
- Worktree: /Users/martinbechard/.codex/worktrees/5785/dev-methodology.
- Started from approved Ready commit 547e2159e5621351adb9a4e975b7659bc1993671.
- Scope remains limited to the approved direct-main completion skill, its metadata, supported generated mirrors, and directly related non-governed tests and documentation.

## Completion Evidence

- Phase: Completed.
- Accepted candidate: e8a25d9b3348673d4a6e967b3b69534c96f48850 on codex/add-direct-main-completion-skill.
- Governed checks: both exact authorized paths returned ALLOWED_APPROVED_DEFINITION_CHANGE before mutation.
- Independent methodology review: APPROVED after the disposable-repository coverage and deterministic non-ancestral replay corrections.
- Independent verifier: VERIFIER PASS for the accepted candidate with seven disposable Git contract tests, two focused bundle tests, metadata freshness, skill-documentation freshness, support-checklist freshness, hierarchy freshness, generated attribution, and diff hygiene.
- Integration claim: direct-main-completion-integration-019f7f8c acquired PRIMARY at event 6f014d25-6b72-46a8-9e8d-92d3731a157f on main base a07d4c8d81c57a77025e860ee05047a4d6c901b8 and released normally at event e43a3a6c-2b02-4f67-8933-23e3b401efd5.
- Semantic integration mapping: 99661ff7a7a33770f9093cd6fd87450259f00940 to 41a9da8, e78c489f54bf54aa08d33ecc042ae2875b55b279 to e8a96f5, and e8a25d9b3348673d4a6e967b3b69534c96f48850 to final delivery commit 8e10117b0d695f12e5acc54576825566e2a3879b.
- Main observation: 8e10117b0d695f12e5acc54576825566e2a3879b was observed on checked-out clean main and remains reachable from current main c2df2eaf1d4629df34e75a1c6896a2d401241c5a.
- Current-main verification: nine focused tests pass; OpenAI metadata, skill documentation, agent-skill hierarchy, and support checklist are current; the accepted skill, metadata, and disposable Git test are byte-identical to current main; main is clean.
- Validation: MCP YAML validation passed. MCP skill validation rejected repository source as outside configured installed skill roots, so no fallback bypass was attempted.
- Review correction evidence: the contract tests cover direct primary delivery, isolated integration, unrelated main advances, unresolved and resolved conflicts, failed verification, missing publication authority, live claim blocking, non-ancestral patch-equivalent replay, provider handoff, and the unmerged-branch negative.
- Integration contention: attempt 1 waited on split-github-integration-019f7f82 at event 860e22c3-cc38-41d9-987d-ec7126804abc; a release-baton retry returned ISOLATE_REQUIRED at event dcb8fc1d-0969-41b2-8e26-3ebf691bfc54 while GitHub closed its backlog; attempt 2 waited on azure-jira-placeholders-integration-019f7f8c at event c9945d9d-3313-463c-b877-a40bd865611d; the next clean baton acquired successfully.
- Terminal backlog claim: direct-main-completion-backlog-019f7f8c acquired PRIMARY for only the active and completed paths at event 5aba46de-242e-4084-be4f-ce93f5f03771 after serialized predecessor releases. Its normal clean release follows this committed archive transaction.
- Cleanup eligibility: the private worktree is clean at e8a25d9b3348673d4a6e967b3b69534c96f48850. The governed skill files and disposable Git contract test are byte-identical to current main. The branch is semantically integrated through the mapping above rather than ancestry-merged, so the parent may remove the clean worktree and safely delete the branch using this patch-equivalence evidence.
- Open issues: none for this work item. The full catalog remains the campaign final-state gate and was intentionally not run for this bounded item.

## Approval Resolution

The user approved the exact governed definition scope as part of the originally requested work-item completion skills.

## Approved Scope

Do you approve creating skills/complete-work-item-direct-main/SKILL.md with its agents/openai.yaml metadata, together with only its supported generated mirrors and directly related non-governed tests and documentation?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Ok - I approve all of the skills that I orignianlly requested”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, message item-2093, applying to the exact direct-main skill question above.

The decision gate is resolved. Delivery completion still requires implementation, the exact governed pre-mutation check, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Summary

Add complete-work-item-direct-main so a verified contribution reaches completion only after its final commit is deliberately integrated into main and observed there.

## Context

This item is a completion lane in the [Work-Item Provider And Completion Contracts series](../../feature-backlog/work-item-provider-and-completion/index.md). The current simple-workitem prototype ends with a verified local commit, which is a useful handoff but does not guarantee that the commit is on main. A temporary isolation branch may be required for safe claim ownership, but that branch is an implementation mechanism rather than the terminal delivery state.

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
