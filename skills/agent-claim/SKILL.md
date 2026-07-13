---
name: agent-claim
description: Use before repository mutation when multiple agents may work concurrently, including optimistic primary-worktree acquisition, isolated worktree selection, overlap blocking, recovery, heartbeat, and clean release.
metadata:
  category: development-practice
---

# Agent Claim

Use this skill before editing files or taking exclusive runtime resources in a repository where more than one agent may be active.

## Goal

Claims make shared work explicit and keep completed work durable. The first independent writer may use a clean primary worktree. Later independent writers use isolated worktrees when their scopes do not overlap. Overlapping work waits. Dirty unclaimed state enters recovery rather than accepting another anonymous edit.

## Claim Registry

Use the repository-global Git common directory returned by:

```bash
git rev-parse --git-common-dir
```

The default registry filename is agent-claims.json inside that directory. Linked worktrees therefore see one registry. Use a configured repository-global path supplied by applicable project instructions when Git worktrees are not the coordination boundary.

Each claim records:

- A stable claim id.
- The agent, task, root task, and optional parent claim.
- Primary, isolated, or recovery mode.
- Files and exclusive runtime resources.
- Worktree path, baseline commit, and baseline status.
- Claim and heartbeat timestamps.

## When To Claim

Claim before:

- Editing, moving, deleting, formatting, staging, committing, or generating files.
- Running commands that monopolize shared state such as production builds, browser-test servers, dev server ports, browser profiles, database resets, seed data, generated output refreshes, shared installations, or long-running test servers.

Read-only inspection does not need a writer claim unless it mutates caches, generated files, databases, browser state, or server state.

Use the smallest useful file and resource scope. A parent agent keeps the root task identity. Writing subagents use the same root task identity and their parent claim id, but still receive distinct ownership.

## Atomic Claim Command

Use the bundled command before mutation:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . acquire \
  --claim-id task-123 \
  --agent agent-name \
  --task "Short task description" \
  --root-task-id task-123 \
  --file src \
  --resource build:production \
  --branch codex/task-123 \
  --worktree-path ../project-task-123
```

The command uses an exclusive registry lock and returns one outcome:

- PRIMARY means no other writer claim exists and the clean primary worktree is now owned by this task.
- ISOLATE means another non-overlapping writer exists and a branch plus linked worktree was created atomically for this task.
- WAIT means a requested file or resource overlaps an active claim. Do not edit or create a competing worktree.
- RECOVERY_REQUIRED means the primary worktree is dirty without an active claim. Do not add more work.
- RECOVER means an explicitly authorized recovery owner claimed the dirty primary state with the allow-recovery option.

Keep the heartbeat current during long work:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . heartbeat --claim-id task-123
```

## Runtime Resources

Resource names should be stable and descriptive. Common patterns include:

```text
port:3000
build:production
test:e2e
browser-test:primary
database:seed
generated:codegen
shared-install:skills
git:commit
```

Prefer repository-specific names when the project defines them.

## Overlap And Isolation

- Any active writer claim causes a later non-overlapping independent writer to use an isolated branch and worktree.
- File ancestry overlaps. A claim for src overlaps src/api and a claim for the complete repository overlaps every path.
- Identical exclusive resources overlap even when files differ.
- Overlap returns WAIT. Worktree isolation does not make conflicting changes logically safe.
- Never stage, commit, revert, or clean another claim owner’s files unless acting as the explicit integration owner.
- If the task expands, stop before touching the new scope and acquire or hand off the additional ownership.

## Stale Claims

A claim may be stale when its heartbeat is old and no matching task, process, or worktree activity exists. Do not remove it merely because it is inconvenient.

Before removing a stale claim:

1. Check task status, logs, running processes, worktrees, Git status, and recent commits.
2. Treat a live process or dirty claimed worktree as active or interrupted work needing handoff.
3. Preserve recovery evidence.
4. Remove only the confirmed stale entry.

If ownership is unclear, leave the claim and report the exact blocker.

## Recovery

Recovery is the one-time bridge from anonymous dirty state to normal coordination.

1. Stop new mutation and obtain handoffs from active writers.
2. Assign one recovery owner for the complete dirty scope.
3. Acquire with allow-recovery.
4. Create a checkpoint commit on a recovery branch before attempting cleanup or historical separation.
5. Validate and stabilize the committed recovery state.
6. Release only after the recovery worktree is clean and its commit differs from the recorded baseline.

Do not require perfect historical commit reconstruction before preserving accumulated work. Preserve first, then stabilize.

## Completion And Release

A modifying task is not complete merely because implementation or tests are complete. A clean finish includes:

- Required verification passed or the blocker is documented.
- Task changes are committed, or the task explicitly produced no changes.
- The claimed worktree is clean.
- Long-running resources are stopped or explicitly handed off.
- The claim is released with the bundled command.
- The final response reports the commit hash, verification, and final status.

```bash
python3 skills/agent-claim/scripts/claim.py --repo . release --claim-id task-123
```

Release rejects dirty worktrees and claims with neither a new commit nor an explicit no-change result. If a safe commit cannot be created, the work remains incomplete and the claim remains active or is handed off explicitly.
