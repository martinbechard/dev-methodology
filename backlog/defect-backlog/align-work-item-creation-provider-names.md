# Align Work-Item Creation Provider Names

Status: Ready

Type: Defect

Provider: file

Work Item ID: align-work-item-creation-provider-names

Completion: direct-main

## Summary

Create an exact `create-work-item` Interface Skill and rename every creation Provider Skill so the `create-work-item-*` family label, provider identities, project routing, and consumer vocabulary share one stem.

## Context

The current family is shown as `create-*-work-item`, with providers named `create-file-work-item`, `create-github-work-item`, `create-gitlab-work-item`, `create-azure-devops-work-item`, and `create-jira-work-item`. This makes the provider technology part of the middle of the operation name and prevents the family from using the terminal-wildcard convention.

The diagrams also show a shared interface contract without a corresponding loadable Interface Skill. The corrected structure is:

- Interface Skill: `create-work-item`
- Family notation: `create-work-item-*`
- Providers: `create-work-item-file`, `create-work-item-github`, `create-work-item-gitlab`, `create-work-item-azure-devops`, and `create-work-item-jira`

Source inspection also found one duplicated condition in `create-file-work-item`: "The item can state one concrete question whose answer changes what happens next." appears twice in the same User Action Required rule list. This confirmed source defect is recorded here because the renamed file is already in the exact correction scope.

## Source Evidence

On 2026-08-05, the user requested further naming and responsibility changes to be logged as work items and stated: "the pattern is to have * at the end of the interface, not in the middle. Some provider skills don't have names that match the interface stem." The current identities and the nonterminal `create-*-work-item` family are visible in `skills/create-*-work-item`, `design/skill-groups/backlog-management.md`, and `design/skill-groups/concurrent-tasking.md`.

## Requirements

- Add `skills/create-work-item/SKILL.md` as the exact Interface Skill containing the provider-neutral work-item identity, input, result, and Create Work Item procedure contract.
- Rename all five provider packages and frontmatter identities to the `create-work-item-<provider>` form listed in Context.
- Preserve file, GitHub, GitLab, Azure DevOps, and Jira provider-specific authority, duplicate-detection, partial-mutation, evidence, unsupported-operation, and no-fallback behavior.
- Make applicable Agent definitions consume the `create-work-item` interface while AGENTS.md and generated project guidance select one exact provider from Persistence.
- Update exact-name references in other skills without making one provider depend on another provider.
- Update the object-oriented group models to show the exact Interface Skill and the `create-work-item-*` family consistently.
- Remove the duplicated User Action Required condition while preserving its single intended rule.
- Update individual interface and provider evaluations, catalogs, metadata, generated adapters, and documentation; remove every live old skill identity after migration.

## Acceptance Criteria

- `create-work-item` is a loadable Interface Skill with one provider-neutral creation contract.
- Every creation provider name begins with `create-work-item-` and ends with its provider identity.
- No maintained source, role, project template, evaluation, catalog, generated output, or documentation page refers to the five retired skill identities or `create-*-work-item`.
- Consumers retain the same Create Work Item meaning while Persistence changes only the selected provider implementation.
- Supported providers retain their native behavior, and Azure DevOps and Jira retain truthful zero-mutation unsupported results.
- The duplicated User Action Required condition appears exactly once.
- Focused interface, provider, routing, migration, and stale-name checks pass.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate the new interface and all renamed provider skill packages.
- Run the five provider probes, provider fixtures, Persistence routing tests, role tests, bundle tests, and evaluation coverage checks.
- Regenerate skill metadata, native adapters, hierarchy views, and documentation, then run freshness checks.
- Search the maintained tree for all retired creation identities and the nonterminal family label.
- Run `git diff --check` and obtain fresh independent methodology review and verification.

## Open Questions

None. Future Ideas remain in the file provider until the separately logged responsibility-split item is delivered.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-file-work-item/SKILL.md
- skills/create-github-work-item/SKILL.md
- skills/create-gitlab-work-item/SKILL.md
- skills/create-azure-devops-work-item/SKILL.md
- skills/create-jira-work-item/SKILL.md
- skills/create-work-item/SKILL.md
- skills/create-work-item-file/SKILL.md
- skills/create-work-item-github/SKILL.md
- skills/create-work-item-gitlab/SKILL.md
- skills/create-work-item-azure-devops/SKILL.md
- skills/create-work-item-jira/SKILL.md
- skills/route-documentation-work/SKILL.md
- skills/manage-github-work-items/SKILL.md
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml

### Allowed Dependent Artifacts

- AGENTS.md
- PROJECT.yaml
- README.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/skill-groups/backlog-management.md
- design/skill-groups/concurrent-tasking.md
- design/work-item-provider-and-completion-contracts.md
- design/orchestrated-development-lifecycle.html
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- evals/agent-tests/dev-backlog-steward/suite.yaml
- evals/agent-tests/dev-orchestrator/test_fixtures.py
- scripts/render-agents-technology-skills.py
- scripts/test_bundle_content.py
- scripts/test_codex_workitem_coordination.py
- scripts/test_technology_detection.py
- Provider package `agents/openai.yaml` metadata moved or generated for only the approved old and new package identities.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify naming and responsibility changes and log them as additional work items, including the explicit decisions that interface wildcards belong at the end and providers must match their interface stem. Approval is limited to the exact governed canonical paths above and the stated rename destinations. It does not authorize changes to another governed definition.

## Notes

The naming-standard work item and this item can be implemented independently because this item records the exact target identities. Shared documentation and generated-output edits require normal resource coordination.
