# Align Work-Item Creation Provider Names

Status: Completed

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

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Align work-item creation provider names.

Dispatch Time: 2026-08-06T03:45:24Z.

Intended Root Role: Root Dev Orchestrator.

Launch Result: Not attempted.

Canonical Conversation: None.

Owner: Unowned pending the task's Starting -> Running transition.

Last Contact: 2026-08-06T03:45:24Z; parent Coordinator recorded the reservation.

Next Reconciliation: No later than 2026-08-06T04:00:24Z.

Required Next Lifecycle Transition: The new task must directly record Starting -> Running, establish its exact Work Item ID activity=work claim, and then begin scoped implementation.

## Current Execution

Transition: Starting -> Running.

Canonical Conversation: 019fd52f-7ec5-7bf1-9cbc-6523870fc790.

Root Agent Task: /root.

Owner: Root Dev Orchestrator 019fd52f-7ec5-7bf1-9cbc-6523870fc790.

Branch: codex/align-work-item-creation-provider-names.

Worktree: /Users/martinbechard/.codex/worktrees/a82d/dev-methodology.

Phase: Verifying integrated candidate.

Accepted Candidate Commit: 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca.

Candidate Evidence: Dev Coder returned a clean isolated-worktree commit after focused provider/interface fixtures, 28 Dev Orchestrator fixtures, exact skill validation, metadata and generated-output freshness, Python compilation, diff validation, and a maintained stale-name audit passed. Two broader failures reproduced unchanged on the clean baseline and were excluded under the requested focused-test boundary.

Review Evidence: Fresh Dev Code Reviewer found no provider-semantic or migration defect and confirmed generated/source consistency, but returned two P2 test gaps: the maintained stale-name audit was not encoded as a regression, and the new interface test protected headings without its substantive provider-neutral contract clauses.

Correction Attempt: 1 of 2. The original Dev Coder owns both exact focused-test corrections; no production or governed-definition expansion is authorized or required.

Correction Result: Replacement candidate 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca adds only the two requested focused regressions in scripts/test_bundle_content.py. The exact focused test and diff checks passed, and the isolated worktree is clean.

Re-review Result: PASS. A new fresh-context Dev Code Reviewer verified that both regression gaps are closed, the exclusions are exact and consumption-bounded, the interface assertions cover the substantive contract, and no production, governed-definition, or generated bytes changed in the correction.

Confirmed Issue Disposition: Both review findings were corrected in replacement candidate 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca; no issue was excluded from this delivery.

Independent Verification Result: PASS. Seven creation/provider regressions, 28 Dev Orchestrator fixtures, seven routing tests, exact skill and metadata validation, four affected freshness checks, changed-Python compilation, maintained stale-name observation, diff validation, and clean worktree and index checks passed. Broad suites and two reproduced unrelated baseline failures remained explicitly excluded.

Integration Branch: codex/integrate-creation-provider-names-019fd52f.

Integration Worktree: /private/tmp/creation-provider-naming-integration.B1odZH.

Integration Base: current main 49a1471cc2fd15618f49655e4085709ce94b44fd.

Integration Evidence: Applying accepted candidate 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca exposed eight conflicts where current-main deliver-work-item interface advances overlap generated and documentation surfaces. Dev Merge Coordinator owns exact conflict resolution and supported regeneration while preserving both accepted intents.

Integration Commit: 1370a3359120974c62bcc9d715d2a61a688307b6.

Source-to-Integration Mapping: Candidate 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca was replayed with -x onto current-main snapshot 49a1471cc2fd15618f49655e4085709ce94b44fd. Dev Merge Coordinator resolved the eight overlaps by reconciling the two hand-authored design documents and regenerating the six generated documentation, hierarchy, definition-data, and adapter-manifest surfaces from combined canonical sources.

Integration Checks: Four affected freshness checks, four focused creation/delivery interface tests under Python 3.11, staged diff validation, and post-commit show validation passed; the integration worktree is clean.

Review Availability Reconciliation: The parent Coordinator supplied a terminal recovery review verdict of GOOD for immutable integration commit 1370a3359120974c62bcc9d715d2a61a688307b6. The review found no material issue in 49a1471cc2fd15618f49655e4085709ce94b44fd..1370a3359120974c62bcc9d715d2a61a688307b6, confirmed the creation-provider rename and interface, preserved deliver-work-item and Dev Orchestrator changes, retained both accepted intents through conflict resolution, found generated artifacts aligned with sources, and found no new stale creation-provider identity. Residual risk is limited to the already-declared skipped broad suite. No further review is authorized or required.

Accepted Execution Evidence: The canonical root task is executing, has accepted this exact work item, created the isolated work-item branch, and acquired the update and provider-path claims required for this atomic transition.

Provider Operation Evidence: Work Item ID update claim update-align-work-item-creation-provider-names-019fd52f and exact path claim path-update-align-work-item-creation-provider-names-019fd52f returned SHARED_CHECKOUT_ACQUIRED.

Required Conversation Title: Implementing — Align Work-Item Creation Provider Names.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator 019fd52f-7ec5-7bf1-9cbc-6523870fc790.

Evidence: Parent recovery review is terminal GOOD for immutable integration commit 1370a3359120974c62bcc9d715d2a61a688307b6. The canonical task has resumed and will dispatch exactly one integration-sensitive Dev Verifier; no additional review or broad suite will run.

Observed At: 2026-08-06T05:01:00Z.

Started At: 2026-08-06T05:01:00Z.

Deadline or Expires At: 2026-08-06T09:01:00Z.

Next Action: Dispatch exactly one integration-sensitive Dev Verifier against immutable integration commit 1370a3359120974c62bcc9d715d2a61a688307b6, then advance main only after PASS.

Next Reconciliation At: 2026-08-06T05:16:00Z.

## Completion Evidence

Transition: Running -> Completed.

Completed At: 2026-08-06T05:08:00Z.

Accepted Candidate Commit: 7d87faee8dec5d7edc99c38a7517b4f1b2c91fca.

Reviewed Integration Commit: 1370a3359120974c62bcc9d715d2a61a688307b6, based on 49a1471cc2fd15618f49655e4085709ce94b44fd.

Review Result: GOOD. Parent recovery review found no material issue, confirmed both creation-provider and delivered deliver-work-item intents, confirmed generated/source alignment, and found no new stale creation-provider identity.

Integration-Sensitive Verification: PASS. The single fresh Dev Verifier observed immutable 1370a3359120974c62bcc9d715d2a61a688307b6; four focused combined-interface tests, four declared freshness checks, the maintained stale-name scan, diff and show mapping, and clean worktree/index checks passed under Python 3.11. The broad suite remained deliberately skipped.

Delivered Main Commit: ac560d5eb135840cfa57499ed35d8eff1f5aef44.

Source-to-Main Mapping: Integration commit 1370a3359120974c62bcc9d715d2a61a688307b6 was replayed with -x onto current main. Both commits have stable patch ID 6531f1f2836c34118b5bd814c5ba91474f108444. Post-integration git diff validation passed and main was clean.

Delivered Scope: Added the exact create-work-item Interface Skill; renamed the five creation providers to the create-work-item-<provider> family; preserved provider-specific behavior and the delivered deliver-work-item interface changes; updated approved routing, role, evaluation, documentation, metadata, and generated dependents; removed the duplicated User Action Required condition; and added focused stale-name and substantive-interface regressions.

Provider Closure: The canonical file record is terminal Completed and archived at backlog/completed-backlog/defects/align-work-item-creation-provider-names.md. Exact update, source-path, and destination-path claims owned the atomic terminal transaction; all task-owned claims are released after commit verification.
