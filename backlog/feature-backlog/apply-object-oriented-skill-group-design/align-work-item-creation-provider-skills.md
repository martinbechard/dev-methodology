# Align Work-Item Creation Provider Skills

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-work-item-creation-provider-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Summary

Give all five work-item creation providers the shared Create Work Item public procedure while preserving each provider's storage, duplicate, authority, and partial-mutation behavior.

## Context

The Backlog Management proposal keeps the provider-specific skill names and aligns their procedure vocabulary. create-file-work-item, create-github-work-item, create-gitlab-work-item, create-azure-devops-work-item, and create-jira-work-item should all explain how to Create Work Item for their own technology. The interface alignment must not imply that placeholder providers are operational when they are not.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact provider recommendations are in design/skill-groups/backlog-management.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Introduce a Create Work Item heading in each provider and retain provider-specific implementation rules beneath it.
- Preserve current availability, placeholder, duplicate-detection, authority, exact-transaction, readback, and ambiguous-outcome boundaries.
- Align input and result terminology where the providers already express equivalent concepts.
- Add an individual positive and provider-appropriate negative evaluation for every provider.
- Keep technology choice in project routing; do not make providers directly name one another.

## Acceptance Criteria

- All five definitions expose Create Work Item as the shared public procedure.
- File, GitHub, and GitLab providers retain their distinct operational contracts.
- Azure DevOps and Jira remain truthfully classified according to their implemented availability.
- Every provider has focused evaluation evidence for its shared procedure and its provider-specific boundary.
- Catalog and generated mirror freshness checks pass.

## Dependencies

- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-documentation-methodology-skills.md

## Verification

- Run the supported definition-change precheck for all five governed paths.
- Run each provider's individual probe and available provider fixture tests.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Compare all five public headings and input or result terms for coherence.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine the strongest truthful negative evaluation for the two placeholder providers without fabricating unavailable external behavior.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-file-work-item/SKILL.md
- skills/create-github-work-item/SKILL.md
- skills/create-gitlab-work-item/SKILL.md
- skills/create-azure-devops-work-item/SKILL.md
- skills/create-jira-work-item/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-work-item-creation-provider-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-steward
- scripts/test_github_work_item_provider_fixture.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, provider fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the five governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
