---
name: resource-claim-helper-mcp
description: Use a verified MCP provider for the Resource Claim Helper interface when complete parity is available.
metadata:
  category: development-practice
---

# Resource Claim Helper MCP

This Provider Skill realizes Resource Claim Helper through MCP tool calls. Apply resource-claim for policy and resource-claim-helper for the common operation, input, result, and uncertain-outcome contract.

This skill owns MCP tool mapping, protocol-specific result envelopes, connection recovery, and the provider availability boundary. It does not define claim policy or the shared helper contract.

## Current Availability

Do not configure the current mcp-agent-ops provider as the claim helper. Its exposed tool surface omits `claim_extend_deadline` and `claim_reset`, so it cannot realize the complete interface even though it exposes journal maintenance and contention reporting.

No MCP implementation of the complete Resource Claim Helper interface is currently available. The tool mappings below define the required provider contract for future verification. They do not prove that the current provider implements it.

## Helper Setup

Project Configurator must verify every operation, input, result field, and availability requirement before selecting an MCP server. After selection, use only that server for claim operations.

If a required tool is missing or the server cannot start, ask Project Configurator to configure a working claim helper.

## MCP Results

Each completed tool call returns exit_code and result. Read result.outcome before deciding what to do. A nonzero exit_code can still contain a valid claim outcome.

Pass the absolute project root in repository for every tool call.

## Read Claim Status

Map Read Claim Status to claim_status:

```json
{"repository": "/workspace/project"}
```

## Acquire Claim

Map Acquire Claim to claim_acquire with repository, claim_id, agent, task, root_task_id, and one common scope shape.

Work-item acquisition:

```json
{
  "repository": "/workspace/project",
  "claim_id": "work-item-123-work",
  "agent": "implementation-agent",
  "task": "work-item-123",
  "root_task_id": "work-item-123",
  "work_item_id": "provider-opaque-id-123",
  "activity": "work"
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

A file scope uses `files` and a tree scope uses `trees`. Broad path domains use `project_files`, `backlog`, or `all_files` plus `scope_reason`. A resource scope uses one `resources` value plus `resource_class`, `resource_id`, `expected_duration_seconds`, and `requested_hard_stop_duration_seconds`. Preserve `parent_claim_id`. Isolated-checkout creation uses `branch`, `base`, and `worktree_path`.

## Extend Claim

Map Extend Claim to claim_extend with `repository`, `claim_id`, and only the net-new path-domain or resource scope. Use the same path-domain and resource fields as Acquire Claim, excluding work-item and isolated-checkout inputs.

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

## Extend Claim Deadline

Map Extend Claim Deadline to claim_extend_deadline:

```json
{
  "repository": "/workspace/project",
  "claim_id": "browser-check-123",
  "requested_hard_stop_duration_seconds": 2400,
  "extension_evidence": "one final accessibility case remains"
}
```

## Heartbeat Claim

Map Heartbeat Claim to claim_heartbeat:

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

## Release Claim

Map Release Claim to claim_release. Supply disposition and blocker_reference only when the common interface and resource-claim require them.

A successful release returns canonical outcome `RELEASED`.

```json
{
  "repository": "/workspace/project",
  "claim_id": "work-item-123-work",
  "disposition": "handoff"
}
```

## Reset Claim Registry

Map Reset Claim Registry to claim_reset:

```json
{"repository": "/workspace/project"}
```

## Maintain Claim Journal

Map Maintain Claim Journal to claim_maintain_journal. hot_days defaults to 2.

```json
{"repository": "/workspace/project", "hot_days": 2}
```

## Report Claim Contention

Map Report Claim Contention to claim_report. `since` defaults to `2d`. A successful call returns canonical outcome `REPORT` with `window`, `event_count`, `metrics`, `work_items`, and `coverage_gaps`.

```json
{"repository": "/workspace/project", "since": "2d"}
```

## Reconcile an Uncertain Tool Call

If the MCP connection fails after sending a mutating tool call, the outcome is uncertain. Do not repeat the call. Reconnect to the same server, call claim_status for the same repository, and reconcile the reported claim state.

If the server cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
