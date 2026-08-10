# Add Dev Architect Agent

Status: Ready

Type: Feature

Provider: file

Work Item ID: add-dev-architect-agent

Completion: main-branch

## Summary

Add a Dev Architect conceptual Agent that turns requirements into technically sound, implementable design choices, primarily for architecture documents and high-level designs.

## Context

The current catalog has no general software-architecture Agent. Dev Documentation Writer can author architecture documents and Dev Artifact Reviewer can review them, but neither role has a primary responsibility to establish that the selected technical approach correctly implements the requirements. The new role should follow Dev Coder's disciplined discovery, scoping, verification, and clean-candidate workflow while producing technical design decisions rather than production code.

## Source Evidence

The user requested on 2026-08-10 in task 019fb057-1767-7ef2-b5fa-41f4417b20b3: “create it like a Dev Coder but its goal is to ensure choices make technical sense and are a proper way of implementing the requirements. It will normally be used for architecture documents and high-level designs. It will use XHigh reasoning. Create a work item for this.”

## Requirements

- Add the conceptual role dev-architect under the Dev Activities role group.
- Give Dev Architect a Dev Coder-like workflow for scoped discovery, requirements traceability, repository-pattern inspection, focused validation, clean candidate commits, and bounded correction handoff.
- Make Dev Architect responsible for selecting and explaining technically sound, implementable approaches that satisfy the stated requirements and constraints.
- Route architecture documents and high-level designs to Dev Architect when their technical choices require creation or material revision.
- Keep document prose quality and template conformance with Dev Documentation Writer, and keep independent artifact review with Dev Artifact Reviewer.
- Prevent Dev Architect from silently expanding requirements, implementing unrelated production code, or presenting an unverified preference as an architectural decision.
- Add an architecture semantic model profile that maps to XHigh reasoning in Codex and to the closest explicitly supported high-capability setting in other adapters.
- Add materially distinct success and blocked examples, including insufficient requirements or unresolved technical constraints.
- Add focused positive and boundary evaluation coverage for the role and its routing.
- Regenerate all supported native Agent projections and repository-owned role documentation from canonical sources.

## Acceptance Criteria

- The role catalog contains dev-architect with repository mutation, skills, instructions, examples, dependencies, and output contracts valid under role schema version 8.
- The Codex Dev Architect projection uses XHigh reasoning.
- Dev Architect traces each material technical choice to requirements, constraints, repository evidence, or an explicitly stated assumption.
- Architecture and high-level-design workflows can route technical design work to Dev Architect without replacing Dev Documentation Writer or Dev Artifact Reviewer.
- Focused evaluation proves both a technically justified design outcome and a safe blocked outcome when the available requirements cannot support a responsible choice.
- Generated adapters, role documentation, evaluation projections, hierarchy artifacts, and support-checklist projections are current.
- Focused role, model-profile, generation, evaluation-catalog, and bundle checks pass.

## Dependencies

None.

## Verification

- Validate the new conceptual role against agents/role-schema.yaml.
- Run focused model-profile, role-generation, routing, mutation-policy, evaluation-catalog, and bundle contract tests.
- Run repository-authorized generators in write mode, followed by their freshness checks.
- Run git diff --check.

## Open Questions

Resolve the closest supported non-Codex adapter mappings from each adapter's documented model and effort capabilities without weakening the required Codex XHigh setting.

## Governed Definition Approval

### Governed Canonical Sources

- agents/roles/dev-activities/dev-architect.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- agents/model-profiles.yaml
- adapters/claude/model-profiles.yaml
- adapters/codex/model-profiles.yaml
- adapters/gemini/model-profiles.yaml
- adapters/junie/model-profiles.yaml
- README.md
- evals/agent-scenarios.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- scripts/test_bundle_content.py
- scripts/test_role_mutation_policy.py
- design/agent-skill-hierarchy.svg
- design/agent-skill-test-coverage-checklist.md
- design/generated/role-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generated native Agent projections owned by scripts/build-skill-docs.py.
- Generator-owned evaluation, hierarchy, and support-checklist projections affected by the new role and scenarios.

### Approval Resolution

Approved at creation by the user's quoted 2026-08-10 request in task 019fb057-1767-7ef2-b5fa-41f4417b20b3. Approval is limited to the Dev Architect role, the exact routing roles, the architecture model profile, focused evaluation and contract coverage, and their repository-authorized generated projections.
