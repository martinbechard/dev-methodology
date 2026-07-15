---
name: agent-claim
description: Use before repository mutation when multiple agents may work concurrently, including atomic narrow-scope extension, explicit broad scopes, repository-global journals, contention reporting, worktree isolation, recovery, and clean release.
metadata:
  category: development-practice
---

# Agent Claim

Use this skill before editing files or taking exclusive runtime resources in a repository where more than one agent may be active.

## Goal

Claims make shared work explicit and keep completed work durable. The first independent writer may use a clean primary worktree. Later independent writers use isolated worktrees when their scopes do not overlap. Overlapping work waits. Dirty unclaimed state enters recovery rather than accepting another anonymous edit.

Start with the narrow scope supported by current evidence. Extend the same claim atomically when another file or resource becomes necessary. Do not speculate about entire directories merely because future scope is unknown.

## Repository-Global State

Use the Git common directory returned by:

```bash
git rev-parse --git-common-dir
```

The live agent-claims.json registry in that directory is the coordination authority. Linked worktrees therefore see the same claims. Use a configured repository-global path supplied by applicable project instructions when Git worktrees are not the coordination boundary. The agent-claim-events directory beside it contains diagnostic history:

- hot contains today and yesterday as uncompressed UTC daily JSON Lines files under the default policy.
- archive contains immutable compressed daily JSON Lines history.
- journal contains compact daily summaries.

External agent transcripts are not claim history. The journal contains coordination identifiers, normalized scopes, modes, outcomes, conflicts, worktree identifiers, and relevant commit identifiers. It does not contain prompts, reasoning, responses, arbitrary tool output, or task descriptions.

## Claim Scope

Use one scope form for each intended ownership kind:

- file names one exact intended file. A future file that does not exist yet is valid.
- tree names one directory subtree and overlaps its descendants.
- all-files names the complete repository file tree.
- resource names one exclusive repository-global runtime or integration resource.

Tree and all-files scope require a short coordination-only scope reason. Do not put prompts, sensitive company information, or personal information in the reason.

The command rejects repository root, wildcards, and existing directories passed through file. It also rejects an existing file passed through tree. A temporary compat-file-directories switch converts existing directories passed through file into warned tree scopes, but still requires a scope reason. New callers use the explicit forms.

## When To Claim

Claim before:

- Editing, moving, deleting, formatting, staging, committing, or generating files.
- Running commands that monopolize shared state such as production builds, browser-test servers, dev server ports, browser profiles, database resets, seed data, generated output refreshes, shared installations, or long-running test servers.

Read-only inspection does not need a writer claim unless it mutates caches, generated files, databases, browser state, or server state.

Use the smallest useful file and resource scope. A parent agent keeps the root task identity. Writing subagents use the same root task identity and their parent claim id, but still receive distinct ownership.

## Atomic Acquisition

Use the bundled command before mutation:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . acquire \
  --claim-id task-123 \
  --agent agent-name \
  --task claim-task-123 \
  --root-task-id task-123 \
  --file src/feature.py \
  --resource build:production \
  --branch codex/task-123 \
  --worktree-path ../project-task-123
```

Use an explicit broad form only when the operation truly owns that scope:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . acquire \
  --claim-id migration-123 \
  --agent agent-name \
  --task migration-123 \
  --root-task-id migration-123 \
  --tree generated \
  --scope-reason "regenerate the owned output tree"
```

For a true repository-wide migration, replace the tree argument with:

```bash
--all-files --scope-reason "repository-wide migration"
```

The command uses an exclusive registry lock and returns one established outcome:

- PRIMARY means no other writer claim exists and the clean primary worktree is now owned by this task.
- ISOLATE means another non-overlapping writer exists and a branch plus linked worktree was created atomically for this task.
- WAIT means requested scope overlaps an active claim. The result includes conflicting claim identifiers and exact overlap pairs. Do not edit or create a competing worktree.
- ISOLATE_REQUIRED means another non-overlapping claim exists but the required branch and worktree path were not supplied.
- RECOVERY_REQUIRED means the primary worktree is dirty without an active claim. Do not add more work.
- RECOVER means an explicitly authorized recovery owner claimed the dirty primary state with the allow-recovery option.

