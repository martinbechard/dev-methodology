# Align Documentation Methodology Skills

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-documentation-methodology-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Summary

Rename the four Documentation Methodology skills to their canonical verb-first identities, update every maintained governed reference, and revise the individual documentation and setup evaluations that load them.

## Context

The reviewed design renames development-methodology to route-documentation-work, documentation-bootstrap to bootstrap-project-documentation, documentation-reverse-engineer to reverse-engineer-project-documentation, and documentation-page-verify to verify-documentation-page. These skills are named directly by several Agents and peer skills. The delivery must therefore update the complete live reference graph atomically rather than leave compatibility aliases or dangling old names.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact approved identities and relationships are in design/skill-groups/documentation-methodology.md and the proposal registry at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Apply all four canonical renames, including frontmatter, metadata, exact Agent references, peer-skill references, catalogs, and generated mirrors.
- Preserve routing, bootstrap, reverse-engineering, and page-verification responsibilities; do not turn the documentation router into a general development skill.
- Remove stale live references to the four former names without rewriting historical result records.
- Update each affected Agent suite and each renamed skill's individual probe or case.
- Keep direct exact-name loading semantics; do not invent an injectable family where the current design uses named skills.

## Acceptance Criteria

- The four proposed skill directories are canonical and the four former directories no longer remain as live definitions.
- Every listed Agent and skill definition names the canonical replacement where it previously named a former skill.
- No maintained live catalog, fixture, project guidance source, or generated adapter refers to a former identity.
- Individual evaluations exercise routing, bootstrap, reverse engineering, and sentence or page verification through the new names.
- Full focused Agent suites and generated-output freshness checks pass.

## Dependencies

- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-baseline-development-skills.md
- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-project-setup-skills.md

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run focused suites for Dev Documentation Writer, Methodology Maintainer, Methodology Artifact Reviewer, Project Bootstrapper, Project Configurator, Dev Artifact Reviewer, Wiki Architect, and Wiki Artifact Reviewer.
- Run the four individual skill probes plus scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Search maintained sources for all four former names and classify any retained occurrence as intentional historical or migration evidence.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Resolve whether any nonhistorical example must mention both old and new names for migration explanation; default to removing the old name from live instructions.

## Governed Definition Approval

### Governed Canonical Sources

- skills/development-methodology/SKILL.md
- skills/development-methodology/agents/openai.yaml
- skills/route-documentation-work/SKILL.md
- skills/route-documentation-work/agents/openai.yaml
- skills/documentation-bootstrap/SKILL.md
- skills/documentation-bootstrap/agents/openai.yaml
- skills/bootstrap-project-documentation/SKILL.md
- skills/bootstrap-project-documentation/agents/openai.yaml
- skills/documentation-reverse-engineer/SKILL.md
- skills/documentation-reverse-engineer/agents/openai.yaml
- skills/reverse-engineer-project-documentation/SKILL.md
- skills/reverse-engineer-project-documentation/agents/openai.yaml
- skills/documentation-page-verify/SKILL.md
- skills/documentation-page-verify/agents/openai.yaml
- skills/verify-documentation-page/SKILL.md
- skills/verify-documentation-page/agents/openai.yaml
- skills/create-architecture/SKILL.md
- skills/create-file-work-item/SKILL.md
- skills/create-functional-spec/SKILL.md
- skills/create-high-level-design/SKILL.md
- skills/create-module-design/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/create-unit-test-plan/SKILL.md
- skills/project-wiki-create/SKILL.md
- skills/project-wiki-review/SKILL.md
- skills/review-architecture/SKILL.md
- skills/review-functional-spec/SKILL.md
- skills/review-high-level-design/SKILL.md
- skills/review-module-design/SKILL.md
- skills/review-structured-artifact/SKILL.md
- skills/review-unit-test-plan/SKILL.md
- agents/roles/dev-activities/dev-artifact-reviewer.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- agents/roles/wiki-activities/wiki-architect.role.yaml
- agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml

### Allowed Dependent Artifacts

- approval-record-align-documentation-methodology-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-artifact-reviewer
- evals/agent-tests/dev-documentation-writer
- evals/agent-tests/methodology-artifact-reviewer
- evals/agent-tests/methodology-maintainer
- evals/agent-tests/project-bootstrapper
- evals/agent-tests/project-configurator
- evals/agent-tests/wiki-architect
- evals/agent-tests/wiki-artifact-reviewer
- evals/projects/project-configuration-routing
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- Directly related non-governed documentation, fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." The reviewed Documentation Methodology and Project Setup diagrams make the four renames and their direct Agent and peer-skill relationships explicit. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
