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

Do not configure the current mcp-agent-ops provider as the claim helper yet. It has not been verified to support claim deadlines or claim_extend_deadline. It also lacks verified parity evidence for journal maintenance and contention reporting.

No MCP implementation of this work-item lifecycle contract is currently available. The operation schemas below define the required interface for a future provider; they are not evidence that the current provider implements it.

## Helper Setup

Project Configurator must verify every operation and result field in this skill before selecting an MCP server. After selection, use only that server for claim operations.

If a required tool is missing or the server cannot start, ask Project Configurator to configure a working claim helper.

If a tool returns result.outcome, the helper ran. Follow agent-claim for that outcome.

## Tool Results

Each completed tool call returns exit_code and result. Read result.outcome before deciding what to do next.

A nonzero exit_code can still contain a valid claim outcome. Follow agent-claim for that outcome. Do not repeat the operation through another claim helper.

Pass the absolute project-root path in repository for every operation below.

## Read Claim Status

Call claim_status with repository.

Each live work-item claim includes work_item_id and activity together with claim_id, incarnation_id, agent, root_task_id, claimed_at, heartbeat, acquisition_outcome, and the existing ownership fields.

```json
{"repository": "/workspace/project"}
```

## Acquire Claim

Call claim_acquire with repository, claim_id, agent, task, root_task_id, and one scope selected through agent-claim.

Use work_item_id with activity, or use files, project_files, or resources for the scope. Work-item activity must be exactly work or update and cannot be combined with path or resource scope. Project_files also requires scope_reason. A resource request accepts one resources value plus resource_class, resource_id, expected_duration_seconds, and requested_hard_stop_duration_seconds. The result includes the configured limits and calculated deadlines.

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

Another live claim for the same Work Item ID returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED regardless of activity. Distinct Work Item IDs coexist.

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

## Extend Claim

Call claim_extend with repository, claim_id, and the net-new scope. A resource extension also requires resource_class, resource_id, expected_duration_seconds, and requested_hard_stop_duration_seconds.

A work-item claim cannot be extended with path or resource scope. Acquire each operational path or resource claim separately when its own Claim Event occurs.

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

Call claim_extend_deadline with repository, claim_id, requested_hard_stop_duration_seconds, and extension_evidence.

```json
{
  "repository": "/workspace/project",
  "claim_id": "browser-check-123",
  "requested_hard_stop_duration_seconds": 2400,
  "extension_evidence": "one final accessibility case remains"
}
```

## Heartbeat Claim

Call claim_heartbeat with repository and claim_id.

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

## Release Claim

Call claim_release with repository and claim_id.

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

A work-item claim requires disposition with exactly done, blocked, or handoff. Blocked may include one bounded opaque blocker_reference; when present, it must be canonical, non-empty, single-line, and at most 200 characters. blocker_reference is prohibited for done and handoff.

```json
{
  "repository": "/workspace/project",
  "claim_id": "work-item-123-work",
  "disposition": "handoff"
}
```

```json
{
  "repository": "/workspace/project",
  "claim_id": "work-item-123-update",
  "disposition": "blocked",
  "blocker_reference": "dependency-456"
}
```

The result and RELEASED journal event preserve work_item_id, activity, disposition, blocker_reference, claim and incarnation identity, owner, root task, timestamps, and outcome. Invalid or missing work-item combinations return INVALID_WORK_ITEM_RELEASE without changing the registry. Non-work-item claims retain the legacy release call without disposition.

Release removes only the exact named live claim under the configured helper's registry lock and appends RELEASED journal evidence. Release does not inspect Git state, file contents, delivery evidence, or completion state.

## Maintain Claim Journal

Call claim_maintain_journal with repository. Hot_days defaults to 2.

```json
{"repository": "/workspace/project", "hot_days": 2}
```

## Report Claim Contention

Call claim_report with repository. Since defaults to 2d.

```json
{"repository": "/workspace/project", "since": "2d"}
```

The result retains the existing report schema and adds work_items with schema_version 1. That section groups deterministic activity segments by work_item_id. Each segment reports acquired and released times, activity, disposition, owner, duration, and open and live state. Diagnostics identify missing release, release without acquisition, contradictory events, and historical non-work-item events without inventing Work Item IDs.

## Work-Item Result Contract

No live MCP execution is claimed here. A future verified MCP provider must return the same structured work-item outcomes and evidence as the command helper, including unchanged-registry semantics for validation failures.

```json
{
  "acquire_success": {
    "outcome": "SHARED_CHECKOUT_ACQUIRED",
    "claim_fields": ["work_item_id", "activity", "acquisition_outcome"]
  },
  "same_id_conflict": {
    "outcome": "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
    "evidence": ["conflicting_claim_ids", "overlaps.scope_kind=work_item"]
  },
  "status_live": {
    "outcome": "STATUS",
    "claim_fields": ["work_item_id", "activity", "claim_id", "incarnation_id", "agent", "root_task_id", "claimed_at", "heartbeat", "acquisition_outcome"]
  },
  "release_blocked_without_reference": {
    "outcome": "RELEASED",
    "disposition": "blocked",
    "blocker_reference": null
  },
  "release_blocked_with_reference": {
    "outcome": "RELEASED",
    "disposition": "blocked",
    "blocker_reference": "dependency-456"
  },
  "release_done": {"outcome": "RELEASED", "disposition": "done"},
  "release_handoff": {"outcome": "RELEASED", "disposition": "handoff"},
  "invalid_acquire": {
    "outcome": "INVALID_WORK_ITEM_SCOPE",
    "registry_unchanged": true
  },
  "invalid_release": {
    "outcome": "INVALID_WORK_ITEM_RELEASE",
    "registry_unchanged": true
  },
  "report": {
    "schema_version": 2,
    "work_items_schema_version": 1,
    "diagnostics": ["missing_release_event_ids", "release_without_acquisition_event_ids", "contradictory_event_ids", "historical_non_work_item_event_ids"]
  }
}
```

## Uncertain Tool Outcome

Apply the uncertain-outcome policy from agent-claim if the connection fails after sending a mutating tool call. Do not repeat it.

Reconnect to the same server. Run Read Claim Status by calling claim_status for the same repository, then continue from the reported claim state.

If the server cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
