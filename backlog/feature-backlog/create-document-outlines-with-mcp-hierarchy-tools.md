# Create Document Outline Skill with MCP Hierarchy Tools

Status: Ready

Type: Feature

Provider: file

Work Item ID: create-document-outlines-with-mcp-hierarchy-tools

Completion: main-branch

## Summary

Create a portable Skill that instructs an Agent to organize a large or structurally complex body of source information into a generic hierarchy and use the configured mcp-agent-ops tools to render it as reviewable HTML before writing the full document.

## Context

Large or structurally complex documents can benefit from reviewing a proposed hierarchy before prose is written. The Agent performs the semantic work: it reads the authorized source information, identifies topics and relationships, chooses an appropriate section order, and represents that structure as a hierarchy. The configured mcp-agent-ops server owns hierarchy persistence and HTML rendering.

The Skill defines when to create the outline, how to express it using the generic hierarchy contract, how to invoke the configured tools, and how to incorporate review feedback. No document-specific software layer belongs between the Agent and that interface.

## Source Evidence

The user requested a new Skill that improves documentation writing by converting a large body of raw information into an HTML outline through mcp-agent-ops. The outline is intended for document preparation or human review when a document must incorporate substantial source material. On 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user clarified that the model performs the semantic work: it determines the document structure and places that structure into the generic hierarchy used by the MCP tools. This request authorizes the Skill and its exact governed routing scope below.

## Requirements

- Create the portable create-document-outline Skill.
- Activate it when the work involves many sources, competing possible structures, substantial topic breadth, or an explicit request to review an outline before drafting prose.
- Read the configured mcp-agent-ops documentation and tool schemas before writing the Skill instructions, then name the actual supported hierarchy operations and inputs precisely.
- Instruct the Agent to read all authorized inputs, identify the document's topics and relationships, and choose an ordered hierarchy appropriate to the document type and audience.
- Express the proposed document structure using the generic hierarchy contract accepted by the configured mcp-agent-ops server.
- Invoke the configured hierarchy tools directly to create or update the hierarchy and render its HTML representation.
- Identify source-supported content, proposed organization, unresolved conflicts, and missing information in the hierarchy when those distinctions matter to review, without defining a separate document-outline schema.
- Let a person or Agent review the rendered hierarchy, revise the proposed structure, and render the revised hierarchy before full document writing begins.
- Preserve the authorized sources for downstream writing and Verification; the outline does not replace Evidence.
- Use only artifact locations and retention behavior supported by the configured MCP tools.
- Stop with a clear unavailable-tool result when a required configured operation is missing. Do not install a package, import the server's Python package directly, or implement a substitute renderer.
- Do not introduce a document-specific executable helper, transformation service, schema, artifact manager, synchronization protocol, or filesystem security layer between the Agent and the configured MCP tools.
- Route the Skill conditionally to the approved Agent definitions that write documents or ingest source material.
- Use repository-authorized generators for generated projections and adapters.

## Acceptance Criteria

- Given representative multi-source information, the Agent produces a coherent generic hierarchy whose sections and nesting are suitable for the intended document.
- The Skill invokes the documented configured mcp-agent-ops hierarchy operations directly, and those operations produce structured hierarchy data and reviewable HTML.
- A reviewer can request structural changes, after which the revised hierarchy and HTML both reflect those changes.
- The Skill clearly distinguishes outline preparation from final prose writing and requires the original sources to remain available to the writer.
- Missing configured MCP hierarchy functionality stops the workflow with a clear error and no alternate installation, import, or renderer path.
- The delivered Skill contains no document-specific executable helper, custom hierarchy schema, or duplicate renderer.
- Conditional Agent routing activates the Skill only for document work that benefits from outline review.
- The Skill instructions use the actual installed tool names and fields documented by the configured server.
- Focused Skill, routing, MCP interaction, and generated-freshness checks pass.

## Dependencies

None.

## Verification

- Validate the create-document-outline Skill and its OpenAI metadata with the configured validators.
- Exercise the configured MCP hierarchy tools with one representative document hierarchy and inspect the resulting structured data and HTML.
- Revise the hierarchy once through the MCP workflow and verify that both representations reflect the revision.
- Confirm that the Skill package contains no document-specific executable helper and no direct import of mcp_agent_ops.
- Run focused routing, Skill-probe, bundle-contract, and repository-authorized generated-freshness checks.
- Obtain fresh methodology review and independent verification against this work item's requirements and acceptance criteria.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-document-outline/SKILL.md
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml

### Allowed Dependent Artifacts

- skills/create-document-outline/agents/openai.yaml
- evals/skill-probes.yaml
- scripts/test_bundle_content.py
- scripts/test_agent_skill_evaluation_docs.py
- README.md
- design/generated/skill-definitions.js
- design/agent-and-skill-evaluations.html
- design/agent-skill-hierarchy.svg

### Approval Resolution

Approved at creation. The user explicitly requested a new document-outline Skill using mcp-agent-ops and clarified on 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 that the model determines the document structure before submitting it through the generic MCP hierarchy interface. Approval covers exactly the governed canonical sources and dependent artifacts listed above. It does not authorize another Skill, Agent definition, local executable helper, or unrelated generated surface.

## Notes

- The outline is a preparation and review artifact, not the completed document.
- Creation of this Ready Work item does not dispatch implementation.
