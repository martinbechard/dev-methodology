# Select Resource Coordination Per Project

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/selectable-resource-coordination.md

Completion: direct-main

## Historical Blocked State

- Owner: Unowned
- Claim: None
- Blocker: The required Configure Agent Claim Transport Adapters work item has not yet completed and its accepted transport contract is an input to this item.
- Unblock condition: backlog/feature-backlog/configure-agent-claim-transport-adapters.md is integrated, focused-verified, and archived as Completed on main.
- Next action owner: Dev Backlog Coordinator.
- Resumption: Reconcile the completed dependency, transition this item through Ready, acquire new exclusive ownership for one canonical Dev Orchestrator, and only then record Running.
- Evidence: The Dependencies section names Configure Agent Claim Transport Adapters; claim block-selectable-resource-coordination-dependency acquired event 0e436d62-4184-48ec-a689-e6aa12d56df5 to record this non-user dependency.

## Execution / Ownership

- Owner: Unowned
- Canonical task: 019f8b05-5251-7d73-9cc9-4057edfef9a0
- Claim: None
- Artifact claim: None.
- Branch: codex/selectable-resource-coordination-discovery-20260722
- Canonical worktree: /Users/martinbechard/.codex/worktrees/e483/dev-methodology
- Phase: awaiting exact governed-definition approval.
- Starting main: 1560326152977581d2c62711e9fb861e7f2cf8f0
- Lifecycle transition: Blocked eligibility was reconciled, the completed dependency made the item Ready, and fresh ownership then transitioned it to Running.
- Candidate: Pending.
- Accepted commit: Pending.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Dependency evidence: backlog/completed-backlog/features/configure-agent-claim-transport-adapters.md is Status Completed; integration commit 1b1b819fa051f9f0f1d572184b18f18c06d3cba0 is reachable from main; focused verification, archive, clean integration-claim release, and cleanup-eligibility evidence are recorded; Open issues is None.
- Preserved dependency boundary: The completed transport-adapter contract remains the required input to this item.
- Open issues: Exact scope-specific user approval is required before governed-definition mutation.
- Delivery evidence: Dependency unblock and discovery evidence are preserved; implementation is prohibited pending approval.
- Next owner: Unowned pending a user answer.

Creation Claim: draft-selectable-mutation-coordination

Refinement Claims: improve-selectable-mutation-coordination-019f850e, capture-resource-coordination-dialogue-20260721

## Cold-Start Recovery Execution — 2026-07-22

- Canonical task identity reconciled to 019f8b05-5251-7d73-9cc9-4057edfef9a0.
- Backlog recovery claim: cold-start-backlog-reconcile-2-019f8b00, acquired event 66822334-e85a-41aa-b2ad-6a6c433b6798 from primary main.
- Recovery phase: bounded governed-path discovery pending exact approval.
- The completed transport-adapter dependency and all prior evidence remain preserved.

## User Action Required

### Question For The User

Do you approve changes to exactly the following 40 governed-definition paths for Select Resource Coordination Per Project, so projects can select resource coordination as none or agent-claim, repositoryMutation remains an independent capability declaration, and none loads or requires no coordination lifecycle or evidence? Supported generated mirrors and directly related ordinary configuration, renderer, test, and documentation changes are included; no other governed definition will change without separate approval.

### Exact Governed Definition Manifest

- skills/agent-claim/SKILL.md
- skills/agent-claim/agents/openai.yaml
- skills/agent-role-authoring/SKILL.md
- skills/agent-work-merge/SKILL.md
- skills/codex-workitem-coordination/SKILL.md
- skills/codex-workitem-coordination/agents/openai.yaml
- skills/complete-work-item-direct-main/SKILL.md
- skills/complete-work-item-feature-branch/SKILL.md
- skills/create-file-work-item/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/documentation-reverse-engineer/SKILL.md
- skills/maintain-methodology-documentation/SKILL.md
- skills/manage-file-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md
- skills/structured-design/SKILL.md
- agents/roles/dev-activities/dev-artifact-reviewer.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-browser-operator.role.yaml
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml
- agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml
- agents/roles/dev-activities/dev-security-reviewer.role.yaml
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
- agents/roles/wiki-activities/wiki-researcher.role.yaml
- agents/roles/wiki-activities/wiki-source-collector.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Why User Input Is Required

Repository policy requires exact scope-specific approval before these governed definition mutations.

### Excluded Governed Surface

agents/role-schema.yaml is excluded because repositoryMutation remains unchanged and independent.

### Ordinary Companion Scope

PROJECT.yaml, AGENTS.md, README.md, project template, scripts/build-skill-docs.py, scripts/render-agents-technology-skills.py, focused role-policy/transport/renderer/bundle tests, relevant design pages, and supported generated role/skill/native-adapter/hierarchy/explorer/checklist/manifest outputs.

### Unattended Work Boundary

