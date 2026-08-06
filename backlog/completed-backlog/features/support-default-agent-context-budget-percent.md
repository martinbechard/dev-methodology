# Support a Default Agent Context Budget Percent

Status: Completed

Type: Feature

Provider: file

Work Item ID: support-default-agent-context-budget-percent

Completion: direct-main

## Summary

Support one canonical default context-budget percentage for conceptual agents, set that default to 75%, and retain per-role percentages only where an agent needs an explicit override.

## Context

The current [conceptual role schema](../../../agents/role-schema.yaml) requires contextBudgetPercent in every role, and every role repeats a value even when most agents should share the same allocation. The [agent generator](../../../scripts/build-skill-docs.py) consumes each explicit value and correctly derives adapter-specific token budgets, but it has no fallback owned by the canonical definition contract.

The completed [context-budget generation feature](generate-agent-context-budget-from-model-capacity.md) established per-role percentage ownership, model-capacity derivation, and adapter instructions. This enhancement builds on that behavior by reducing repeated default declarations while preserving agent-specific allocations.

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

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator in task 019fd7d3-0008-7b41-9164-b0f5af9832d6.

Canonical Conversation: 019fd7d3-0008-7b41-9164-b0f5af9832d6.

Root Agent Task: 019fd7d3-0008-7b41-9164-b0f5af9832d6.

Branch: codex/support-default-agent-context-budget-019fd7d3.

Worktree: /Users/martinbechard/.codex/worktrees/c866/dev-methodology.

Evidence: The parent Dev Backlog Coordinator completed the Ready to Starting reservation and explicit handoff. This canonical root Dev Orchestrator task accepted execution at authoritative main commit fe29ca578fce70e6fdfcb830c0f32324efe4fee2, established the clean canonical branch and worktree above from that commit, synchronized the conversation title, and is proceeding within the approved role, schema, generator, adapter, documentation, generated-artifact, and focused-test scope.

Observed At: 2026-08-06T16:08:02Z.

Started At: 2026-08-06T16:08:02Z.

Deadline or Expires At: 2026-08-06T16:23:02Z.

Next Action: Commit this provider-only Running transition, release its update and path claims, acquire the exact Work Item ID activity=work claim, and begin scoped implementation with fresh independent review and verification.

Next Reconciliation At: 2026-08-06T16:23:02Z.

Conversation Title Evidence: The canonical conversation title is Starting — Support Default Agent Context Budget.

## Completion Evidence

- Provider: file. Completion selector: direct-main. Completion disposition: READY. Lifecycle disposition: Completed.
- Completed at: 2026-08-06T16:32:29Z.
- Completed provider reference: backlog/completed-backlog/features/support-default-agent-context-budget-percent.md.
- Accepted source and integration commit: 2a36362939a7fce04c1d6c95d54f56b127c59f14 on codex/support-default-agent-context-budget-019fd7d3, based directly on Running provider commit 529ce7fd1bcb0767f7fe25cdd3db51cf4d2279c1. Authoritative main fast-forwarded to the same accepted commit, so no source-to-integration identity change occurred.
- Independent review: a fresh Dev Code Reviewer reported APPROVED with no findings or open questions. It confirmed all 143 changed paths were approved, the schema-owned 75% default and explicit 35/50/50 precedence were correct, omission remained distinct from invalid explicit input, all four adapters and model stages used the resolved value, generated outputs were fresh, and non-context behavior was unchanged.
- Independent verification: a fresh Dev Verifier reported PASS on the immutable candidate. Eight named focused tests passed; generator freshness passed; 30 role sources resolved as 27 default 75%, one explicit 35%, and two explicit 50%; 164 allocations including 44 model-stage allocations matched floor arithmetic with zero reserve; changed YAML and 120 native definitions parsed or packaged correctly; and base-to-candidate invariance proved model selection, effort, responsibilities, tools, skills, mutation policy, and delegation behavior unchanged.
- Post-integration verification: seven directly affected context-budget, adapter, invalid-value, documentation, non-context-preservation, and freshness tests passed on authoritative main. The separately reconciled model-profile semantic preservation test passed, and scripts/build-skill-docs.py --check reported current generated outputs. Commit-range diff validation and both primary and source worktree clean-state checks passed.
- Unrelated focused-selector warning: an accidentally selected existing dev-documentation-writer inventory test reported that its expected documentation-profile set omits dev-document-topic-editor. The accepted candidate changes no modelProfile value, and independent byte-invariance proves the failure is unrelated to this item; it was not fixed or used to broaden verification.
- Main observation: authoritative branch main and the clean source branch both resolve to 2a36362939a7fce04c1d6c95d54f56b127c59f14, which is reachable from main as its tip. Local main is 18 commits ahead of origin/main. Remote publication is not configured as a completion requirement for this item, so no push was performed.
- Claim evidence: the activity=work claim acquired at event 22ff34b8-ceff-4820-a254-3a9e9098aa00 and released with handoff at event de92fe64-c677-45a1-b5df-2ade7216d722. The primary integration claim acquired at event 0320be86-59f1-4d92-8bda-072daad381dc and released at event be0bf195-307c-4149-9df9-f9f6b52bcc8d. The terminal update claim acquired at event 3651dea1-8949-4f78-be78-40c14123ff51, and the exact active and archive path claim acquired at event f646ef1b-23ed-412a-9bea-1b7c8b00b9e1; their releases follow this committed terminal transaction.
- Scoped omissions: no broad repository suite, simulator, framework, browser, end-to-end runtime, or live-model check ran, as explicitly directed.

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
