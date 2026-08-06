# Support a Default Agent Context Budget Percent

Status: Starting

Type: Feature

Provider: file

Work Item ID: support-default-agent-context-budget-percent

Completion: direct-main

## Summary

Support one canonical default context-budget percentage for conceptual agents, set that default to 75%, and retain per-role percentages only where an agent needs an explicit override.

## Context

The current [conceptual role schema](../../agents/role-schema.yaml) requires contextBudgetPercent in every role, and every role repeats a value even when most agents should share the same allocation. The [agent generator](../../scripts/build-skill-docs.py) consumes each explicit value and correctly derives adapter-specific token budgets, but it has no fallback owned by the canonical definition contract.

The completed [context-budget generation feature](../completed-backlog/features/generate-agent-context-budget-from-model-capacity.md) established per-role percentage ownership, model-capacity derivation, and adapter instructions. This enhancement builds on that behavior by reducing repeated default declarations while preserving agent-specific allocations.

## Source Evidence

In the current Codex conversation on 2026-08-06, the user requested: “Ok log an enhancement to support a default context value and have it set to 75%.” The immediately preceding request set explicit values of 35% for Dev Backlog Coordinator and 50% for both Dev Backlog Watchdog and Dev Documentation Writer. Together, these messages authorize a 75% default that does not replace those explicit overrides.

## Requirements

- Define one canonical default context-budget percentage and set it to 75.
- Permit a conceptual role to omit contextBudgetPercent and resolve the omitted value to the canonical default.
- Treat an explicit role value as an override of the default, including 35 for Dev Backlog Coordinator and 50 for Dev Backlog Watchdog and Dev Documentation Writer.
- Keep explicit percentage validation unchanged for fractional, zero, negative, and above-100 values. Distinguish a valid omission with a configured default from an invalid explicit value.
- Use the effective resolved percentage for primary-model and model-stage token derivation in every supported adapter.
- Record the effective percentage in generated agent definitions, role documentation data, and the generation manifest without changing model selection, effort, responsibilities, skills, tools, mutation policy, or delegation behavior.
- Remove repeated role-level declarations that merely equal the 75% default while retaining intentional overrides.
- Document the source and precedence of the default and explicit overrides.

## Acceptance Criteria

- A role without contextBudgetPercent validates and generates with an effective value of 75.
- A role with an explicit contextBudgetPercent generates with that value instead of 75.
- Dev Backlog Coordinator generates at 35%, and Dev Backlog Watchdog and Dev Documentation Writer each generate at 50%.
- Invalid explicit percentages remain rejected with actionable errors.
- Primary-model and model-stage allocations use the same resolved percentage and preserve the existing rounding and zero-reserve rules.
- Generated definitions and the generation manifest are fresh and expose the resolved effective percentage for every role.
- Focused regression tests prove default resolution, override precedence, invalid-value handling, and unchanged non-context generated behavior.

## Dependencies

None.

## Verification

- Add focused schema and parser tests for omitted values, the 75% default, explicit overrides, and invalid explicit values.
- Add focused generator tests for default and override allocations across every supported adapter and representative model stages.
- Regenerate role documentation data, native adapter definitions, and the generation manifest with the repository-owned generator.
- Run generated-output freshness checks, targeted bundle-content tests, YAML validation for changed sources, and git diff --check.
- Obtain an independent review of default ownership, override precedence, generated results, and regression coverage.

## Open Questions

- Which canonical source should own the default so schema validation, parser behavior, documentation, and generators cannot drift?
- Should generated metadata distinguish whether the effective percentage came from the default or an explicit override, or is the effective value alone sufficient?

## Starting Handoff Evidence

Starting Recorded At: 2026-08-06T16:04:50Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Add a canonical 75% default context budget, preserve the explicit 35% and 50% role overrides, and generate the resolved effective percentage without changing unrelated agent behavior.

Launch Result: Not attempted

Canonical Conversation: None

Last Contact At: None

Next Reconciliation At: 2026-08-06T16:19:50Z

Intended Root Role: Dev Orchestrator

## Governed Definition Approval

### Governed Canonical Sources

- agents/role-schema.yaml
- agents/roles/dev-activities/dev-artifact-reviewer.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-browser-operator.role.yaml
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/roles/dev-activities/dev-document-topic-editor.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml
- agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml
- agents/roles/dev-activities/dev-security-reviewer.role.yaml
- agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml
- agents/roles/dev-activities/dev-ux-specialist.role.yaml
- agents/roles/dev-activities/dev-verifier.role.yaml
- agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- agents/roles/project-setup/project-organiser.role.yaml
- agents/roles/wiki-activities/wiki-architect.role.yaml
- agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/wiki-activities/wiki-query-responder.role.yaml
- agents/roles/wiki-activities/wiki-researcher.role.yaml
- agents/roles/wiki-activities/wiki-source-collector.role.yaml
- agents/roles/wiki-activities/wiki-topic-verifier.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Allowed Dependent Artifacts

- scripts/build-skill-docs.py
- scripts/test_bundle_content.py
- README.md
- design/generic-agent-definitions-source.html
- design/agent-and-skill-definitions.html
- design/generated/role-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generator-owned Codex, Claude Code, Gemini CLI, and Junie CLI native definitions corresponding to the governed role sources above
- Focused test fixtures or documentation files directly required to prove default and override behavior

### Approval Resolution

Approved at creation. The user’s 2026-08-06 message in the current Codex conversation explicitly requests an enhancement that supports a default context value set to 75%. The preceding message explicitly names the three required overrides. This approval covers only the exact governed sources listed above and their supported dependent artifacts; additional governed sources require separate exact-path approval.

## Notes

- The default is a canonical role-definition convenience. Adapter-owned model capacities and context-budget mechanisms remain unchanged.
- The enhancement must not interpret omission as an adapter-specific unlimited context setting.
