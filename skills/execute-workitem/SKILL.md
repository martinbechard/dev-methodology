---
name: execute-workitem
description: Execute a normalized interactive, file-backed, or issue-backed work item through the project-selected simple-workitem or feature-branch-workitem delivery process. Use when Dev Coder is asked to implement, resume, correct, or deliver a scoped work item and must follow the configured local-commit or pull-request lifecycle.
metadata:
  category: development-practice
---

# Execute Work Item

Complete one bounded work item through the delivery process selected by applicable project guidance or the request.

## Inputs

Resolve these inputs before repository mutation:

- Work-item identifier or an explicit interactive request.
- Source reference when the item comes from a backlog.
- Title, requirements, acceptance criteria, dependencies, and verification expectations.
- Delivery process: simple-workitem or feature-branch-workitem.

An explicit request for local-only delivery or pull-request delivery selects that process for the current task. When neither project guidance nor the request selects a process, ask the user before creating a branch or modifying files. Do not infer the process from a remote, hosting account, issue, or pull-request template.

## Work-Item Contract

Normalize every input into one work item containing:

- identifier
- source and source reference
- title
- requirements
- acceptance criteria
- dependencies
- verification expectations

Mark unknown requirements or acceptance criteria as open questions. Do not invent missing behavior from a terse issue title or filename.

## Process Selection

- For simple-workitem, read and apply [the simple work-item process](references/simple-workitem.md).
- For feature-branch-workitem, read and apply [the feature-branch work-item process](references/feature-branch-workitem.md).
- For an unknown process identifier, stop and ask for a supported selection.

Read only the selected process. Keep backlog persistence separate from delivery: report lifecycle evidence to the configured backlog owner rather than embedding file or issue operations in this skill.

## Resource Coordination

Apply the project-wide resource_coordination selection independently from the delivery process:

- When agent-claim is selected, load that enabled implementation and its configured transport before protected repository or runtime mutation. Preserve its acquire, isolation, heartbeat, handoff, release, and evidence requirements through the selected process.
- When none is selected, do not discover or load a coordination implementation or transport, inspect coordination state, invoke coordination operations, create a coordination-only branch, or report coordination evidence. Perform no coordination operations or evidence collection while still preserving the authorized scope, coherent commits, required verification, clean worktree, delivery record, and backlog handoff.

## Common Boundaries

- Follow the resource-coordination branch above before repository mutation and preserve unrelated work.
- Keep one work item within one coherent delivery scope.
- Return implementation findings to the work-item owner instead of silently expanding the item.
- Apply review corrections to the same work item and delivery branch unless the accepted correction changes the independent review boundary.
- Do not mark a backlog item complete merely because a commit or pull request exists.
- Report READY only after the selected process reaches its required terminal evidence.
- Report AWAITING_REVIEW only for a published feature-branch work item waiting on external review.
- Report BLOCKED when authority, required inputs, dependencies, an enabled coordination conflict, verification, or delivery capability prevents safe progress.

## Result

Return:

- work-item identifier and source reference
- selected delivery process
- changed scope and commits
- verification evidence and omissions
- local branch or pull-request reference required by the selected process
- READY, AWAITING_REVIEW, or BLOCKED status with its deciding evidence
- backlog lifecycle update that the configured backlog owner must record
