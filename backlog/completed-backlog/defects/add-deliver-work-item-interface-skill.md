# Add Deliver Work Item Interface Skill

Status: Completed

Type: Defect

Provider: file

Work Item ID: add-deliver-work-item-interface-skill

Completion: direct-main

## Summary

Add a loadable `deliver-work-item` Interface Skill so Dev Orchestrator can depend on one delivery contract while AGENTS.md selects either `deliver-work-item-direct-main` or `deliver-work-item-feature-branch`.

## Context

The delivery provider names already follow the terminal-wildcard family `deliver-work-item-*`, and both providers expose Deliver Work Item. The applied diagrams nevertheless point the consumer at a `<<Skill interface>>` node for which no `skills/deliver-work-item/SKILL.md` exists. This hides implementation choice visually but does not create the file dependency described by the object-oriented factory pattern.

The corrected model keeps the two existing provider names. It adds the exact interface package, makes the Agent consume that package when delivery is required, and leaves project Commit routing responsible for selecting the provider.

## Source Evidence

On 2026-08-05, the user requested a repository-wide audit of naming and responsibilities, specifically requiring terminal-wildcard interfaces and Provider Skills that match their interface stem. Source comparison found that `deliver-work-item-*` and its provider names already conform, but `design/skill-groups/direct-main-delivery.md` and `design/skill-groups/concurrent-tasking.md` show a shared interface that has no corresponding skill package.

## Requirements

- Add `skills/deliver-work-item/SKILL.md` as the exact Interface Skill for `deliver-work-item-*`.
- Publish the provider-neutral accepted-commit input, delivery result states, delivery evidence, and Deliver Work Item procedure that both providers must supply.
- Make Dev Orchestrator consume the interface whenever an accepted change must be delivered, without naming either provider in the Agent definition.
- Keep AGENTS.md and generated project guidance responsible for selecting direct-main or feature-branch from the Commit setting.
- Make both providers explicitly coherent with the interface while preserving their different internal procedures and outcomes.
- Keep direct-main integration behavior, feature-branch publication and review behavior, and provider lifecycle closure as separate responsibilities.
- Update the applicable diagrams from an analysis-only contract to the exact Interface Skill and retain terminal-wildcard family notation where the family is discussed.
- Add focused interface-consumer, provider-conformance, routing, and evaluation coverage.

## Acceptance Criteria

- `deliver-work-item` is a loadable Interface Skill and contains only provider-neutral public data and procedures.
- Dev Orchestrator depends on `deliver-work-item`; changing Commit changes only the selected provider.
- Both existing Provider Skills realize the same Deliver Work Item meaning without losing their direct-main or feature-branch behavior.
- Maintained diagrams distinguish the exact interface file from the `deliver-work-item-*` family label.
- Catalogs, generated adapters, role documentation, and evaluation documentation include the new interface.
- Focused routing and provider-conformance checks pass for both Commit values.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate the new interface and both provider skill packages.
- Run Dev Orchestrator, direct-main, feature-branch, Commit-routing, bundle, and evaluation coverage tests.
- Regenerate skill metadata, Agent adapters, hierarchy views, and documentation, then run freshness checks.
- Run `git diff --check` and obtain fresh independent methodology review and verification.

## Open Questions

None. The existing User Action Required item `respect-optional-resource-coordination-in-workflow-skills` remains a separate correction; this item must not silently resolve or bypass its pending approval boundary.

## Governed Definition Approval

### Governed Canonical Sources

- skills/deliver-work-item/SKILL.md
- skills/deliver-work-item-direct-main/SKILL.md
- skills/deliver-work-item-feature-branch/SKILL.md
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- AGENTS.md
- PROJECT.yaml
- README.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/skill-groups/concurrent-tasking.md
- design/skill-groups/direct-main-delivery.md
- design/work-item-provider-and-completion-contracts.md
- design/orchestrated-development-lifecycle.html
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-orchestrator/scenarios.yaml
- evals/agent-tests/dev-orchestrator/suite.yaml
- scripts/test_bundle_content.py
- scripts/test_codex_workitem_coordination.py
- New `skills/deliver-work-item/agents/openai.yaml` metadata produced from the approved interface source.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify naming and responsibility changes and log them as additional work items, including the direction that provider families use a terminal wildcard and Provider Skills match their interface stem. Approval is limited to the exact governed canonical paths above and does not resolve the separate optional-resource-coordination approval question.

## Notes

This item may share provider, role, documentation, and generated-output paths with other queued work. Those overlaps must be coordinated at mutation and integration time; they are not hard prerequisites.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Add the deliver-work-item interface skill.

