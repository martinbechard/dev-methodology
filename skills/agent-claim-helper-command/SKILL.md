---
name: agent-claim-helper-command
description: Use the configured local command-line provider for the Agent Claim Helper interface.
metadata:
  category: development-practice
---

# Agent Claim Helper Command

This Provider Skill realizes Agent Claim Helper through one local command-line program. Apply agent-claim for policy and agent-claim-helper for the common operation, input, result, and uncertain-outcome contract.

This skill owns command discovery, argument mapping, process results, and command-specific reconciliation. It does not define claim policy or the shared helper contract.

## Helper Setup

Find the configured script before the first claim operation. Use that script for every claim operation in the task.

Use the script path in project guidance when it is present. Otherwise, use scripts/claim.py beside this SKILL.md.

In the dev-methodology source checkout:

```bash
CLAIM_SCRIPT=skills/agent-claim-helper-command/scripts/claim.py
```

In a Codex user-level installation:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-helper-command/scripts/claim.py"
```

If the script or Python cannot start, ask Project Configurator to configure a working claim helper.

## Command Invocation

Invoke the script with Python, an absolute project root, and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, reset, maintain-journal, and report.

Except for a successful `report --format text`, each completed command writes one JSON document to standard output. Read `outcome` from that document. Several results share a process exit code, so do not decide from the exit code alone.

`report --format text` is an explicit human-readable exception. It writes prose without `schema_version` or `outcome` and is not valid for automated result handling or provider-parity verification. Omit `--format` or use `--format json` when the structured Agent Claim Helper contract is required.

## Read Claim Status

Map Read Claim Status to status:

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

## Acquire Claim

Map the common acquire inputs to long options. Use one scope shape selected through agent-claim.

Work-item acquisition:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id work-item-123-work \
  --agent implementation-agent \
  --task work-item-123 \
  --root-task-id work-item-123 \
  --work-item-id provider-opaque-id-123 \
  --activity work
```

Project-files acquisition:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent implementation-agent \
  --task task-123 \
  --root-task-id task-123 \
  --project-files \
  --scope-reason "project implementation"
```

A file scope uses one `--file` option for each file and a tree scope uses one `--tree` option for each tree. Broad path domains use `--project-files`, `--backlog`, or `--all-files` plus `--scope-reason`. A resource scope uses `--resource` plus `--resource-class`, `--resource-id`, `--expected-duration-seconds`, and `--requested-hard-stop-duration-seconds`. Map `parent_claim_id` to `--parent-claim-id`. Isolated-checkout creation maps `branch`, `base`, and `worktree_path` to `--branch`, `--base`, and `--worktree-path`.

## Extend Claim

Map Extend Claim to extend with `--claim-id` and only the net-new path-domain or resource scope. Use the same path-domain and resource options as Acquire Claim, excluding work-item and isolated-checkout inputs.

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --resource port:3000 \
  --resource-class database-port \
  --resource-id port:3000 \
  --expected-duration-seconds 600 \
  --requested-hard-stop-duration-seconds 1200
```

## Extend Claim Deadline

Map Extend Claim Deadline to extend-deadline:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend-deadline \
  --claim-id browser-check-123 \
  --requested-hard-stop-duration-seconds 2400 \
  --extension-evidence "one final accessibility case remains"
```

## Heartbeat Claim

Map Heartbeat Claim to heartbeat:

```bash
python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123
```

## Release Claim

Map Release Claim to release. Supply disposition and blocker-reference only when the common interface and agent-claim require them.

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id work-item-123-work \
  --disposition handoff
```

Non-work-item release keeps the disposition-free form:

```bash
python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

## Reset Claim Registry

Map Reset Claim Registry to reset:

```bash
python3 "$CLAIM_SCRIPT" --repo . reset
```

## Maintain Claim Journal

Map Maintain Claim Journal to maintain-journal. hot-days is optional.

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
```

## Report Claim Contention

Map Report Claim Contention to report. `since` and `format` are optional command arguments. JSON mode returns canonical outcome `REPORT` with `window`, `event_count`, `metrics`, `work_items`, and `coverage_gaps`.

```bash
python3 "$CLAIM_SCRIPT" --repo . report --since 2d --format json
```

## Reconcile an Uncertain Command

If the process stops after it sends a mutating command, the outcome is uncertain. Do not repeat the command. Run Read Claim Status through this same script and reconcile the reported claim state.

If the script cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
