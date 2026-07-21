# Selectable Repository Mutation Coordination

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/selectable-repository-mutation-coordination.md

Completion: direct-main

Creation Claim: draft-selectable-mutation-coordination

## Summary

Introduce a neutral repository-mutation coordination contract and a simple project-level selector so a project can deliberately use agent claims or operate under an explicit single-writer contract without rewriting agent definitions and workflow skills.

## Context

Repository mutation capability and claim coordination are currently coupled. Canonical agent definitions declare repositoryMutation and load agent-claim directly, generation validates that relationship, and several workflow skills prescribe claim acquisition, heartbeat, release, and claim-release evidence.

The desired architecture combines two previously discussed options:

- Define a neutral mutation-coordination interface that roles and workflow skills depend on instead of depending directly on agent-claim.
- Expose one project-level selector that chooses the coordination implementation.

Work-item ownership and operational resource ownership are different concerns. GitHub, GitLab, and file-backed providers may record assignment, lifecycle state, or the agent currently working on an item. They must not be treated as the authority for exclusive repository paths or shared runtime resources. Browsers, browser profiles, databases, ports, servers, generated-output refreshes, integration targets, and other exclusive runtime resources belong to the selected operational coordination provider, not to GitHub or another work-item provider.

## Source Evidence

- The user requested a draft work item combining option 2, a mutation-coordination interface, with option 1, a project-level selection mechanism, on 2026-07-21.
- The user clarified that shared browser or database ownership must not be recorded in GitHub and rejected conflating work-item assignment with operational resource coordination.
- Live source inspection found direct claim behavior in agent-claim, agent-work-merge, codex-workitem-coordination, both completion skills, and the file-work-item creation and management skills. Role generation currently validates agent-claim membership against repositoryMutation.

## Proposed Design Direction

Define one provider-neutral coordination contract for operations such as:

- inspect current operational ownership;
- acquire and extend repository-path or exclusive-resource ownership;
- report contention;
- maintain ownership during long-running work;
- release or hand off operational ownership; and
- produce provider-appropriate completion evidence.

Supply at least two implementations:

- agent-claim: use the repository-global coordination registry and retain the current file, worktree, shared-resource, heartbeat, recovery, and release semantics;
- single-writer: perform no claim-registry mutation because the project or execution environment guarantees a single writer, while retaining clean-worktree, resource-cleanup, commit, and truthful completion requirements.

Add one explicit project selector, separate from work-item provider and completion workflow selection. The exact field name is a design decision, but its meaning must be equivalent to selecting agent-claim or single-writer for operational mutation coordination. Existing projects should default to agent-claim unless they explicitly choose another supported provider.

## Proposed Governed Definition Scope

The following is a draft scope for later explicit approval. Creation of this work item does not authorize mutation of these definitions.

### New Definition

- skills/repository-mutation-coordination/SKILL.md

### Existing Skill Definitions

- skills/agent-claim/SKILL.md
- skills/agent-role-authoring/SKILL.md
- skills/agent-work-merge/SKILL.md
- skills/codex-workitem-coordination/SKILL.md
- skills/complete-work-item-direct-main/SKILL.md
- skills/complete-work-item-feature-branch/SKILL.md
- skills/create-file-work-item/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/maintain-methodology-documentation/SKILL.md
- skills/manage-file-work-items/SKILL.md
- skills/manage-github-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md

### Conceptual Agent Definitions

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

### Definition Schema And Supporting Implementation

- agents/role-schema.yaml
- skills/development-methodology/assets/templates/project-template.yaml
- scripts/build-skill-docs.py
- scripts/render-agents-technology-skills.py
- focused tests, supported generated mirrors, README inventory, and design documentation directly owned by the approved canonical changes

The implementation owner must re-run source discovery before requesting approval. If the design can avoid changing some listed definitions, narrow the approval scope. If another governed definition is necessary, stop and obtain additional exact approval before mutation.

## Requirements