The result includes the claim mode, branch, and target worktree so the owner can distinguish primary, isolated, and recovery behavior.

## Atomic Scope Extension

Stop before touching newly discovered scope. Extend the existing claim while its original ownership remains active:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . extend \
  --claim-id task-123 \
  --file tests/test_feature.py \
  --resource generated:codegen
```

Extension checks only net-new scope against every other active claim under the registry lock. All requested additions succeed together or WAIT leaves the live claim unchanged. Repeating scope the claim already owns succeeds idempotently and the structured result separates added scope from already-owned scope. Extension preserves the original worktree, branch, mode, baseline commit, and claim timestamp.

Scope contraction is not supported. Relinquishing a path while it still has uncommitted changes requires a separate safety design.

## Heartbeat

Keep the heartbeat current during long work:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . heartbeat --claim-id task-123
```

## Runtime And Integration Resources

Resource names are stable and descriptive. Common patterns include:

```text
port:3000
build:production
test:e2e
browser-test:primary
database:seed
generated:codegen
shared-install:skills
merge:integration:main
```

Use repository-specific names when applicable. Separate linked worktrees have independent indexes, branches, and commits. An isolated writer may commit to its unique branch without a repository-global commit resource.

The shared Git operation is integration into a target branch. Acquire a target-specific resource such as merge:integration:main only for the merge, cherry-pick, rebase, or equivalent update of that target, then release it promptly. Integrations into different target branches do not conflict unless another declared shared resource overlaps. Continue using dedicated resources for shared hooks, generators, databases, ports, installations, and output locations that cross worktree boundaries.

## Overlap And Isolation

- Any active writer claim causes a later non-overlapping independent writer to use an isolated branch and worktree.
- Exact files overlap only the same exact file.
- Trees overlap descendants and intersecting ancestor or descendant trees.
- All-files overlaps every exact file and tree.
- Identical exclusive resources overlap even when file scope differs.
- Overlap returns WAIT. Worktree isolation does not make conflicting changes logically safe.
- Never stage, commit, revert, or clean another claim owner’s files unless acting as the explicit integration owner.

## Event Journal Safety

Acquire, extension, heartbeat, recovery, wait, and release outcomes append one versioned event under the same Git common directory. Event identifiers are created at command execution, so replaying or forking an external task transcript cannot duplicate an event.

The live registry remains authoritative. For a registry-changing operation, the command writes the registry first and then appends one fsynced JSON line while still holding the registry lock. A journal failure returns a structured journal_write_failed warning without reversing or weakening the live coordination result. A process crash after the registry write and before the append may therefore create an observable audit gap, but it cannot grant unsafe ownership. Reporting surfaces incomplete lifecycles and malformed or duplicate journal evidence as coverage gaps.

Journal maintenance uses a separate narrow lock and processes only completed UTC days. Claim acquisition remains available while old files are compressed.

## Journal Maintenance

Keep today and the preceding UTC calendar day hot, and archive every older complete day:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . maintain-journal --hot-days 2
```

Maintenance writes a temporary compressed file, validates that decompression exactly matches the hot source, atomically renames the archive, writes a deterministic daily summary, and only then removes the hot file. Reruns are idempotent. An interruption before validation leaves the hot source intact. Compressed archives remain indefinitely by default; deletion requires a separate explicit policy.

## Contention Report

Use only the event journal and live registry for claim diagnostics:

```bash
python3 skills/agent-claim/scripts/claim.py --repo . report --since 2d
python3 skills/agent-claim/scripts/claim.py --repo . report --since 12h --format text
```

The versioned JSON report counts primary, isolated, and recovery acquisitions; waits and rejected transitions; correlated wait episodes; claim duration statistics; exact-file, tree, and resource hotspots; broad-scope reasons; open and incomplete claims; stale heartbeat evidence; integration-resource use; and journal coverage gaps. Repeated WAIT polling by the same claim and action becomes one wait episode while preserving the raw attempt count. Report is read-only and never parses agent harness transcripts.

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
