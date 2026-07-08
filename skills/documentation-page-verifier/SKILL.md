---
type: Skill
name: documentation-page-verifier
description: Use when verifying functional specs, architecture, high-level design, module design, project wiki subclasses, or methodology template outputs.
---

# Documentation Page Verifier

Use this skill before finishing specialized software documentation pages or methodology template outputs. The verifier checks that a page is source-backed, wiki-compatible, steady-state, and useful to future agents.

## Verification Inputs

- The page being verified.
- The matching template from development-methodology assets.
- Related source files, tests, procedures, backlog items, wiki pages, and project metadata.
- Project-specific documentation rules from AGENTS.md or procedures.

## Shared Page Contract

Confirm the page starts with the shared sections in this order:

1. Current Understanding
2. Authoritative Sources
3. Related Code
4. Related Tests
5. Related Backlog Items
6. Related Wiki Pages
7. Open Questions
8. Maintenance Notes

Each section must contain source-backed content or a clear Not yet identified entry. Open Questions may state that no open questions are recorded only when the evidence supports that.

## Source And Link Checks

1. Confirm claims cite the strongest available source at the point where the prose depends on it.
2. Prefer code and tests for actual behavior.
3. Use functional specifications and requirements for intended behavior.
4. Use procedures and agent instructions for workflow obligations.
5. Use backlog files for tracked work and known status.
6. Use architecture, high-level design, module design, and plans for design intent.
7. Use wiki pages as synthesis and navigation, not as the highest authority.
8. Check that Related Code and Related Tests are project-relative or explicitly marked as not yet identified.
9. Check that source links resolve when the repository is available.

## Specialized Section Checks

Functional specifications should describe actors, entry points, workflow steps, states, permissions, edge cases, acceptance behavior, and verification from the user's point of view.

Architecture documents should describe system purpose, scope, context, technology stack, file organization, layers, dependency direction, major components, cross-cutting concerns, invariants, risks, trade-offs, and verification.

High-level designs should describe a complete subsystem or feature family, constituent components, interaction model, lifecycle, data contracts, configuration ownership, implementation order, invariants, non-goals, definition of good, and verification.

Module designs should describe one implementation unit, runtime path, parent context, responsibilities, callers, dependencies, public contracts, internal state, processing rules, invariants, configuration, external interfaces, UI behavior when applicable, error handling, and verification.

Project wiki subclass pages should maintain durable synthesis and navigation without silently replacing the specialized source document when one exists.

## Diagram Checks

Diagrams are useful only when they clarify a real structure:

- Sequence or handoff.
- Association.
- Aggregation or containment.
- Dependency.
- Lifecycle.
- Data movement.
- Ownership or responsibility.
- Verification coverage.

Confirm Mermaid or another editable source remains authoritative. Rendered SVG artifacts may be linked as companions, but they should not be the only maintained source.

## Steady-State Checks

1. Remove unresolved TODO markers unless the page intentionally remains a template.
2. Avoid framing the page around a previous version unless the section is explicitly historical.
3. Replace comparative terms such as enhanced, revised, old, and new when they imply unstated prior context.
4. Keep implementation detail out of functional specifications unless the user needs it to understand behavior.
5. Keep broad architecture pages from duplicating every module detail.
6. Keep module pages focused on one coherent responsibility.

## Output

Return findings first, ordered by severity, when verification finds problems. Include file paths and section names. If no problems are found, say that the page passes verification and name any residual test or source gaps.
