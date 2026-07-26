---
name: agent-claim-mcp
description: Use the configured MCP claim helper.
metadata:
  category: development-practice
---

# Agent Claim MCP

Use this skill to call the MCP claim helper selected in PROJECT.yaml.

Follow agent-claim for all claim rules. This skill explains only how to call the configured MCP helper.

## Current Availability

Do not configure the current mcp-agent-ops provider as the claim helper yet. It has not been verified to support claim deadlines or claim_extend_deadline.

## Helper Setup

Project Configurator must verify every operation and result field in this skill before selecting an MCP server. After selection, use only that server for claim operations.

If a required tool is missing or the server cannot start, ask Project Configurator to configure a working claim helper.

If a tool returns result.outcome, the helper ran. Follow agent-claim for that outcome.

## MCP Operations

Use exactly the tool matching the intended operation:

| Operation | Tool | Required arguments |
|---|---|---|
| Read live ownership | claim_status | repository |
| Acquire ownership | claim_acquire | repository, claim_id, agent, task, root_task_id, and one supported scope |
| Extend scope | claim_extend | repository, claim_id, and net-new scope |
| Extend a deadline | claim_extend_deadline | repository, claim_id, requested_hard_stop_duration_seconds, and extension_evidence |
| Refresh heartbeat | claim_heartbeat | repository, claim_id |
| Release ownership | claim_release | repository and claim_id |
| Maintain journal | claim_maintain_journal | repository; hot_days defaults to 2 |
| Report contention | claim_report | repository; since defaults to 2d |

Pass the absolute project-root path in repository.

Use files, project_files, or resources for the scope chosen from the Claim Events table.

Project_files also requires scope_reason.

A resource request accepts one resources value plus resource_class, resource_id, expected_duration_seconds, and requested_hard_stop_duration_seconds. The result includes the configured limits and calculated deadlines.

## Tool Results

Each completed tool call returns exit_code and result. Read result.outcome before deciding what to do next.

A nonzero exit_code can still contain a valid claim outcome. Follow agent-claim for that outcome. Do not repeat the operation through another claim helper.

## Tool Examples

Read live ownership:

```json
{"repository": "/workspace/project"}
```

File-scope acquisition:

```json
{
  "repository": "/workspace/project",
  "claim_id": "update-work-item-123",
  "agent": "backlog-steward",
  "task": "update-work-item-123",
  "root_task_id": "work-item-123",
  "files": ["backlog/feature-backlog/work-item-123.md"]
}
```

Project-files acquisition:

```json
{
  "repository": "/workspace/project",
  "claim_id": "task-123",
  "agent": "implementation-agent",
  "task": "task-123",
  "root_task_id": "task-123",
  "project_files": true,
  "scope_reason": "project implementation"
}
```

Resource acquisition:

```json
{
  "repository": "/workspace/project",
  "claim_id": "browser-check-123",
  "agent": "browser-operator",
  "task": "browser-check-123",
  "root_task_id": "task-123",
  "resources": ["browser-test:primary"],
  "resource_class": "browser-server",
  "resource_id": "browser-test:primary",
  "expected_duration_seconds": 900,
  "requested_hard_stop_duration_seconds": 1800
}
```

Resource-scope extension:

```json
{
  "repository": "/workspace/project",
  "claim_id": "task-123",
  "resources": ["port:3000"],
  "resource_class": "database-port",
  "resource_id": "port:3000",
  "expected_duration_seconds": 600,
  "requested_hard_stop_duration_seconds": 1200
}
```

Deadline extension:

```json
{
  "repository": "/workspace/project",
  "claim_id": "browser-check-123",
  "requested_hard_stop_duration_seconds": 2400,
  "extension_evidence": "one final accessibility case remains"
}
```

Heartbeat:

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

Release:

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

Release removes only the exact named live claim under the configured helper's registry lock and appends RELEASED journal evidence. Release does not inspect Git state, file contents, delivery evidence, or completion state.

```json
{"repository": "/workspace/project", "hot_days": 2}
```

Report:

```json
{"repository": "/workspace/project", "since": "2d"}
```

## Uncertain Tool Outcome

If the connection fails after sending a tool call that changes claim state, the operation may have completed. Do not repeat it.

Reconnect to the same server. Call claim_status for the same repository. Continue from the reported claim state.

If the server cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
