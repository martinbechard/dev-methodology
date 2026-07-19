---
name: agent-claim
description: Use before repository mutation when multiple agents may work concurrently, including atomic narrow-scope extension, explicit broad scopes, repository-global journals, contention reporting, worktree isolation, recovery, and clean release.
metadata:
  category: development-practice
---

# Agent Claim

Use this skill before editing files or taking exclusive runtime resources in a repository where more than one agent may be active.

## Goal

Claims make shared work explicit and keep completed work durable. The first independent writer may use a clean primary worktree. Later independent writers use isolated worktrees when their scopes do not overlap. Every isolated checkout lives in the canonical .worktrees directory beneath the primary worktree, with the claim id as one portable directory component. Each isolated worktree uses worktree-specific sparse checkout so the repository-root backlog/ directory remains available only from the primary worktree. Overlapping work waits. Dirty unclaimed state enters recovery rather than accepting another anonymous edit.

Start with the narrow scope supported by current evidence. Extend the same claim atomically when another file or resource becomes necessary. Do not speculate about entire directories merely because future scope is unknown.

## Operation Selection

Use the mcp-agent-ops claim tools when the host exposes them. They are the preferred deterministic interface because they accept structured arguments and return a structured exit_code plus result object without shell construction or JSON parsing.

Use the tool that matches the intended operation:

| Operation | MCP tool | Fallback subcommand |
|---|---|---|
| Read live ownership | claim_status | status |
| Acquire ownership | claim_acquire | acquire |
| Extend scope | claim_extend | extend |
| Refresh heartbeat | claim_heartbeat | heartbeat |
| Release ownership | claim_release | release |
| Maintain the journal | claim_maintain_journal | maintain-journal |
| Report contention | claim_report | report |

For an acquisition or extension that includes backlog scope, and for an isolation acquisition that supplies branch or worktree arguments, use the MCP operation only when its exposed contract explicitly advertises PRIMARY_REQUIRED and backlog sparse-checkout behavior, plus canonical primary-root worktree placement. Otherwise resolve and run the loaded agent-claim skill's claim.py script before dispatch. Following ISOLATE_REQUIRED with the required isolation arguments is the documented state transition, not a retry of a failed mutation.

Always inspect result.outcome. PRIMARY, ISOLATE, RECOVER, WAIT, PRIMARY_REQUIRED, ISOLATE_REQUIRED, RECOVERY_REQUIRED, and structured rejections are valid coordination results. A valid result is not an MCP failure and must not be retried through a fallback command.

Outside that explicit capability route, use a fallback only when the tool is absent or the MCP server cannot initialize or connect before request dispatch. Never use a fallback after a path, root, authorization, input-policy, or other structured rejection; those results enforce the active boundary. Prefer the installed mcp-agent-ops-claims command when available. For the capability-routed sparse or backlog flows, use the claim.py script inside the loaded agent-claim package when the copied command does not advertise the required behavior. Resolve the script path once and reuse it for every fallback command in the task. Do not assume the target repository contains skills/agent-claim.

When a transport interruption makes a mutating claim call ambiguous after dispatch, do not repeat the mutation or switch transports immediately. Reconcile with claim_status first. Reconnect and use the MCP status operation when possible; if the server remains unavailable, use only the read-only status fallback. Continue, retry, or release only from the observed registry state so a successful but unacknowledged acquisition cannot become a duplicate claim.

## Fallback Command Path

The distributed script fallback can be resolved with:

```bash
CLAIM_SCRIPT=/absolute/path/to/the-loaded-agent-claim-skill/scripts/claim.py
```

Inside the dev-methodology source checkout, the bundle-owned path is:

```bash
CLAIM_SCRIPT=skills/agent-claim/scripts/claim.py
```

For a normal Codex user-level installation, use:

```bash
CLAIM_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/agent-claim/scripts/claim.py"
```

That default resolves to:

```text
~/.codex/skills/agent-claim/scripts/claim.py
```

Other runtimes use the scripts/claim.py file beside the loaded skill’s SKILL.md. The workflow examples below show the portable script fallback. The installed mcp-agent-ops-claims command accepts the same arguments without python3 and the script path. Use the help option only to diagnose an installed-version mismatch or an unsupported option, not to locate the command or discover the standard workflow.

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

Resolve the primary worktree from Git worktree metadata, even when the command runs from a linked checkout. The canonical linked-checkout root is the .worktrees directory immediately beneath that primary worktree. Never derive it from the current linked worktree, never create it below another linked checkout, and never embed its machine-specific absolute path in portable project guidance. Applicable root project instructions may declare .worktrees as ignored operational state, but the command owns absolute path calculation and enforcement.

## Claim Scope

