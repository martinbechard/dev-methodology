---
name: agent-claim-command
description: Invoke the transport-neutral agent-claim contract through the adapter-bundled structured command without runtime probing or transport fallback.
metadata:
  category: development-practice
---

# Agent Claim Command

Apply this adapter only when Project Configurator selected command in agent_claim_transport and verified this package, Python, and its executable script. Apply agent-claim for scope, ownership, state, recovery, heartbeat, release, and completion semantics.

## Availability Boundary

Resolve the adapter-bundled script once before the first operation and reuse that exact path for the task. Do not search for MCP tools or change to an MCP transport. Do not assume the target repository contains the adapter package.

Use an explicit path supplied by configured project guidance when present. Otherwise use the scripts/claim.py file beside this loaded SKILL.md. Inside the dev-methodology source checkout, the bundle-owned path is:

```bash
CLAIM_SCRIPT=skills/agent-claim-command/scripts/claim.py
```

For a normal Codex user-level installation, the default is:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-command/scripts/claim.py"
```

If the configured script or Python interpreter is absent, unreadable, or cannot start before dispatch, stop with CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration. Do not switch transports. An argument, path, root, authorization, input-policy, or other structured rejection returned by the command is not unavailability.

## Command Contract

Invoke the script with Python and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, heartbeat, release, maintain-journal, and report. Each completed invocation writes one JSON document to standard output. Decode it and inspect result.outcome. The top-level exit_code and process exit code are stable automation aids; the structured outcome is authoritative.

Stable process exit codes are:

- 0 for successful execution, including acquired ownership and read-only operations.
- 1 for a structured rejection such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, or RELEASE_REJECTED.
- 3 for CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, or SHARED_CHECKOUT_RELEASE_REQUIRED.
- 4 for ISOLATED_CHECKOUT_SETUP_REQUIRED.
- 5 for DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED.
- 2 for command-line parsing failure before coordination dispatch.

Several outcomes share one exit code. Never branch on the process code alone. A completed structured rejection is a valid coordination result; do not switch transports or retry it through MCP.

## Command Arguments

Acquire requires claim-id, agent, task, and root-task-id. Scope arguments are repeatable file, tree, and resource values or one mutually exclusive broad selector: project-files, backlog, or all-files. Tree, project-files, and all-files require scope-reason. Optional acquisition arguments are parent-claim-id, branch, base, allow-recovery, and the compatibility-only worktree-path and compat-file-directories options.

Extend requires claim-id plus net-new scope. Heartbeat and release require claim-id. Release accepts no-change only for a truthful no-change result. Journal maintenance accepts hot-days, defaulting to 2. Reporting accepts since and format; use JSON output for automation.

## Exact Invocations

Read live ownership:

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

Acquire one exact file:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent implementation-agent \
  --task task-123 \
  --root-task-id task-123 \
  --file src/feature.py
```

Acquire broad project ownership:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent implementation-agent \
  --task task-123 \
  --root-task-id task-123 \
  --project-files \
  --scope-reason "project implementation"
```

Repeat an isolation-required acquisition with the same claim identity:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent implementation-agent \
  --task task-123 \
  --root-task-id task-123 \
  --file src/feature.py \
  --branch codex/task-123 \
  --base main
```

Acquire authorized recovery ownership:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id recovery-123 \
  --agent recovery-owner \
  --task recovery-123 \
  --root-task-id recovery-123 \
  --all-files \
  --scope-reason "recover anonymous dirty state" \
  --allow-recovery
```

Extend, heartbeat, and release:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --file tests/test_feature.py \
  --resource generated:codegen

python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123

python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

Declare a clean no-change result:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --no-change
```

Maintain the journal and report contention:

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
python3 "$CLAIM_SCRIPT" --repo . report --since 2d --format json
```

## Ambiguous Dispatch

When process control or output capture fails after submitting a mutating command, the dispatch is ambiguous. Do not repeat the mutation and do not switch transports. Invoke status through the same CLAIM_SCRIPT path and reconcile the live registry before continuing.

If the same command transport cannot provide status, preserve the ambiguous state, report CLAIM_TRANSPORT_UNAVAILABLE, and request Project Configurator reconfiguration or an explicit ownership handoff. Never invoke the MCP adapter to guess whether the command mutation succeeded.

## Behavioral Equivalence

Both configured transports expose the same engine outcomes and next-action semantics. Their invocation envelopes differ, but this adapter never renames, suppresses, retries, or translates a structured coordination outcome.
