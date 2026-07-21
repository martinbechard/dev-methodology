---
name: codex-workitem-coordination
description: Coordinate multiple file-backed repository work items through one parent backlog coordinator and one Dev Orchestrator task per Running item. Use when Codex must sustain a queue, integrate reviewed work, close completed items, and recover stalled integration without a separate task registry.
metadata:
  category: development-practice
---

# Codex Work-Item Coordination

Use one Dev Backlog Coordinator as the parent dispatcher. Give each Running work item to one user-visible Dev Orchestrator task that owns delivery through review, integration, focused verification, work-item completion, and terminal handoff.

## Authority And Roles

- The file-backed work item is the only durable task record.
- Git records branches, commits, integration, and cleanup eligibility.
- The coordination registry records temporary shared-mutation protection. It prevents concurrent conflicts but does not determine whether reviewed, verified, committed delivery exists.
- Codex task state and title are display and execution state, not lifecycle authority.
- Dev Backlog Coordinator owns queue inventory, priority, dispatch, stalled-integration investigation, and terminal task cleanup.
- Dev Orchestrator owns one work item from Running through delivery or a truthful terminal outcome. It may start Dev Coder, independent reviewer, and verifier subagents inside that task.
- Dev Backlog Steward applies [manage-backlog](../manage-backlog/SKILL.md) when it performs a specialized backlog mutation. The parent coordinator follows this skill's bounded retry and queue rules.

Do not create a separate parent ledger, baton registry, waiting-task registry, or task database. Do not copy this procedure into AGENTS.md or a Dev Orchestrator definition.

## Work-Item Execution Record

Every Running work item records these facts in its ownership, open-issues, and evidence sections:

- canonical Codex task identifier and Dev Orchestrator owner
- branch and worktree
- current phase
- accepted candidate commit
- integration-wait or completion-wait start time
- claim attempt count, last outcome, next attempt time, and blocking claim identifiers
- open issues and the owner of each next action
- review, integration, focused verification, claim-release, completion, and cleanup evidence as those events occur

Update the work item when a material phase changes. Preserve the same canonical task identifier through corrections, integration, and closeout. Never infer identity from the task title alone.

## Queue Target And Dispatch

Derive active capacity from the backlog files:

1. Count work items whose file-backed Status is Running.
2. When the count is below ten, select eligible Ready items and dispatch enough distinct Dev Orchestrator tasks to restore ten Running items.
3. Record each canonical task identifier in its work item as part of the Running transition.
4. Use exactly one user-visible task per Running work item.
5. Dispatch only work that can begin implementation or another bounded delivery phase. Do not create a task merely to wait for approval, a dependency, a reviewer, a claim, or an integration window.
6. When an item leaves Running, fill the vacancy promptly.

Blocked, User Action Required, Holding, Completed, Failed, and Abandoned items do not count toward ten. If fewer than ten eligible items exist, run all eligible items and report the shortage instead of manufacturing placeholder work.

## Dispatch Reconciliation

Treat a task-creation error, timeout, disconnect, or ambiguous response as an ambiguous mutation.

Before retrying, reconcile active and archived tasks using all available identity evidence:

- source parent task identifier
- canonical backlog path
- normalized objective
- creation time
- task status

If exactly one match exists, adopt it. If multiple matches exist, preserve one canonical task, stop every duplicate before mutation, verify no unique work is lost, and archive the duplicates when supported. If no match is immediately visible, allow one bounded settlement interval and reconcile again. Retry creation only once after that settled read still shows no match, then reconcile once more.

## Task Execution Compatibility And Titles

Create each Dev Orchestrator task in an environment that can perform its ordinary repository work without asking the user to approve Git, shell, test, process-inspection, or claim commands. The dispatch prompt must state that these ordinary operations are already authorized by the work item and that the task must not open or wait on a user approval prompt for them.

