# Create Document Outline Skill with MCP Hierarchy Tools

Status: Blocked

Owner: Unowned

Type: Feature

Provider: file

Work Item ID: create-document-outlines-with-mcp-hierarchy-tools

Completion: main-branch

## Summary

Create a portable Skill that instructs an Agent to organize selected source material into a generic document hierarchy, produce structured hierarchy data and HTML through mcp-agent-ops, and apply targeted changes without rewriting the entire hierarchy.

## Context

The Agent performs the semantic work: it reads the source material explicitly selected for the outline, identifies topics and relationships, chooses an appropriate section order, and represents that structure as a hierarchy. The configured mcp-agent-ops server creates the structured hierarchy and HTML.

The Skill defines how to create the outline and how to modify a specific part of an existing outline through the configured hierarchy tools. Its responsibility ends when the structured hierarchy and HTML outline have been created or updated.

## Source Evidence

The user requested a new Skill that converts selected source material into an HTML document outline through mcp-agent-ops. On 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user clarified that the model performs the semantic work: it determines the document structure and places that structure into the generic hierarchy used by the MCP tools. The user also required instructions for targeted modifications through special-purpose tools that do not rewrite the entire hierarchy. This request authorizes the Skill and its exact governed routing scope below.

## Requirements

- Create the portable create-document-outline Skill.
- Activate it when the user or an applicable document-writing Workflow requires a document outline.
- Read the configured mcp-agent-ops documentation and tool schemas before writing the Skill instructions, then name the supported hierarchy creation, rendering, and targeted-modification operations and inputs precisely.
- Instruct the Agent to use only the source material explicitly selected for the outline. Do not search for or load additional material unless the user adds it to the outline scope.
- Identify the selected material's topics and relationships, then choose an ordered hierarchy appropriate to the document type and audience.
- Express the proposed document structure using the generic hierarchy contract accepted by the configured mcp-agent-ops server.
- Invoke the configured hierarchy tools directly to create the hierarchy and render its HTML representation. Do not add a document-specific executable helper or renderer.
- When a targeted change is requested, use the special-purpose MCP modification tool for the addressed node, subtree, or field instead of rebuilding the hierarchy.
- Preserve every hierarchy element outside the requested modification and use the MCP tools to keep the structured hierarchy and HTML synchronized.
- Route the Skill to the approved Agent definitions that create documents or document outlines.

## Acceptance Criteria

- Given representative source material, the Agent produces a coherent generic hierarchy whose sections and nesting are suitable for the intended document.
- The Skill invokes the documented configured mcp-agent-ops hierarchy operations directly, and those operations produce structured hierarchy data and HTML.
- A targeted change modifies only the requested hierarchy element, preserves every unaffected element, and updates the HTML without rewriting the entire hierarchy.
- The workflow does not search for or load source material outside the explicitly selected outline scope.
- The delivered Skill contains no document-specific executable helper or duplicate renderer.
- Agent routing makes the Skill available where document outlines are created.
- The Skill instructions match the current tool names and input fields exposed by the configured server.
- Focused Skill, routing, MCP interaction, and generated-freshness checks pass.

## Dependencies

- remove-superseded-document-outline-skill-implementation

Blocker owner: Work Item remove-superseded-document-outline-skill-implementation.

Blocked to Ready condition: remove-superseded-document-outline-skill-implementation is Completed with the rejected Skill package, helper, routing, probe, tests, and generated projections removed from main.

Requested Coordinator action: complete the removal item, confirm the obsolete implementation is absent, then transition this Work Item from Blocked to Ready before dispatch.

## Verification

- Validate the create-document-outline Skill and its OpenAI metadata with the configured validators.
- Exercise the configured MCP hierarchy tools with one representative document hierarchy and inspect the resulting structured data and HTML.
- Apply one targeted modification through the documented special-purpose MCP tool and verify that the requested element changes while every unaffected hierarchy element remains unchanged.
- Confirm that the Skill package contains no document-specific executable helper and no direct import of mcp_agent_ops.
- Run focused routing, Skill-probe, bundle-contract, and repository-authorized generated-freshness checks.
- Independently verify the delivered Skill against this Work item's Requirements and Acceptance criteria.

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

- The structured hierarchy and HTML outline are the Skill outputs. The Skill ends after creating them.
- Creation of this Ready Work item does not dispatch implementation.
