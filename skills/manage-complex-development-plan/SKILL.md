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
└── .history/<plan-name>/
```

The history directory is bounded operational evidence. It is not a backlog or provider ledger. The helper retains at most 20 settled pre-mutation snapshots and does not prune unresolved uncertain operations.

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

Use an exact one-based dotted path or an exact unique item title. Prefer a dotted path after peer insertion because later item numbers can change.

Mark one item complete:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target 2 --complete
```

Add one discovered subtask beneath an existing task:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target 2 --add-child "Verify the discovered boundary"
```

Add one discovered peer workstream after an existing task:

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target 3 --add-peer-after "Document the new interface"
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

Inspect parses the authoritative JSON and uses render_hierarchy_html without an output file. It compares the rendered bytes with the sibling HTML.

- SYNCED means the files match and supplies their hashes plus a reconciliation token.
- DRIFT means the HTML does not match the authoritative JSON.
- INVALID_PLAN means the JSON cannot be accepted as the hierarchy-plan authority.

For valid JSON with HTML drift, run the deterministic reconcile command. It backs up the current artifacts and rebuilds only the sibling HTML through render_hierarchy_html.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  reconcile
```

An exception after a mutation starts returns UNCERTAIN_UPDATE or UNCERTAIN_RECONCILIATION. Do not repeat that command. Run inspect, then reconcile when HTML drift exists. If the files are already synchronized, pass the current inspect reconciliation token to the next update. Stop when JSON validity or artifact authority cannot be established.

```bash
python3 [skill-root]/scripts/plan.py \
  --workspace /absolute/workspace \
  --root-task-id task-123 \
  --plan-name delivery \
  update --target 2 --complete --reconciliation-token <token-from-inspect>
```

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

The remove choice deletes only the selected plan JSON, sibling HTML, and its bounded operational history. It never changes provider state, another plan, source-control history, or delivery evidence.

Finalization fails closed when an actionable item is incomplete, the artifacts drift, or any uncertain operation remains unresolved.
If removal may have stopped after changing an artifact, the helper returns UNCERTAIN_CLEANUP. Do not retry removal. Reconcile the exact selected plan paths and retained terminal evidence first.

## Result

Return the complexity-gate decision, fixed task-owned paths, helper outcomes, before-and-after hashes for mutations, discovery additions, reconciliation evidence, final authority comparison, and explicit retention result.
