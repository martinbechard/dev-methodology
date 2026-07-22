# Select Resource Coordination Per Project

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/selectable-resource-coordination.md

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

- Owner: Dev Orchestrator
- Canonical task: 019f8b1d-5817-72f3-be99-ba471da716b9
- Claim: start-selectable-resource-coordination-019f8b1d (backlog transition only)
- Artifact claim: Pending fresh artifact claim.
- Branch: codex/selectable-resource-coordination-implementation-20260722
- Canonical worktree: /Users/martinbechard/.codex/worktrees/3da9/dev-methodology
- Phase: implementing approved resource-coordination loading separation.
- Starting main: f5534ec28fd8e1c75efb65970de61918406992a0
- Lifecycle transition: Ready -> Running after exact approval, fresh canonical task assignment, and successful serialized backlog claim acquisition.
- Candidate: Pending.
- Accepted commit: Pending.
- Review: Pending.
- Verification: Pending.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Dependency evidence: backlog/completed-backlog/features/configure-agent-claim-transport-adapters.md is Status Completed; integration commit 1b1b819fa051f9f0f1d572184b18f18c06d3cba0 is reachable from main; focused verification, archive, clean integration-claim release, and cleanup-eligibility evidence are recorded; Open issues is None.
- Preserved dependency boundary: The completed transport-adapter contract remains the required input to this item.
- Open issues: None for lifecycle dispatch; implementation remains within the approved scope.
- Delivery evidence: Dependency unblock, discovery evidence, and exact approval are preserved; implementation, review, verification, integration, and acceptance are pending.
- Next owner: Dev Orchestrator.

Creation Claim: draft-selectable-mutation-coordination

Refinement Claims: improve-selectable-mutation-coordination-019f850e, capture-resource-coordination-dialogue-20260721

## Running Dispatch — 2026-07-22

- Canonical task: 019f8b1d-5817-72f3-be99-ba471da716b9.
- Backlog transition claim: start-selectable-resource-coordination-019f8b1d, acquired event a7765c3b-c035-4ea1-834a-e959cfdab2f5 from primary main.
- Branch and worktree: codex/selectable-resource-coordination-implementation-20260722 at /Users/martinbechard/.codex/worktrees/3da9/dev-methodology.
- Starting main: f5534ec28fd8e1c75efb65970de61918406992a0.
- Phase: implementing approved resource-coordination loading separation.
- The complete approval Resolution, 40-path manifest, loading clarification, and discovery evidence remain preserved below.

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

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "ok make sure it is clear in the workitem" followed immediately by "that was my approval" in parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2.
- Approved governed scope: exactly the 40-path manifest above.
- Approved dependent scope: supported generated mirrors plus PROJECT.yaml, AGENTS.md, README.md, project template, scripts/build-skill-docs.py, scripts/render-agents-technology-skills.py, focused role-policy/transport/renderer/bundle tests, relevant design pages, and supported generated role/skill/native-adapter/hierarchy/explorer/checklist/manifest outputs.
- Exclusion: no other governed definition is authorized.
- Disposition: Ready for fresh canonical dispatch. This approval does not create or assign a canonical task and does not authorize a transition to Running.

### Why User Input Is Required

Repository policy requires exact scope-specific approval before these governed definition mutations.

### Excluded Governed Surface

agents/role-schema.yaml is excluded because repositoryMutation remains unchanged and independent.

### Ordinary Companion Scope

PROJECT.yaml, AGENTS.md, README.md, project template, scripts/build-skill-docs.py, scripts/render-agents-technology-skills.py, focused role-policy/transport/renderer/bundle tests, relevant design pages, and supported generated role/skill/native-adapter/hierarchy/explorer/checklist/manifest outputs.

### Unattended Work Boundary

The user approved the exact governed manifest and dependent scope recorded in Resolution. Do not mutate any other governed definition. The canonical discovery task 019f8b05-5251-7d73-9cc9-4057edfef9a0 remains preserved as discovery evidence; current ownership remains unowned until fresh canonical dispatch.

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
- On 2026-07-22, the user asked for clarification of generic core workflow skills versus the project-selected resource-coordination implementation and directed that it be clear in this work item.

## Core Workflow And Selected Implementation Boundary

- Conceptual core role definitions do not directly list or load the project-selected resource-coordination implementation, including agent-claim.
- Generic technology-agnostic workflow skills, such as codex-workitem-coordination, may remain core skills of roles that own those workflows. This change does not move every coordination-related workflow skill into AGENTS.md.
- PROJECT.yaml independently selects resource coordination as none or agent-claim.
- Generated project-level AGENTS.md guidance references the selected implementation by name and by reference only when it is enabled. Agents operating in that project apply that selected implementation together with their core role and workflow skills.
- Selecting none renders no resource-coordination skill reference or procedure and requires no claim lifecycle or evidence.
- Intended chain: core role -> generic workflow skills -> PROJECT.yaml resource-coordination selection -> generated AGENTS.md reference -> selected resource-coordination implementation.

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
- Keep generic workflow skills in conceptual core role definitions where their owners need them; do not directly list or load the project-selected resource-coordination implementation there.
- Render the selected resource-coordination implementation from PROJECT.yaml into project-level AGENTS.md by name and reference only when enabled.
- Make mutating roles and ordinary workflow skills consume the project-selected coordination policy rather than hard-code agent-claim.
- Preserve agent-claim behavior when agent-claim is selected.
- Ensure none produces no coordination procedure and no claim-specific evidence requirements.
- Keep work-item assignment and lifecycle providers separate from operational resource ownership.
- Update the repository configuration and project template together; reject configurations missing the new required selector.
- Identify every governed canonical definition path and obtain exact, scope-specific user approval before mutating any of them.

## Acceptance Criteria

- The same mutating conceptual role can be configured for none or agent-claim without per-project edits to its canonical definition.
- Generated AGENTS.md guidance references the selected coordination skill only when coordination is enabled.
- Conceptual core role definitions retain generic workflow skills but do not directly list or load the selected resource-coordination implementation.
- The generated loading chain is core role -> generic workflow skills -> PROJECT.yaml resource-coordination selection -> generated AGENTS.md reference -> selected resource-coordination implementation.
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
