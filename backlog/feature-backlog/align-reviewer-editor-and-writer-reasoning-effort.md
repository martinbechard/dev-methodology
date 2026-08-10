# Align Reviewer, Editor, and Writer Reasoning Effort

Status: Ready

Type: Feature

Provider: file

Work Item ID: align-reviewer-editor-and-writer-reasoning-effort

Completion: main-branch

## Summary

Assign every conceptual Reviewer or Editor role to the low-effort verification profile, every conceptual Writer role to the medium-effort implementation profile, and the additional coordination, maintenance, ingest, and verification roles named by the user to their requested profiles.

## Context

The repository now provides semantic implementation and verification model profiles. Dev Code Reviewer already uses verification, while the remaining Reviewer and Editor roles still use high-effort profiles. Dev Documentation Writer and Wiki Writer also still use a high-effort documentation profile.

## Source Evidence

The user directed on 2026-08-10 in task 019fb057-1767-7ef2-b5fa-41f4417b20b3: “reviewers/editors should use the review (low) level, and writers need to use (medium).” The user then added: “Dev Backlog Coordinator, Dev Orchestrator - low, Dev Merge Coordinator - implementation, Methodlogy maintainer - implementation, Wiki Topic Verifier - verifier, Wiki Ingester - implementation,” followed by: “make the source collector a low in the same work item.”

## Requirements

- Assign every conceptual role whose role name identifies it as a Reviewer or Editor to model profile verification.
- Assign every conceptual role whose role name identifies it as a Writer to model profile implementation.
- Assign Dev Backlog Coordinator and Dev Orchestrator to model profile verification.
- Assign Dev Merge Coordinator, Methodology Maintainer, and Wiki Ingester to model profile implementation.
- Assign Wiki Topic Verifier to model profile verification.
- Assign Wiki Source Collector to model profile verification.
- Preserve all role behavior, skills, tools, budgets, and instructions unrelated to model-profile selection.
- Regenerate every supported native Agent projection from the conceptual role sources.
- Add focused contract coverage that prevents Reviewer, Editor, or Writer roles from returning to a high-effort profile.

## Acceptance Criteria

- Dev Artifact Reviewer, Dev Code Reviewer, Dev Document Topic Editor, Dev Prompt Reviewer, Dev Security Reviewer, Dev Skill Lint Reviewer, Methodology Artifact Reviewer, and Wiki Artifact Reviewer resolve to low effort in adapters that support an effort setting.
- Dev Documentation Writer and Wiki Writer resolve to medium effort in adapters that support an effort setting.
- Dev Backlog Coordinator, Dev Orchestrator, and Wiki Topic Verifier resolve to low effort in adapters that support an effort setting.
- Wiki Source Collector resolves to low effort in adapters that support an effort setting.
- Dev Merge Coordinator, Methodology Maintainer, and Wiki Ingester resolve to medium effort in adapters that support an effort setting.
- Generated role definitions, native Agent projections, and the generation manifest are current.
- Focused role-profile contract tests pass.

## Dependencies

None.

## Verification

- Run the focused model-profile and role-generation contract tests in scripts/test_bundle_content.py.
- Run scripts/build-skill-docs.py with its freshness option.
- Run git diff --check.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- agents/roles/dev-activities/dev-artifact-reviewer.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-document-topic-editor.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml
- agents/roles/dev-activities/dev-security-reviewer.role.yaml
- agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/wiki-activities/wiki-source-collector.role.yaml
- agents/roles/wiki-activities/wiki-topic-verifier.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Allowed Dependent Artifacts

- scripts/test_bundle_content.py
- design/generated/role-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generated native Agent projections owned by scripts/build-skill-docs.py for the listed roles.

### Approval Resolution

Approved by the user's quoted 2026-08-10 requests in task 019fb057-1767-7ef2-b5fa-41f4417b20b3. Approval is limited to the listed conceptual roles, their focused contract coverage, and generator-owned projections.