- Use the exposed mcp-agent-ops claim operations for claim status, acquisition, extension, heartbeat, and release whenever they are available. Do not invoke the shell claim fallback merely as a routine preflight when the MCP operations are available.
- Keep implementation and focused tests in the task-owned private worktree. The environment must permit ordinary writes to that worktree and the Git worktree metadata needed for local commits.
- When a work item depends on a special runtime capability, test that capability through the same nested execution path the real workload uses before assigning more equivalent work to that environment. A direct command is not sufficient evidence for a runner that invokes the command from a child process.
- Treat prior task-capability evidence as stale after any agent-definition or metadata generation, adapter installation, MCP refresh, Codex configuration change, permission-profile change, application update, or host restart. Before dispatching real work again, run one disposable worktree pilot through the effective child task runtime.
- The post-change pilot must prove the effective task profile and ordinary operations, not merely read the requested configuration or repeat permission wording in its prompt. Inspect the child task's effective approval, sandbox, and permission profile; create a harmless Git commit; invoke every special capability through the same nested helper used by the real workload; and read the claim registry through MCP.
- If the requested configuration and effective child runtime differ, or any representative operation fails, stop equivalent dispatch immediately. Record the exact requested and effective profiles, archive the failed pilot, correct or replace the launch environment, and rerun the pilot. Do not treat a successful direct command, parent capability, config file, or earlier task as evidence for the failing child runtime.
- If an ordinary required operation fails because the task environment lacks a capability, the task stops immediately, preserves its work, releases any claim truthfully, and reports the exact failed operation to the parent. It must not request escalation from the user.
- The parent promptly re-homes or replaces that task in a compatible environment, updates the canonical task identifier in the work item, and fills any resulting Running vacancy. Do not leave an approval prompt or an execution-incompatible task consuming a Running slot.

Set a concise plain-text title when the task is created and update it only at material phase changes. Use a phase prefix such as Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —, Waiting for Help —, Waiting for User —, Done —, Blocked —, Failed —, or Abandoned — followed by a short work-item name. Never use raw prompt text, XML or delegation tags, error output, task identifiers, or generic titles as the display title. Preserve the stable task identifier; the title remains display state and never becomes lifecycle authority or delivery evidence.

## Private Worktree Work

Implementation, correction, review, and focused local tests on a task-owned private branch and worktree do not require a project-file claim when they cannot mutate shared repository state or a named shared resource.

Acquire a claim before mutating shared state, including:

- files on main during direct integration
- the file-backed backlog on main
- generated output or another shared output location
- shared installations, ports, browsers, databases, or test resources that cannot safely run concurrently

Keep every shared claim limited to the exact files and named resources required for that operation. Isolation never authorizes modification of another task's owned shared surface.

## Direct Delivery Without A Pull Request

The work item's Dev Orchestrator owns integration and completion.

1. Finish implementation and independent review on the task branch.
2. Acquire one integration claim covering every path on main that the integration may modify, the target integration resource, and the exact shared test resources needed for focused verification.
3. Under that ownership, refresh current main and create a fresh reconciliation branch from that exact commit. Designate this fresh branch as the task integration and cleanup branch. Record the prior candidate branch, accepted source commit, and path set as source provenance before applying content.
4. Apply only the accepted file content or explicitly selected in-scope commits to the fresh current-main branch. Preserve required current-main and accepted contracts, regenerate supported outputs, and review the reconciled diff when semantic reconciliation is required.
5. Record source commit identifiers and accepted paths in the integration commit and work item. Do not import cumulative branch ancestry merely to preserve provenance. Use a full-history merge only when the complete history is intentional, reviewed, and in scope.
6. Integrate the bounded reconciliation commit into main.
7. Run the smallest project-native tests that cover the changed behavior and credible regression risk.
8. Record the main commit and test results in the work item, then release the integration claim from clean main.
9. Acquire a separate short claim for exactly the active work-item path and its completed destination.
10. Record completion evidence, set Status to Completed, move the item to the applicable completed-backlog folder, commit, and release the work-item claim.
11. Notify the parent with the main commit, test evidence, integration and work-item release events, branch, worktree, and cleanup eligibility.
12. The parent verifies that the fresh task integration branch is fully merged, removes its clean worktree, safely deletes that merged branch, prunes worktree metadata, sets the task title to Done — item, and archives the task when supported. A prior candidate branch used only as a non-ancestral content source is not the task cleanup branch; preserve or remove it separately according to repository policy after confirming the durable source mapping and absence of unique unintegrated work.
13. The parent immediately recounts file-backed Running items and dispatches eligible Ready work until ten are Running or no eligible work remains.

