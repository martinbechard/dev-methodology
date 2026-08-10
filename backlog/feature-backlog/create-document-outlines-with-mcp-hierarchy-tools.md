# Create Document Outlines with MCP Hierarchy Tools

Status: Ready

Type: Feature

Provider: file

Work Item ID: create-document-outlines-with-mcp-hierarchy-tools

Completion: main-branch

## Summary

Create a portable document-outline skill that has the model organize substantial raw information into a generic hierarchy and use the configured mcp-agent-ops hierarchy tools to produce structured data and reviewable HTML before full document writing.

## Context

Large documents benefit from reviewing their proposed structure before prose is written. The semantic work belongs to the model: it reads the authorized information, identifies the topics and relationships, resolves an appropriate section order, and represents the result as a hierarchy. The configured mcp-agent-ops server provides the hierarchy operations and HTML rendering.

The workflow should remain small. The skill supplies model-facing instructions for producing and reviewing the hierarchy, then calls the configured MCP tools. It does not need a document-specific software layer between the model and the generic hierarchy interface.

## Source Evidence

The user requested a new skill for improving documentation writing by converting a large amount of raw information into an HTML outline through mcp-agent-ops, for preparation of a full document or human review. On 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user clarified that the model should take the document structure it has developed and put that structure into a hierarchy. The user then directed:

> Create a new workitem as if we had never done anything.

This request authorizes a clean implementation of that outcome without assuming an earlier implementation or migration path.

## Requirements

- Create a portable create-document-outline skill for document work involving enough source volume or structural complexity to benefit from outline review before prose authoring.
- Tell the model to read all authorized inputs, identify the document's topics and relationships, and choose an ordered hierarchy appropriate to the selected document type and audience.
- Represent the proposed document structure using the generic hierarchy data accepted by the configured mcp-agent-ops server.
- Use the configured MCP hierarchy tools directly to create or update the structured hierarchy and render its synchronized HTML representation.
- Make clear which hierarchy content is supported by source material, proposed by the model, unresolved, or missing when those distinctions are material to review.
- Let a human or Agent review the rendered hierarchy, revise the proposed structure, and regenerate the HTML before full document writing begins.
- Preserve the original authorized sources for downstream writing and verification; the outline does not replace source evidence.
- Keep temporary outline artifacts within locations allowed by the configured MCP server. Retain them only when needed for the active writing workflow or when the user requests them as deliverables.
- Stop with a clear unavailable-tool result if the required configured MCP hierarchy operation does not exist. Do not install a package, import the server's Python package directly, or implement a substitute renderer.
- Do not introduce a document-specific Python helper, transformation service, schema, artifact manager, synchronization protocol, or filesystem security layer between the model and the configured generic MCP hierarchy tools.
- Route the skill conditionally to the approved document-producing and source-ingest Agent definitions.
- Use repository-authorized generators for generated projections and adapters.

## Acceptance Criteria

- Given representative multi-source information, the model produces a coherent generic hierarchy whose sections and nesting are suitable for the intended document.
- The configured mcp-agent-ops hierarchy operation accepts the model-produced hierarchy and creates synchronized structured data and standalone HTML.
- A reviewer can request structural changes, after which the updated hierarchy and regenerated HTML reflect those changes.
- The skill clearly distinguishes outline preparation from final prose writing and requires the original sources to remain available to the writer.
- Missing configured MCP hierarchy functionality stops the workflow with a clear error and no alternate installation, import, or renderer path.
- The delivered workflow contains no document-specific executable helper or duplicate hierarchy implementation.
- Conditional Agent routing activates the skill only for document work that benefits from a reviewable outline.
- Focused skill, routing, MCP interaction, and generated-freshness checks pass.

## Dependencies

None.

## Verification

- Validate the create-document-outline skill and its OpenAI metadata with the configured validators.
- Exercise the configured MCP hierarchy tools with one representative document hierarchy and inspect the resulting structured data and HTML.
- Revise the hierarchy once through the MCP workflow and verify that both representations reflect the revision.
- Confirm that the skill package contains no document-specific Python helper and no direct import of mcp_agent_ops.
- Run focused routing, skill-probe, bundle-contract, and repository-authorized generated-freshness checks.
- Obtain fresh methodology review and independent verification against this work item's requirements and acceptance criteria.

## Open Questions

- Resolve the installed mcp-agent-ops hierarchy tool names and exact input fields from current configured-server documentation and tool discovery before writing the skill instructions.

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

Approved at creation. The user explicitly requested a new document-outline skill using mcp-agent-ops and, on 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, directed that this work item be created from a clean-slate understanding. Approval covers exactly the governed canonical sources and dependent artifacts listed above. It does not authorize another skill, Agent definition, local executable helper, or unrelated generated surface.

## Notes

- The outline is a preparation and review artifact, not the completed document.
- Creation of this Ready work item does not dispatch implementation.
