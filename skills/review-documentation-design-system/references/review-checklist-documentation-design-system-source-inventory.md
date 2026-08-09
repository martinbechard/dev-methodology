<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 7dbe5299-9dd1-4fb5-96cd-d2da51c05dbc
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

# Source Inventory Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-INV-001 | The hero names the repository, full source commit, and audit date; those values identify an available immutable snapshot. | Exact values plus successful revision-resolution evidence. |
| DDS-INV-002 | The primary-page table contains all 11 audited documentation pages and, for each, records source path, theme, section-navigation family, and distinctive elements. | Row/column inventory compared with tracked HTML at the declared commit. |
| DDS-INV-003 | The styled backlog report is classified as a tracked output example, lists its contributions, and explicitly excludes brand header, sequence, hero, section navigation, shared settings, and footer from its boundary. | Report card text and source inspection. |
| DDS-INV-004 | Exactly four fixtures are classified as test sources, with source path, purpose, and represented elements; the negative accessibility fixture is not classified as production styling. | Fixture table inventory and source inspection. |
| DDS-INV-005 | Element coverage includes metadata/viewport; skip/header/brand/main/sections/navigation/hero; h1–h4 and prose semantics; lists; articles/asides/cards/panels/callouts/notes; code/trees; tables; metrics/labels; forms/actions/live feedback/dialog; figures/SVG/CSS diagrams/object fallback; and responsive/print behavior. | Coverage-list mapping to live examples in the nine concern pages. |
| DDS-INV-006 | The audit method lists tracked *.html, compares tracked and live files, classifies each surface, extracts semantic/style/asset/script data, inspects unique/accessibility structures, and records common patterns and variations with sources, pros, and cons. | Ordered method steps and reproducible command/output evidence. |
| DDS-INV-007 | Counts reconcile 17 tracked HTML files into 16 design-relevant sources and one excluded format-only fixture: 11 primary pages, one report example, four interaction fixtures, and one provenance-validator fixture, with no duplicate or unclassified path. | Machine-readable tracked-file list and one-to-one classification reconciliation. |
| DDS-INV-008 | Every source path exists at the declared commit, and every stated distinctive element, count, theme, navigation type, or behavior is directly observable there. | Per-row source evidence or deterministic extraction output. |
| DDS-INV-009 | The page records the excluded provenance-validator fixture and states that the audit does not modify, stage, or overwrite included or excluded source content. | Audit command scope and exact visible boundary statement. |
