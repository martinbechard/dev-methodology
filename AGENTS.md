## Resource Coordination Skill Reference

Project Configurator selected resource-coordination skill resource-claim. Apply that bundled skill by reference before taking ownership of repository paths or exclusive runtime and integration resources.

The selected skill owns its coordination procedure and evidence. Work-item providers own durable assignment and lifecycle records; they do not own operational resources.

Configured resource deadline policy:

- backlog-mutation: maximum 600 seconds; cleanup grace 120 seconds
- main-integration: maximum 2700 seconds; cleanup grace 600 seconds
- browser-server: maximum 3600 seconds; cleanup grace 600 seconds
- database-port: maximum 1800 seconds; cleanup grace 300 seconds
- live-model-evaluation: maximum 14400 seconds; cleanup grace 1800 seconds

Exact resource-id overrides:

- None.

## Resource Claim Helper

Project Configurator selected and verified the command claim helper. Apply resource-claim for policy and use the inlined resource-claim-helper-command Provider Skill to realize resource-claim-helper.

Use only this configured claim helper. If it cannot start, ask Project Configurator to configure a working helper.

----- BEGIN INLINED CLAIM HELPER SKILL: resource-claim-helper-command -----
# Resource Claim Helper Command

This Provider Skill realizes Resource Claim Helper through one local command-line program. Apply resource-claim for policy and resource-claim-helper for the common operation, input, result, and uncertain-outcome contract.

This skill owns command discovery, argument mapping, process results, and command-specific reconciliation. It does not define claim policy or the shared helper contract.

## Helper Setup

Find the configured script before the first claim operation. Use that script for every claim operation in the task.

Use the script path in project guidance when it is present. Otherwise, use scripts/claim.py beside this SKILL.md.

In the dev-methodology source checkout:

```bash
CLAIM_SCRIPT=skills/resource-claim-helper-command/scripts/claim.py
```

In a Codex user-level installation:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/resource-claim-helper-command/scripts/claim.py"
```

If the script or Python cannot start, ask Project Configurator to configure a working claim helper.

## Command Invocation

Invoke the script with Python, an absolute project root, and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, reset, maintain-journal, and report.

Except for a successful `report --format text`, each completed command writes one JSON document to standard output. Read `outcome` from that document. Several results share a process exit code, so do not decide from the exit code alone.

`report --format text` is an explicit human-readable exception. It writes prose without `schema_version` or `outcome` and is not valid for automated result handling or provider-parity verification. Omit `--format` or use `--format json` when the structured Resource Claim Helper contract is required.

## Read Claim Status

Map Read Claim Status to status:

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

## Acquire Claim

Map the common acquire inputs to long options. Use one scope shape selected through resource-claim.

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

Map Release Claim to release. Supply disposition and blocker-reference only when the common interface and resource-claim require them.

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
----- END INLINED CLAIM HELPER SKILL: resource-claim-helper-command -----

## Work-Item Workflow Skill References

Project Configurator owns the independent Persistence and Commit selectors. Persistence routes durable work-item storage; Commit routes delivery. Workflow skills are referenced by name only and technology skill routing remains separate.

- Default persistence file: create with create-work-item-file; manage with manage-work-items-file.
- Default commit main-branch: use deliver-work-item-main-branch.

Most-specific matching folder pattern wins independently for Persistence and Commit overrides. A folder override changes only its own selector.

When a selector is UNSET, the pertinent agent asks at the stated operation boundary and does not infer either value from repository or hosting evidence, files, remotes, templates, plugins, or available tools.

## Technology Skills

Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.

Before acting on files under a matching folder, every agent must read each listed skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills.

Folder skillsets:

When configured folder patterns overlap, the most-specific matching pattern wins.

- scripts/**: load python before acting.
  - python evidence: Python source evidence: scripts/build-agent-skill-hierarchy.py and sibling .py files
- skills/project-wiki/scripts/**: load python before acting.
  - python evidence: Python package evidence: skills/project-wiki/scripts/project_wiki_ops/__init__.py and sibling .py files
- skills/detect-technology-skills/scripts/**: load python before acting.
  - python evidence: Python source evidence: skills/detect-technology-skills/scripts/detect.py
- evals/projects/python-inventory/**: load python before acting.
  - python evidence: Python source evidence: evals/projects/python-inventory/src/inventory.py; Owning manifest evidence: evals/projects/python-inventory/pyproject.toml requires Python 3.11 or newer
- evals/projects/fastapi-orders/**: load fastapi, python before acting.
  - fastapi evidence: Owning manifest dependency: evals/projects/fastapi-orders/pyproject.toml declares fastapi; Framework source evidence: evals/projects/fastapi-orders/app/main.py imports FastAPI and declares an application route
  - python evidence: Python source evidence: evals/projects/fastapi-orders/app/main.py

## Project Skill Extensions

These references apply through the root AGENTS.md only. Load each selected skill completely in the declared order when starting project work. Skill definitions remain in their bundled or registered catalogs and are not copied here.

- dev-methodology-repository-maintenance
