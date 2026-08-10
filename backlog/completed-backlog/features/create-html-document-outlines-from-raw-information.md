# Create HTML Document Outlines from Raw Information

Owner: Dev Orchestrator task /root/create_document_outline

Status: Completed

Type: Feature

Provider: file

Work Item ID: create-html-document-outlines-from-raw-information

Completion: main-branch

## Summary

Create a portable create-document-outline skill that turns a large body of raw information into a source-traceable structured outline and renders it as reviewable HTML through mcp-agent-ops before full document authoring begins.

## Context

The mcp-agent-ops repository at commit ebc26f060c4a70d82a3a0cd4495ed37f76fefe62 includes a document-outline gallery example. Its Markdown source models a Product Requirements Document through nested headings and review text. The example converts that outline into structured data and renders a numbered, collapsible HTML hierarchy with the outline theme.

The gallery reference states that Markdown parsing belongs only to the example generator. The public renderer accepts structured Python data, JSON, YAML, or JSON/YAML files. It does not accept Markdown or raw document evidence directly. A methodology skill must therefore own evidence inventory, synthesis, section hierarchy, traceability, and the boundary between an outline and the final document.

The current hierarchy and plan APIs are direct Python APIs rather than MCP tools. Work Item use-mcp-hierarchy-plans-for-complex-development already owns the user decision and implementation boundary for exposing the underlying create and update behavior through the MCP server. This item must not duplicate that question or implement a separate server wrapper.

## Source Evidence

The user requested this work on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3:

> improve documentation writing by converting raw information into an html outline using the mcp-agent-ops to be used in preparation to creating a full document, and/or for human review. This is a new skill - creating a doc outline - to be used by agents that need to write documents when documents need to incorporate a lot of data.

Supporting evidence:

- /Users/martinbechard/dev/mcp-agent-ops/examples/hierarchy-gallery/data/document-outline.md supplies a complete nested document-outline example.
- /Users/martinbechard/dev/mcp-agent-ops/examples/hierarchy-gallery/generate_gallery.py converts headings and leaf review text into structured hierarchy data and rejects skipped levels, duplicate sibling headings, branch body text, and empty leaves.
- /Users/martinbechard/dev/mcp-agent-ops/examples/hierarchy-gallery/README.md documents the numbered, collapsible outline-theme HTML result and states that Markdown parsing is example-only.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/hierarchy-html-renderer.md documents safe structured inputs, self-contained HTML, numbering, progressive level controls, copy support, accessibility metadata, escaping, and path validation.

## Requirements

- Add one portable create-document-outline skill for document work whose source volume, topic breadth, contradictions, or review needs make a visible outline useful before prose authoring.
- Define a clear activation threshold so ordinary short documents do not require an outline artifact.
- Inventory all authorized raw inputs before synthesis and retain a source identity for every material outline section or unresolved question.
- Convert the evidence into structured JSON with a single document root, ordered sections, nested subsections, concise scope statements, source references, unresolved conflicts, and explicit missing information.
- Preserve the distinction between source facts, proposed organization, unresolved questions, and final-document decisions. Do not present outline synthesis as completed prose or verified source truth.
- Render a synchronized, self-contained HTML outline through the configured mcp-agent-ops server using numbering, progressive level controls, accessible tree semantics, complete copy support, and an appropriate document-review theme.
- Allow an agent or human reviewer to inspect the HTML outline before full document writing and record the accepted section order, required corrections, and remaining gaps.
- Revise the structured source and regenerate HTML when review changes the outline. Do not hand-edit the derived HTML.
- Require downstream document writing to consume the accepted outline together with the original source evidence. The outline must not replace source verification, document-type templates, provenance, or artifact-specific review.
- Define retention and cleanup rules for temporary outlines and durable placement rules when the user requests the outline as a deliverable.
- Route the skill conditionally to the primary document-producing and source-ingest Agents named in the approved manifest.
- Keep credentials, personal information, unauthorized proprietary content, and unnecessary raw payloads out of MCP inputs and rendered artifacts.

## Acceptance Criteria

- A large multi-source example produces a structured JSON outline and synchronized standalone HTML through MCP before final prose is written.
- Every material outline branch links to its source evidence or is explicitly labeled as a proposed organization, unknown, or conflict.
- The HTML shows the complete section hierarchy, preserves source order, supports progressive levels and copy, escapes untrusted text, and remains usable at narrow widths and with keyboard and assistive technology.
- Review corrections change the structured source and regenerated HTML without modifying original evidence or hand-editing the projection.
- The skill states when to use an outline, when not to use one, how to reconcile review feedback, and how the accepted outline feeds the selected document-writing methodology.
- Dev Documentation Writer, Wiki Writer, Wiki Ingester, and Methodology Maintainer use the skill only when its high-volume or high-complexity activation condition applies.
- Focused tests detect missing source coverage, duplicate or skipped hierarchy levels, branch text conflicts, empty leaves, unsafe output paths, stale HTML, and loss of unresolved questions.
- Independent methodology review and verification accept the integrated skill, routing, examples, and generated artifacts.

