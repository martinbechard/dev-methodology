# Align Integration And Delivery Skills

Status: Blocked

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-integration-and-delivery-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Summary

Rename agent-work-merge to integrate-agent-work and both Commit implementations to deliver-work-item variants, align their shared delivery interface, and clarify the create-pull-request procedure.

## Context

The approved design places integration with Feature Branch And Worktrees and treats direct-main and feature-branch delivery as alternative implementations of Deliver Work Item. The canonical names are integrate-agent-work, deliver-work-item-feature-branch, and deliver-work-item-direct-main. create-pull-request keeps its name and exposes Create Or Update Pull Request. end-to-end-verification currently names both delivery providers and must remain coherent until its later Review And Verification rename.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact identities and relationships are in design/skill-groups/concurrent-tasking.md, design/skill-groups/direct-main-delivery.md, and the proposal registry at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Apply all three canonical renames, including frontmatter, metadata, exact Agent and peer-skill references, project Commit selection, catalogs, and generated mirrors.
- Expose Deliver Work Item in both delivery providers while preserving feature-branch and direct-main internal procedures and result dispositions.
- Rename the create-pull-request Workflow heading to Create Or Update Pull Request.
- Preserve the separation among integration, Commit delivery, Persistence completion, resource claims, pull-request publication, and verification.
- Update end-to-end-verification references to the two renamed delivery providers without otherwise implementing its later rename in this item.
- Add or update individual evaluations for integration, both delivery providers, and pull-request publication.

## Acceptance Criteria

- The three proposed identities are the only maintained live names for their responsibilities.
- Both Commit implementations expose Deliver Work Item and retain distinct direct-main or feature-branch behavior.
- integrate-agent-work covers merge, replay, selected commits, accepted file content, and reconciliation without becoming the delivery provider.
- The configured Commit selection and generated AGENTS.md use the new provider name.
- end-to-end-verification and all focused evaluations use the new live identities.
- Generated mirrors, catalogs, delivery contract tests, and focused suites pass.

## Dependencies

- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-resource-coordination-skills.md
- backlog/feature-backlog/apply-object-oriented-skill-group-design/align-codex-work-item-coordination-skill.md

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run individual probes and focused Dev Merge Coordinator, feature-branch delivery, direct-main delivery, pull-request, and end-to-end verification tests.
- Run scripts/test_complete_work_item_feature_branch.py, scripts/test_direct_main_completion_contract.py, scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Search maintained sources for the three former names and classify historical evidence separately.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Resolve the least disruptive project-configuration migration for existing Commit values while ensuring the final maintained configuration uses only the new provider identities.

## Crisis Dependency Reclassification

Reclassified At: 2026-08-05T17:10:30Z.

Transition: Ready -> Blocked.

Owner: Unowned.

Exact Blocker: Required dependency backlog/feature-backlog/apply-object-oriented-skill-group-design/align-codex-work-item-coordination-skill.md is Blocked. The resource-coordination dependency is Completed.

Blocker Owner: Dev Backlog Coordinator resolving the named dependency chain in Backlog Crisis Mode.

Unblock Condition: Align Codex Work-Item Coordination Skill reaches a terminal successful disposition and its delivered coordination interface is available on current main.

Coordinator Next Action: Keep this item in the crisis dependency set and do not dispatch it. After the unblock condition is satisfied, reconcile it through Blocked -> Ready under the normal lifecycle.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-work-merge/SKILL.md
- skills/agent-work-merge/agents/openai.yaml
- skills/integrate-agent-work/SKILL.md
- skills/integrate-agent-work/agents/openai.yaml
- skills/complete-work-item-feature-branch/SKILL.md
- skills/complete-work-item-feature-branch/agents/openai.yaml
- skills/deliver-work-item-feature-branch/SKILL.md
- skills/deliver-work-item-feature-branch/agents/openai.yaml
- skills/complete-work-item-direct-main/SKILL.md
- skills/complete-work-item-direct-main/agents/openai.yaml
- skills/deliver-work-item-direct-main/SKILL.md
- skills/deliver-work-item-direct-main/agents/openai.yaml
- skills/create-pull-request/SKILL.md
- skills/end-to-end-verification/SKILL.md
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml

### Allowed Dependent Artifacts

- approval-record-align-integration-and-delivery-skills.yaml
- PROJECT.yaml
- AGENTS.md
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-merge-coordinator
- evals/agent-tests/dev-verifier
- scripts/test_complete_work_item_feature_branch.py
- scripts/test_direct_main_completion_contract.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- scripts/render-agents-technology-skills.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/work-item-provider-and-completion-contracts.md
- design/orchestrated-development-lifecycle.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, configuration fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." The reviewed Concurrent Tasking and Direct Main Delivery diagrams show the exact renames, delivery family, and governed relationships covered here. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
