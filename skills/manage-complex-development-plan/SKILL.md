---
name: manage-complex-development-plan
description: Maintain a task-owned JSON and HTML execution plan for complex development through deterministic mcp-agent-ops hierarchy commands.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 41EA8048-6F20-4605-ABA6-47DA6C9A2CA2
Created-UTC: 2026-08-10T01:27:38Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe928-e31e-71e2-aaa8-7f9bef12c7b0
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Manage Complex Development Plan

Use one task-owned hierarchy plan to keep a complex delivery visible while its decomposition changes. The JSON file is authoritative. Its sibling HTML file is a synchronized read-only projection.

This plan is an execution aid. It is not a provider record, work-item queue, source-control record, review verdict, verification result, or Commit result.

## Complexity Gate

Create a plan when at least one of these conditions is true:

- The initial decomposition has four or more actionable tasks and at least one dependency between them.
- The delivery needs three or more independently owned contribution lanes.
- The delivery is expected to cross a task resumption or more than one bounded review, correction, or integration cycle.
- Material discovery can add or reorder work after the first contributor dispatch.

Do not create a plan for one routine contribution lane with its ordinary review, verification, and Commit steps. Do not count those standard gates alone as complexity.

## Helper Boundary

Use the repository-owned scripts/plan.py helper in this skill package. Run its commands directly. Never improvise Python snippets, ad hoc shell mutation logic, or alternate hierarchy wrappers.

The helper imports and signature-checks these public package APIs:

- mcp_agent_ops.hierarchy.create_hierarchy_plan
- mcp_agent_ops.hierarchy.update_hierarchy_plan
- mcp_agent_ops.hierarchy.render_hierarchy_html

If the current Python cannot import the package, the helper can re-exec through the discovered mcp-agent-ops executable interpreter. If capabilities remain unavailable, stop and report CAPABILITY_UNAVAILABLE. Do not install, change, release, or emulate mcp-agent-ops.

Run the capability check before plan initialization:

```bash
python3 [skill-root]/scripts/plan.py capabilities
```

Every completed helper command writes one JSON result. Decide from outcome, not only from the process exit code.

## Task-Owned Paths

Supply a canonical absolute workspace path, a safe root task ID, and a safe plan name. The helper fixes the plan location to this project-relative root:

```text
.codex/plans/<root-task-id>/
├── <plan-name>.json
├── <plan-name>.html
├── .history/<plan-name>/
└── .locks/<plan-name>.lock
```

The history directory is bounded operational evidence. It is not a backlog or provider ledger. Before every create, update, reconcile, or cleanup effect, the helper creates an operation directory, writes a pending operation record, and preserves the available pre-mutation files. A missing, malformed, pending, or otherwise nonterminal result remains unresolved and is never silently skipped or pruned. The helper retains at most 20 operation directories by pruning only terminal history when space is needed.

The lock file coordinates one selected plan across processes. The helper holds its standard-library POSIX or Windows lock from inspection and target validation through package dispatch, artifact checks, and terminal result persistence. LOCK_TIMEOUT means another writer retained that boundary; do not bypass the lock or improvise a mutation. An unsupported lock backend fails with CAPABILITY_UNAVAILABLE.

Keep the complete plan root ignored as operational state. Do not commit the plan, copy it into backlog, or use it to control provider lifecycle.

## Plan Initialization

Initialize the plan before detailed decomposition or contributor dispatch. Start with the accepted objective and the coarse tasks that justify the complexity gate. Add detailed work as discovery proceeds.

Create a temporary definition file inside the absolute workspace with this schema:

```json
{
  "schema": "dev-methodology-complex-plan-input",
  "version": 1,
  "title": "Delivery plan",
  "objective": "Deliver the accepted outcome",
  "tasks": [
    {
      "title": "Discovery",
      "dependsOn": [],
      "evidence": ["work-item:example"],
      "complete": false,
      "children": []
    },
    {
      "title": "Implementation",
      "dependsOn": ["Discovery"],
      "evidence": [],
      "complete": false,
      "children": []
    }
  ]
}
```

Use ordinary structured file editing for the definition. Do not assemble it with shell text or a Python snippet. Keep references concise. Exclude credentials, personal information, unauthorized proprietary content, prompt bodies, and unnecessary source payloads.

Do not use `Dependency reference: ` or `Evidence reference: ` at the start of an actionable task title. The helper reserves both prefixes for complete structural reference leaves and rejects them in task definitions and discovered child or peer text.

Create the canonical plan through the helper:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  create --definition /absolute/workspace/plan-definition.json
```

The helper calls create_hierarchy_plan and returns CREATED only when the canonical JSON and sibling HTML are synchronized. Remove the temporary definition after CREATED. Preserve it when creation is uncertain.

## Plan Updates

Update the plan when discovery changes the decomposition and when authoritative evidence completes a task. Each update invocation calls update_hierarchy_plan exactly once and accepts exactly one mutation.

Prefer an exact unique item title. Structural insertions can shift dotted paths, so prefer unique titles after any child or peer insertion. Before every dotted target, reread the current authoritative JSON and supply the title currently found at that path through `--expected-title`. The helper fails without mutation when the expected title is absent or the path has shifted.

Mark one item complete:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target 2 --expected-title Discovery --complete
```