Dispatch Time: 2026-08-06T03:51:56Z.

Intended Root Role: Root Dev Orchestrator.

Launch Result: Not attempted.

Canonical Conversation: None.

Owner: Unowned pending the task's Starting -> Running transition.

Last Contact: 2026-08-06T03:51:56Z; parent Coordinator recorded the reservation.

Next Reconciliation: No later than 2026-08-06T04:06:56Z.

Required Next Lifecycle Transition: The new task must directly record Starting -> Running, establish its exact Work Item ID activity=work claim, and then begin scoped implementation. Final reconciliation must preserve the provider-name work that reaches main first.

## Current Running Execution Evidence

Transition: Starting -> Running.

Canonical Conversation: 019fd533-e93d-7802-a081-de974adb096f.

Root Agent Task: 019fd533-e93d-7802-a081-de974adb096f.

Owner: Root Dev Orchestrator.

Branch: Detached implementation worktree at d96b62c3f26b48c5a7c4a8c5eeff5a139b721773; final direct-main integration must reconcile the current main branch.

Worktree: /Users/martinbechard/.codex/worktrees/8a55/dev-methodology.

Started At: 2026-08-06T03:54:27Z.

Accepted Execution Evidence: The canonical task received the exact provider path, parent Coordinator identity, authorized Starting-to-Running transition, direct-main completion selection, and approved governed-definition scope.

Phase: Scoped implementation and focused verification.

Next Action: Establish the exact Work Item ID activity=work claim, then implement only the approved canonical sources and dependent artifacts while preserving provider-name changes that reach main first.

## Completion Evidence

Transition: Running -> Completed.

Completion Disposition: READY.

Completed At: 2026-08-06T04:30:58Z.

Completion Selector: direct-main.

Accepted Source Commit: a72911c4ad8747ab2474d10585f05f60ddfb401e.

Source Commit Sequence: fd241de6d4a5bed44b301d248ed6ca58522d7233 followed by bounded correction a72911c4ad8747ab2474d10585f05f60ddfb401e.

Integration Strategy: Cherry-pick with source provenance onto current main.

Source-to-Integration Mapping: fd241de6d4a5bed44b301d248ed6ca58522d7233 -> 79ada3a68bfb237979744d819e017e9cfa52da61; a72911c4ad8747ab2474d10585f05f60ddfb401e -> 4c0ca95a8dc6ce49c0f2e276145a5f2975707a9c.

Observed Main Branch: main.

Observed Delivery Tip: 4c0ca95a8dc6ce49c0f2e276145a5f2975707a9c.

Reachability Evidence: Both integration commits were confirmed ancestors of main, and the complete non-backlog candidate content was byte-equivalent at the observed delivery tip.

Independent Review: The single fresh methodology reviewer approved candidate a72911c4ad8747ab2474d10585f05f60ddfb401e after both bounded corrections were resolved.

Source Verification: The single verifier passed six focused interface, provider, routing, direct-main, and feature-branch tests; two focused Awaiting Review Persistence tests; the Dev Orchestrator validate-only suite; metadata and generated-output freshness; and diff hygiene.

Post-Integration Verification: The same verifier passed five integration-sensitive interface, provider, routing, and Persistence tests plus metadata, skill documentation, hierarchy, support-checklist, evaluation-document freshness, and diff hygiene on primary main.

Skill Validation: The authoritative parent-root mcp-agent-ops validation of skills/deliver-work-item/SKILL.md, skills/deliver-work-item-direct-main/SKILL.md, and skills/deliver-work-item-feature-branch/SKILL.md returned ok true with no findings. The earlier child-root structured refusal was preserved and not retried privately.

YAML Validation: Primary-root validation checked the changed Dev Orchestrator role, evaluation catalogs, suite, scenarios, workflow packs, and new OpenAI metadata with no findings.

Scoped Omissions: No broad suite, live evaluation, private fallback validator, remote publication, or optional-resource-coordination work was required or performed.

Remote Observation: This repository-local direct-main delivery requires local main observation; origin/main was not part of the configured completion gate.

Clean Evidence: The accepted candidate worktree was clean. Primary main was clean at delivery observation and after integrated verification, with no integration residue.

Claim Evidence: The primary project-files integration claim and exact outcome-work claim were released after Commit READY. This terminal update used separate exact Work Item ID and source/destination provider claims.

Terminal Provider Commit: The commit containing this status-and-archive transaction.

Completed Archive Path: backlog/completed-backlog/defects/add-deliver-work-item-interface-skill.md.
