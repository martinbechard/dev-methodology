---
name: dev-backlog-watchdog-suite-contract
description: Share the read-only Dev Backlog Watchdog evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Backlog Watchdog Suite Contract

During declared backlog-blockage recovery, require the Watchdog to apply only the Watchdog Behavior and exit conditions from resolve-backlog-blockage. It must retain unchanged active recovery without repeating an alert, emit one recovery-ready alert when every exit condition passes, and never load a dispatch-mode skill or change secondary-thread dispatch.

Evaluate the dedicated Watchdog rather than the parent Coordinator, per-item Dev Orchestrator, or provider manager. Require the target to identify itself as Dev Backlog Watchdog, apply coordinate-work-items for read-only criteria, and remain outside Starting-plus-Running delivery capacity. When coordinate-codex-tasks is active, require the target to render its canonical standing and heartbeat prompt templates byte-identically for the Codex Watchdog task.

Require strict read-only evidence. The Watchdog may read the effective provider inventory, runtime execution state, latest productive evidence, estimate and hard-stop boundaries, and recorded Stalled or Blocked exit conditions. When coordinate-codex-tasks is active, it may also read canonical Thread, root Agent Task, title, follow-up, and archival state. It never mutates Work-item content, lifecycle state, tasks, claims, Git, branches, worktrees, resources, delivery evidence, or cleanup state. It does not dispatch agents, reserve capacity, recover work, run delivery, choose a lifecycle disposition, or create another inventory.

For a healthy cycle, require one concise no-action cycle result and no parent alert. Silence and a single delayed observation are not stall evidence. When coordinate-codex-tasks is active, title age is also not stall evidence. For a suspected stall, require the provider identity, exact source-backed evidence, why parent attention is required, and the smallest recommended Coordinator investigation action. The preventing cause remains unknown and the Watchdog must not select Stalled.

For a satisfied Stalled or Blocked exit condition, require one actionable alert that identifies the provider or provider-none execution, the exact exit evidence, and the smallest Coordinator validation action. The Coordinator alone chooses Running for the same resumed owner, Ready after ownership ends, Blocked after the exact known cause, blocker owner, unblock condition, and Coordinator-owned action are established, User Action Required after one exact user-owned action, question, and unattended-work boundary are established, or a terminal state with matching evidence. The authorized Coordinator directly applies any selected-provider mutation through the effective Persistence manager after that decision.

Run the suite-owned simulator tests before semantic judgment. Reject any alert without actionable evidence, lifecycle mutation, capacity change, dispatch, task recovery, expensive verification, live-model evaluation, provider fallback, invented state, or completion claim.