Use one scope form for each intended ownership kind:

- file names one exact intended file. A future file that does not exist yet is valid.
- tree names one directory subtree and overlaps its descendants.
- all-files names the complete repository file tree.
- resource names one exclusive repository-global runtime or integration resource.

Tree and all-files scope require a short coordination-only scope reason. Do not put prompts, sensitive company information, or personal information in the reason.

The command rejects repository root, wildcards, and existing directories passed through file. It also rejects an existing file passed through tree. A temporary compat-file-directories switch converts existing directories passed through file into warned tree scopes, but still requires a scope reason. New callers use the explicit forms.

The repository-root backlog directory is primary-worktree-only. Claim backlog paths from the primary worktree. When another claim already owns the primary worktree, a backlog acquisition or an isolated claim extension into backlog returns PRIMARY_REQUIRED and preserves the live registry unchanged.

The claim id also names the canonical isolated checkout directory. It must be one portable path component containing only letters, digits, dots, underscores, or hyphens. Invalid identifiers return INVALID_IDENTIFIER before any worktree is created.

## When To Claim

Claim before:

- Editing, moving, deleting, formatting, staging, committing, or generating files.
- Running commands that monopolize shared state such as production builds, browser-test servers, dev server ports, browser profiles, database resets, seed data, generated output refreshes, shared installations, or long-running test servers.

Read-only inspection does not need a writer claim unless it mutates caches, generated files, databases, browser state, or server state.

Use the smallest useful file and resource scope. A parent agent keeps the root task identity. Writing subagents use the same root task identity and their parent claim id, but still receive distinct ownership.

## Stable Exit Codes

The structured JSON outcome is the authoritative coordination result. Stable process exit codes support shell control flow:

- 0 means the command succeeded. Acquisition success returns PRIMARY, ISOLATE, or RECOVER.
- 1 means a general rejection or failure such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, RELEASE_REJECTED, or worktree creation failure.
- 3 means WAIT. Requested scope overlaps another active claim.
- PRIMARY_REQUIRED with exit code 3 means backlog scope must wait until it can run from the primary worktree.
- 4 means ISOLATE_REQUIRED. Another non-overlapping claim exists, but branch and worktree arguments were not supplied.
- 5 means RECOVERY_REQUIRED. The unclaimed primary worktree is dirty and explicit recovery authorization was not supplied.

Several successful and error outcomes share exit codes 0 and 1, so always inspect the JSON outcome. A malformed command line may be rejected by the Python argument parser with exit code 2 before claim coordination runs; that is not a claim outcome.

## Acquisition Workflow

The acquisition command uses an exclusive registry lock. Its result includes the claim mode, branch, and target worktree.

### Primary Acquisition

Request only the narrow scope currently supported by evidence. When no other claim exists and the primary worktree is clean, this returns PRIMARY with exit code 0:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent agent-name \
  --task claim-task-123 \
  --root-task-id task-123 \
  --file src/feature.py
```

Use an explicit broad form only when the operation truly owns that scope:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
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

### Isolation Acquisition

When another non-overlapping claim is active, the primary command without a branch returns ISOLATE_REQUIRED with exit code 4 and does not create a claim. The structured result reports the canonical worktree root and suggested checkout. Retry the same claim identifier with a unique branch:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent agent-name \
  --task claim-task-123 \
  --root-task-id task-123 \
  --file src/feature.py \
  --branch codex/task-123 \
  --base main
```

This returns ISOLATE with exit code 0. The base option selects the Git commit or ref from which the isolated branch is created; it defaults to HEAD. The command derives the target as the primary worktree's .worktrees/task-123 directory, creates the linked checkout with worktree-specific sparse checkout, and omits the backlog/ directory without changing primary-worktree status. The worktree-path compatibility option is accepted only when it resolves exactly to that derived target; any other value returns INVALID_WORKTREE_PATH. Before creation, .worktrees must match the anchored /.worktrees/ pattern in the project .gitignore or another Git ignore source; otherwise the command returns WORKTREE_ROOT_NOT_IGNORED. Do not supply isolation arguments to bypass overlap: conflicting scope still returns WAIT.

### Primary-Only Backlog Acquisition

Backlog creation, lifecycle changes, and archive movements run from the primary worktree. When another claim already exists, a non-overlapping request for a file or tree under backlog returns PRIMARY_REQUIRED with exit code 3 instead of creating an isolated checkout. Wait for the primary claim to finish, then retry without branch or worktree arguments.

### WAIT

Given an active claim that already owns src/feature.py, this overlapping request returns WAIT with exit code 3, conflicting claim identifiers, and exact overlap pairs:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id blocked-task-456 \
  --agent agent-name \
  --task blocked-task-456 \
  --root-task-id blocked-task-456 \
  --file src/feature.py
