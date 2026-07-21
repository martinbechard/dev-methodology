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

## Coordination Registry Authority

The coordination registry is temporary conflict protection for shared mutation. It records which exact paths and exclusive resources currently require protection so concurrent owners do not collide. It does not decide whether reviewed, verified, committed product delivery exists, whether accepted bytes are integrated, or whether a work item is complete.

Treat acquisition, wait, heartbeat, release, and release-validation outcomes as coordination evidence. Reconcile those diagnostics with the durable work item, Git commits and content, review evidence, verification evidence, processes, worktrees, and resource state. A coordination failure does not erase evidence owned by those other records.

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

For an acquisition or extension that includes backlog scope, and for an isolation acquisition that supplies branch or worktree arguments, use the MCP operation only when its exposed contract explicitly advertises SHARED_CHECKOUT_REQUIRED and SHARED_CHECKOUT_RELEASE_REQUIRED, backlog sparse-checkout behavior, and canonical primary-root worktree placement. Otherwise resolve and run the loaded agent-claim skill's claim.py script before dispatch. Following ISOLATED_CHECKOUT_SETUP_REQUIRED with the required isolation arguments is the documented state transition, not a retry of a failed mutation.

Always inspect result.outcome. SHARED_CHECKOUT_ACQUIRED, ISOLATED_CHECKOUT_ACQUIRED, DIRTY_CHECKOUT_RECOVERY_ACQUIRED, CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, SHARED_CHECKOUT_RELEASE_REQUIRED, ISOLATED_CHECKOUT_SETUP_REQUIRED, DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED, and structured rejections are valid coordination results. A valid result is not an MCP failure and must not be retried through a fallback command.

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
- project-files names every project file except backlog and ignored operational worktree state.
- backlog names the complete repository-root backlog subtree.
- all-files names the explicit union of project-files and backlog.
- resource names one exclusive repository-global runtime or integration resource.

Tree, project-files, and all-files scope require a short coordination-only scope reason. Do not put prompts, sensitive company information, or personal information in the reason.

Select at most one broad file domain. Exact files and trees are classified into project-files or backlog ownership. A request that mixes project and backlog paths is rejected atomically with INVALID_SCOPE and mixed_file_domains. Explicit backlog paths remain compatible and produce the compat_backlog_path warning so status, journal events, and diagnostics make the normalization visible. Resources may accompany any one selected file domain.

The command rejects repository root, wildcards, and existing directories passed through file. It also rejects an existing file passed through tree. A temporary compat-file-directories switch converts existing directories passed through file into warned tree scopes, but still requires a scope reason. New callers use the explicit forms.

The repository-root backlog directory and all-files ownership are primary-worktree-only. Claim backlog paths from the primary worktree. When another claim already owns that shared checkout, a backlog acquisition returns SHARED_CHECKOUT_RELEASE_REQUIRED and preserves the live registry unchanged. An isolated claim extension into backlog returns SHARED_CHECKOUT_REQUIRED because the caller must hand the work to the shared checkout. Project-files claims remain eligible for canonical isolated worktrees.

Every claim and scope result records file_domain as project_files, backlog, all_files, or none and records the matching broad booleans. The none value is used when no file scope was selected. Existing no-file-scope callers retain complete-worktree clean-release compatibility.

Status normalizes active claims written by an earlier registry schema for display without silently rewriting the registry. A legacy claim with paths in both domains is reported as legacy_mixed, cannot extend into another file scope, and retains complete-worktree release rules. A claim that lacks a trustworthy out-of-domain baseline also retains complete-worktree release rules. This compatibility boundary prevents old ownership from being relabeled or from gaining permission through missing evidence.

The claim id also names the canonical isolated checkout directory. It must be one portable path component containing only letters, digits, dots, underscores, or hyphens. Invalid identifiers return INVALID_IDENTIFIER before any worktree is created.

## When To Claim

Claim before:

- Editing, moving, deleting, formatting, staging, committing, or generating files.
- Running commands that monopolize shared state such as production builds, browser-test servers, dev server ports, browser profiles, database resets, seed data, generated output refreshes, shared installations, or long-running test servers.

Read-only inspection does not need a writer claim unless it mutates caches, generated files, databases, browser state, or server state.

Use the smallest useful file and resource scope. A parent agent keeps the root task identity. Writing subagents use the same root task identity and their parent claim id, but still receive distinct ownership.

## Stable Exit Codes

The structured JSON outcome is the authoritative coordination result. Result schema version 2 uses the canonical outcome vocabulary and includes legacy_outcome only when a canonical name replaces a schema version 1 name. Stable process exit codes support shell control flow:

- 0 means the command succeeded. Acquisition success returns SHARED_CHECKOUT_ACQUIRED, ISOLATED_CHECKOUT_ACQUIRED, or DIRTY_CHECKOUT_RECOVERY_ACQUIRED.
- 1 means a general rejection or failure such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, RELEASE_REJECTED, or worktree creation failure.
- 3 with CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED means requested scope overlaps another active claim.
- 3 with SHARED_CHECKOUT_REQUIRED means the operation must be handed to the shared checkout before it can proceed.
- 3 with SHARED_CHECKOUT_RELEASE_REQUIRED means another owner must release the shared checkout before the operation can proceed there.
- 4 means ISOLATED_CHECKOUT_SETUP_REQUIRED. Another non-overlapping claim exists, but branch and worktree arguments were not supplied.
- 5 means DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED. The unclaimed shared checkout is dirty and explicit recovery authorization was not supplied.

Several successful and error outcomes share exit codes 0 and 1, so always inspect the JSON outcome. A malformed command line may be rejected by the Python argument parser with exit code 2 before claim coordination runs; that is not a claim outcome.

### Result Migration

Schema version 2 result documents use these canonical outcomes. During the compatibility period, legacy_outcome carries the prior result name shown below. Outcomes not listed here keep their existing name and omit legacy_outcome.

| Canonical outcome | Plain-language meaning | Required next action | Legacy outcome |
|---|---|---|---|
| SHARED_CHECKOUT_ACQUIRED | Ownership was acquired in the repository's existing shared checkout. | Work only within the acquired scope there. | PRIMARY |
| ISOLATED_CHECKOUT_ACQUIRED | Ownership was acquired in a newly prepared isolated checkout. | Work only within the acquired scope in the returned checkout. | ISOLATE |
| DIRTY_CHECKOUT_RECOVERY_ACQUIRED | Recovery ownership was acquired over explicitly authorized dirty state. | Preserve the state in a checkpoint commit before cleanup. | RECOVER |
| CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED | No ownership was acquired because requested scope overlaps another owner. | Wait for a handoff or choose genuinely non-overlapping scope. | WAIT |
| SHARED_CHECKOUT_REQUIRED | No ownership was acquired because the operation must run from the shared checkout. | Hand the operation to that checkout and reconcile status there. | PRIMARY_REQUIRED |
| SHARED_CHECKOUT_RELEASE_REQUIRED | No ownership was acquired because another claim currently owns the shared checkout. | Wait for its release notification before retrying there. | PRIMARY_REQUIRED |
| ISOLATED_CHECKOUT_SETUP_REQUIRED | No ownership was acquired because an isolated branch and checkout must be prepared. | Repeat the acquisition with the required isolation arguments. | ISOLATE_REQUIRED |
| DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED | No ownership was acquired because dirty state requires explicit recovery authority. | Obtain authority before repeating with recovery enabled. | RECOVERY_REQUIRED |

Schema version 1 journal events remain append-only and retain the original outcome strings. Reporting readers interpret recognized legacy and canonical strings through the same meanings, publish canonical outcome counts, and retain raw outcome counts so historical provenance is not rewritten or hidden.

## Acquisition Workflow

The acquisition command uses an exclusive registry lock. Its result includes the claim mode, branch, and target worktree.

### Shared Checkout Acquisition

Request only the narrow scope currently supported by evidence. When no other claim exists and the shared checkout is clean, this returns SHARED_CHECKOUT_ACQUIRED with exit code 0:

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

For broad ordinary implementation work, use:

```bash
--project-files --scope-reason "project implementation"
```

For a short serialized queue transition from the primary worktree, use:

```bash
--backlog
```

### Isolated Checkout Acquisition

When another non-overlapping claim is active, the command without a branch returns ISOLATED_CHECKOUT_SETUP_REQUIRED with exit code 4 and does not create a claim. The structured result reports the canonical worktree root and suggested checkout. Retry the same claim identifier with a unique branch:

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

This returns ISOLATED_CHECKOUT_ACQUIRED with exit code 0. The base option selects the Git commit or ref from which the isolated branch is created; it defaults to HEAD. The command derives the target as the primary worktree's .worktrees/task-123 directory, creates the linked checkout with worktree-specific sparse checkout, and omits the backlog/ directory without changing primary-worktree status. The worktree-path compatibility option is accepted only when it resolves exactly to that derived target; any other value returns INVALID_WORKTREE_PATH. Before creation, .worktrees must match the anchored /.worktrees/ pattern in the project .gitignore or another Git ignore source; otherwise the command returns WORKTREE_ROOT_NOT_IGNORED. Do not supply isolation arguments to bypass overlap: conflicting scope still returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED.

### Shared-Checkout-Only Backlog Acquisition

Backlog creation, lifecycle changes, and archive movements run under a short backlog claim from the primary worktree. When another claim owns that shared checkout, a backlog request returns SHARED_CHECKOUT_RELEASE_REQUIRED with exit code 3 instead of creating an isolated checkout. Wait for a direct baton handoff or completion notification, then retry without branch or worktree arguments. Do not poll. When the caller is in an isolated checkout but the shared checkout is available, SHARED_CHECKOUT_REQUIRED directs a handoff to the shared checkout.

### Claim Scope Conflict Wait

