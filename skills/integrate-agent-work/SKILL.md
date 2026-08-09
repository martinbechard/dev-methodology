---
name: integrate-agent-work
description: Use when combining accepted work from multiple branches, worktrees, or agents.
metadata:
  category: development-practice
---

# Integrate Agent Work

Use this skill when accepted work from separate branches or worktrees must be integrated into main.

## Goal

Keep work separate during implementation. Merge only reviewed, verified, and committed changes. The merge agent resolves conflicts, verifies the combined result, and records cleanup eligibility.

## Preconditions

Before merging a worktree:

- Applicable project instructions own resource-coordination selection. They load the selected
  procedure, if any. Apply the loaded resource-coordination procedure when its event contract
  requires protection during integration. Preserve the complete behavior and evidence that the
  loaded procedure requires. When applicable project instructions select none and load no
  resource-coordination procedure, perform no claim procedure and no claim-specific evidence
  handling. Do not discover, acquire, heartbeat, or release claims.
- Confirm the source worktree has no uncommitted task changes unless the handoff explicitly says how to handle them.
- Confirm the source branch has a meaningful commit for the completed unit.
- Read the source agent status, final notes, verification results, and known risks.
- Confirm the integration worktree is the intended target.

## Merge Workflow

1. Inspect all source worktrees and branches.
2. Order merges by dependency. Merge shared foundation changes before leaf UI or tests.
3. For each source, inspect status, recent commits, and changed files.
4. Reconcile one source at a time on a fresh branch based on current main, applying only the accepted file content or explicitly selected commits required by the work item.
5. Resolve conflicts by preserving the intended steady-state behavior, not by blindly choosing either side.
6. Run focused verification when a merge can affect behavior.
7. Commit each coherent merged unit before starting the next source.
8. Regenerate shared outputs only after the branches containing their source changes are integrated.
9. Run the smallest post-integration tests that prove the merged behavior.
10. Record the source commits, resulting integration commits, and cleanup eligibility.

## Fresh Current-Main Reconciliation

When a candidate branch contains unrelated commits, create a new integration branch from current main. Apply only the accepted files or commits. Do not merge unrelated branch history merely to preserve it.

Record the source commit IDs and accepted files in the integration commit and work item. If integration changes a commit ID, record the source-to-integration mapping.

If current main and the accepted contribution both contain required changes, combine those changes on the new branch. Regenerate only affected outputs. Review and verify the complete result before integration.

## Commands

Inspect source worktrees:

```bash
git worktree list
git status --short
git log --oneline --decorate -n 5
git diff --stat main...HEAD
```

Use a full-history merge only when that complete ancestry is intentional, reviewed, and in scope:

```bash
git merge --no-ff source-branch
```

If the project prefers rebased or squash integration, follow the repository instructions instead.

By default, create a new branch from current main and apply only the accepted content. Identify the source commits and accepted files in the resulting commit.

## Conflict Handling

- Read both sides before resolving a conflict.
- Check specs, tests, and source agent notes when intent is unclear.
- Do not delete functionality merely because it conflicts.
- If two agents changed the same behavior differently, preserve the documented product intent and update tests to match it.
- If intent cannot be determined safely, stop and report the exact conflicting files and decisions needed.

## Verification

Select tests from the merged files, changed behavior, and actual dependency paths:

- Run focused unit or contract tests for the changed behavior.
- Run an integration test only when the merge crosses a real component boundary.
- Run an end-to-end test only when the changed behavior is observable only through that workflow.
- Run git diff --check before committing.

Never treat a clean merge as proof that the merged application works.

## Cleanup

After a source is merged and verified:

- Record the merge commit or integration commit.
- Stop or hand off runtime resources.
- Remove completed worktrees only when the repository policy allows it and the branch has been safely integrated.
- Leave failed or blocked worktrees intact with a clear status note.

## Final Report

Report:

- Source branches or worktrees merged.
- Commit hashes created.
- Verification commands and outcomes.
- Claim results or remaining blockers.
- Worktrees removed or intentionally kept.
