<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 21ebeca5-4d3d-4588-8103-8720ad69e501
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

# Shared Page Checklist

Apply these checks to every conforming design-system HTML page before its page-specific checklist.

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-COM-001 | The document declares HTML, lang="en", UTF-8, a responsive viewport, a non-empty title, and a stylesheet link to the design-system CSS. | Source lines showing the doctype, html, required metadata, title, and stylesheet URL. |
| DDS-COM-002 | The design-system-version metadata and visible .ds-version footer text contain the same exact version, and that version exactly matches the canonical design/documentation-design-system/VERSION value; neither value says latest or uses a range. | The three literal values with file/line or DOM evidence. |
| DDS-COM-003 | A keyboard-focusable skip link precedes repeated navigation and moves focus/location to the unique main#main-content. | Source selectors plus a browser keyboard trace showing the first Tab and activation result. |
| DDS-COM-004 | The brand header contains one linked product identity and a logo with meaningful alternative text; the suite navigation follows the header and has a distinct accessible name. | DOM/source evidence for header, brand link, logo alt, navigation order, and aria-label. |
| DDS-COM-005 | Suite navigation exactly matches the caller-supplied expected navigation inventory for visible labels, href values, order, and current-page href; it uses anchors, marks exactly that current page with aria-current="page", and wraps without obscuring labels at narrow width. | Exact label/href/order comparison against the supplied inventory, current-link selector, and desktop/narrow screenshots or DOM plus computed-layout evidence. |
| DDS-COM-006 | There is exactly one h1; every content section with aria-labelledby resolves to a unique visible heading; landmarks and visual reading order match DOM reading order. | Heading/ID inventory and DOM-order inspection. |
| DDS-COM-007 | The page begins at body#top; section navigation uses an anchor to #top; links and controls have visible three-pixel-equivalent :focus-visible treatment and remain keyboard reachable. | Source/computed-style evidence and keyboard trace. |
| DDS-COM-008 | At narrow width, padding reduces as needed, navigation wraps, columns and complex structures stack, and wide tables scroll inside a dedicated wrapper without losing content or interaction. | Viewport width and screenshots or measured overflow/layout evidence; identify every checked component. |
| DDS-COM-009 | Meaning is not conveyed by color alone; icon-only controls are named; decorative glyphs are hidden from accessibility APIs; meaningful visuals have text alternatives. | Accessible-name/role inspection for each applicable component. |
| DDS-COM-010 | The footer follows main, visibly states the design-system version, and includes truthful page-specific provenance, scope, or compatibility context. | Source/DOM evidence for order and exact footer text. |
