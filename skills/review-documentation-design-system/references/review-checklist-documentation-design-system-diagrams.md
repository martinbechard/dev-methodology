<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 5e1cf78a-31db-4b52-8b4a-03084ba9c483
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

# Diagrams Page Checklist

| ID | Observable pass criterion | Required evidence |
| --- | --- | --- |
| DDS-DGM-001 | A horizontal flow presents ordered stages and direction, has a complete text alternative, and stacks in the same order at narrow width. | DOM order, accessible name, and desktop/narrow rendering evidence. |
| DDS-DGM-002 | A lifecycle rail uses semantic ordered data; every station includes a number, label, and short outcome and preserves left-to-right meaning in its text alternative. | ol/item inventory and accessible-name/description evidence. |
| DDS-DGM-003 | Every block-entry connector stops before the block and uses a separate reusable short-stem arrow on the entrance centerline; no entering connector uses marker-end. | SVG source/path/symbol inspection and rendered close-up. |
| DDS-DGM-004 | Ordinary and combined-flow arrows are defined once with symbol and placed with use; the combined-flow arrow is visibly stronger without changing the semantic meaning. | SVG definition/use inventory and computed/rendered comparison. |
| DDS-DGM-005 | Entrance geometry is reproducible from destination boundary B and centerline C: connector end B-18, arrow at (C-7, B-18), and tip at B; specimens show a 9-unit stem and 9-unit head. | Coordinate calculation matched to actual SVG attributes and rendered boundary contact. |
| DDS-DGM-006 | Fan-out uses independent non-crossing routes and one arrow per destination; fan-in routes all inputs to one convergence point and uses one strong arrow with no collector rail. | Path topology inspection and rendered correct/incorrect specimen comparison. |
| DDS-DGM-007 | Connector paths use rounded caps, smooth curves, consistent related color/weight, clear label whitespace, no unintended intersections, no doubled/detached/clipped segments, and no arrowhead inside a block at desktop or narrow width. | Source/computed styles and screenshots at both widths. |
| DDS-DGM-008 | A folder tree represents containment using preserved preformatted structure rather than a path-comparison table. | DOM/text evidence and rendered whitespace check. |
| DDS-DGM-009 | Each meaningful diagram is a figure with adjacent visible figcaption and a relationship-focused text equivalent; SVGs have title and desc, CSS visuals use role="img" with text, and decorative geometry is hidden. | Figure/caption/accessible-name inventory for every diagram. |
| DDS-DGM-010 | Embedded maintained images use object fallback content that remains a usable link or equivalent text when the object cannot load. | Source markup and failed-object rendering test. |