Do not mutate any governed definition, supported generated mirror, or ordinary companion surface until the user explicitly approves the exact manifest above. The canonical discovery task 019f8b05-5251-7d73-9cc9-4057edfef9a0 remains preserved as discovery evidence; current ownership remains unowned.

## Summary

Let each project explicitly choose whether it needs resource coordination and, when it does, which coordination skill supplies the policy. Projects that select none must not load or execute a coordination lifecycle.

## Context

The user-reviewed design dialogue on 2026-07-21 established that coordination covers more than repository mutation. Exclusive resources can include repository paths, browsers, browser profiles, databases, ports, servers, generated outputs, backlog state, and integration targets.

Current PROJECT.yaml configuration independently selects a work-item provider and completion process but has no resource-coordination selector. Conceptual mutating roles and several workflow skills are coupled directly to agent-claim, and scripts/build-skill-docs.py validates repositoryMutation by checking agent-claim membership. This makes claim use an agent-definition property instead of a project choice.

Work-item assignment is not operational resource ownership. GitHub, GitLab, and file-backed lifecycle records must not be used as the coordination mechanism for shared browsers, databases, repository paths, or similar resources.

## Source Evidence

- On 2026-07-21, the user corrected the original inventory by stating that shared browser and database use must not be recorded as GitHub assignment.
- In the subsequent reviewed dialogue, the user selected resource-coordination as the neutral concept, none and agent-claim as the immediate choices, project-level AGENTS.md rendering, no folder overrides, and no compatibility window.
- On 2026-07-21, the user explicitly requested creation of work items based on those conversations.

## Design Principles

- Name the neutral concept resource-coordination.
- Keep repositoryMutation as a declaration of mutation capability, independent from coordination selection.
- Add one project-wide selector with initial values none and agent-claim.
- Treat every value other than none as a real bundled or registered skill identifier.
- Do not support folder overrides initially because many coordinated resources cross folder boundaries.
- Render the selected coordination skill by reference in AGENTS.md only when coordination is enabled.
- When none is selected, load no coordination skill and require no acquisition, heartbeat, handoff, registry, or release evidence.
- Preserve ordinary durability through commits, clean-state checks, work-item evidence, cleanup, and recovery rules even when coordination is none.
- Keep provider-specific outcomes and evidence inside the selected coordination skill.
- Reject a missing or unsupported selector with direct guidance. Do not add a migration window or implicit default.
- Do not design a claims broker until a real claims-broker skill is proposed and approved.

## Requirements

- Add an explicit project-level resource-coordination selection independent from provider and completion selection.
- Support none and agent-claim initially.
- Make Project Configurator validate the selection and render the resulting reference-only AGENTS.md guidance.
- Remove the invariant that repositoryMutation directly determines agent-claim membership.
- Make mutating roles and ordinary workflow skills consume the project-selected coordination policy rather than hard-code agent-claim.
- Preserve agent-claim behavior when agent-claim is selected.
- Ensure none produces no coordination procedure and no claim-specific evidence requirements.
- Keep work-item assignment and lifecycle providers separate from operational resource ownership.
- Update the repository configuration and project template together; reject configurations missing the new required selector.
- Identify every governed canonical definition path and obtain exact, scope-specific user approval before mutating any of them.

## Acceptance Criteria

- The same mutating conceptual role can be configured for none or agent-claim without per-project edits to its canonical definition.
- Generated AGENTS.md guidance references the selected coordination skill only when coordination is enabled.
- A project selecting none performs no claim discovery, acquisition, heartbeat, registry mutation, or release.
- A project selecting agent-claim retains repository-path and named-resource contention, worktree, recovery, heartbeat, and release safety.
- Browser, database, port, server, generated-output, repository-path, backlog, and integration scenarios use the selected coordination policy rather than a work-item provider record.
- Missing and unsupported selections fail deterministically without fallback.
- Role validation no longer equates repositoryMutation with agent-claim membership.
- Focused configuration, generation, role, and lifecycle tests cover both selections.

## Dependencies

- [Configure Agent Claim Transport Adapters](configure-agent-claim-transport-adapters.md)

## Verification

- Repeat source discovery and produce the exact governed-source and supported-mirror manifest before implementation.
- Run the governed-definition pre-mutation check for every approved canonical definition.
- Test configuration validation and AGENTS.md rendering for none, agent-claim, missing, and unsupported selections.
- Exercise equivalent mutating work with coordination disabled and with agent-claim selected, including a named browser or database resource.
- Confirm provider records never act as operational resource authorities.
- Run focused generator freshness and bundle tests, Git diff validation, and independent methodology review.

## Open Questions

- Can every supported runtime compose a neutral coordination contract with one selected implementation without duplicating instructions, or must generation materialize a runtime-specific composition?
- Which existing workflow skills need a neutral coordination dependency, and which should remain unaware of coordination because their callers own that boundary?

## Notes

- none replaces the earlier single-writer proposal. Single-writer is not a coordination implementation.
- A future broker must be introduced as its own skill and work item.
- The exact governed-definition manifest is change-control evidence produced after source discovery, not a design principle.
