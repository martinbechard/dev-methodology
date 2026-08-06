---
name: coordinate-codex-tasks
description: Map portable work-item coordination to Codex task creation, resumption, identity, titles, follow-up, reconciliation, watchdog operation, and archival. Use only when coordinated work runs through Codex tasks.
metadata:
  category: development-practice
---

# Coordinate Codex Tasks

Codex task control maps one portable work-item execution to one canonical Codex task and its retained user-visible context. Apply coordinate-work-items together with this skill. This skill does not create provider lifecycle authority, delivery authority, or resource ownership.

## Codex Capability Check

Create a coordinated Codex task only in an environment where its root Agent can perform the ordinary operations authorized by the work item. The dispatch prompt states that ordinary repository writes, Git operations, focused tests, process inspection, and selected resource-coordination commands are already authorized. The Agent must not open or wait on a user approval prompt for those operations.

When work depends on a special runtime capability, test it through the same nested execution path used by the real workload. Direct parent execution is not sufficient evidence for a child Agent. Treat prior capability evidence as stale after agent-definition generation, metadata generation, adapter installation, MCP refresh, Codex configuration changes, permission-profile changes, application updates, or host restart.

The capability pilot proves the effective Agent profile and ordinary operations. Inspect the child Agent's effective approval, sandbox, and permission profile. Create a harmless Git commit in a disposable worktree. Invoke each selected special capability through the same nested helper as the workload. If the requested configuration and effective child runtime differ, stop equivalent dispatch, record both profiles, archive the failed pilot, correct the environment, and rerun one pilot.

If an ordinary required operation fails because the Agent lacks a capability, the Agent stops, preserves work, and reports the exact failed operation to the parent. It must not request escalation from the user. The parent re-homes the task or replaces its root Agent, reconciles the canonical identity, and supplies current runtime evidence to coordinate-work-items.

## Codex Task Creation And Resumption

The parent Dev Backlog Coordinator may create at most one root Dev Orchestrator task after coordinate-work-items records the Starting reservation and permits runtime dispatch. Use Codex task creation for that bounded root assignment. Record the returned task identifier and retained user-visible context as runtime evidence; neither result changes provider lifecycle.

When an existing canonical task was preserved through User Action Required, Stalled, Blocked, or another resumable state, resume that task. Do not create a replacement merely because the task is idle. The portable lifecycle owner first records the required Starting handoff. The task then accepts Running through the portable contract.

Do not create a task merely to wait for approval, a dependency, a reviewer, a shared resource, or a delivery window. Do not retry task creation after an error, timeout, disconnect, or ambiguous response. Reconcile the result first.

## Canonical Codex Task Identity

A Codex task is the canonical runtime execution identity for one root Dev Orchestrator assignment. A conversation is the retained user-visible context for that assignment. The task identifier and conversation identifier are distinct, even when the runtime exposes one combined surface.

Record these fields when the runtime supplies them:

```markdown
Codex Task ID: [opaque task identifier]
Conversation ID: [opaque retained-context identifier]
Root Role: Dev Orchestrator
Parent Task ID: [opaque coordinator task identifier]
```

Do not infer either identity from the conversation title, prompt text, branch, worktree, or provider record path. Preserve the same canonical task and conversation through corrections, review, verification, delivery, and resumable lifecycle pauses. A replacement requires explicit duplicate reconciliation and a recorded identity handoff.

## Conversation Title Contract

The canonical conversation keeps one stable identity. Its conversation title is display state, never lifecycle authority, active-execution evidence, or delivery evidence. Use the format phase label — short work-item title.

Use this lifecycle and phase mapping:

- Ready: Ready — short work-item title.
- Starting: Starting — short work-item title.
- Running: Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —, or Waiting for Help — short work-item title.
- User Action Required: Waiting for User — short work-item title.
- Stalled: Stalled — short work-item title.
- Blocked: Blocked — short work-item title.
- Holding: Holding — short work-item title.
- Awaiting Review: Awaiting Review — short work-item title.
- Completed: Done — short work-item title.
- Failed: Failed — short work-item title.
- Abandoned: Abandoned — short work-item title.

The owning Coordinator or Orchestrator is accountable after every successful lifecycle transition. When Codex grants rename authority, rename the canonical conversation directly. Otherwise send the exact required title to its owner and verify the handoff before reporting title coordination complete. A failed title update does not roll back a durable lifecycle transition. Preserve the provider mutation and report title coordination incomplete.

Apply the title contract when the task is created, after each successful lifecycle transition, and at each material Running phase change. Never use raw prompt text, markup, error output, identifiers, or a generic title.

## Codex Runtime Reconciliation

Treat a task-creation error, timeout, disconnect, or ambiguous response as an ambiguous runtime mutation. Reconcile active and archived Codex tasks using all available evidence:

- source parent task identifier
- provider selector and opaque Work Item ID when present
- normalized objective
- creation time
- task and conversation state

