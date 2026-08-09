---
name: review-documentation-design-system
description: Review a documentation HTML page against the adopted Documentation Design System v0.1.0 contracts and return evidence-backed pass or fail results. Use for design-system conformance reviews of an index, foundation, shell, content, data-display, form, diagram, accessibility, variation-audit, or source-inventory page.
metadata:
  category: documentation-methodology
---

<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 581a34af-d5ea-420c-9a26-bfaae0277e33
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

# Review Documentation Design System

Review one rendered HTML page and its source. Do not treat the audit examples in variations.html as adopted patterns unless that page explicitly marks them adopted or resolved.

## Inputs

- The HTML file or rendered URL under review.
- Its intended page type.
- The design-system version it claims.
- Browser access when behavior or responsive rendering is in scope.

If the page type or claimed version is unavailable, report that as missing evidence; do not infer conformance.

## Workflow

1. Open [review-checklist-documentation-design-system-shared.md](references/review-checklist-documentation-design-system-shared.md) and the one page-type checklist listed below.
2. Inspect source for semantic, metadata, link, and text requirements.
3. Inspect the rendered page at desktop and narrow width for visual and behavioral requirements. Exercise keyboard interactions when the page contains controls.
4. Record every checklist ID as PASS, FAIL, or NOT TESTED. Use NOT TESTED only when required evidence cannot be obtained, and name the missing evidence.
5. For each result, cite concrete evidence: file and line, DOM selector or snippet, browser viewport, interaction performed, screenshot, or audit command and output.
6. Return an overall PASS only when every applicable item passes. Any FAIL or NOT TESTED prevents an overall pass.

## Page Checklists

- [Index](references/review-checklist-documentation-design-system-index.md)
- [Foundations](references/review-checklist-documentation-design-system-foundations.md)
- [Page shell](references/review-checklist-documentation-design-system-page-shell.md)
- [Content](references/review-checklist-documentation-design-system-content.md)
- [Data display](references/review-checklist-documentation-design-system-data-display.md)
- [Forms and actions](references/review-checklist-documentation-design-system-forms-and-actions.md)
- [Diagrams](references/review-checklist-documentation-design-system-diagrams.md)
- [Accessibility and responsive behavior](references/review-checklist-documentation-design-system-accessibility.md)
- [Variation audit](references/review-checklist-documentation-design-system-variations.md)
- [Source inventory](references/review-checklist-documentation-design-system-source-inventory.md)

## Result Format

Report the page, claimed version, overall result, and a table with ID, Result, Evidence, and Remediation. Keep remediation specific to failed criteria. End with untested evidence and remaining uncertainty.
