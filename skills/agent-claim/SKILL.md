---
name: agent-claim
description: Use when multiple agents may edit the same repository, share runtime resources, touch overlapping files, run builds or tests concurrently, or need claim coordination before modifying files.
metadata:
  category: development-practice
---

# Agent Claim

Use this skill before editing files or taking exclusive runtime resources in a repository where more than one agent may be active.

## Goal

Claims make shared work explicit. They prevent two agents from editing the same files, running incompatible verification, or mutating shared generated data at the same time.

## Claim File

Default location:

```text
.agents/agent-claims.json
```

If a repository documents another path in AGENTS.md, README, a runtime-specific instruction file, or a local skill, use that path instead.

Expected shape:

```json
{
  "claims": [
    {
      "agent": "agent-name-or-id",
      "task": "Short task description",
      "files": ["path/from/repo/root.ts"],
      "resources": ["build:production"],
      "claimed_at": "2026-06-10T20:30:00Z",
      "heartbeat": "2026-06-10T20:35:00Z",
      "worktree": "/absolute/path/to/worktree-or-repo"
    }
  ]
}
```

## When To Claim

Claim before:

- Editing, moving, deleting, formatting, staging, or generating files.
- Running commands that monopolize shared state such as production builds, browser-test servers, dev server ports, browser profiles, database resets, seed data, generated output refreshes, or long-running test servers.
- Inspecting is safe without a claim, unless the inspection command mutates caches, generated files, databases, browser state, or server state.

Use the smallest useful claim. Claim exact files when known. If discovery is still in progress, claim the narrow directory or resource, then narrow it once the target files are known.

## Claim Protocol

1. Read the repository coordination instructions.
2. Read the current claim file. If it is missing, create it with an empty claims array when the first claim is needed.
3. Check for active claims that overlap your files, directories, or resources.
4. If another active agent owns the target, do not edit it. Wait, switch tasks, or report blocked status.
5. Add your claim before editing or starting the exclusive command.
6. Keep the heartbeat current while working.
7. Expand the claim before touching additional files or resources.
8. Release your claim as soon as the edit, command, merge, or handoff is complete.

## Runtime Resources

Resource names should be stable and descriptive. Common patterns:

```text
port:3000
port:5173
build:production
build:next
test:unit
test:e2e
browser-test:primary
browser-test:server
database:seed
database:e2e
generated:reports
generated:codegen
browser:chrome-profile
```

Prefer repository-specific names when the project already defines them.

## Stale Claims

A claim may be stale when its heartbeat is old and no matching status file or process is alive. Do not delete another agent's claim just because it is inconvenient.

Before removing a stale claim:

1. Check status files, logs, running processes, and recent git activity when available.
2. Treat long-running builds or tests as active if the process still exists.
3. Preserve evidence in your notes or status before cleanup.
4. Remove only the stale entry, not unrelated active claims.

If the evidence is unclear, leave the claim in place and report the exact blocker.

## File Edits

- Never edit a file or directory claimed by another active agent.
- Never stage or commit another agent's claimed files unless you are explicitly performing the merge or integration role.
- If you discover your task needs a claimed file, stop before editing and update your status.
- If you accidentally touched an unclaimed or conflicting file, stop, explain the file, and either claim it if safe or revert only your own accidental change.

## Completion

A clean finish includes:

- Related verification has run or the blocker is documented.
- Your claim entry is removed.
- Any long-running resource is stopped or explicitly handed off.
- The final response names active blockers if claims prevented completion.
