---
name: documentation-page-verify
description: Use when verifying mixed, unknown, custom, or shared methodology documentation concerns that do not have a clearer artifact-specific review skill.
metadata:
  category: documentation-methodology
---

# Documentation Page Verify

Use this skill for shared methodology documentation checks when the artifact type is mixed, unknown, custom, or not covered by a clearer artifact-specific review skill. The verifier checks that a page is source-backed, format-appropriate, steady-state, and useful to future agents.

## Prefer Artifact-Specific Review

- Use project-wiki-review for project wiki pages and project-wiki-template artifacts.
- Use review-functional-spec for functional specification artifacts.
- Use review-architecture for architecture artifacts.
- Use review-high-level-design for high-level design artifacts.
- Use review-module-design for module design artifacts.

## Verification Inputs

- The page being verified.
- The matching template from development-methodology assets.
- The completed review checklist when an artifact-specific review skill produced one.
- Related source files, tests, procedures, backlog items, wiki pages, and project metadata.
- Project-specific documentation rules from AGENTS.md or procedures.

## Format Selection

Before checking sections, identify the selected structure from the user request, file type, runtime schema, existing document, surrounding documentation, or methodology template.

When a specific structure or format is indicated, that structure is authoritative. Verify source support, links, steady-state prose, completeness, diagrams, and unresolved questions within the indicated format. Do not require shared page sections unless the selected artifact is a docs/wiki page, a project wiki methodology artifact, or another methodology template that explicitly uses the shared page contract.

Examples of format-owned artifacts include design HTML pages, README files, runtime adapter profiles, generated data files, native agent definition files, package metadata, and vendor schema documents.

## Completed Review Checklist Evidence

When a completed review checklist is available, use it as the evidence record for verification.

1. Read the completed review checklist before writing the assessment.
2. Check that each applicable item has status, question, quoted evidence, and assessment.
3. Use the quoted evidence to complete shared page contract, source authority, link, diagram, and steady-state verification.
4. Re-read the cited source text when quoted evidence is unclear, incomplete, or contradicted.
5. Do not complete verification from memory or from the checklist question text alone.
6. Base the final assessment on the completed review checklist plus any source text rechecked during verification.

## Shared Page Contract

Apply this section only when the selected artifact type uses the shared page contract. When a specific non-wiki structure is indicated, skip this section and verify the indicated format instead.

For shared-page-contract artifacts, confirm the page starts with these sections in this order:

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
