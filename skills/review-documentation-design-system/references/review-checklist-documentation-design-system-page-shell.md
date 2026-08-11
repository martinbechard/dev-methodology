<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: f1857779-84d0-49e6-be92-5012c56886fd
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

# Page Shell Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-SHL-001 | The anatomy example presents skip link, brand header, suite navigation, main#main-content, sequence navigation, hero, section navigation, content section, and footer in that order. | Parsed example or visible code block showing the complete ordered anatomy. |
| DDS-SHL-002 | Suite navigation is explicitly adopted for every multi-page suite, uses illustrative labels and destinations only in specimens, uses the target suite's authoritative navigation inventory, uses anchors rather than badges, exposes exactly one current page, retains stable labels/order, and wraps before resorting to horizontal scrolling. | Guidance text, specimen classification, target-inventory statement, specimen DOM, and narrow-width rendering evidence. |
| DDS-SHL-003 | Each detail page has named sequence navigation with previous and next anchors using rel="prev" and rel="next"; boundary links correctly connect the index and final inventory back into the sequence. | Link/rel inventory for the page and, when reviewing the suite, a complete sequence traversal. |
| DDS-SHL-004 | The default hero has an optional eyebrow, one h1 page title, a short scope lede, and aria-labelledby resolving to that title. | Specimen/source markup and resolved accessible name. |
| DDS-SHL-005 | A two-column hero is used only for a page-wide principle, scope boundary, evidence limitation, or source snapshot; its title column precedes the named aside and stacks above it at narrow width. | Content classification, DOM order, accessible name, and narrow screenshot/layout evidence. |
| DDS-SHL-006 | Section navigation starts with a #top link, stays visible at wide width, becomes a wrapping non-sticky block at narrow width, and all targets resolve to visible sections. | Link-target audit plus wide/narrow computed-position and rendering evidence. |
| DDS-SHL-007 | Section hierarchy uses either a direct h2 or a grouped .section-heading with summary; heading levels remain sequential within subsections. | Heading outline and section-markup inspection. |
| DDS-SHL-008 | The versioning section accurately defines the required exact metadata/footer pairing and the major/minor/patch compatibility rules, while distinguishing source commit provenance from design-system version. | Exact visible requirements and comparison of metadata, footer, and VERSION. |
