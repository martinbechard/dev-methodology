# Split GitHub Work-Item Skills

Status: Completed

Type: Feature

## Running Ownership

- Canonical Dev Orchestrator task: 019f7f82-4118-76d3-9581-09facc586cf6.
- Branch: codex/split-github-work-item-skills.
- Worktree: /Users/martinbechard/.codex/worktrees/e0d3/dev-methodology.
- Started from approved Ready commit 77492898a96db592d5beab27177ef42bd361f9fc.
- Scope remains limited to the approved legacy GitHub skill, the two replacement packages, their metadata, supported generated mirrors, and directly related non-governed tests and documentation.

## Completion Evidence

- Accepted source commit: ff8a0f40c17b16f62e34cc9a54eecba5507297d7 on codex/split-github-work-item-skills.
- Independent methodology review: the fresh reviewer identified missing executable provider coverage, premature migration wording, and incomplete mutation readback; the corrected candidate resolved every finding and was accepted with no remaining actionable issue.
- Independent focused verification: a separate verifier confirmed the clean candidate, three mocked-provider tests, eight focused bundle tests, evaluation catalogs, exact-package metadata freshness, generated skill documentation, hierarchy and support freshness, and Git integrity.
- Integrated delivery: the accepted sources and current-main generated hierarchy were integrated as eba27afa052b9a72a6e66eff34407061f3588d07 and observed as main HEAD.
- Focused post-integration verification: three mocked-provider tests and six directly related bundle tests passed on main; exact-package metadata, generated skill documentation, hierarchy freshness, commit diff validation, main reachability, and clean status passed.
- Provider coverage: the fixture-backed github-work-item-provider case covers search, duplicate prevention, creation, lifecycle update, dependencies, block, reopen, close, authentication failure, permission denial, ambiguous partial mutation, completion independence, and no shadow backlog path.
- Compatibility boundary: github-issues-backlog now routes current generated and configured callers to the canonical pair until the separately governed selector and role migration changes those callers. The combined provider behavior has moved to create-github-work-item and manage-github-work-items.
- Validation omissions: the preferred MCP skill and YAML validators rejected the linked worktree because it is outside their configured roots, so their policy rejection was not bypassed. No live disposable-repository smoke mutation ran because no explicit disposable GitHub repository authority was supplied.
- Baseline warning: current main already contained create-gitlab-work-item and manage-gitlab-work-items without probe declarations at integration baseline 337e65e7f943cf81f9a28db1a421129ea41a26e8. That unrelated state blocks the broader support-checklist generator on current main and does not invalidate the focused GitHub checks.
- Integration ownership: exact project paths and merge:integration:main were released normally from clean main at event ae07378a-9d5b-408f-b572-a28ca639baae.
- Terminal ownership: exact active and completed backlog paths were acquired separately at event 9cb7d51e-65b8-487b-9e17-62158c4ae1fb and are released immediately after this archive commit is clean.
- Cleanup eligibility: the private branch and worktree are clean, their accepted source patch is integrated on main, and the parent may remove the worktree and safely delete the coordination branch after reconciling the current-main generated hierarchy.

## Approval Resolution

The user approved the exact governed definition scope.

## Approved Scope

Do you approve changing or retiring skills/github-issues-backlog/SKILL.md and its agents/openai.yaml metadata, and creating skills/create-github-work-item/SKILL.md and skills/manage-github-work-items/SKILL.md with their agents/openai.yaml metadata, together with only their supported generated mirrors and directly related non-governed tests and documentation?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Ok”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, message item-2084, directly answering the exact question above.

The decision gate is resolved. Delivery completion still requires implementation, exact governed pre-mutation checks, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Summary

Replace github-issues-backlog with symmetric create-github-work-item and manage-github-work-items skills that use GitHub provider tools as the sole authority and never create shadow backlog files.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](../../feature-backlog/work-item-provider-and-completion/index.md). The current github-issues-backlog prototype combines creation and lifecycle management in one skill. Separating those responsibilities makes GitHub symmetric with other providers while keeping issue lifecycle distinct from pull-request delivery.

## Requirements

- Create create-github-work-item for duplicate search, issue creation, typed content, labels, relationships, acceptance criteria, and initial ownership evidence.
- Create manage-github-work-items for lookup, claim or assignment, lifecycle updates, dependencies, delivery references, blocking, completion, reopening, and reporting.
- Use the authenticated GitHub provider tools for every read and mutation that establishes issue authority.
- Verify the observed repository, issue number, URL, state, labels, assignees, relationships, and updated content after mutation.
- Preserve GitHub issue terminology and do not describe an issue as a pull request or merge request.
- Prohibit repository backlog files, cached issue mirrors, or fallback local queues when GitHub is selected.
- Return BLOCKED when authentication, repository authority, required provider capability, or mutation permission is unavailable.
- Keep issue completion independent from direct-main or feature-branch delivery completion and preserve configured lifecycle rules.
- Record branch, pull-request, commit, review, check, and merge references when available without treating publication alone as issue completion.
- Support one-item explicit GitHub requests without silently changing the project default.
- Retire github-issues-backlog after all procedures and references move to the canonical pair.
- Provide migration guidance for existing PROJECT.yaml and AGENTS.md references.

## Acceptance Criteria

- Creation and management route to distinct symmetric GitHub skills.
- Both skills use provider evidence and return the observed issue identity and state.
- Duplicate detection prevents a second issue for the same durable work.
- A missing provider tool or permission blocks without writing under backlog.
- Pull-request creation or an AWAITING_REVIEW delivery state does not automatically close the issue.
- Configured completion evidence can close the issue and is visible in its durable history.
- github-issues-backlog can be removed without losing behavior.
- No active GitHub provider path creates or instructs creation of a shadow file item.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add mocked provider tests for search, create, duplicate, update, dependency, block, reopen, close, permission denial, authentication failure, and partial mutation.
- Add authorized disposable-repository smoke tests for create and manage operations without using production work items.
- Add negative tests proving no backlog file is created on success or provider failure.
- Verify issue states remain independent from direct-main and feature-branch completion states.
- Run Agent Skill validation, metadata and generated-output checks, provider contract tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- create-pull-request remains a subordinate delivery capability, not a GitHub work-item provider skill.
- Provider mutation smoke tests require explicit repository authority.
