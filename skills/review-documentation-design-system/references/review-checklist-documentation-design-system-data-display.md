<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 432c07ce-5aa2-45a5-9f7e-f8b146b88a31
Created-UTC: 2026-08-09T00:26:37Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe3cd-577c-76b1-965c-06fb8793ae42
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Data Display Page Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-DAT-001 | A table is used only for records sharing the same fields and includes semantic headers; wide tables retain native table display inside a dedicated horizontal-overflow wrapper. | Table DOM, header association, computed display, wrapper overflow, and narrow viewport evidence. |
| DDS-DAT-002 | Each metric has exactly one prominent value and one short interpretation and is used for a count, ratio, limit, or current state. | Metric DOM/content inventory. |
| DDS-DAT-003 | Statuses, badges, and tags are non-interactive labels whose visible text carries verdict, workflow-state, or taxonomy meaning without relying on color. | Role/link audit, text/color comparison, and accessibility-tree evidence. |
| DDS-DAT-004 | Pill-shaped navigation remains an anchor and is not mislabeled or implemented as a status/badge. | DOM evidence for every pill-shaped interactive specimen. |
| DDS-DAT-005 | Catalog cards contain repeated narrative records that need more content than table cells and expose a consistent record structure across peers. | Field/content mapping across all catalog specimens. |
| DDS-DAT-006 | Structured metadata uses a description list with explicit term/value pairs instead of prose forced into a comparison table. | dl/dt/dd DOM inventory and visible rendering. |
| DDS-DAT-007 | Source notes identify the observed metric, table, and compact-label families and explicitly acknowledge unresolved naming/overflow variants. | Visible source and variation statements. |
