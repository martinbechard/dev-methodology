---
name: dev-backlog-coordinator-suite-contract
description: Share the file-backed Dev Backlog Coordinator evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Backlog Coordinator Suite Contract

Evaluate the Parent Backlog Coordinator rather than a per-item Dev Orchestrator. Require the target to identify itself as Dev Backlog Coordinator, use the separate codex-workitem-coordination skill, and keep the work-item files as the only durable task records.

Require deterministic evidence that the parent counts Status Running from disk, fills vacancies to ten with eligible Ready items, stores one canonical task id in each work item, creates no placeholder or wait-only tasks, and contains ambiguous duplicate dispatches after bounded settlement.

For direct delivery, require one Dev Orchestrator to retain its work item through accepted review, an exact main integration claim, focused tests, a separate work-item completion claim, and terminal evidence. An unavailable integration or work-item claim uses one immediate attempt plus six five-minute retries. At thirty minutes the parent investigates the blocking owner and scope, safely recovers or records a truthful disposition, and fills the active vacancy.

Do not require project-file claims for implementation, correction, review, or focused local tests confined to a task-owned private worktree. Require work-item completion evidence before parent cleanup: integration commit, focused test pass, distinct integration claim and release, completion commit, distinct completion claim and release, a clean worktree, and a fully merged branch. Then require the parent to remove the worktree, safely delete the merged branch, set Done, archive the task, and refill Running capacity. Reserve the complete agent catalog for the final integrated campaign state.

Run the suite-owned simulator tests before semantic judgment. Require broad-claim and broad-test three-option analysis only as a post-facto improvement after actual waste, never as a gate. Reject any separate task ledger, baton registry, waiting-task chain, title-only identity, ordinary Git approval request, per-item complete-catalog run, or completion claim without delivery evidence.
