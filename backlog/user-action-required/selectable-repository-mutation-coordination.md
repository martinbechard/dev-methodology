# Selectable Operational Coordination

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/selectable-repository-mutation-coordination.md

Completion: direct-main

Creation Claim: draft-selectable-mutation-coordination

Refinement Claim: improve-selectable-mutation-coordination-019f850e

## Summary

Introduce a provider-neutral operational coordination contract and one independent project selector. Mutating roles and workflow skills use the contract, while the selector chooses either agent-claim or an explicit single-writer model.

## Source Evidence

- Repository mutation authority and operational coordination are separate decisions. The repositoryMutation field states whether a role may or must mutate repository state; it does not select the coordination implementation.
- Work-item providers record assignment and lifecycle state. They do not own repository paths or exclusive operational resources.
- Shared browsers, browser profiles, databases, ports, servers, generated-output refreshes, integration targets, and similar resources must be coordinated through the selected operational coordination implementation.
- The requested initial implementations are agent-claim and an explicit single-writer model.
- Creating and refining this work item does not authorize implementation or any governed-definition change.

## Context

### Current Facts

Live inspection on 2026-07-21 found:

- PROJECT.yaml and its template define independent provider and completion selectors, but no operational coordination selector.
- scripts/render-agents-technology-skills.py accepts only provider, completion, and optional selection policy under workflow_selection.
- agents/role-schema.yaml requires repositoryMutation with required, conditional, or never values.
- scripts/build-skill-docs.py directly validates repositoryMutation against fixed, conditional, or absent agent-claim membership.
- Twenty-five conceptual roles declare required or conditional repository mutation, and the same twenty-five role definitions reference agent-claim.
- Eight skills other than agent-claim name agent-claim directly: agent-role-authoring, agent-work-merge, complete-work-item-direct-main, complete-work-item-feature-branch, create-file-work-item, create-project-configuration, maintain-methodology-documentation, and manage-file-work-items.
- codex-workitem-coordination embeds claim-specific status, acquisition, heartbeat, release, wait, and completion-evidence behavior without naming agent-claim as a skill dependency.
- manage-github-work-items uses the phrase Claim or start for issue assignment and lifecycle transition, while manage-gitlab-work-items retains claim-release delivery evidence. These facts support a terminology and evidence-boundary review, but do not establish that either provider skill must implement operational coordination.

These facts identify coupling that a design must address. They are not an approved implementation manifest.

### Accepted Decision Boundaries

- Keep repositoryMutation independent from the selected operational coordination implementation.
- Keep work-item provider, completion process, and operational coordination as independent project decisions.
- Treat work-item ownership as assignment and lifecycle state only.
- Route ownership of repository paths and exclusive operational resources through the selected operational coordination implementation, never through GitHub, GitLab, or file-backed work-item records.
- Keep agent-claim as a supported implementation rather than removing it.
- Define single-writer as an explicit exclusivity model, not an absence of concurrency safety.

## Proposed Design

Define a provider-neutral contract for the operational lifecycle needed by mutating work:

- inspect current ownership or exclusivity state;
- establish ownership of repository paths and named operational resources;
- handle contention or unavailable exclusivity;
- maintain long-running ownership when the implementation requires it;
- release or hand off ownership; and
- return implementation-appropriate completion evidence.

Add one project-level selector, independent from provider and completion selection, with these initial implementations:

- agent-claim uses the repository-global claim registry and retains its current atomic ownership, contention, worktree, recovery, heartbeat, shared-resource, and release behavior.
- single-writer performs no claim-registry operations because an identified project or execution authority guarantees exclusive mutation. It still requires clean delivery state, resource cleanup, verification, commit or truthful no-change evidence, and safe handoff.

The contract form, selector field name, override shape, compatibility default, and exact source placement remain design decisions.

## Evidence-Backed Candidate Scope

A design pass must re-check and narrow these surfaces before seeking implementation approval:

- operational contract and agent-claim provider behavior;
- the eight directly coupled workflow and authoring skills listed under Current Facts;
- claim-specific behavior in codex-workitem-coordination;
- PROJECT.yaml, the project template, and project-guidance rendering and validation;
- repositoryMutation validation in agents/role-schema.yaml and scripts/build-skill-docs.py;
- the twenty-five mutating or conditionally mutating conceptual role definitions;
- focused tests, supported generated mirrors, README inventory, and design pages owned by approved canonical changes; and
- provider terminology or terminal-evidence wording only where inspection proves that it confuses assignment with operational ownership.

Do not treat this candidate scope as exact governed-definition approval. The implementation request must enumerate every governed canonical path, remove unnecessary paths, identify supported generated mirrors, and obtain scope-specific approval before mutation.

## Open Decisions

