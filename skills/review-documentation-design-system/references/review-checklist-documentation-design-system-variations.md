<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: dc318eba-c680-45aa-9dd5-c872320373f5
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

# Variation Audit Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-VAR-001 | The page defines a variation as multiple implementations of one concern, distinguishes valid families from unresolved inconsistency, and states that classifications apply only to the design system and do not change source files. | Hero/review-status text. |
| DDS-VAR-002 | The variation index links to exactly 21 uniquely identified comparisons, numbered 08.1–08.21, and every fragment resolves to its comparison heading. | Link/ID/number inventory and fragment-resolution check. |
| DDS-VAR-003 | Shell comparisons cover section navigation, section headings, five hero compositions, and footer content; hero status marks default as standard, two-column as optional, other compositions as review variants, and footer versioning as resolved. | 08.1–08.4 headings, specimen inventory, and decision-label text. |
| DDS-VAR-004 | Visual-foundation comparisons cover three themes, two token-name families, five maximum widths (1120–1240px), and three title-scale families (3.55–5.8rem). | 08.5–08.8 value/specimen inventory. |
| DDS-VAR-005 | Component comparisons cover generic/domain cards, status/badge/tag families, three table-overflow owners, and four code treatments. | 08.9–08.12 class/owner/treatment inventory. |
| DDS-VAR-006 | Implementation comparisons cover embedded/shared/injected CSS, inline declarations versus named classes, settings injection, uneven creation provenance, and all nine documented breakpoints from 520 through 900px. | 08.13–08.17 source/specimen/value inventory. |
| DDS-VAR-007 | Coverage comparisons report nine index cards versus ten detail pages, one versus missing skip links, nine explicitly labeled heroes versus one visual-only hero, and five print-enabled surfaces versus browser defaults. | 08.18–08.21 count and source evidence checked against the authoritative snapshot. |
| DDS-VAR-008 | Every unresolved comparison visibly supplies at least two rendered/source specimens, provenance, a concrete advantage, and a concrete disadvantage; it does not silently choose a winner. | Per-comparison completeness matrix. |
| DDS-VAR-009 | Every adopted, partly classified, or resolved decision is visibly labeled and links to or states its usage contract; specimens retained only for audit are not described as recommended components. | Decision-label and cross-link inventory. |
