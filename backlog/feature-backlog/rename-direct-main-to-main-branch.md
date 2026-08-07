# Rename Direct Main To Main Branch

Status: Starting

Type: Feature

Provider: file

Work Item ID: rename-direct-main-to-main-branch

Completion: direct-main

## Summary

Replace direct-main terminology with main-branch terminology across the delivery provider, project Commit selection, documentation, generated artifacts, tests, and evaluations.

## Context

The current direct-main name is difficult to interpret because it combines a destination with an implied implementation mechanism. The delivery provider actually promises that accepted work reaches the main branch. Implementation may occur directly in the primary worktree or on a separate branch and worktree followed by integration, so main-branch describes the stable delivery destination more accurately.

The current name appears in the deliver-work-item-direct-main Provider Skill, the Commit selector, project templates, generated guidance and adapters, documentation, backlog examples, tests, evaluation fixtures, and a focused evaluation project. The rename must retain the distinction between main-branch delivery and feature-branch delivery while preserving both supported implementation paths to the main branch.

## Source Evidence

On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user stated: “Another bad name: direct-main should actually be main-branch” and then confirmed: “we need an item for that one too.”

## Requirements

- Rename the deliver-work-item-direct-main Provider Skill package, frontmatter identity, title, metadata, and references to deliver-work-item-main-branch.
- Rename the project Commit selector value from direct-main to main-branch wherever the current configuration model, templates, generated guidance, validation, and user-facing explanations expose it.
- Preserve the delivery contract: the provider completes accepted work on the main branch whether implementation happened in the primary worktree or in a separate branch and worktree that must be integrated.
- Keep feature-branch as the alternative delivery provider and update comparisons, diagrams, tables, routing examples, and setup language so the two choices are coherent.
- Rename current source, generated, test, fixture, and evaluation artifacts whose filenames or directory names encode direct-main when their identity represents the renamed concept.
- Update focused tests and individual evaluations that exercise completion selection, main-branch integration, unrelated dirty-file preservation, provider-family naming, project configuration, work-item creation, documentation generation, and catalog membership.
- Regenerate every supported derived artifact from its canonical source rather than editing generated outputs as independent sources.
- Define and verify the upgrade behavior for existing PROJECT.yaml files and installed project guidance that still use direct-main. Do not silently reinterpret malformed or unrelated values.
- Retain historical completed and failed work-item evidence without rewriting historical records merely to remove the former name.

## Acceptance Criteria

- The installed skill catalog exposes deliver-work-item-main-branch with aligned directory, frontmatter, title, metadata, and provider-family naming.
- New project configuration and generated AGENTS.md guidance use Commit main-branch and select deliver-work-item-main-branch.
- The main-branch provider supports both direct primary-worktree implementation and integration of accepted separate-branch or worktree contributions without changing the established delivery safeguards.
- Current agent definitions, skills, templates, documentation, generators, generated adapters, tests, and active evaluation fixtures contain no operational dependency on direct-main.
- Any remaining direct-main text is limited to deliberate historical evidence, compatibility handling, or migration documentation whose purpose is explicit.
- Existing configurations using direct-main receive verified migration or compatibility behavior with an explicit supported boundary.
- Focused delivery, configuration, provider-family, work-item, generation, and affected agent-evaluation tests pass under the new terminology.
- Skill validation, metadata synchronization, generated-document freshness checks, Markdown validation, and git diff checks pass.
- An independent review confirms that main-branch consistently names the delivery destination and that no documentation incorrectly implies all implementation occurs directly on main.

## Dependencies

None.

## Verification

- Search the complete repository before and after the rename for direct-main, Direct Main, direct_main, and the new main-branch variants; classify every intentional residual occurrence.
- Run the renamed main-branch completion contract tests, provider-family naming tests, project configuration and technology-generation tests, bundle-content tests, work-item coordination tests, and affected individual agent-evaluation suites.
- Run the separate-branch and worktree integration cases together with unrelated dirty-primary-file preservation cases to prove that the destination rename did not narrow supported implementation paths.
- Run the supported skill metadata, documentation, native-adapter, hierarchy, and support-checklist generators with their freshness checks.
- Validate the renamed Provider Skill and confirm that every conceptual and generated agent skill reference resolves to an installed bundle identity.
- Verify existing PROJECT.yaml migration or compatibility behavior using focused valid, legacy, and invalid configuration fixtures.
- Run Markdown link validation and git diff checks on the completed change.

## Open Questions

- Resolve during implementation whether direct-main remains a temporary accepted configuration alias or requires an explicit migration step. Base the decision on upgrade safety and supported configuration policy.
- Determine which historical artifact filenames must remain unchanged as evidence and which current evaluation or documentation artifact identities should be renamed.

## Governed Definition Approval

### Governed Canonical Sources

- skills/deliver-work-item-direct-main/SKILL.md
- skills/coordinate-work-items/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/manage-future-ideas/SKILL.md
- skills/manage-work-items-gitlab/SKILL.md
- skills/verify-end-to-end-workflow/SKILL.md

### Allowed Dependent Artifacts

- skills/deliver-work-item-direct-main/agents/openai.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- PROJECT.yaml
- AGENTS.md
- README.md
- skills/route-documentation-work/assets/templates/file-work-item-template.md
- skills/route-documentation-work/assets/templates/project-template.yaml
- scripts/generate-backlog-report.py
- scripts/render-agents-technology-skills.py
- scripts/test_bundle_content.py
- scripts/test_direct_main_completion_contract.py
- scripts/test_generate_backlog_report.py
- scripts/test_path_limited_backlog_git.py
- scripts/test_provider_family_naming.py
- scripts/test_role_mutation_policy.py
- scripts/test_ste_technical_writing.py
- scripts/test_technology_detection.py
- scripts/test_work_item_coordination.py
- evals/agent-scenarios.yaml
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/projects/direct-main-unrelated-dirty-contract/TASK.md
- evals/projects/file-work-item-template-contract/verify.py
- evals/agent-tests/dev-backlog-steward/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
- evals/agent-tests/dev-backlog-steward/test_contract.py
- evals/agent-tests/dev-orchestrator/test_fixtures.py
- design/agent-and-skill-evaluations.html
- design/agent-skill-specialization-examples.html
- design/agent-skill-test-coverage-checklist.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/orchestrated-development-lifecycle.html
- design/skill-groups/concurrent-tasking.md
- design/skill-groups/direct-main-delivery.md
- design/skills-modularization.html
- design/wiki-skills-and-project-context.html
- design/work-item-provider-and-completion-contracts.md
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- design/generated/template-definitions.js
- generated/adapters/claude/agents/project-configurator.md
- generated/adapters/codex/agents/project-configurator.toml
- generated/adapters/gemini/agents/project-configurator.md
- generated/adapters/junie/agents/project-configurator.md
- Affected exact evaluation suite, scenario, fixture, and suite-contract files identified by the required repository-wide reference search.

### Approval Resolution

Approved at creation. On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user requested that direct-main be changed to main-branch and explicitly requested a work item for that rename. This approval covers the exact governed canonical sources listed above only. Any additional governed skill-definition path discovered during implementation requires separate scope-specific approval; existing approval for the listed paths remains valid.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T01:14:14Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Rename the direct-main delivery provider and Commit selection to main-branch across approved operational sources, generated artifacts, focused tests, evaluations, and compatibility handling while preserving the established main-branch delivery safeguards and historical evidence.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-07T01:29:14Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: The overlapping resource-claim rename is Completed and archived at main commit `102c5fe6ae5b560befd6e9aac3485a51804508ca`; its shared source, generator, installation, and integration lanes are released.
