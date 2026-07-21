---
name: agent-work-merge
description: Use when integrating work from multiple agents, linked git worktrees, parallel task branches, claim-coordinated repositories, subagent outputs, or concurrent implementation lanes.
metadata:
  category: development-practice
---

# Agent Work Merge

Use this skill when multiple agents complete work in separate git worktrees or branches and their results need to be merged into the main integration checkout.

## Goal

Keep parallel work isolated during implementation, then merge only verified, committed, and claimed work into the integration lane. The merge agent owns coordination, conflict resolution, final verification, and cleanup.

## Preconditions

Before merging a worktree:

- Use the agent-claim skill for files and runtime resources touched during integration.
- Confirm the source worktree has no uncommitted task changes unless the handoff explicitly says how to handle them.
- Confirm the source branch has a meaningful commit for the completed unit.
- Read the source agent status, final notes, verification results, and known risks.
- Confirm the integration checkout is the intended target lane.
- Confirm the source claim was released after a clean commit or explicitly handed to the integration owner.
- Reject anonymous dirty state. Route it through the recovery workflow in agent-claim before integration.

## Merge Claim

Claim the target-specific integration resource only for the shared target update, together with any files likely to be touched by conflict resolution. Separate worktrees may commit to their unique branches without a repository-global commit resource. Release the integration resource promptly after the merge, cherry-pick, rebase, or equivalent target update and its required verification complete.

Example claim:

```json
{
  "agent": "merge-agent",
  "task": "Merge completed agent work",
  "files": ["src/feature/file.ts", "test/feature/file.test.ts"],
  "resources": ["merge:integration:main", "build:production"],
  "claimed_at": "2026-06-10T20:30:00Z",
  "heartbeat": "2026-06-10T20:30:00Z",
  "worktree": "/absolute/path/to/integration-checkout"
}
```

## Merge Workflow

1. Inspect all source worktrees and branches.
2. Order merges by dependency. Merge shared foundation changes before leaf UI or tests.
3. For each source, inspect status, recent commits, and changed files.
4. Reconcile one source at a time on a fresh branch based on current main, applying only the accepted file content or explicitly selected commits required by the work item.
5. Resolve conflicts by preserving the intended steady-state behavior, not by blindly choosing either side.
6. Run focused verification after each risky merge.
7. Commit each coherent merged unit before starting the next source.
8. Regenerate shared outputs only after the branches containing their source changes are integrated.
9. Run final repository verification required by the project.
10. Release claims only after verification, a clean integration commit, and cleanup are complete.

## Fresh Current-Main Reconciliation

Prefer a fresh reconciliation branch from current main when a candidate branch contains cumulative, unrelated, or out-of-scope ancestry. Apply the exact accepted paths, or cherry-pick only the explicitly selected commits whose complete changes are in scope. Do not merge cumulative feature-branch history merely to preserve provenance.

Record every source commit identifier, accepted path set, and any non-ancestral content mapping in the reconciliation commit message and durable work item. That evidence preserves provenance without making unrelated history reachable from main. Use a full-history merge only when the complete imported history is intentional, reviewed, and inside the integration ownership scope.

When current main and an accepted contribution both contain contracts that must survive, reconcile their semantic union on the fresh branch. Regenerate only supported outputs, review the complete reconciled diff in a fresh context, and verify the bounded result before integration. Content equivalence and durable source mapping are valid provenance evidence; a two-parent merge is not required.

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

The default ancestry-bounded path is a fresh branch from current main with exact accepted content or selected commits applied according to the repository's supported workflow. The resulting commit must identify its source commits and accepted paths.

## Conflict Handling

- Read both sides before resolving a conflict.
- Check specs, tests, and source agent notes when intent is unclear.
- Do not delete functionality merely because it conflicts.
- If two agents changed the same behavior differently, preserve the documented product intent and update tests to match it.
- If intent cannot be determined safely, stop and report the exact conflicting files and decisions needed.

## Verification

Run the project-required checks for the merged surface. At minimum:

- Syntax or build verification when code changed.
- Focused unit tests for changed units.
- E2E or smoke tests when routing, auth, UI workflows, middleware, server startup, generated output, or shared runtime behavior changed.
- Diff hygiene before commit when broad or conflict-heavy changes were made.

Never treat a clean merge as proof that the merged application works.

## Cleanup

After a source is merged and verified:

- Record the merge commit or integration commit.
- Remove only claims owned by the merge task.
- Stop or hand off runtime resources.
- Remove completed worktrees only when the repository policy allows it and the branch has been safely integrated.
- Leave failed or blocked worktrees intact with a clear status note.
- Never release the integration claim while newly created uncommitted work remains.
- Keep inactive coordination-registry cleanup, Git integration, and terminal backlog closeout as distinct operations with separate evidence. A successful administrative reset is not an integration or completion event.

## Final Report

Report:

- Source branches or worktrees merged.
- Commit hashes created.
- Verification commands and outcomes.
- Claims released or remaining blockers.
- Worktrees removed or intentionally kept.
