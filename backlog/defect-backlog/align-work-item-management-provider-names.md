# Align Work-Item Management Provider Names

Status: Running

Type: Defect

Provider: file

Work Item ID: align-work-item-management-provider-names

Completion: direct-main

## Summary

Create an exact `manage-work-items` Interface Skill and rename every management Provider Skill so the `manage-work-items-*` family, provider identities, project routing, and lifecycle consumers share one stem.

## Context

The current family is shown as `manage-*-work-items`, with providers named `manage-file-work-items`, `manage-github-work-items`, `manage-gitlab-work-items`, `manage-azure-devops-work-items`, and `manage-jira-work-items`. This places the provider inside the operation name and differs from terminal-wildcard families such as `deliver-work-item-*`.

The diagrams expose a provider-neutral lifecycle contract, but no exact `manage-work-items` Interface Skill publishes its shared data and procedures. The corrected structure is:

- Interface Skill: `manage-work-items`
- Family notation: `manage-work-items-*`
- Providers: `manage-work-items-file`, `manage-work-items-github`, `manage-work-items-gitlab`, `manage-work-items-azure-devops`, and `manage-work-items-jira`

## Source Evidence

On 2026-08-05, the user requested further naming and responsibility changes to be logged as work items and stated: "the pattern is to have * at the end of the interface, not in the middle. Some provider skills don't have names that match the interface stem." The current identities and family label are present in `skills/manage-*-work-items`, `design/skill-groups/backlog-management.md`, `design/skill-groups/concurrent-tasking.md`, and the reusable object-oriented examples.

## Requirements

- Add `skills/manage-work-items/SKILL.md` as the exact Interface Skill containing the shared work-item identity, lifecycle definitions, result vocabulary, and five public management procedures.
- Rename all five provider packages and frontmatter identities to the `manage-work-items-<provider>` form listed in Context.
- Preserve each provider's native inventory, lifecycle, recovery, completion, reporting, authority, ambiguous-outcome, unsupported-operation, and no-fallback behavior.
- Make Dev Backlog Coordinator, Dev Backlog Steward, Dev Backlog Watchdog, and Dev Orchestrator consume the provider-neutral interface where their definitions require lifecycle procedures.
- Keep Persistence routing in AGENTS.md and generated project guidance responsible for selecting one exact management provider.
- Update exact-name references in creation skills and all maintained consumers without making providers depend on their siblings.
- Update the object-oriented group models to show the exact Interface Skill and `manage-work-items-*` family consistently.
- Update individual interface and provider evaluations, catalogs, metadata, generated adapters, and documentation; remove every live old skill identity after migration.

## Acceptance Criteria

- `manage-work-items` is a loadable Interface Skill publishing the complete shared lifecycle contract.
- Every management provider name begins with `manage-work-items-` and ends with its provider identity.
- No maintained source, role, project template, evaluation, catalog, generated output, or documentation page refers to the five retired identities or `manage-*-work-items`.
- All four lifecycle consumers use the same provider-neutral vocabulary while Persistence changes only the selected implementation.
- File, GitHub, and GitLab behavior remains provider-accurate; Azure DevOps and Jira retain truthful zero-mutation unsupported results.
- Focused interface, provider, routing, migration, and stale-name checks pass.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate the new interface and all renamed provider skill packages.
- Run every provider probe, provider fixture, Persistence routing test, affected Agent suite, bundle test, and evaluation coverage check.
- Regenerate skill metadata, native adapters, hierarchy views, and documentation, then run freshness checks.
- Search the maintained tree for all retired management identities and the nonterminal family label.
- Run `git diff --check` and obtain fresh independent methodology review and verification.

## Open Questions

