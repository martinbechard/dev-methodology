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
- The claim registry records current shared mutation authority.
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
2. Acquire one integration claim covering every path on main that the integration may modify and the exact shared test resources needed for focused verification.
3. Integrate the accepted commit into main.
4. Run the smallest project-native tests that cover the changed behavior and credible regression risk.
5. Record the main commit and test results in the work item, then release the integration claim from clean main.
6. Acquire a separate short claim for exactly the active work-item path and its completed destination.
7. Record completion evidence, set Status to Completed, move the item to the applicable completed-backlog folder, commit, and release the work-item claim.
8. Notify the parent with the main commit, test evidence, integration and work-item release events, branch, worktree, and cleanup eligibility.
9. The parent verifies that the branch is fully merged, removes the clean worktree, deletes the merged branch with a safe non-forcing delete, prunes worktree metadata, sets the task title to Done — item, and archives the task when supported.
10. The parent immediately recounts file-backed Running items and dispatches eligible Ready work until ten are Running or no eligible work remains.

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

If the wait remains unresolved after investigation, record the precise open issue and move the item to the truthful Blocked or User Action Required state so it no longer consumes a Running slot. Dispatch a replacement Ready item immediately when available.

## Tiered Verification

Per-item verification is proportional to changed behavior and risk:

- run changed-module and directly related regression tests first
- add generated-output freshness, shared-resource, or integration tests only when the changed surfaces require them
- expand after a focused failure or evidence-backed cross-cutting risk
- do not run the complete agent catalog for an individual work item

Run the complete accepted agent catalog once against the final integrated campaign state after every accepted work-item fix is on main. Retain the final per-suite and global reports and disposition every failure.

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

Completed requires integrated delivery, required independent review, focused verification, released integration and work-item claims, and committed terminal backlog evidence. The Dev Orchestrator supplies a clean worktree and a fully merged branch as cleanup eligibility; the parent then removes the worktree and branch before setting Done or archiving the task. An idle, stopped, titled, or archived Codex task proves none of those facts.

Archive a terminal task only after the work-item disposition is committed, all claims are released, the worktree is removed or deliberately preserved, the merged branch is safely deleted when eligible, and no unresolved notification remains. If archival does not persist, record the tool limitation in the work item and do not report success.