## Dependencies

- use-mcp-hierarchy-plans-for-complex-development

Blocker owner: Resolved by completed Work Item use-mcp-hierarchy-plans-for-complex-development.

Blocked to Ready condition: the dependency is Completed with typed MCP creation and rendering behavior that can produce the required structured JSON and synchronized HTML inside configured workspace roots.

Dependency Resolution: Satisfied on 2026-08-10. Work Item use-mcp-hierarchy-plans-for-complex-development is Completed and delivered the documented hierarchy-plan API, synchronized JSON and HTML behavior, focused tests, and repository integration required by this item.

Next Action: Dev Backlog Coordinator may reserve one separate Dev Orchestrator task for implementation under active sequential SOLO crisis recovery.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-10T19:48:53Z

Coordinator: parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Normalized Objective: Create, verify, integrate, and complete the portable create-document-outline skill and its approved routing and dependent artifacts.

Launch Result: Requested

Canonical Execution: Pending child task creation

Last Contact At: 2026-08-10T19:48:53Z

Next Reconciliation At: 2026-08-10T20:03:53Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task /root/create_document_outline

Evidence: The canonical root Dev Orchestrator accepted the Starting handoff and is implementing the approved document-outline skill as the single active SOLO crisis work-item task.

Observed At: 2026-08-10T19:49:51Z

Started At: 2026-08-10T19:49:51Z

Deadline or Expires At: 2026-08-10T21:49:51Z

Next Action: Implement the exact approved skill, routing, focused tests, generated artifacts, review, verification, delivery, and provider closure.

Next Reconciliation At: 2026-08-10T20:04:51Z

## Verification

- Validate skills/create-document-outline/SKILL.md through the configured skill validator.
- Run focused source-coverage and hierarchy-shape tests using multiple raw inputs, conflicting facts, missing evidence, and a corrected review pass.
- Run the MCP plan or hierarchy creation tool against an allowed temporary workspace and verify the paired JSON and HTML bytes.
- Verify structured rejection for unsafe paths, invalid hierarchies, duplicate siblings, skipped levels, empty leaves, stale projection state, and unauthorized input content.
- Regenerate and check affected skill documentation and conceptual Agent adapters from canonical sources.
- Run focused bundle assertions for the new skill, its conditional Agent routing, and its source-to-outline-to-document boundary.
- Verify the generated HTML with applicable accessibility, markup, link, overflow, and browser-console checks.
- Run Git diff checks for the exact integrated paths.

## Open Questions

- Which project-relative location should hold temporary source JSON and HTML outlines without turning them into provider records or permanent documentation by default?
- Should the skill define one generic source-reference field or reuse artifact-specific provenance identifiers when the selected document methodology already supplies them?

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-document-outline/SKILL.md
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml

### Allowed Dependent Artifacts

- skills/create-document-outline/agents/openai.yaml
- README.md
- scripts/test_bundle_content.py
- Generated skill documentation and conceptual Agent adapters produced by repository-authorized generators
- Focused non-governed outline examples, fixtures, and tests whose exact paths are resolved during implementation

### Approval Resolution

Approved at creation. The user explicitly requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 a new document-outline skill for Agents writing documents from large amounts of data. This approval covers exactly the governed canonical sources above. It does not authorize another governed skill or Agent definition.

## Notes

- The HTML outline is a preparation and review artifact, not the final document.
- The public renderer does not parse Markdown. The skill must create structured data from source evidence before invoking MCP.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.

## Completion Evidence

Completed At: 2026-08-10T21:13:18Z

Accepted Source Commit: 28627c0b421717b787035d82180cbddac6383c62

Main Delivery Commit: 6e9ad25976beb349220b13cff5c3df93e0c3df7c

Independent Review: Fresh methodology review returned GOOD. Fresh bounded final verification returned PASS / GOOD.

Verification Result: Focused helper, evaluation-documentation, bundle-routing, skill, provenance, metadata, generated-documentation, hierarchy, support-checklist, and diff checks accepted the candidate. Integrated-main checks confirmed the affected tests and generated projections. The current integration Python reports CAPABILITY_UNAVAILABLE when mcp-agent-ops is absent, as required, instead of installing or discovering another runtime.

Delivery Result: The accepted source commits were replayed onto a fresh integration branch and merged into main. The integrated skill, conditional role routing, focused probe, generated projections, and tests match the accepted candidate.

Archive Path: backlog/completed-backlog/features/create-html-document-outlines-from-raw-information.md