None. Provider-specific refinements may add data or restrict supported operations, but they must preserve the interface's member meanings.

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-file-work-items/SKILL.md
- skills/manage-github-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md
- skills/manage-azure-devops-work-items/SKILL.md
- skills/manage-jira-work-items/SKILL.md
- skills/manage-work-items/SKILL.md
- skills/manage-work-items-file/SKILL.md
- skills/manage-work-items-github/SKILL.md
- skills/manage-work-items-gitlab/SKILL.md
- skills/manage-work-items-azure-devops/SKILL.md
- skills/manage-work-items-jira/SKILL.md
- skills/create-github-work-item/SKILL.md
- skills/create-work-item-github/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml

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
- evals/agent-tests/dev-backlog-coordinator/coordination_simulator.py
- evals/agent-tests/dev-backlog-coordinator/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-coordinator/test_coordination_simulator.py
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- evals/agent-tests/dev-backlog-steward/suite.yaml
- scripts/render-agents-technology-skills.py
- scripts/test_bundle_content.py
- scripts/test_codex_workitem_coordination.py
- scripts/test_generate_backlog_report.py
- scripts/test_technology_detection.py
- Provider package `agents/openai.yaml` metadata moved or generated for only the approved old and new package identities.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify naming and responsibility changes and log them as additional work items, including the explicit decisions that interface wildcards belong at the end and providers must match their interface stem. Approval is limited to the exact governed canonical paths above and the stated rename destinations. It does not authorize changes to another governed definition.

## Notes

The naming-standard work item and this item can be implemented independently because this item records the exact target identities. Shared documentation and generated-output edits require normal resource coordination.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Align work-item management provider names.

Dispatch Time: 2026-08-06T03:46:35Z.

Intended Root Role: Root Dev Orchestrator.

Launch Result: Not attempted.

Canonical Conversation: None.

Owner: Unowned pending the task's Starting -> Running transition.

Last Contact: 2026-08-06T03:46:35Z; parent Coordinator recorded the reservation.

Next Reconciliation: No later than 2026-08-06T04:01:35Z.

Required Next Lifecycle Transition: The new task must directly record Starting -> Running, establish its exact Work Item ID activity=work claim, and then begin scoped implementation. Its final direct-main integration follows the creation-provider naming item because their manifests overlap.

## Current Running Evidence

Transition: Starting -> Running.

Owner: Root Dev Orchestrator in task 019fd52f-7ec5-7bf1-9cbc-65032dd1af06.

Canonical Conversation: 019fd52f-7ec5-7bf1-9cbc-65032dd1af06.

Root Agent Task: /root.

Branch: Detached candidate checkout at bfd80b6e933805b5f152a295eb106a7c63aa7511.

Worktree: /Users/martinbechard/.codex/worktrees/4bd4/dev-methodology.

Phase: Bounded owned wait for align-work-item-creation-provider-names to complete its already-running verification and integrate first on main.

Started At: 2026-08-06T03:49:41Z.

Accepted Execution Evidence: The delegated Root Dev Orchestrator accepted ownership in the isolated worktree, recorded this transition through the configured file provider, and will defer only the final overlapping-manifest integration until the creation-provider naming item is represented on main.

Next Action: Establish the exact Work Item ID activity=work claim and implement the approved governed definitions and dependent artifacts with focused verification.

## Active Execution Evidence

Condition Type: owned-wait.

Owner: Root Dev Orchestrator in task 019fd52f-7ec5-7bf1-9cbc-65032dd1af06.

Evidence: Accepted candidate 2925eca30eb0310d7b2c85299167ff4abdf1b070 is clean, same-reviewer APPROVED, and independently VERIFIED PASS on the declared focused and freshness gates. Final reconciliation must follow align-work-item-creation-provider-names because their manifests overlap. That item passed source verification, resolved eight expected current-main conflicts into clean integration commit 1370a335, and passed focused integration checks and freshness; it is completing required post-integration review and verification before main advances. Current main 50a34b31eeec12751325c3dad52baba7d70d6841 does not yet contain that integration.

Observed At: 2026-08-06T04:44:31Z.

Started At: 2026-08-06T03:49:41Z.

Deadline or Expires At: 2026-08-06T04:59:31Z.

Next Action: Commit this path-limited owned-wait evidence, reacquire the exact Work Item ID activity=work claim, observe the named creation-provider integration event, then reconcile overlapping manifests and apply direct-main delivery without repeating accepted source gates.

Next Reconciliation At: 2026-08-06T04:59:31Z.

Conversation Title Evidence: The canonical conversation was directly renamed to Waiting for Claim — Align Work-Item Management Provider Names for the exact integration-order wait.
