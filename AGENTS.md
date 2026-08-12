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

Project Configurator selected and verified the mcp claim helper. Apply resource-claim for policy and use the inlined resource-claim-helper-mcp Provider Skill to realize resource-claim-helper.

Use only this configured claim helper. If it cannot start, ask Project Configurator to configure a working helper.

----- BEGIN INLINED CLAIM HELPER SKILL: resource-claim-helper-mcp -----
# Resource Claim Helper MCP

This Provider Skill realizes Resource Claim Helper through MCP tool calls. Apply resource-claim for policy and resource-claim-helper for the common operation, input, result, and uncertain-outcome contract.

This skill owns MCP tool mapping, protocol-specific result envelopes, connection recovery, and the provider availability boundary. It does not define claim policy or the shared helper contract.

## Current Availability

The current mcp-agent-ops provider exposes the complete Resource Claim Helper tool surface:

- `claim_status`
- `claim_acquire`
- `claim_extend`
- `claim_extend_deadline`
- `claim_heartbeat`
- `claim_release`
- `claim_reset`
- `claim_maintain_journal`
- `claim_report`

Project Configurator may select this provider only after it verifies the tool schemas, schema-version-2 results, and startup availability in the target runtime. Availability in one live runtime does not prove availability in another runtime or configuration.

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
----- END INLINED CLAIM HELPER SKILL: resource-claim-helper-mcp -----

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

## Shared Agent Skills

These project-wide references apply to every Agent. Load a listed skill only when its condition applies; the skill definitions remain in the bundled catalog and are not copied here.

- structured-explanation: load when an Agent must present technical reasoning as explicit queries, facts, hypotheses, unknowns, and answers.
- organise-project-files: load when an Agent must choose or audit the location of a project file or directory.
- document-provenance: load when an Agent creates, generates, migrates, or accepts a maintained document governed by the project document_provenance configuration.

## Document Provenance

Load document-provenance when an Agent creates, generates, migrates, or accepts a maintained document governed by the project document_provenance configuration.

Governed maintained-document paths:

- README.md
- design/*.md
- design/**/*.md
- design/*.html
- design/**/*.html
- docs/*.md
- docs/**/*.md
- docs/*.html
- docs/**/*.html
- skills/*/SKILL.md
- skills/*/references/*.md
- skills/*/references/**/*.md
- skills/route-documentation-work/assets/templates/*.md

Required copyright text: Copyright (c) 2026 Martin.Bechard@DevConsult.ca

Placement rules:

- Markdown front matter remains the first construct; place the canonical provenance comment immediately after it. Without front matter, place the comment first.
- HTML doctype remains the first construct; place the canonical provenance comment immediately after it.
- Exclusions override governed path matches.

Excluded paths and artifact classes:

- backlog/**
- Clippings/**
- raw/**
- external/**
- vendor/**
- **/*.yaml
- **/*.yml
- **/*.json
- **/*.toml
- **/*.lock
- **/*.csv
- **/*.tsv
- **/*.xml
- **/*.ini
- **/*.conf
- **/*.bin
- **/*.pdf
- **/*.png
- **/*.jpg
- **/*.jpeg
- **/*.gif
- **/*.svg
- **/__pycache__/**
- **/*.pyc
- .cache/**
- node_modules/**
- design/generated/**
- generated/**
- design/agent-skill-test-coverage-checklist.md

Runtime provenance fields must come from the coordinator, orchestrator, or harness as runtime-supplied values. Never infer or reconstruct them from history.

Generated maintained documents inherit provenance through their generator or owning source and runtime envelope; do not hand-edit generated projections.

For an unsupported maintained-document format, use a project-authorized sidecar or manifest. If none is authorized, report the gap and leave the artifact unchanged.

## Project Skill Extensions

These references apply through the root AGENTS.md only. Load each selected skill completely in the declared order when starting project work. Skill definitions remain in their bundled or registered catalogs and are not copied here.

- dev-methodology-repository-maintenance
- backlog-dispatcher
