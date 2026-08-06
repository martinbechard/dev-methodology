# Align Codex Work-Item Coordination Skill

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/align-codex-work-item-coordination-skill.md

Completion: direct-main

Series: backlog/completed-backlog/features/apply-object-oriented-skill-group-design/index.md

## Summary

Rename codex-workitem-coordination to coordinate-codex-work-items and align its public coordination procedures with the finalized work-item management and resource-coordination interfaces.

## Context

The Concurrent Tasking proposal gives the coordinating package an operation-shaped identity while retaining its multi-procedure contents. It consumes provider management, selected resource coordination, and selected delivery through project routing. It must not hard-code one Persistence, Commit, or claim-helper implementation where the project configuration selects a provider.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact rename and relationships are in design/skill-groups/concurrent-tasking.md and the proposal registry at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Rename the skill, frontmatter, metadata, self-references, exact Agent references, catalogs, and generated mirrors to coordinate-codex-work-items.
- Retain Resource Coordination, Queue Target And Dispatch, and Effective Commit Delivery And Persistence Closure as distinct public procedures.
- Use the finalized provider-management and resource-coordination procedure vocabulary without naming a concrete provider unnecessarily.
- Preserve lifecycle ownership, dispatch capacity, task identity, claims, review, verification, delivery, and closeout boundaries.
- Update individual skill probes and all affected coordinator, steward, watchdog, and orchestrator scenarios.

## Acceptance Criteria

- coordinate-codex-work-items is the only live identity for the coordinating skill.
- The four Agent definitions use the new exact name and retain their distinct responsibilities.
- The skill consumes management and resource procedures coherently and does not absorb provider lifecycle or transport policy.
- Every affected suite and individual probe uses the new identity and verifies at least one coordination boundary behaviorally.
- Generated mirrors, catalogs, and focused coordination tests are fresh and passing.

## Dependencies

- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-work-item-management-provider-skills.md
- backlog/feature-backlog/apply-object-oriented-skill-group-design/split-backlog-blockage-and-dispatch-mode-skills.md
- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-resource-coordination-skills.md

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run the individual coordination probe and focused Dev Backlog Coordinator, Dev Backlog Steward, Dev Backlog Watchdog, and Dev Orchestrator suites.
- Run scripts/test_codex_workitem_coordination.py, scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Search maintained sources for stale codex-workitem-coordination references and classify historical evidence separately.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine whether any internal heading should be split further to separate routing instructions from operational procedure content; do not broaden the approved responsibility set.

## Crisis Dependency Reclassification

Reclassified At: 2026-08-05T17:10:30Z.

Transition: Ready -> Blocked.

Owner: Unowned.

Exact Blocker: Required dependency backlog/feature-backlog/apply-object-oriented-skill-group-design/split-backlog-blockage-and-dispatch-mode-skills.md is currently Blocked. The other two declared dependencies are Completed.

Blocker Owner: Dev Backlog Coordinator resolving the named dependency in Backlog Crisis Mode.

Unblock Condition: Split Backlog Blockage And Dispatch-Mode Skills reaches a terminal successful disposition and its delivered identities and interfaces are available on current main.

Coordinator Next Action: Keep this item in the crisis dependency set and do not dispatch it. After the unblock condition is satisfied, reconcile it through Blocked -> Ready under the normal lifecycle.

## Governed Definition Approval

### Governed Canonical Sources

- skills/codex-workitem-coordination/SKILL.md
- skills/codex-workitem-coordination/agents/openai.yaml
- skills/coordinate-codex-work-items/SKILL.md
- skills/coordinate-codex-work-items/agents/openai.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- approval-record-align-codex-work-item-coordination-skill.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-coordinator
- evals/agent-tests/dev-backlog-steward
- evals/agent-tests/dev-backlog-watchdog
- evals/agent-tests/dev-orchestrator
- scripts/test_codex_workitem_coordination.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." The reviewed Concurrent Tasking diagram shows the exact skill rename and the four exact Agent relationships covered here. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.

## Crisis Completion

Completed At: 2026-08-05T19:22:53Z.

Disposition: Completed directly by the Backlog Crisis Mode Coordinator after all three declared dependencies reached terminal successful dispositions.

Delivery Commit: 84eb9937.

Verification: The renamed skill validated; 106 claim-contract tests and focused coordination, skill-evaluation, coverage-catalog, evaluation-documentation, bundle-contract, Coordinator, Steward, Watchdog, and Orchestrator checks passed where current-main baselines apply; generated skill, role, hierarchy, evaluation, and support-checklist outputs are current; diff checks passed. Pre-existing Steward Future-Idea fixture failures remain unchanged and outside this item.

Outcome: coordinate-codex-work-items is the sole live skill identity, the four owning roles and focused evaluation surfaces use it, and the three approved public procedure headings remain intact.
