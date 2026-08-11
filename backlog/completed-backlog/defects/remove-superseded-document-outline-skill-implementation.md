# Remove Superseded Document Outline Skill Implementation

Status: Completed

Type: Defect

Provider: file

Work Item ID: remove-superseded-document-outline-skill-implementation

Completion: main-branch

## Summary

Remove the rejected create-document-outline implementation and its routing, tests, probes, and generated projections without implementing its replacement.

## Context

Completed Work Item create-html-document-outlines-from-raw-information delivered a document-specific Python helper and related methodology integration in main delivery commit 6e9ad25976beb349220b13cff5c3df93e0c3df7c. Subsequent review established that the helper duplicated semantic work and MCP hierarchy responsibilities, creating unnecessary complexity. A separate Ready Work Item, create-document-outlines-with-mcp-hierarchy-tools, defines the clean replacement and must begin from a repository state that no longer presents the superseded implementation as supported.

## Source Evidence

On 2026-08-10 in task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user directed: “we can now discard the previous attempt at creating the skill to use the hierarchy tool.” This authorizes removal of the exact rejected implementation and its attributable integrations while retaining historical provider records.

## Requirements

- Delete the current skills/create-document-outline package, including its document-specific helper, helper tests, example, and metadata.
- Remove create-document-outline routing from the four conceptual Agent definitions changed by the rejected implementation.
- Remove the obsolete skill probe and focused bundle, evaluation-documentation, and portability assertions owned only by the rejected implementation.
- Regenerate affected Agent adapters, skill documentation, evaluation documentation, hierarchy SVG, and support checklist from the remaining canonical sources.
- Preserve the completed and failed backlog records as historical evidence.
- Do not implement the replacement Skill or change mcp-agent-ops behavior in this Work Item.

## Acceptance Criteria

- No distributed create-document-outline Skill, helper, metadata, probe, example, or Agent routing from the rejected implementation remains.
- Generated projections are current and contain no stale create-document-outline entry.
- Historical completed and failed work-item records remain intact.
- No source or behavior belonging to the clean replacement is introduced.
- Focused bundle, generation-freshness, evaluation-catalog, hierarchy, and diff checks pass.

## Dependencies

None.

## Verification

- Run repository-authorized generators for each affected projection and their focused freshness checks.
- Run focused bundle, role-routing, evaluation-probe, hierarchy, and portability checks affected by removal.
- Confirm the rejected package paths are absent and historical backlog records remain.
- Run git diff --check.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-document-outline/SKILL.md
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Allowed Dependent Artifacts

- skills/create-document-outline/agents/openai.yaml
- skills/create-document-outline/examples/large-multi-source-outline.json
- skills/create-document-outline/scripts/outline.py
- skills/create-document-outline/scripts/test_outline_helper.py
- evals/skill-probes.yaml
- README.md
- scripts/test_agent_skill_evaluation_docs.py
- scripts/test_bundle_content.py
- scripts/test_python_windows_portability.py
- design/agent-and-skill-evaluations.html
- design/agent-skill-hierarchy.svg
- design/agent-skill-test-coverage-checklist.md
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generated native Agent projections and repository-owned documentation projections affected by removing the Skill and its routing.

### Approval Resolution

Approved by the user's quoted discard instruction on 2026-08-10. Approval is limited to removing the rejected create-document-outline implementation and its attributable integrations; it does not authorize implementing the replacement.

## Completion Evidence

Completed At: 2026-08-10T20:16:00-04:00

Main Delivery Commit: 955cc4b68e3eb7ef570f5f16213c2591e5f7a9ab

Verification Result: The rejected package, helper, routing, probe, focused assertions, and generated projections are absent. Focused evaluation-documentation tests and all affected generator freshness checks pass; Git diff validation passes.

Archive Path: backlog/completed-backlog/defects/remove-superseded-document-outline-skill-implementation.md
