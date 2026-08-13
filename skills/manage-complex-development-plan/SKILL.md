---
name: manage-complex-development-plan
description: Create and update an externalized implementation hierarchy, when explicitly required, through configured MCP plan operations.
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

Use this Skill only when Dev Coder's assignment explicitly requires an externalized hierarchy plan. Dev Coder always owns the plan semantics and decomposition. When the assignment records that no externalized plan is needed, Dev Coder still creates and returns a bounded implementation and TDD plan without MCP persistence. The configured MCP operations own persistence and rendering for an externalized plan. A user instruction to code without planning bypasses both plan forms.

The returned JSON plan is authoritative, and its same-named HTML file is the synchronized rendering. The plan is an implementation aid, not Work-item content, a work-item queue, a review verdict, a verification result, a Commit result, or a source-control record.

## Required Capabilities

Before creating a plan, confirm that all three capabilities are available:

- The configured MCP `create_hierarchy_plan` operation.
- A runtime file-read capability that can read the returned JSON plan and its sibling HTML.
- The configured MCP `update_hierarchy_plan` operation.

If creation, plan reading, or targeted update is unavailable, stop with `PLAN_TOOL_UNAVAILABLE` and name the missing capability. Do not install or import a package, call server code directly, create another adapter, or use a local substitute.

## Create The Plan

Turn the bounded implementation and TDD plan into the `source` hierarchy accepted by `create_hierarchy_plan`. Keep requirements, dependencies, implementation tasks, and focused verification visible without copying the full Work-item content.

This generic source produces the requested display numbering 1, 2, 2.1, 2.2, and 3. A single outer mapping supplies the root label without adding another numbered level.

```json
{
  "Development plan": [
    "First item",
    {
      "Second item": [
        "First child of the second item",
        "Second child of the second item"
      ]
    },
    "Third item"
  ]
}
```

Invoke the configured MCP `create_hierarchy_plan` operation directly with:

- `source`: the inline mapping, sequence, JSON, YAML, or authorized absolute source path.
- `output_filename`: a base `.html` filename; the operation creates same-named JSON and HTML files.
- `title`: the plan title, such as `Development plan`.
- `output_folder`: an authorized absolute workspace folder when the configured default is not appropriate.
- Optional `theme`, `themes_folder`, or `completed_items` only when the assignment requires them.

The operation returns the authoritative JSON plan path. Read that JSON and its `htmlFilename` sibling. Confirm that both artifacts exist, their root and items match the intended hierarchy, and the rendered numbering is 1, 2, 2.1, 2.2, and 3. Return the authoritative JSON plan path to Dev Orchestrator so plan review and later progress tracking use this same record.

## Apply One Targeted Update

Read the current authoritative JSON plan before every update. Resolve the intended item from the current state by an exact dotted path or an exact unique title. When a title is duplicated or structural insertion may have shifted numbering, reread and use the current dotted path; never guess a target.

Invoke the configured MCP `update_hierarchy_plan` operation directly with the absolute `plan_path`, the resolved `target`, and exactly one of `completed`, `text`, `add_child`, `replace_children`, or `add_peer_after`. Each of these is one separate valid call:

```text
completed=true
completed=false
text="Revised item"
add_child="Discovered child"
replace_children=["First replacement", "Second replacement"]
add_peer_after="Discovered peer"
```

Use `add_child` for newly discovered work within the target and `add_peer_after` for a newly discovered adjacent workstream. Use `replace_children` only when the accepted decomposition deliberately replaces that target's children. Do not rewrite the full plan to conceal when work was discovered.

Set `completed=true` only when completed development evidence supports the item. Set `completed=false` when authoritative evidence reopens it. Parent completion may cascade when every child completes; treat the operation's `automatically_completed` and `next_task` fields as current navigation results, not as lifecycle authority.

After every update:

1. Require `success=true` and confirm the returned `plan_path` is the selected authoritative plan.
2. Reread the authoritative JSON plan and its sibling HTML.
3. Confirm the requested field or structure changed at the resolved target and that unaffected items remain unchanged from the pre-update read.
4. Confirm the HTML names the current items, numbering, text, and completion state represented by the JSON so the synchronized current artifact/result reflects the update.

If the result is ambiguous, the target no longer resolves, either artifact cannot be read, or the intended and unaffected-state checks fail, stop without retrying a guessed mutation. Report the observed state and leave the authoritative plan for explicit reconciliation.

## Shared Plan Progress

Dev Orchestrator may require this plan, compare it with the bounded assignment, and follow material progress. It must inspect the authoritative path returned by Dev Coder without creating a second plan record. Work-item lifecycle, accepted commits, independent review, verification, integration, Persistence, and Commit evidence remain authoritative when they differ from plan state.

Update the same plan after a material discovery or completed development result changes the actionable decomposition. Preserve completed work and unaffected structure.

## Result

Return `CREATED`, `UPDATED`, or `PLAN_TOOL_UNAVAILABLE`; the authoritative JSON plan path; the invoked operation and target when applicable; the intended-change and unaffected-item checks; the current JSON and HTML check; discovered child or peer additions; and the development evidence supporting completion changes.
