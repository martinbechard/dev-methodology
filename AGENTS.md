## Resource Coordination Skill Reference

Project Configurator selected resource-coordination skill agent-claim. Apply that bundled skill by reference before taking ownership of repository paths or exclusive runtime and integration resources.

The selected skill owns its coordination procedure and evidence. Work-item providers own durable assignment and lifecycle records; they do not own operational resources.

Configured resource deadline policy:

- backlog-mutation: maximum 600 seconds; cleanup grace 120 seconds
- main-integration: maximum 2700 seconds; cleanup grace 600 seconds
- browser-server: maximum 3600 seconds; cleanup grace 600 seconds
- database-port: maximum 1800 seconds; cleanup grace 300 seconds
- live-model-evaluation: maximum 14400 seconds; cleanup grace 1800 seconds

Exact resource-id overrides:

- None.

## Agent Claim Helper

Project Configurator selected and verified the command claim helper. Apply agent-claim for claim rules and use the inlined agent-claim-command skill to run the helper.

Use only this configured claim helper. If it cannot start, ask Project Configurator to configure a working helper.

----- BEGIN INLINED CLAIM HELPER SKILL: agent-claim-command -----
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
----- END INLINED CLAIM HELPER SKILL: agent-claim-command -----

## Work-Item Workflow Skill References

Project Configurator owns the independent Persistence and Commit selectors. Persistence routes durable work-item storage; Commit routes delivery. Workflow skills are referenced by name only and technology skill routing remains separate.

- Default persistence file: create with create-file-work-item; manage with manage-file-work-items.
- Default commit direct-main: use complete-work-item-direct-main.

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