Keep administrative coordination-registry cleanup, Git integration, and terminal backlog completion as three distinct operations. Each operation has its own authority, evidence, and outcome; none can manufacture or replace another.

Do not leave a reviewed commit for a separate integration task. The Dev Orchestrator performs this sequence because it knows the accepted commit, affected main paths, and required focused tests.

## Pull-Request Delivery

When the selected workflow uses a pull request, the authorized reviewer or merge owner merges it. The implementation task does not acquire a duplicate main integration claim.

After merge evidence is available, the Dev Orchestrator runs or confirms the required focused verification, performs the separate work-item completion transaction, and notifies the parent for clean worktree, merged-branch, and task cleanup.

## Claim Retry Window

When an integration or work-item claim is unavailable, the Dev Orchestrator records the wait in the work item and owns this bounded retry schedule:

1. Attempt immediately.
2. Retry at five, ten, fifteen, twenty, twenty-five, and thirty minutes.
3. Before each retry, inspect the blocking claim and update the work item with the outcome and next attempt.
4. Stop retrying as soon as the claim succeeds.

This is one initial attempt plus no more than six retries. Do not create a waiting task, transfer the wait through a task chain, poll more frequently, or ask the user to approve ordinary Git or shell commands already covered by the work item.

At thirty minutes, Dev Backlog Coordinator investigates instead of allowing another passive wait. Identify the blocking owner, verify whether its claim is active or stale, and choose a safe remedy: request prompt release, narrow or split an unnecessarily broad claim, complete the blocking integration first, or route a genuine technical or user-decision blocker. Never release or override a claim whose owner has uncommitted or otherwise unpreserved work.

An evidence-backed administrative reset is available only for an inactive coordination-registry entry. Before reset, inspect the task and logs, matching processes, claimed worktrees, Git cleanliness and preserved commits, every claimed shared resource, other registry entries, and journal evidence. Retain a readable snapshot or journal reference. Reset only registry state after proving the owner inactive, all work completed or preserved, all resources stopped or handed off, and no active protection affected. A live owner, dirty unpreserved worktree, resource in use, or unclear evidence blocks reset.

Perform the reset only through a host-supported targeted atomic operation that names the exact entry, locks the coordination registry, revalidates those safeguards at mutation time, removes no peer entry, and journals the administrative outcome. The bundled portable claim command has no reset operation. If a supported atomic operation is unavailable, stop and route the reset instead of editing the registry file manually.

Treat inactive-entry or ancestry-only release-validation failures as coordination diagnostics. They do not automatically invalidate correct integrated bytes, independent review, focused verification, or durable completion evidence. Reconcile each evidence owner separately and never invent a successful release.

If the wait remains unresolved after investigation, record the precise open issue and move the item to the truthful Blocked or User Action Required state so it no longer consumes a Running slot. Dispatch a replacement Ready item immediately when available.

## Tiered Verification

Per-item verification is proportional to changed behavior and risk:

- run changed-module and directly related regression tests first
- add generated-output freshness, shared-resource, or integration tests only when the changed surfaces require them
- expand after a focused failure or evidence-backed cross-cutting risk
- do not run the complete agent catalog for an individual work item

Run the complete accepted agent catalog once against the final integrated campaign state after every accepted work-item fix is on main. Retain the final per-suite and global reports and disposition every failure.

## Long-Running Task Control

Treat a heartbeat as ownership evidence only. It does not prove useful progress, justify the current command, or make an expensive phase healthy.

When a command or phase is expected to take more than five minutes, the Dev Orchestrator exposes before starting it:

- the exact currently active unit and any later units that have not started
- the expected duration or best evidence-based estimate
- a hard stop condition and the retained evidence path
- the distinct acceptance criterion that requires the expensive operation

