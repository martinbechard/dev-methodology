# Replace Document Outline Helper with Direct MCP Workflow

Status: Ready

Type: Defect

Provider: file

Work Item ID: replace-document-outline-helper-with-direct-mcp-workflow

Completion: main-branch

## Summary

Replace the overengineered document-outline implementation with a skill in which the model performs the semantic outline work, represents the result as a generic hierarchy, and invokes the configured mcp-agent-ops hierarchy tools directly to create synchronized JSON and HTML.

## Context

The completed Work Item create-html-document-outlines-from-raw-information introduced a document-specific Python helper, helper tests, a custom outline schema, filesystem and output management, renderer discovery, synchronization hashes, capability handling, and broad dependent checks. That architecture is incorrect for the requested workflow.

The model is responsible for reading the authorized source information, deciding the document structure, and expressing that structure as the generic hierarchy accepted by mcp-agent-ops. The configured MCP server is responsible for hierarchy persistence and HTML rendering. A document-specific Python adapter cannot perform the semantic work and should not duplicate MCP behavior, sandboxing, artifact management, or renderer validation.

The current delivered implementation must remain intact until a bounded forensic inventory identifies every artifact and assertion introduced solely by the incorrect architecture. Replacement work must then remove or revise those artifacts deliberately rather than deleting evidence before the examination is complete.

## Source Evidence

On 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user clarified that document outlining should consist of taking the model-created document structure and putting it into a hierarchy, and that a Python helper does not contribute to this semantic work. The user then directed:

> This whole massive undertaking is incorrect. Create a new workitem with your improved understanding. We will need to discard all this work after our forensic examinination and start again.

The completed implementation provides concrete forensic evidence: skills/create-document-outline/scripts/outline.py imports the mcp-agent-ops Python renderer directly and implements a document-specific schema, path checks, output replacement, repeated rendering, hashes, and custom outcomes. Its focused MCP activity used validation tools rather than the hierarchy creation and rendering tools that should perform the core operation.

## Requirements

- Begin with a bounded forensic inventory of the completed item's source, tests, examples, routing, evaluation entries, and generated projections. Record which parts exist solely because of the incorrect helper architecture and which generic skill-routing changes remain useful.
- Preserve the existing implementation until that inventory and removal manifest are complete.
- Rewrite create-document-outline so the model inventories the authorized raw information, performs the semantic analysis, chooses an ordered document structure, and expresses it directly as the generic hierarchy accepted by the configured mcp-agent-ops tools.
- Invoke the configured MCP hierarchy creation or update and HTML rendering operations directly. Do not import mcp_agent_ops as a Python library or install, discover, or substitute another runtime.
- Remove the outline-specific Python helper, its helper-specific tests, and helper-only example or projection contracts after the forensic manifest proves they are no longer required.
- Do not introduce a replacement document-specific adapter, schema, artifact manager, launcher discovery mechanism, synchronization hash protocol, duplicate renderer, or custom filesystem security layer unless a separately documented MCP contract gap proves it necessary and receives explicit scope approval.
- Treat source references, facts, proposals, conflicts, and unknowns as model-authored hierarchy content or ordinary supported metadata when useful. Do not require a separate document-outline data model merely to rename generic hierarchy fields.
- Keep review status and accepted section order in the writing workflow, not in the renderer input contract unless the generic hierarchy API already supports them naturally.
- If the configured hierarchy tools are absent or cannot perform the documented operation, stop with a clear tool-unavailable error. Do not fall back to direct Python imports or package installation.
- Preserve conditional routing for document-producing Agents only where a large or complex source set makes a reviewable outline useful.
- Use repository-authorized generators to update generated projections; do not hand-edit generated files.
- Keep tests and reviews bounded to the revised model-to-MCP workflow. Do not add broad portability, sandbox duplication, or hypothetical security requirements that are not part of this acceptance contract.

## Acceptance Criteria

- A representative multi-source document is semantically organized by the model into a generic nested hierarchy and submitted through the configured mcp-agent-ops hierarchy tool.
- The MCP operation produces synchronized structured data and standalone HTML whose visible hierarchy matches the submitted structure.
- The create-document-outline workflow contains no outline-specific Python helper and no direct mcp_agent_ops Python import.
- No document-specific schema or transformation layer duplicates the generic MCP hierarchy contract.
- Missing configured hierarchy functionality produces a clear stop/error without installing packages or using a local-library fallback.
- The forensic inventory accounts for every removed, retained, or regenerated artifact introduced by create-html-document-outlines-from-raw-information.
- Focused routing and generated-freshness checks pass without invoking the broad Python portability inventory for a workflow that no longer adds Python files.
- Fresh independent review evaluates only the revised acceptance contract and reports no requirement for portability or custom sandbox controls absent concrete in-scope evidence.

## Dependencies

None.

## Verification

- Exercise the configured MCP hierarchy tool with one representative document hierarchy and inspect both the structured output and rendered HTML.
- Search the final skill package for direct mcp_agent_ops imports, outline-specific helper code, custom renderer invocation, and helper-only synchronization hashes; require none.
- Validate skills/create-document-outline/SKILL.md and skills/create-document-outline/agents/openai.yaml with the configured skill and metadata validators.
- Run only focused skill-routing, probe, bundle-contract, and repository-authorized generated-freshness checks affected by the replacement.
- Review the forensic manifest against the completed work item's changed paths so no obsolete helper artifact or assertion remains accidentally.
- Obtain fresh methodology review and independent verification against this work item's explicit requirements and acceptance criteria.

## Open Questions

- During forensic inventory, determine the exact names and input schemas of the configured mcp-agent-ops hierarchy tools from the installed server documentation and tool discovery. This is agent-resolvable and does not block Ready status.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-document-outline/SKILL.md
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml

### Allowed Dependent Artifacts

- skills/create-document-outline/agents/openai.yaml
- skills/create-document-outline/examples/large-multi-source-outline.json
- skills/create-document-outline/scripts/outline.py
- skills/create-document-outline/scripts/test_outline_helper.py
- evals/skill-probes.yaml
- scripts/test_bundle_content.py
- scripts/test_python_windows_portability.py
- scripts/test_agent_skill_evaluation_docs.py
- README.md
- design/generated/skill-definitions.js
- design/agent-and-skill-evaluations.html

### Approval Resolution

Approved at creation. On 2026-08-10 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user explicitly directed creation of a new work item to discard the incorrect document-outline undertaking after forensic examination and restart with the improved understanding. Approval covers exactly the governed sources and dependent artifacts listed above. It does not authorize changes to another skill, Agent definition, or unrelated generated surface.

## Notes

- This item replaces the implementation architecture; it does not reject the original user outcome of producing a reviewable HTML outline before writing a large document.
- File deletion is not the first action. The forensic inventory and exact removal manifest must precede removal.
- Generic hierarchy content may carry concise source labels or unknown markers, but their meaning is authored by the model rather than enforced by a custom Python schema.
