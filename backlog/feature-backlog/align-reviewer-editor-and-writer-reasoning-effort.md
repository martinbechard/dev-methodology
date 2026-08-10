# Align Reviewer, Editor, and Writer Reasoning Effort

Status: Ready

Type: Feature

Provider: file

Work Item ID: align-reviewer-editor-and-writer-reasoning-effort

Completion: main-branch

## Summary

Assign every conceptual Reviewer or Editor role to the low-effort verification profile and every conceptual Writer role to the medium-effort implementation profile.

## Context

The repository now provides semantic implementation and verification model profiles. Dev Code Reviewer already uses verification, while the remaining Reviewer and Editor roles still use high-effort profiles. Dev Documentation Writer and Wiki Writer also still use a high-effort documentation profile.

## Source Evidence

The user directed on 2026-08-10 in task 019fb057-1767-7ef2-b5fa-41f4417b20b3: “reviewers/editors should use the review (low) level, and writers need to use (medium).”

## Requirements

- Assign every conceptual role whose role name identifies it as a Reviewer or Editor to model profile verification.
- Assign every conceptual role whose role name identifies it as a Writer to model profile implementation.
- Preserve each role's model family and all behavior, skills, tools, budgets, and instructions unrelated to reasoning effort.
- Regenerate every supported native Agent projection from the conceptual role sources.
- Add focused contract coverage that prevents Reviewer, Editor, or Writer roles from returning to a high-effort profile.

## Acceptance Criteria

- Dev Artifact Reviewer, Dev Code Reviewer, Dev Document Topic Editor, Dev Prompt Reviewer, Dev Security Reviewer, Dev Skill Lint Reviewer, Methodology Artifact Reviewer, and Wiki Artifact Reviewer resolve to low effort in adapters that support an effort setting.
- Dev Documentation Writer and Wiki Writer resolve to medium effort in adapters that support an effort setting.
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
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-document-topic-editor.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml
- agents/roles/dev-activities/dev-security-reviewer.role.yaml
- agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml
- agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Allowed Dependent Artifacts

- scripts/test_bundle_content.py
- design/generated/role-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generated native Agent projections owned by scripts/build-skill-docs.py for the listed roles.

### Approval Resolution

Approved at creation by the user's quoted 2026-08-10 request in task 019fb057-1767-7ef2-b5fa-41f4417b20b3. Approval is limited to the listed conceptual roles, their focused contract coverage, and generator-owned projections.