Add one discovered subtask beneath an existing task:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target Discovery --add-child "Verify the discovered boundary"
```

Add one discovered peer workstream after an existing task:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target Implementation --add-peer-after "Document the new interface"
```

Do not rewrite completed items or prior structure to make discovery appear linear. Add the new child or peer at the point where it became necessary. Use separate invocations for separate discoveries.

## Authority And Cadence

Update the plan after each material discovery, accepted contribution, independent review result, verification result, integration result, and Commit or Persistence transition that changes what remains actionable.

Provider lifecycle, work-item state, Git commits, independent review, verification, and the effective Commit result have precedence over plan state. If they differ, reconcile the plan to those sources. Never change an authoritative source to match the plan.

Record concise evidence references in task text or the initial definition. Do not duplicate the complete provider record or review report.

## Inspection And Recovery

Inspect without changing the JSON or HTML artifacts:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  inspect
```

Inspect parses the authoritative JSON and uses render_hierarchy_html without an output file. It compares the rendered bytes with the sibling HTML and reads every operation record without changing either artifact.

- SYNCED means the files match and no operation is unresolved.
- ABSENT means neither selected artifact exists and no operation is unresolved, so create can retry.
- DRIFT means valid authoritative JSON has missing or different sibling HTML.
- RECOVERY_REQUIRED means at least one operation is unresolved, even when JSON and HTML already synchronize or both are absent.
- ORPHANED_HTML means HTML exists without JSON and without a pending operation that authorizes recovery.
- INVALID_PLAN means the JSON cannot be accepted as the hierarchy-plan authority.

Recoverable inspect outcomes include artifact hashes, artifact state, unresolved operation details, and a recovery token bound to that exact state. INVALID_PLAN is instead a structured non-recoverable error and does not promise those recovery-envelope fields. For valid JSON with ordinary HTML drift, run the deterministic reconcile command with the current token. It records its own pending operation before rebuilding only the sibling HTML through render_hierarchy_html.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  reconcile --recovery-token <token-from-inspect>
```

An exception after an effect may have started returns UNCERTAIN_CREATE, UNCERTAIN_UPDATE, UNCERTAIN_RECONCILIATION, or UNCERTAIN_CLEANUP. A process stop can leave only the earlier pending record. Do not repeat the interrupted command, even when the artifacts appear synchronized. Run inspect, then pass its current recovery token to reconcile. A stale token fails before mutation; inspect again instead of guessing.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  reconcile --recovery-token <token-from-inspect>
```

Reconcile excludes only its own current pending record while rechecking the recovery inputs. Before it settles a prior operation or changes a canonical artifact, it persists a prepared decision bound to the operation records, result records, snapshots, canonical artifact hashes, and expected rendered output. A later reconcile resumes that exact prepared decision after another interruption. It uses these deterministic recovery outcomes:

- Valid JSON is retained as authority and HTML is rendered to match it. This covers JSON-only and synchronized interrupted creates, updates, and reconciliations.
- An interrupted create with HTML only or without valid JSON is cleaned to confirmed absence so create can retry.
- An interrupted cleanup continues HTML removal first and JSON removal last, then confirms both artifacts are absent.
- Invalid or absent JSON for an interrupted update or reconciliation is restored only from a valid helper-owned pre-mutation JSON snapshot. Without one, recovery stops.

Reconcile marks prior operations terminal only after it has confirmed synchronized retention or complete absence, then marks its own record terminal. Stop when JSON authority, snapshot validity, or synchronization cannot be established. Never delete partial artifacts or edit operation evidence by hand.

## Final Reconciliation And Retention

Before finalization, reconcile every plan item with provider state, accepted commits, independent review, verification, integration, and Commit evidence. Mark an item complete only when its authoritative evidence supports completion. Run inspect after the final update.

Finalize with an explicit retention choice. The helper never removes artifacts by default.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  finalize --retention keep
```

Use keep while the task can resume, review is pending, or local plan evidence is still needed. Use remove only after terminal provider and Commit evidence is secured, required review and verification are complete, and project policy does not require local retention.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  finalize --retention remove
```

The remove choice deletes only the selected sibling HTML first, the selected plan JSON last, and then its bounded operational history after confirmed absence. It retains pending evidence until the absence result is terminal. It never changes provider state, another plan, source-control history, or delivery evidence.

Finalization fails closed when an actionable item is incomplete, the artifacts drift, or any uncertain operation remains unresolved. Both reserved structural prefixes remain invalid for incomplete or parent items, so actionable text cannot be hidden from the completion check.

If removal may have stopped after changing an artifact, the helper returns UNCERTAIN_CLEANUP or leaves a pending cleanup record. Do not retry removal. Inspect the exact selected plan and pass the current recovery token to reconcile. Reconciliation must reach confirmed absence before create or cleanup can retry.

## Result

Return the complexity-gate decision, fixed task-owned paths, helper outcomes, before-and-after hashes for mutations, discovery additions, reconciliation evidence, final authority comparison, and explicit retention result.
