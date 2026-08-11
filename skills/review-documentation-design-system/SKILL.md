---
name: review-documentation-design-system
description: Review a documentation HTML page against the adopted Documentation Design System v0.1.1 contracts and return evidence-backed pass or fail results. Use for design-system conformance reviews of an index, foundation, shell, content, data-display, form, diagram, accessibility, variation-audit, or source-inventory page.
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
- Exactly one supplied checklist from this skill's references.
- The design-system version it claims.
- For the Shared checklist, the expected suite-navigation inventory as each visible label and href in exact order, plus the current-page href.
- Browser access when behavior or responsive rendering is in scope.

The caller must supply one nonblank page identity, one nonblank checklist identity, and the exact unique expected-ID inventory. A missing, ambiguous, malformed, or whitespace-only identity is a caller-owned pre-dispatch BLOCKED condition; do not invoke the checklist runner or choose an identity silently.

For a Shared-checklist invocation, the caller must also supply the target page's expected suite-navigation inventory. Each visible label and href must be nonblank, each href must be unique, and the current-page href must identify exactly one inventory entry. A missing, malformed, or ambiguous navigation inventory is a caller-owned pre-dispatch BLOCKED condition. Do not substitute labels or destinations from a design-system specimen.

Use NOT TESTED only after the exact page, checklist, and expected-ID inventory exists and required source, rendered, responsive, keyboard, or other review evidence cannot be obtained. Name that missing evidence; do not infer conformance.

## Workflow

1. Open exactly the checklist supplied for this invocation. Do not add the Shared checklist or a page-type checklist automatically.
2. Inspect source for semantic, metadata, link, and text requirements.
3. Inspect the rendered page at desktop and narrow width for visual and behavioral requirements. Exercise keyboard interactions when the page contains controls.
4. Record every checklist ID as PASS, FAIL, or NOT TESTED. Use NOT TESTED only when required evidence cannot be obtained, and name the missing evidence.
5. For each result, cite concrete evidence: file and line, DOM selector or snippet, browser viewport, interaction performed, screenshot, or audit command and output.
6. Return NOT TESTED when any assigned item lacks evidence, including when another item fails. Otherwise return FAIL when any item fails, and PASS only when every assigned item passes.

For a standalone full-page review, the caller schedules separate invocations for the Shared checklist and the applicable page-type checklist. Each invocation remains one page and one checklist.

## Page Checklists

- [Shared](references/review-checklist-documentation-design-system-shared.md)
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

When the caller supplies a strict output contract, return only that contract's fields and nested shapes. Do not add the prose or table below to a role-owned strict response.

As the standalone fallback when no strict caller contract applies, report the page, claimed version, overall result, and a table with ID, Result, Evidence, and Remediation. Keep remediation specific to failed criteria. End with untested evidence and remaining uncertainty.
