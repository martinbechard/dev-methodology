# Separate Work-Item Coordination From Codex Task Control

Status: Starting

Type: Feature

Provider: file

Work Item ID: separate-work-item-coordination-from-codex-task-control

Completion: direct-main

## Summary

Split `coordinate-codex-work-items` into provider-neutral `coordinate-work-items` policy and Codex-specific `coordinate-codex-tasks` runtime guidance so the platform name appears only on the responsibility that actually depends on Codex.

## Context

The current 700-line `coordinate-codex-work-items` skill combines two different concerns. Most of the file defines provider-neutral queue authority, Starting and Running evidence, capacity, dependency handling, dispatch, blockage reconciliation, review and verification availability, Commit delivery, Persistence closure, watchdog observation, and reporting. A smaller set of sections depends on Codex task creation, runtime capability checks, canonical task identity, conversation titles, Codex state, and task archival.

The `codex` qualifier therefore describes only part of the package. It makes portable coordination policy appear runtime-specific and causes Claude Code, Gemini, and Junie Agent adapters to carry a Codex-named dependency even where the procedure itself is provider- and harness-neutral.

## Source Evidence

On 2026-08-05, the user requested further naming and responsibility changes to be logged as work items and observed that some skill names contain `codex` even though their responsibilities are not Codex-specific. `skills/coordinate-codex-work-items/SKILL.md` confirms the mixed boundary: Queue Target And Dispatch, Blocker Classification, Effective Commit Delivery And Persistence Closure, and Reporting are provider-neutral, while Conversation Execution Compatibility, Conversation Title Contract, Codex runtime reconciliation, task creation, and archival use Codex-specific mechanics.

## Requirements

- Replace the current package with `skills/coordinate-work-items/SKILL.md` and `skills/coordinate-codex-tasks/SKILL.md`.
- Put provider-neutral work-item authority, lifecycle evidence, active-capacity policy, dependency rules, scheduling, blockage and stall reconciliation, review and verification availability, Commit/Persistence handoff, watchdog criteria, and reporting in `coordinate-work-items`.
- Put Codex task creation and resumption, runtime capability checks, canonical Codex task identity, conversation-title synchronization, Codex runtime-state reconciliation, task follow-up, and task archival in `coordinate-codex-tasks`.
- Keep provider lifecycle authority in the Persistence-selected manager, delivery authority in the Commit-selected provider, and resource ownership in the selected resource-coordination skill.
- Make the relevant backlog Agents consume `coordinate-work-items` according to their existing core or conditional responsibility.
- Load `coordinate-codex-tasks` only when Codex task mechanics are actually required; do not inject it into non-Codex scenarios merely because they coordinate work items.
- Keep the two skills complementary peers. Agent definitions or project guidance must load both where needed instead of making either skill directly absorb or duplicate the other's procedures.
- Replace exact old-name references, standing prompt references, role instructions, metadata, tests, catalogs, and generated adapters without retaining a compatibility alias.
- Split current tests into portable work-item coordination assertions and Codex-specific task-control assertions.

## Acceptance Criteria

- `coordinate-work-items` contains no Codex-only tool, title, task-creation, or archival instruction.
- `coordinate-codex-tasks` contains only the Codex runtime mapping and does not redefine provider lifecycle, Commit, Persistence, resource coordination, or generic backlog policy.
- Dev Backlog Coordinator, Dev Backlog Steward, Dev Backlog Watchdog, and Dev Orchestrator have understandable core and conditional dependencies after the split.
- Non-Codex generated Agent definitions do not present provider-neutral coordination as a Codex capability.
- Codex generated Agent definitions retain every required dispatch, reconciliation, title, follow-up, and archival behavior through the two complementary skills.
- No maintained source or generated output refers to `coordinate-codex-work-items` after migration.
- Portable coordination and Codex task-control evaluations pass independently and together.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate both new skill packages and all four changed Agent definitions.
- Run Dev Backlog Coordinator, Steward, Watchdog, and Orchestrator suites for provider none and durable providers.
- Run portable queue/lifecycle tests separately from Codex runtime, task identity, title, and archival tests.
- Regenerate Agent adapters for Codex, Claude Code, Gemini, and Junie and compare their resolved skill dependencies.
- Search the maintained tree for the retired skill identity and misplaced Codex-only vocabulary in the portable skill.
- Run bundle, evaluation coverage, generated-output freshness, Markdown link, and `git diff --check` validation.
- Obtain fresh independent methodology review and verification.

## Open Questions

- Determine the smallest shared data contract for canonical execution identity and active-execution evidence that remains portable while allowing the Codex skill to add task and conversation fields.

## Governed Definition Approval

### Governed Canonical Sources

- skills/coordinate-codex-work-items/SKILL.md
- skills/coordinate-work-items/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- PROJECT.yaml
- README.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/skill-groups/backlog-management.md
- design/skill-groups/concurrent-tasking.md
- design/agentic-configuration.html
- design/orchestrated-development-lifecycle.html
- design/work-item-provider-and-completion-contracts.md
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-coordinator/scenarios.yaml
- evals/agent-tests/dev-backlog-coordinator/suite.yaml
- evals/agent-tests/dev-backlog-watchdog/scenarios.yaml
- evals/agent-tests/dev-backlog-watchdog/suite.yaml
- scripts/test_codex_workitem_coordination.py split or renamed according to the two responsibility boundaries.
- scripts/test_bundle_content.py
- New package `agents/openai.yaml` metadata produced from only the approved new skill sources.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify and log additional naming and responsibility changes, including the explicit observation that a `codex` qualifier is incorrect for responsibilities that are not Codex-specific. Approval is limited to the exact governed canonical paths above and the two stated replacement skill identities.

## Notes

This is a static responsibility split, not a diagram of one runtime scenario. The portable skill states the dependencies and procedure ownership that always exist; the Codex skill states the conditional platform mapping used only in Codex tasks.

## Starting Reservation — 2026-08-06T08:44:38Z

- Transition: Ready -> Starting.
- Coordinator reservation: Dev Backlog Coordinator reserved this Work Item ID on current main at 2026-08-06T08:44:38Z.
- Dependency reconciliation: Dependencies are None. The claim-helper separation dependency is terminal successful at commit 5742e5973e58cbd533666d69b640aa3b3cc614ba, which is current main.
- Owner handoff: Dev Backlog Coordinator retains reservation ownership and will hand off to one root Dev Orchestrator after launch acceptance.
- Root Agent Task: Not assigned; no child task was created by this reservation transaction.
- Launch result: Pending; this provider transaction does not start a task or create execution ownership.
- Next action: Launch one root Dev Orchestrator and record Starting -> Running only after accepted execution evidence.
