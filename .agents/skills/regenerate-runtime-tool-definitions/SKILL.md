---
name: regenerate-runtime-tool-definitions
description: Regenerate the repository-private, harness-specific catalog of Codex-native and generic runtime tool definitions when reviewing tool availability or preparing tool-aware Agent and skill design.
metadata:
  category: project-maintenance
---

# Regenerate Runtime Tool Definitions

Maintain a reviewable Codex tool catalog without injecting it into Agent definitions or changing tool authorization.

## Outputs

The generated catalog is rooted at references/tools:

- index.md is the sole index. It inventories every included tool, grouped by tool family, and links directly to each tool file.
- Each tool has exactly one Markdown file containing its live name, surface, source, and definition.

The canonical snapshot is references/tool-definitions.json. Generated Markdown is replaceable output; change the snapshot or generator rather than hand-editing it.

## Scope

Include Codex-native and generic runtime tools. Exclude connected-product families and project-specific extensions such as GitHub, Google, Sites, Vercel, Greptile, Agent Report, and agent-ops.

Keep direct runtime tools in the snapshot because they are not returned by ALL_TOOLS. Review those entries when the harness changes its direct tool surface.

## Regeneration

Use an execution-dispatcher call to serialize the complete live ALL_TOOLS array as JSON into one disposable file under .agents/temp. Create and remove that file through apply_patch. Capture mode applies the skill-owned selection rule, preserves reviewed direct-tool entries, updates the snapshot atomically, and regenerates the Markdown catalog.

The execution call should:

1. Create a task-specific .agents/temp subfolder and add all-tools.json containing the complete live ALL_TOOLS JSON array. Each object needs name and description.
2. Run this command from the repository root, substituting the exact temporary path:

```text
python3 .agents/skills/regenerate-runtime-tool-definitions/scripts/generate.py --capture-file .agents/temp/<task>/<utc>/all-tools.json
```

3. Delete the task-specific temporary subfolder after successful or failed capture.

Do not filter the temporary registry or paste connector filtering into the calling prompt. The generator owns selection so repeated captures remain consistent. Do not use shell redirection, terminal input, or a command argument for the registry; the live payload is too large for those boundaries to be reliable.

After capture, inspect references/tools/index.md and run:

```text
python3 .agents/skills/regenerate-runtime-tool-definitions/scripts/generate.py --check
python3 .agents/skills/regenerate-runtime-tool-definitions/scripts/test_generate.py
```

## Consumer Boundary

This catalog is evidence for later harness-aware design. Do not automatically add every tool to Dispatching, Dev Orchestrator, another skill, or a generated Agent definition. A later design must decide stable capability identifiers, selection ownership, authorization semantics, freshness, and whether large definitions are injected or discovered on demand.

When a consumer needs one tool, read that tool's generated file. Read the whole-set index for selection work; do not load every tool file into context by default.

## Result

Report the snapshot date, included tool count, group count, added or removed tools, validation result, and whether direct-tool definitions require manual review.
