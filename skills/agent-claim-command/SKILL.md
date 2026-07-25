---
name: agent-claim-command
description: Invoke the agent-claim contract through the adapter-bundled claim command-line interface without runtime probing or interface fallback.
metadata:
  category: development-practice
---

# Agent Claim Command

Apply this adapter only when Project Configurator selected command in the compatibility field agent_claim_transport and verified this package, Python, and its executable script. That field selects how the claim helper is invoked. Apply agent-claim for scope, ownership, state, recovery, heartbeat, release, and completion semantics.

The command-line implementation flow is Python claim command -> claim helper -> claim registry and journal. The command parser and helper functions are implemented together in scripts/claim.py inside this adapter; the helper writes repository-global registry and journal state under the Git common directory.

## Availability Boundary

Resolve the adapter-bundled script once before the first operation and reuse that exact path for the task. Do not search for MCP tools or change the configured claim-helper interface. Do not assume the target repository contains the adapter package.

Use an explicit path supplied by configured project guidance when present. Otherwise use the scripts/claim.py file beside this loaded SKILL.md. Inside the dev-methodology source checkout, the bundle-owned path is:

```bash
CLAIM_SCRIPT=skills/agent-claim-command/scripts/claim.py
```

For a normal Codex user-level installation, the default is:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-command/scripts/claim.py"
```

If the configured script or Python interpreter is absent, unreadable, or cannot start before dispatch, stop with CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration. Do not switch claim-helper interfaces. An argument, path, root, authorization, input-policy, or other structured rejection returned by the command is not unavailability.

## Command Contract

Invoke the script with Python and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, maintain-journal, and report. Each completed invocation writes one JSON document to standard output. Decode it and inspect result.outcome. The top-level exit_code and process exit code are stable automation aids; the structured outcome is authoritative.

Stable process exit codes are:

- 0 for successful execution, including acquired ownership and read-only operations.
- 1 for a structured rejection such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, or RELEASE_REJECTED.
- 3 for CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, or SHARED_CHECKOUT_RELEASE_REQUIRED.
- 4 for ISOLATED_CHECKOUT_SETUP_REQUIRED.
- 5 for DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED.
- 2 for command-line parsing failure before coordination dispatch.

Several outcomes share one exit code. Never branch on the process code alone. A completed structured rejection is a valid coordination result; do not switch claim-helper interfaces or retry it through MCP.

RECONCILIATION_RECOVERY_REQUIRED means a durable pending reconciliation marker still controls transaction recovery. A prepared marker protects the exact original registry and journal snapshots; its RELEASE_PENDING line is not a release. A committed marker makes the exact released registry authoritative and finalizes exactly one RELEASED journal event. Scoped commands and journal maintenance attempt validated deterministic recovery under the registry lock. Report remains read-only and returns this outcome before journal loading when a marker exists.

When this outcome appears:

1. Invoke status through this same CLAIM_SCRIPT path.
2. If the outcome persists, preserve the marker, registry, journal, command result, and relevant filesystem evidence.
3. Escalate that evidence. Do not manually edit or remove the marker, registry, journal, or protected claim.

## Command Arguments

Acquire requires claim-id, agent, task, and root-task-id. Scope arguments are repeatable file and tree values, at most one resource value, or one mutually exclusive broad selector: project-files, backlog, or all-files. Tree, project-files, and all-files require scope-reason. A named resource also requires resource-class, resource-id, expected-duration-seconds, and requested-hard-stop-duration-seconds; the command resolves configured maximum and cleanup grace from PROJECT.yaml. Optional acquisition arguments are parent-claim-id, branch, base, allow-recovery, and the compatibility-only worktree-path and compat-file-directories options.

Extend requires claim-id plus net-new scope and uses the same complete timing arguments when adding the claim's one named resource. Extend-deadline requires claim-id, requested-hard-stop-duration-seconds, and extension-evidence. Heartbeat and release require claim-id. Release accepts no-change only for a truthful no-change result. The mutually exclusive reconciliation variant accepts reconcile-out-of-domain-commit with one full 40-character SHA and requires prior-rejected-release-reference for the matching rejected release event. Journal maintenance accepts hot-days, defaulting to 2. Reporting accepts since and format; use JSON output for automation.

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

Acquire one deadline-bound resource. The project policy, not this command, supplies the configured maximum and cleanup grace:

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

Extend scope, explicitly extend a resource deadline, heartbeat, and release:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --file tests/test_feature.py

python3 "$CLAIM_SCRIPT" --repo . extend-deadline \
  --claim-id browser-check-123 \
  --requested-hard-stop-duration-seconds 2400 \
  --extension-evidence "one final accessibility case remains"

python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123

python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

Heartbeat is liveness only and never extends a deadline. Extend-deadline succeeds only when the evidence is non-empty, the requested duration increases, and it stays within the immutable configured maximum recorded at acquisition. Status reports overdue and cleanup-grace state without auto-release or delivery inference.

Declare a clean no-change result:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --no-change
```

Reconcile one retained primary scoped claim only after verifying the supplied peer commit and prior rejected release reference:

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

## Ambiguous Dispatch

When process control or output capture fails after submitting a mutating command, the dispatch is ambiguous. Do not repeat the mutation or change the claim-helper interface. Invoke status through the same CLAIM_SCRIPT path and reconcile the live registry before continuing.

If the same claim command-line interface cannot provide status, preserve the ambiguous state, report CLAIM_TRANSPORT_UNAVAILABLE, and request Project Configurator reconfiguration or an explicit ownership handoff. Never invoke the MCP adapter to guess whether the command mutation succeeded.

## Behavioral Equivalence

Both configured claim-helper interfaces expose the same helper outcomes and next-action semantics. Their invocation envelopes differ, but this adapter never renames, suppresses, retries, or translates a structured coordination outcome.
