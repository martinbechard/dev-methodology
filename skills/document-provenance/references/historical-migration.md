<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 52badfc3-ee93-4a3c-8aa8-b4195cacb745
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

# Historical Document Provenance Migration

Historical migration adds an explicit creation record to an existing governed document. It preserves supported facts and deterministically omits unsupported facts from compact HTML. Existing verbose historical comments remain valid for compatibility.

## Evidence Priority

Use the strongest retained evidence available for each field:

1. Use an immutable task or rollout record that names the exact artifact and dispatch.
2. Use Git only for a historical creation timestamp when repository history supports that conclusion. Preserve the evidenced local numeric offset when the retained timestamp contains it.
3. Put every unsupported compact-envelope field in Unknown-Facts; do not render a value or an evidence label for it.

Do not use the current adapter profile, configured model defaults, the Git author, a conversational nickname, or model self-report as historical execution evidence.

## Bounded Migration

1. Select an explicit bounded set of governed documents.
2. Record each supported compact fact as exactly `{"Value": "...", "Evidence": "..."}` in Known-Facts.
3. Preserve a retained Artifact-ID or assign one once with migration-assigned evidence.
4. Make Known-Facts and Unknown-Facts a disjoint, complete partition of Created-UTC, Created-Local, Creating-Agent, Runtime, Dispatched-Model, and Reasoning-Effort.
5. For compact HTML, add the exact doctype-adjacent Artifact-ID correlation comment and render only the copyright plus known reader fields in one semantic footer paragraph. Do not render unknown facts, evidence, Task-ID, or Created-UTC.
6. For a retained verbose historical block, keep `historical-unknown` and its matching evidence labels unchanged.
7. Run the validator with `--historical`. Supply schema version 2 for compact HTML; do not supply an envelope for a retained verbose historical block.
8. Review the evidence and validation result before acceptance.

Do not rewrite vendor documents, external captures, configuration, data, lock files, operational records, or unsupported formats during this audit.

## Git-Derived Creation Time

Git-derived means the selected timestamp comes from retained repository history for that exact document and the history establishes creation rather than only the first retained observation. It does not prove the creating Agent, runtime, model, effort, or task.

When history begins after the document was created, put Created-UTC and Created-Local in Unknown-Facts. Do not present the first retained commit as an exact creation time. When Created-Local and Created-UTC are both known, the validator requires them to represent the same instant.

## Compact Historical Envelope Example

```json
{
  "Record-Type": "historical",
  "Artifact-ID": "550e8400-e29b-41d4-a716-446655440000",
  "Artifact-ID-Evidence": "migration-assigned",
  "Known-Facts": {
    "Created-Local": {
      "Value": "2026-07-20T04:01:32-04:00",
      "Evidence": "git-derived"
    }
  },
  "Unknown-Facts": [
    "Created-UTC",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort"
  ]
}
```

Artifact-ID evidence is external even when it is migration-assigned. Task-ID remains optional and external. This shape makes omitted-known and displayed-unknown failures deterministic.

## Corrections

Creation provenance remains immutable during ordinary edits. Correct a false value only when project authority approves the correction and named retained evidence proves the replacement.

Preserve correction evidence in the completed review artifact or a project-selected append-only record. Do not silently rewrite historical metadata.

## Modification History

Git history is the default authority for ordinary modifications. A project-selected sidecar or append-only ledger may replace that default only when the project defines ownership, synchronization, and deterministic validation.