Given an active claim that already owns src/feature.py, this overlapping request returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED with exit code 3, conflicting claim identifiers, and exact overlap pairs:

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

When the unclaimed shared checkout is dirty, a normal acquisition returns DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED with exit code 5. After explicit authorization to preserve the complete dirty state, acquire recovery ownership with the allow-recovery option:

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

This returns DIRTY_CHECKOUT_RECOVERY_ACQUIRED with exit code 0. Create the required checkpoint commit before cleanup or release.

## Atomic Scope Extension

Stop before touching newly discovered scope. Extend the existing claim while its original ownership remains active:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --file tests/test_feature.py \
  --resource generated:codegen
```

Extension checks only net-new scope against every other active claim under the registry lock. All requested additions succeed together or CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED leaves the live claim unchanged. Repeating scope the claim already owns succeeds idempotently and the structured result separates added scope from already-owned scope. Extension preserves the original worktree, branch, mode, baseline commit, and claim timestamp.

An isolated claim cannot extend into backlog scope. That request returns SHARED_CHECKOUT_REQUIRED and leaves the claim unchanged so backlog work can be retried from the primary worktree.

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
- Overlap returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED. Worktree isolation does not make conflicting changes logically safe.
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

The versioned JSON report counts shared-checkout, isolated-checkout, and dirty-checkout recovery acquisitions; waits and rejected transitions; correlated wait episodes; claim duration statistics; exact-file, tree, and resource hotspots; broad-scope reasons; open and incomplete claims; stale heartbeat evidence; integration-resource use; and journal coverage gaps. Readers normalize recognized legacy aliases into canonical outcome_counts while retaining the original strings in raw_outcome_counts. Repeated conflict-wait events by the same claim and action become one wait episode while preserving the raw attempt count. Report is read-only and never parses agent harness transcripts.

## Administrative Reset Of Inactive Entries

An entry may be inactive when its heartbeat is old and no matching task, process, worktree activity, or claimed resource use exists. Do not reset an entry merely because it is inconvenient or because another task wants its scope.

Before an administrative reset:

1. Inspect the owning task state and logs, matching running processes, every claimed worktree, Git cleanliness, recent commits, and preserved source or integration commits.
2. Inspect every claimed shared resource and confirm that no browser, database, port, server, generator, installation, integration target, or other exclusive facility remains in use or awaiting explicit handoff.
3. Inspect the other coordination registry entries and confirm that removing the target entry cannot erase or weaken another active owner's protection.
4. Inspect the event journal and retain a readable registry snapshot or exact journal references that identify the target, the observations, the decision, and the administrative actor.
5. Treat a live process, a dirty unpreserved claimed worktree, unclear task ownership, or a resource still in use as active or interrupted work requiring handoff. Stop the reset and report the exact blocker.
6. Reset only when the target entry is inactive, its work is completed or preserved in durable commits and evidence, every claimed resource is stopped or handed off, and no other active protection can be affected.
7. Use only a host-supported targeted atomic reset operation that names the exact entry, reacquires the coordination registry lock, revalidates the safeguards at mutation time, removes only that entry, and appends the administrative outcome to the event journal. If no such operation is available, stop and route the reset to an administrator or implementation that supplies those guarantees.

The bundled portable command does not expose an administrative reset subcommand. Never edit the live registry file manually: an unlocked edit can race acquisition, remove an active protection, or bypass the event journal. An administrative reset changes only the inactive coordination registry state. It must not rewrite Git, edit project files, discard a worktree, manufacture a release event, or substitute for review, verification, integration, work-item completion, or cleanup evidence. Preserve the snapshot or journal reference with the durable work-item or incident record.

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

Release validates operational coordination state, not committed content. It checks current owned-domain cleanliness and compares current out-of-domain worktree and index state with the acquisition baseline. Status inspection uses NUL-delimited records so spaces, quotes, non-ASCII text, newlines, rename records, and text resembling a rename arrow remain exact paths. Unchanged pre-existing out-of-domain dirtiness does not become owned work and does not block release. A changed staged, unstaged, or untracked out-of-domain path returns RELEASE_REJECTED with reason out_of_domain_changes and reports only paths whose current state differs from the baseline. The command records the resulting commit and requires either a commit change or an explicit no-change declaration, but it does not traverse commit history, audit committed paths, enforce contribution scope, or interpret merge ancestry. Independent review and integration own committed-content, changed-path, and provenance decisions. The command never stages, commits, reverts, or cleans project paths.

Treat release-validation failures as coordination diagnostics, not automatic delivery verdicts. When an inactive registry entry remains after work and resources are preserved, inspect the administrative-reset safeguards and reconcile the durable Git, review, verification, and work-item evidence. Never use that diagnosis to bypass an active owner, accept a dirty unpreserved worktree, or declare a release that did not occur.

Contention reports count broad events by project_files, backlog, and all_files domain in addition to total broad events and reasons. This keeps ordinary project ownership, serialized backlog transitions, and exceptional repository-wide work distinguishable in historical diagnostics.

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