If exactly one match exists, adopt it as the canonical task. If multiple matches exist, preserve one canonical task, stop every duplicate before mutation, and verify that no unique work is lost. Do not infer, inherit, carry forward, or persist an archival pause from another conversation, task, or earlier campaign direction. A launch failure leaves the portable provider record in Starting for Watchdog and Coordinator recovery.

Map Codex task states into portable evidence without inventing lifecycle. A running Codex process can support active-root-execution evidence. A running child can support delegated-work evidence. An idle, completed, failed, interrupted, or missing task requires portable reconciliation and cannot choose a provider transition by itself.

## Task Follow-Up

When the canonical task is idle but remains the selected resumable execution, send one follow-up to the same canonical task. Use follow-up for a bounded next action, resumption request, or Watchdog heartbeat. Never use follow-up as lifecycle authority, capacity evidence, provider mutation, or proof of progress.

Do not create a replacement task merely because the task is idle, slow, or has not produced a recent message. After a follow-up, preserve the original task identity and reconcile the returned runtime state. If the task cannot resume, report that evidence to the portable lifecycle owner before any replacement decision.

## Watchdog Task Mapping

When coordinate-work-items permits a dedicated read-only Watchdog, create one Codex task under the Dev Backlog Watchdog Role. The standing prompt supplies the parent task identifier, repository root, selected provider context, and applicable resource-coordination context. It instructs the Watchdog to apply coordinate-work-items for read-only criteria and this skill only for Codex runtime identity, title, follow-up, and archival observations.

### Canonical Standing Prompt Template

```text
Act as the dedicated read-only Dev Methodology backlog watchdog for parent task {parent_task_id} in {repository_root}.

Apply skills/coordinate-work-items/SKILL.md for portable active-execution, capacity, lifecycle-reconciliation, Blocked, Stalled, and read-only Watchdog criteria. Apply skills/coordinate-codex-tasks/SKILL.md only for Codex task identity, conversation-title observation, follow-up, and archival mapping. On each cycle, read the selected provider inventory, Git state, configured resource-coordination state when enabled, and Codex runtime state. Evaluate Starting reconciliation, Running Active Execution Evidence, phase age, estimates, hard stops, evidence progress, Blocked and Stalled exit conditions, accepted work stranded before Commit delivery, READY delivery awaiting provider closeout, every terminal Codex task in this Coordinator campaign, complete provider, claim, worktree, branch, notification, preservation, archival, and current scoped archive-pause evidence, and unsafe, stale, or broad shared ownership.

Remain strictly read-only. Do not mutate repository files, provider lifecycle, claims, tasks, branches, worktrees, or shared resources. Do not dispatch, integrate, clean up, archive, or run expensive or live verification. Notify parent task {parent_task_id} only when an actionable condition exists. Send exactly one aggregate alert containing every actionable anomaly, its exact evidence, and its smallest recommended Coordinator action. When healthy, record only one concise no-action cycle result here.
```

### Canonical Heartbeat Prompt Template

```text
Run one complete read-only Watchdog cycle now using this task's standing contract. Notify parent task {parent_task_id} only if an actionable condition exists; otherwise record one concise no-action cycle result here.
```

Substitute only the resolved parent task identifier and repository root. Supply provider and resource-coordination variation through resolved task context without rewriting either canonical prompt.

Use a follow-up on that same Watchdog task for each scheduled heartbeat. Do not create a new Watchdog task per cycle. The Watchdog reports actionable evidence to the parent task and otherwise retains one concise no-action result in its own task. It does not mutate tasks, provider records, claims, Git, branches, worktrees, or resources.

If the Watchdog task is unavailable, the parent performs the portable review directly. Do not create a second ledger or duplicate observer.

## Task Archival

Task archival is mandatory by default after code is merged and coordinate-work-items confirms terminal provider or task-local disposition, accepted delivery evidence, claim reconciliation, safe branch and worktree disposition, preservation acknowledgement, and no unresolved notification remains.

An archival pause is valid only when explicit current user direction names the exact Codex task, limits its scope to Codex task archival, records the exact direction and scope as evidence, and has a recorded acknowledgement. Do not infer, inherit, carry forward, or persist a campaign-wide pause from earlier conversation. A valid pause suppresses archival only for its named tasks. It never suppresses provider closeout, claim reconciliation, worktree cleanup, delivery-branch cleanup, source-branch cleanup, notification, or another terminal reconciliation action.

Before archival, verify the terminal conversation title and preserve the canonical task identity with the terminal handoff. If no valid current named-task pause exists, archive the task after every ordinary gate passes. If archival fails or the runtime does not support it, record the limitation and do not report archival success. An idle, stopped, titled, or archived Codex task proves none of those facts.

Task archival is a runtime cleanup mapping. It does not close a provider record, prove Commit delivery, release a claim, delete a worktree, or delete a branch.
