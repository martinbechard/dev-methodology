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

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, maintain-journal, and report.

Each completed command writes one JSON document to standard output. Read result.outcome. Do not decide from the process exit code alone.

Several outcomes share an exit code. The JSON outcome, not the exit code, identifies the result. Do not switch helpers because a command rejected a request.

## Command Arguments

Acquire requires:

- claim-id;
- agent;
- task;
- root-task-id;
- the scope selected through agent-claim.

Use file, project-files, or resource for the scope chosen from the Claim Events table.

A project-files request also requires scope-reason.

A resource request also requires resource-class, resource-id, expected-duration-seconds, and requested-hard-stop-duration-seconds.

Other operations require:

| Operation | Arguments |
|---|---|
| extend | claim-id and additional scope |
| extend-deadline | claim-id, requested-hard-stop-duration-seconds, and extension-evidence |
| heartbeat | claim-id |
| release | claim-id and any applicable release option |
| maintain-journal | optional hot-days |
| report | optional since and format |

## Command Examples

Read live ownership:

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

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

Extend a claim, extend a resource deadline, send a heartbeat, and release a claim:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --resource port:3000 \
  --resource-class database-port \
  --resource-id port:3000 \
  --expected-duration-seconds 600 \
  --requested-hard-stop-duration-seconds 1200

python3 "$CLAIM_SCRIPT" --repo . extend-deadline \
  --claim-id browser-check-123 \
  --requested-hard-stop-duration-seconds 2400 \
  --extension-evidence "one final accessibility case remains"

python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123

python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

Release a claim after a verified no-change result:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --no-change
```

Release after Project Configurator approves reconciliation:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --reconcile-out-of-domain-commit 0123456789abcdef0123456789abcdef01234567 \
  --prior-rejected-release-reference 12345678-1234-1234-1234-123456789abc
```

Maintain the journal and report contention:

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
python3 "$CLAIM_SCRIPT" --repo . report --since 2d --format json
```

## Uncertain Command Outcome

If the process stops after sending a command that changes claim state, the operation may have completed. Do not repeat it.

Run status through the same script. Continue from the reported claim state.

If the script cannot return status, ask Project Configurator for help. Do not use another helper to guess what happened.