- What is the provider-neutral contract artifact and which component resolves it at runtime or generation time?
- What is the selector field name, and does it support folder overrides or only one project-wide value?
- Which authority records and enforces the single-writer guarantee?
- What deterministic compatibility behavior applies when an existing project lacks the selector?
- Which claim-specific completion evidence becomes generic operational evidence, and which remains exclusive to agent-claim?
- What is the final exact governed-definition manifest after design and fresh discovery?

## Requirements

- Make mutating role definitions and ordinary workflow skills depend on the provider-neutral operational coordination contract rather than directly on agent-claim.
- Add one explicit project selector with initial supported values equivalent to agent-claim and single-writer.
- Preserve repositoryMutation solely as the role mutation-capability declaration.
- Resolve work-item provider, completion process, and operational coordination independently.
- Route repository paths and named exclusive resources through the selected operational coordination implementation.
- Limit GitHub, GitLab, and file-backed work-item ownership to provider-appropriate assignment and lifecycle state.
- Preserve current agent-claim safety behavior when agent-claim is selected.
- Require a named external exclusivity authority and no claim acquisition, heartbeat, registry mutation, or claim-release evidence when single-writer is selected.
- Fail explicitly for unsupported or unavailable coordination selections, and for missing selections after the approved migration boundary makes the selector required. Do not silently switch implementations.
- Preserve normal verification, commit, clean-state, cleanup, publication, and handoff requirements under both implementations where applicable.
- Provide deterministic migration and generation behavior for existing projects and generated role definitions.
- Keep provider procedures out of PROJECT.yaml and AGENTS.md except for source-backed project-specific overrides.
- Perform no governed-definition mutation until the exact path manifest has scope-specific user approval and passes the repository pre-mutation check.

## Acceptance Criteria

- One project setting selects agent-claim or single-writer without changing canonical role definitions per project.
- The same mutating role definition can operate under either supported implementation.
- Role validation no longer equates repositoryMutation directly with agent-claim membership.
- Agent-claim selection preserves current repository-path and shared-resource contention, recovery, worktree, heartbeat, and release outcomes.
- Single-writer selection performs no claim-registry mutation and cannot report claim acquisition or release evidence.
- Single-writer selection identifies the authority that guarantees exclusivity and still enforces normal delivery safety checks.
- Browser, database, port or server, generated-output, repository-path, backlog, and main-integration scenarios route operational ownership through the selected implementation.
- GitHub, GitLab, and file-backed scenarios record assignment and lifecycle state without representing operational resource ownership.
- Unsupported and unavailable selections fail deterministically without fallback. Missing selections follow the approved compatibility rule and fail once the approved migration boundary requires the selector.
- Existing projects follow an explicitly approved and tested compatibility rule.
- Focused tests cover selector validation, role generation, both coordination lifecycles, provider boundaries, and completion evidence.
- Approved canonical sources, only their supported generated mirrors, documentation, and regression expectations remain synchronized.
- Independent methodology review accepts the final contract boundary, migration behavior, and exact governed-definition diff.

## Dependencies

None.

## Verification

- Re-run source discovery and produce an exact canonical-path and generated-mirror manifest before implementation approval.
- Run the governed-definition pre-mutation check for each approved canonical definition.
- Add focused selector, schema, generator, role, provider-boundary, completion, and coordination-lifecycle tests.
- Exercise equivalent mutation work under agent-claim and single-writer, including shared browser and database resources.
- Verify that work-item provider records never act as operational ownership authorities.
- Run applicable freshness checks, focused bundle tests, Git diff validation, and independent methodology review.
- Escalate verification only when the final affected surfaces or failed focused checks justify it.

## User Action Required

The next mutating step requires user authorization. Repository policy also requires a later exact, scope-specific approval before any governed definition changes.

## Question For The User

Do you authorize a design-only precursor that resolves the open decisions and produces the exact governed-definition manifest without changing governed definitions?

## Why User Input Is Required

The current authority covers only this backlog refinement. It does not authorize a new design artifact or implementation, and the current evidence is not an exact governed-definition approval manifest.

## Options And Tradeoffs

- Authorize the design-only precursor: narrow the contract, selector, migration, and exact approval scope before implementation.
- Supply the unresolved design decisions and request an exact approval manifest directly: reduce a separate design step but require the user to choose the open policy details.
- Defer: keep the feature visible and non-dispatchable without creating more artifacts.

## Resolution

Pending.

## Unattended Work Boundary

Read-only discovery and refinement of this one backlog item are allowed. Do not create a design artifact or change any skill, agent definition, schema, generator, generated mirror, project configuration, documentation, test, or implementation file until the required user authorization is recorded. Do not infer approval from this item, repository access, or a request to make validation pass.

## Notes

- Removing agent-claim is not a goal.
- Do not encode the choice as a boolean that leaves the no-claim safety model unnamed.
- The coordination-registry simplification item has a separate outcome and is not a duplicate of this feature.
