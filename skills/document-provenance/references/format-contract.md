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

New documents use a compact reader-facing representation and a schema-version-2 external envelope. Existing package documents keep their verbose provenance comments and schema-version-1 records through the legacy route. Field labels and HTML markers are exact and case-sensitive.

## Canonical New-Document Block

```markdown
<!--
Copyright (c) 2026 Example
Artifact-ID: 550e8400-e29b-41d4-a716-446655440000
Created-Local: 2026-08-08T14:00:00-04:00
Creating-Agent: Wiki Writer
Runtime: Codex
Dispatched-Model: example-model
Reasoning-Effort: high
-->
```

Replace the illustrative copyright statement with the exact project-authorized statement. Keep this exact field order. The external record contains the same six creation values, machine-only Created-UTC, Record-Type `new`, and optionally Task-ID. Created-Local and Created-UTC must represent the same instant.

## Canonical New-Document HTML

Place only this correlation comment after the doctype:

```html
<!doctype html>
<!-- Document-Provenance Artifact-ID: 550e8400-e29b-41d4-a716-446655440000 -->
<html lang="en">
```

Place exactly one provenance paragraph inside the document footer. Each reader field uses its exact marker. Created-Local uses a `time` element whose visible value equals its `datetime` value.

```html
<footer>
  <p data-document-provenance="v2">
    <span data-provenance-field="Copyright">Copyright (c) 2026 Example</span>
    <time data-provenance-field="Created-Local" datetime="2026-08-08T14:00:00-04:00">2026-08-08T14:00:00-04:00</time>
    <span data-provenance-field="Creating-Agent">Wiki Writer</span>
    <span data-provenance-field="Runtime">Codex</span>
    <span data-provenance-field="Dispatched-Model">example-model</span>
    <span data-provenance-field="Reasoning-Effort">high</span>
  </p>
</footer>
```

Do not expose Artifact-ID, Task-ID, Created-UTC, evidence labels, or unknown markers in the visible footnote. The validator requires one correlation comment, one footer descendant with `data-document-provenance="v2"`, one occurrence of every required field, and exact equality with the correlated external record.

## Field Rules

| Field | New-document rule | Compact historical HTML rule |
| --- | --- | --- |
| Artifact-ID | Use the runtime-supplied durable identifier. | Preserve retained identity or assign one during migration and label it migration-assigned. |
| Created-Local | Render the runtime-supplied ISO 8601 timestamp with an explicit numeric UTC offset other than `Z`. | Render only when the external record identifies it as known with retained evidence. |
| Created-UTC | Keep the machine-only `Z` timestamp in the external envelope; it must equal the Created-Local instant. | Keep it external; when both timestamps are known, they must represent the same instant. |
| Creating-Agent | Use the dispatched conceptual Agent identity. | Use retained task or rollout evidence, or historical-unknown. |
| Runtime | Use the dispatching harness identity. | Use retained task or rollout evidence, or historical-unknown. |
| Dispatched-Model | Use the model selected for dispatch. | Use retained task or rollout evidence, or historical-unknown. |
| Reasoning-Effort | Use the effort selected for dispatch. | Use retained task or rollout evidence, or historical-unknown. |
| Task-ID | Keep an optional stable task or execution identity in the external record only. | Keep an optional retained task identity in the external record only. |

Historical envelope facts use these evidence labels:

- runtime-supplied for a value supplied by the dispatching coordinator or harness;
- retained-task-evidence for a value recovered from an immutable task record;
- retained-rollout-evidence for a value recovered from an immutable rollout record;
- migration-assigned for an Artifact-ID created during migration;
- git-derived for a historical Created-UTC value derived from Git;

Unknown facts have no value or evidence object. List their exact field names in Unknown-Facts instead. Known-Facts and Unknown-Facts must be disjoint and together cover Created-UTC, Created-Local, Creating-Agent, Runtime, Dispatched-Model, and Reasoning-Effort.

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

Maintained HTML keeps this order and adds the semantic footer described above:

```html
<!doctype html>
<!-- Document-Provenance Artifact-ID: ... -->
<html lang="en">
```

The provenance comment does not own the Markdown front matter or HTML metadata.

## Runtime Envelope And Routes

The validator uses three explicit routes:

- `--new` accepts compact Markdown or HTML and requires a schema-version-2 `new` record.
- `--legacy` accepts an unchanged verbose legacy block and requires its schema-version-1 record.
- `--historical` accepts either a verbose legacy historical block without an envelope or compact historical HTML with a schema-version-2 `historical` record.

Schema version 2 uses a bounded `Record-Type` union. A `new` record contains Artifact-ID, Created-Local, Created-UTC, Creating-Agent, Runtime, Dispatched-Model, Reasoning-Effort, and optional Task-ID. A `historical` record contains Artifact-ID, Artifact-ID-Evidence, Known-Facts, Unknown-Facts, and optional Task-ID. Use [the bundled schema](../assets/provenance-envelope.schema.json) for deterministic envelope generation.
