<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 0b7a6eef-de34-488e-957d-11788f18314d
Created-UTC: 2026-08-08T18:22:49Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe291-1ba8-7a43-8d21-391a04dfa9a9
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Document Provenance Format Contract

The provenance record is one line-oriented HTML comment. The field labels are exact and case-sensitive.

## Canonical New-Document Block

```markdown
<!--
Copyright (c) 2026 Example
Artifact-ID: 550e8400-e29b-41d4-a716-446655440000
Created-UTC: 2026-08-08T18:00:00Z
Creating-Agent: Wiki Writer
Runtime: Codex
Dispatched-Model: example-model
Reasoning-Effort: high
Task-ID: task-example-001
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->
```

Replace the illustrative copyright statement with the exact project-authorized statement. The external runtime envelope must contain the same seven creation values.

## Field Rules

| Field | New-document rule | Historical rule |
| --- | --- | --- |
| Artifact-ID | Use the runtime-supplied durable identifier. | Preserve retained identity or assign one during migration and label it migration-assigned. |
| Created-UTC | Use a runtime-supplied ISO 8601 timestamp with the Z or +00:00 UTC offset. | Use retained execution evidence, a Git-derived timestamp, or historical-unknown. |
| Creating-Agent | Use the dispatched conceptual Agent identity. | Use retained task or rollout evidence, or historical-unknown. |
| Runtime | Use the dispatching harness identity. | Use retained task or rollout evidence, or historical-unknown. |
| Dispatched-Model | Use the model selected for dispatch. | Use retained task or rollout evidence, or historical-unknown. |
| Reasoning-Effort | Use the effort selected for dispatch. | Use retained task or rollout evidence, or historical-unknown. |
| Task-ID | Use the stable task or execution identity. | Use retained task or rollout evidence, or historical-unknown. |

The allowed evidence labels are:

- runtime-supplied for a value supplied by the dispatching coordinator or harness;
- retained-task-evidence for a value recovered from an immutable task record;
- retained-rollout-evidence for a value recovered from an immutable rollout record;
- migration-assigned for an Artifact-ID created during migration;
- git-derived for a historical Created-UTC value derived from Git;
- historical-unknown when no stronger evidence supports the historical value.

Current profile mappings, configured defaults, self-report, conversational nicknames, and Git authorship are not allowed evidence labels.

## Placement

Markdown with front matter keeps this order:

```markdown
---
type: "Technique"
title: "Example"
---
<!-- provenance block -->
# Example
```

Markdown without front matter starts with the provenance block. A reserved project-wiki index.md or log.md follows the same no-front-matter rule.

Maintained HTML keeps this order:

```html
<!doctype html>
<!-- provenance block -->
<html lang="en">
```

The provenance comment does not own the Markdown front matter or HTML metadata.

## Runtime Envelope

The validator accepts a JSON envelope with schema version 1 and a records array. Each record contains the seven creation fields with exact labels. Use [the bundled schema](../assets/provenance-envelope.schema.json) for deterministic envelope generation.
