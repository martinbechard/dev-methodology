---
name: agent-claim-command
description: Use the configured command-line claim helper.
metadata:
  category: development-practice
---

# Agent Claim Command

Use this skill to run the command-line claim helper selected in PROJECT.yaml.

Follow agent-claim for all claim rules. This skill explains only how to run the configured command-line helper.

## Helper Setup

Find the configured script before the first claim operation. Use that script for every claim operation in the task.

Use the script path in the project instructions when one is provided. Otherwise, use the scripts/claim.py file beside this SKILL.md.

In the dev-methodology source checkout:

```bash
CLAIM_SCRIPT=skills/agent-claim-command/scripts/claim.py
```

In a Codex user-level installation:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-command/scripts/claim.py"
```

If the script or Python cannot start, ask Project Configurator to configure a working claim helper.

If the script returns JSON with result.outcome, the helper ran. Follow agent-claim for that outcome.

## Command Contract

Invoke the script with Python and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, reset, maintain-journal, and report.

Each completed command writes one JSON document to standard output. Read result.outcome. Do not decide from the process exit code alone.

Several outcomes share an exit code. The JSON outcome, not the exit code, identifies the result. Do not switch helpers because a command rejected a request.

## Read Claim Status

Run status with no operation-specific arguments. Read result.outcome from the returned JSON document.

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

## Acquire Claim

Acquire requires claim-id, agent, task, root-task-id, and the scope selected through agent-claim.

Use file, project-files, or resource for that scope. A project-files request also requires scope-reason. A resource request also requires resource-class, resource-id, expected-duration-seconds, and requested-hard-stop-duration-seconds.

File-scope acquisition:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id update-work-item-123 \
  --agent backlog-steward \
  --task update-work-item-123 \
  --root-task-id work-item-123 \
  --file backlog/feature-backlog/work-item-123.md
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

Resource acquisition:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id browser-check-123 \
  --agent browser-operator \
  --task browser-check-123 \
  --root-task-id task-123 \
  --resource browser-test:primary \
  --resource-class browser-server \
  --resource-id browser-test:primary \
  --expected-duration-seconds 900 \
  --requested-hard-stop-duration-seconds 1800
```

## Extend Claim

Extend requires claim-id and the net-new scope. A resource extension also requires resource-class, resource-id, expected-duration-seconds, and requested-hard-stop-duration-seconds.

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

Extend-deadline requires claim-id, requested-hard-stop-duration-seconds, and extension-evidence.

```bash
python3 "$CLAIM_SCRIPT" --repo . extend-deadline \
  --claim-id browser-check-123 \
  --requested-hard-stop-duration-seconds 2400 \
  --extension-evidence "one final accessibility case remains"
```

## Heartbeat Claim

```bash
python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123
```

## Release Claim

```bash
python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

Release removes only the exact named live claim while the helper holds an exclusive OS lock directly on agent-claims.json. The helper updates that same locked file without replacing its inode and appends RELEASED journal evidence. Release does not inspect Git state, file contents, delivery evidence, or completion state.

## Reset Claim Registry

Reset the registry after all agents have stopped:

```bash
python3 "$CLAIM_SCRIPT" --repo . reset
```

Reset locks agent-claims.json and replaces its contents with an empty claims list. It also creates the registry when it is missing and replaces malformed contents.

## Maintain Claim Journal

Maintain-journal accepts optional hot-days.

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
```

## Report Claim Contention

Report accepts optional since and format.

```bash
python3 "$CLAIM_SCRIPT" --repo . report --since 2d --format json
```

## Uncertain Command Outcome

Apply the uncertain-outcome policy from agent-claim when the process stops after sending a mutating command. Do not repeat it.

Run Read Claim Status through the same script and continue from the reported claim state.

If the script cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
