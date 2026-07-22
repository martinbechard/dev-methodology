---
name: agent-claim-mcp
description: Invoke the transport-neutral agent-claim contract through one setup-verified mcp-agent-ops tool surface without runtime probing or transport fallback.
metadata:
  category: development-practice
---

# Agent Claim MCP

Apply this adapter only when Project Configurator selected mcp in agent_claim_transport and verified the complete claim tool surface. Apply agent-claim for scope, ownership, state, recovery, heartbeat, release, and completion semantics.

## Deadline Parity Boundary

This adapter defines the MCP contract required for transport parity, but the live external mcp-agent-ops provider has not been verified to supply the deadline fields and claim_extend_deadline operation below. The bundle records this state as UNRESOLVED_EXTERNAL_PROVIDER. Project Configurator must not select MCP for agent-claim until setup evidence verifies the complete future surface and result schema. Do not claim current live MCP support, emulate the missing operation with another tool, or switch to command at runtime.

## Availability Boundary

Project Configurator verifies the configured server before rendering this adapter. Runtime agents invoke the named tools directly. Do not list tools to rediscover the transport, inspect another transport, execute a claim command, or infer availability from package versions.

If any required claim tool is absent, disconnected, or cannot initialize before dispatch, stop with CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration. Do not switch transports. A path, root, authorization, input-policy, schema, or other structured rejection is a valid tool result, not unavailability.

## MCP Operations

Use exactly the tool matching the intended operation:

| Operation | Tool | Required arguments |
|---|---|---|
| Read live ownership | claim_status | repository |
| Acquire ownership | claim_acquire | repository, claim_id, agent, task, root_task_id, and one supported scope |
| Extend scope | claim_extend | repository, claim_id, and net-new scope |
| Extend a deadline | claim_extend_deadline | repository, claim_id, requested_hard_stop_duration_seconds, and extension_evidence |
| Refresh heartbeat | claim_heartbeat | repository, claim_id |
| Release ownership | claim_release | repository, claim_id; no_change only for a truthful no-change release |
| Maintain journal | claim_maintain_journal | repository; hot_days defaults to 2 |
| Report contention | claim_report | repository; since defaults to 2d |

The repository and worktree_path arguments are absolute paths accepted by the configured server workspace roots. Files and trees are lists. The mutually exclusive broad selectors are project_files, backlog, and all_files. Project-files and all-files require scope_reason. Acquisition also accepts parent_claim_id, branch, base, allow_recovery, and the compatibility-only worktree_path and compat_file_directories inputs.

The required future parity contract permits at most one resource value per claim. A named-resource acquisition or scope extension must also send resource_class, resource_id, expected_duration_seconds, and requested_hard_stop_duration_seconds. The provider must resolve configured_maximum_duration_seconds and cleanup_grace_seconds from the project's exact class or resource-id override, validate expected <= requested <= maximum, and return expected_release_at, hard_stop_at, cleanup_grace_ends_at, and extension history. Callers never supply the configured maximum or cleanup grace. Status must report deadline_status read-only, heartbeat must not change the hard stop, and overdue state must never auto-release ownership.

## Dispatch Contract

Each completed tool call returns one structured wrapper with exit_code and result. Inspect result.outcome before taking the next action. Preserve result.schema_version, result.legacy_outcome when present, warnings, conflicts, claim data, and target data as coordination evidence.

Do not treat a nonzero exit_code as a protocol failure. CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, SHARED_CHECKOUT_RELEASE_REQUIRED, ISOLATED_CHECKOUT_SETUP_REQUIRED, DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED, and every structured rejection are completed coordination results. Follow agent-claim without repeating the operation through another transport.

## Exact Call Shapes

Read live ownership:

```json
{"repository": "/workspace/project"}
```

Acquire one exact file:

```json
{
  "repository": "/workspace/project",
  "claim_id": "task-123",
  "agent": "implementation-agent",
  "task": "task-123",
  "root_task_id": "task-123",
  "files": ["src/feature.py"]
}
```

Acquire broad project ownership:

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

Repeat an isolation-required acquisition with the same claim identity:

```json
{
  "repository": "/workspace/project",
  "claim_id": "task-123",
  "agent": "implementation-agent",
  "task": "task-123",
  "root_task_id": "task-123",
  "files": ["src/feature.py"],
  "branch": "codex/task-123",
  "base": "main"
}
```

Acquire authorized recovery ownership:

```json
{
  "repository": "/workspace/project",
  "claim_id": "recovery-123",
  "agent": "recovery-owner",
  "task": "recovery-123",
  "root_task_id": "recovery-123",
  "all_files": true,
  "scope_reason": "recover anonymous dirty state",
  "allow_recovery": true
}
```

Required future timed-resource acquisition shape:

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

Extend one claim:

```json
{
  "repository": "/workspace/project",
  "claim_id": "task-123",
  "files": ["tests/test_feature.py"],
  "resources": ["generated:codegen"]
}
```

Required future evidence-backed deadline extension shape:

```json
{
  "repository": "/workspace/project",
  "claim_id": "browser-check-123",
  "requested_hard_stop_duration_seconds": 2400,
  "extension_evidence": "one final accessibility case remains"
}
```

Heartbeat, release, journal maintenance, and reporting use these respective argument shapes:

```json
{"repository": "/workspace/project", "claim_id": "task-123"}
```

```json
{"repository": "/workspace/project", "claim_id": "task-123", "no_change": false}
```

```json
{"repository": "/workspace/project", "hot_days": 2}
```

```json
{"repository": "/workspace/project", "since": "2d"}
```

## Ambiguous Dispatch

When a mutating MCP dispatch is ambiguous because the connection breaks after submission, do not repeat the mutation and do not switch transports. Reconnect to the same configured MCP transport and call claim_status for the same repository. Continue only from the observed registry state.

If the same transport cannot provide status, preserve the ambiguous state, report CLAIM_TRANSPORT_UNAVAILABLE, and request Project Configurator reconfiguration or an explicit ownership handoff. Never use the command adapter to guess whether the mutation succeeded.

## Behavioral Equivalence

Both configured transports expose the same engine outcomes and next-action semantics. Their invocation envelopes differ, but this adapter never renames, suppresses, retries, or translates a structured coordination outcome.