- Keep repositoryMutation as the declaration of whether an agent may or must mutate repository state. Do not make that field select a coordination implementation.
- Make agent definitions and ordinary workflow skills depend on the provider-neutral coordination contract rather than directly requiring agent-claim.
- Add an explicit project-level operational-coordination selector whose supported initial choices are agent-claim and single-writer.
- Keep work-item provider selection, completion workflow selection, and operational coordination selection independent.
- Preserve agent-claim as the default for existing projects unless an explicit migration policy approved during implementation selects another default.
- Preserve agent-claim support for exact files, trees, backlog, integration resources, browsers, browser profiles, databases, ports, servers, generated outputs, shared installations, and other named exclusive resources.
- Define single-writer as an explicit external exclusivity contract, not as silent uncontrolled concurrency. Document who or what guarantees that only one mutating execution owns repository and runtime state.
- Do not acquire, heartbeat, release, or require claim-release evidence when single-writer is selected.
- Retain commit, clean-worktree, runtime cleanup, verification, handoff, and truthful no-change requirements under both providers where applicable.
- Replace ambiguous work-item phrases such as claim an item with assign, start, or another provider-accurate lifecycle term. GitHub, GitLab, and file-backed work-item state must not represent ownership of a browser, database, repository path, port, server, or integration target.
- Make unavailable or unsupported coordination selections fail explicitly. Do not silently fall back from agent-claim to single-writer or from single-writer to agent-claim.
- Keep project-specific coordination overrides separate from the generic provider contract and do not copy complete provider procedures into PROJECT.yaml or AGENTS.md.
- Provide a deterministic migration path for existing PROJECT.yaml files and generated agent definitions.

## Acceptance Criteria

- One explicit project setting selects agent-claim or single-writer operational coordination without editing canonical role definitions.
- The same mutating role definition can run under either supported coordination provider.
- Role validation no longer equates repositoryMutation directly with agent-claim membership.
- Selecting agent-claim preserves current atomic path and shared-resource ownership, contention, recovery, worktree, heartbeat, and release behavior.
- Selecting single-writer produces no coordination-registry mutation and no claim-release completion requirement while preserving the declared external exclusivity and normal delivery safety checks.
- GitHub, GitLab, and file-backed work-item providers record only provider-appropriate assignment and lifecycle evidence. They never become the operational authority for shared runtime resources.
- A focused browser-sharing scenario and a focused database-sharing scenario prove that operational resource ownership is routed through the selected coordination provider and not through a work-item provider.
- A focused single-writer scenario proves that a mutating task completes without claim acquisition or release and cannot falsely report claim evidence.
- A focused agent-claim scenario proves that two writers contending for the same repository path or runtime resource retain the current safe outcome.
- Existing projects without the new selector follow the approved compatibility default deterministically.
- Canonical definitions, supported generated mirrors, project configuration rendering, documentation, and focused regression tests remain synchronized.
- Fresh independent methodology review accepts the final provider boundary, migration behavior, and exact governed-definition diff.

## Dependencies

None.

## Verification

- Run the governed-definition approval check separately for every approved canonical definition before mutation.
- Add focused schema and generator tests for independent repository-mutation and coordination-provider selection.
- Add provider-contract tests that execute equivalent mutation lifecycles through agent-claim and single-writer.
- Verify browser, database, repository-path, backlog, and main-integration resource routing.
- Verify GitHub, GitLab, and file-backed work-item records contain assignment and lifecycle evidence without pretending to own operational resources.
- Run focused role-generation, skill validation, configuration rendering, bundle-content, claim-engine compatibility, and completion-workflow tests.
- Regenerate only mirrors supported by the approved canonical source categories and run freshness checks.
- Run Git diff validation and obtain fresh independent methodology review.
- Escalate verification tier only when the final affected surfaces or failed focused checks justify it.

## User Action Required

Explicit scope-specific approval is required before adding or changing the proposed distributed skill definitions, conceptual agent definitions, or agent-definition schema.

## Question For The User

After the draft is reviewed and narrowed as needed, do you approve the exact governed definition paths listed under Proposed Governed Definition Scope for implementation of selectable repository mutation coordination?

## Why User Input Is Required

Repository policy requires exact approval before any governed skill or agent definition changes. The current request authorizes only creation of this draft work item.

## Options And Tradeoffs

- Approve the final exact scope: implement the interface and selector as one coherent cross-cutting feature.
- Request a design-only precursor: produce a non-mutating design that narrows the definition and generator scope before approval.
- Narrow the feature: introduce only the project selector and retain direct agent-claim dependencies temporarily, accepting transitional branching in workflow skills.
- Defer: move the item to Holding without authorizing implementation.

## Resolution

Pending.

## Unattended Work Boundary

Do not create or change any proposed skill definition, agent definition, schema, generated mirror, implementation, or documentation under this item until exact governed-definition approval is recorded. Read-only discovery and refinement of this work item remain allowed.

## Notes

- Removing agent-claim is not a goal. The feature makes operational coordination selectable.
- A bare boolean such as use claims is discouraged because it does not name the safety model used when claims are disabled.
- The existing coordination-registry reset and branch-integration work item has a distinct outcome and is not a duplicate of this provider-selection feature.