```

Do not edit, create a competing worktree, or add isolation arguments. Wait, coordinate a handoff, or choose genuinely non-overlapping scope.

### Recovery Acquisition

When the unclaimed primary worktree is dirty, a normal acquisition returns RECOVERY_REQUIRED with exit code 5. After explicit authorization to preserve the complete dirty state, acquire recovery ownership with the allow-recovery option:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id recovery-123 \
  --agent recovery-owner \
  --task recovery-123 \
  --root-task-id recovery-123 \
  --all-files \
  --scope-reason "recover anonymous dirty state" \
  --allow-recovery
```

This returns RECOVER with exit code 0. Create the required checkpoint commit before cleanup or release.

## Atomic Scope Extension

Stop before touching newly discovered scope. Extend the existing claim while its original ownership remains active:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --file tests/test_feature.py \
  --resource generated:codegen
```

Extension checks only net-new scope against every other active claim under the registry lock. All requested additions succeed together or WAIT leaves the live claim unchanged. Repeating scope the claim already owns succeeds idempotently and the structured result separates added scope from already-owned scope. Extension preserves the original worktree, branch, mode, baseline commit, and claim timestamp.

An isolated claim cannot extend into backlog scope. That request returns PRIMARY_REQUIRED and leaves the claim unchanged so backlog work can be retried from the primary worktree.

Scope contraction is not supported. Relinquishing a path while it still has uncommitted changes requires a separate safety design.

## Heartbeat

Keep the heartbeat current during long work:

```bash
python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123
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
- Every isolated checkout is derived beneath the primary worktree's .worktrees directory, never beneath the caller's current linked worktree.
- The canonical worktree root must be ignored, and double-force Git clean is prohibited while linked checkouts exist.
- Exact files overlap only the same exact file.
- Trees overlap descendants and intersecting ancestor or descendant trees.
- All-files overlaps every exact file and tree.
- Identical exclusive resources overlap even when file scope differs.
- Backlog paths are never materialized in isolated worktrees and may only be claimed from the primary worktree.
- Overlap returns WAIT. Worktree isolation does not make conflicting changes logically safe.
- Never stage, commit, revert, or clean another claim owner’s files unless acting as the explicit integration owner.

## Event Journal Safety

Acquire, extension, heartbeat, recovery, wait, and release outcomes append one versioned event under the same Git common directory. Event identifiers are created at command execution, so replaying or forking an external task transcript cannot duplicate an event.

The live registry remains authoritative. For a registry-changing operation, the command writes the registry first and then appends one fsynced JSON line while still holding the registry lock. A journal failure returns a structured journal_write_failed warning without reversing or weakening the live coordination result. A process crash after the registry write and before the append may therefore create an observable audit gap, but it cannot grant unsafe ownership. Reporting surfaces incomplete lifecycles and malformed or duplicate journal evidence as coverage gaps.

Journal maintenance uses a separate narrow lock and processes only completed UTC days. Claim acquisition remains available while old files are compressed.

## Journal Maintenance

Keep today and the preceding UTC calendar day hot, and archive every older complete day:

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
```

Maintenance writes a temporary compressed file, validates that decompression exactly matches the hot source, atomically renames the archive, writes a deterministic daily summary, and only then removes the hot file. Reruns are idempotent. An interruption before validation leaves the hot source intact. Compressed archives remain indefinitely by default; deletion requires a separate explicit policy.

## Contention Report

Use only the event journal and live registry for claim diagnostics:

```bash
python3 "$CLAIM_SCRIPT" --repo . report --since 2d
python3 "$CLAIM_SCRIPT" --repo . report --since 12h --format text
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
3. Run the Recovery Acquisition command with the allow-recovery option.
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
- A clean released isolated checkout is removed by the orchestration owner only after its verified commit is preserved on a branch or integrated into the target.
- The final response reports the commit hash, verification, and final status.

### Committed Release

After the claimed worktree is clean and contains the verified task commit, release normally:

```bash
python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

After the verified commit is preserved and the claim is released, run cleanup from the primary worktree:

```bash
git worktree remove .worktrees/task-123
git worktree prune
```

Never remove a dirty, active, uncommitted, or unpreserved checkout.

### No-Change Release

When the task legitimately produced no repository change, first confirm the claimed worktree is clean, then declare that result explicitly:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --no-change
```

The no-change option is not permission to discard or ignore dirty files. Release rejects every dirty worktree. Without no-change, release also rejects a claim whose current commit still equals its recorded baseline. If a safe commit or truthful no-change result cannot be produced, the work remains incomplete and the claim remains active or is handed off explicitly.