This is non-blocking operational telemetry in the task update, not a new backlog transaction or parent approval gate. Persist it in the work item at the next already-authorized material phase transition; do not acquire a backlog claim solely to record timing. The task may start without waiting for parent acknowledgement.

The parent observes long-running work at phase start, first failure, timeout, and completion rather than waiting for the fifteen-minute periodic review. This observation must not serialize healthy work. Inspect the actual process, elapsed time, latest evidence-bearing output, and remaining work. Status messages must distinguish one active serial case from selected or queued cases and must not describe queued work as running.

After an expensive failure, classify its failure signature before repeating anything. Reuse retained output, add the smallest offline replay or deterministic regression that reproduces the boundary, and make that focused check pass before another equivalent live or broad run. Run one cheapest representative first. Start a second expensive representative only when it covers a distinct acceptance criterion that retained evidence and deterministic checks cannot prove.

If the active unit reaches its hard stop, repeats the same failure signature, or stops producing evidence-bearing progress within its declared bound, stop that exact unit, preserve or commit owned work, stop or hand off every claimed resource, and prove the applicable worktree clean before releasing its shared claim. If safe release is not yet possible, retain and heartbeat the claim or hand it off explicitly rather than releasing unsafely. Return to focused correction only after truthful claim disposition. Do not let later serial cases start automatically after a shared-boundary failure. Two unproductive attempts or fifteen minutes beyond the declared phase estimate require immediate parent investigation and a revised plan rather than another retry.

## Fifteen-Minute Parent Review

Every fifteen minutes while queue work remains, Dev Backlog Coordinator reviews:

- Running count and vacancies against the target of ten
- work items by phase and age of the current phase
- integration and completion waits, especially every wait at or beyond thirty minutes
- active claims, their exact scopes, owners, and heartbeat freshness
- accepted commits awaiting integration
- completed integrations awaiting work-item closeout
- task anomalies, duplicates, stopped tasks, and missing canonical identifiers
- interval delivery counts: accepted commits, reviews, verifier gates, integrations, terminal transitions, and completed items
- average productively active and blocked task counts using the available interval samples

Make a scheduling or recovery adjustment during the same review whenever delivery worsens, vacancies remain, or a wait exceeds its limit. The work items hold all durable follow-up facts; the review must not create a second registry.

## Post-Facto Efficiency Audit

These audits improve the next equivalent operation. They are not pre-dispatch, claim-acquisition, review, verification, or integration gates.

After evidence shows that a claim was broad enough to delay other work:

1. Record the actual contention and exclusive work.
2. Identify three concrete scope reductions.
3. Implement the best safe reduction for the next or resumed equivalent operation.

After evidence shows that a broad suite or workflow performed substantial mostly unrelated work:

1. Record the broad command, cost, and evidence actually required.
2. Identify three targeted alternatives, including a focused selector and, when useful, a new script, test surface, or fixture validator.
3. Implement the best alternative before repeating that broad work.

Do not retroactively invalidate valid evidence or weaken the final campaign-wide catalog gate.

## User Decisions And Terminal State

A user answer resolves a decision gate once; it does not prove delivery. Record the exact answer and provenance in the work item and never ask it again. Route approved work to Ready, deferred work to Holding, and declined work to the applicable terminal disposition.

Completed requires integrated delivery, required independent review, focused verification, released integration and work-item claims, and committed terminal backlog evidence. The Dev Orchestrator supplies a clean worktree and a fully merged fresh task integration branch as cleanup eligibility. When content came from an older candidate branch without importing its ancestry, the durable mapping proves source provenance but does not make that older branch the task cleanup branch. Preserve or remove the source branch separately according to repository policy after confirming that it contains no unique unintegrated work. An idle, stopped, titled, or archived Codex task proves none of those facts.

Archive a terminal task only after the work-item disposition is committed, all claims are released, the worktree is removed or deliberately preserved, the merged branch is safely deleted when eligible, and no unresolved notification remains. If archival does not persist, record the tool limitation in the work item and do not report success.
