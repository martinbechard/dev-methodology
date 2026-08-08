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

Historical migration adds an explicit creation record to an existing governed document. It preserves known facts and labels every unsupported fact as historical-unknown.

## Evidence Priority

Use the strongest retained evidence available for each field:

1. Use an immutable task or rollout record that names the exact artifact and dispatch.
2. Use Git only for a historical Created-UTC value when repository history supports that conclusion.
3. Use historical-unknown when no stronger evidence exists.

Do not use the current adapter profile, configured model defaults, the Git author, a conversational nickname, or model self-report as historical execution evidence.

## Bounded Migration

1. Select an explicit bounded set of governed documents.
2. Record the source and strength of evidence for each creation field.
3. Preserve a retained Artifact-ID or assign one once with migration-assigned evidence.
4. Add the canonical block at the format-specific location.
5. Use historical-unknown for every unsupported field.
6. Run the validator with historical state.
7. Review the evidence and validation result before acceptance.

Do not rewrite vendor documents, external captures, configuration, data, lock files, operational records, or unsupported formats during this audit.

## Git-Derived Creation Time

Git-derived means the selected timestamp comes from retained repository history for that document. It does not prove the creating Agent, runtime, model, effort, or task.

When history begins after the document was created, use historical-unknown for Created-UTC. Do not present the first retained commit as an exact creation time.

## Corrections

Creation provenance remains immutable during ordinary edits. Correct a false value only when project authority approves the correction and named retained evidence proves the replacement.

Preserve correction evidence in the completed review artifact or a project-selected append-only record. Do not silently rewrite historical metadata.

## Modification History

Git history is the default authority for ordinary modifications. A project-selected sidecar or append-only ledger may replace that default only when the project defines ownership, synchronization, and deterministic validation.
