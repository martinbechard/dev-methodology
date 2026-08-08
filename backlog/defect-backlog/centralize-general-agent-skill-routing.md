# Centralize General Agent Skill Routing

Status: Running

Type: Defect

Provider: file

Owner: Dev Orchestrator task 019faeed-f816-7d43-819d-814bad4e309c

Work Item ID: centralize-general-agent-skill-routing

Completion: main-branch

Canonical Conversation: 019faeed-f816-7d43-819d-814bad4e309c

Root Agent Task: 019faeed-f816-7d43-819d-814bad4e309c

Branch: main

Worktree: /Users/martinbechard/dev/dev-methodology

Phase: Independent review findings awaiting Coordinator disposition

## Summary

Represent skills that apply across all Agents in one General Agent Skills design and in the shared configuration mechanisms that supply them, instead of repeating them as role-owned dependencies in selected Agent definitions and skill-group documents.

## Context

`organise-project-files` is already configured once in `PROJECT.yaml` through `shared_agent_skills`, so any Agent can load it when file placement must be chosen or audited. `structured-explanation` has a similarly general activation boundary, but it is currently repeated in twelve role definitions and several Agent-group diagrams. That mixture makes the same class of dependency look project-wide in one case and role-owned in the other, and it obscures how general skills apply to every Agent.

## Source Evidence

On 2026-08-06, while reviewing the Agent and skill organization, the user instructed: “General skills like structured-explanation and organise-project-files should be in a separate skills design explaining how they apply to all of the agents.” Repository inspection then confirmed that `organise-project-files` is project-wide through `PROJECT.yaml`, while `structured-explanation` is repeated in twelve role definitions. The user also instructed: “don't forget to log defects for corrections.”

## Requirements

- Add one steady-state General Agent Skills design that explains universally supplied skills and project-wide conditional skills.
- Configure `structured-explanation` as a project-wide conditional skill alongside `organise-project-files`.
- Keep `effective-communication` and `ste-technical-writing` as universal role-schema skills and explain their narrower operating boundaries.
- Remove duplicate role-owned `structured-explanation` declarations and repeated general-skill nodes from Agent-group diagrams.
- Link Agent-group documents to the General Agent Skills design instead of restating the shared routing.
- Regenerate derived Agent definitions, root guidance, hierarchy artifacts, and documentation data from their authoritative sources.

## Acceptance Criteria

- One design shows how all Agents receive universal and conditional general skills without drawing an Agent-to-`AGENTS.md` dependency.
- `PROJECT.yaml` and its project template both route `structured-explanation` and `organise-project-files` through `shared_agent_skills` with explicit conditions.
- No role definition directly declares `structured-explanation` or `organise-project-files`.
- Agent-group diagrams contain only dependencies specific to the Agents and groups they explain.
- Generated adapters and documentation remain synchronized with the role schema, role definitions, and project configuration.
- Focused shared-skill, bundle, generation, and documentation checks pass.

## Dependencies

None.

## Verification

- Run the focused shared Agent skill tests.
- Run Agent rendering and generated-artifact synchronization checks.
- Run the focused bundle tests that validate role and shared-skill relationships.
- Run Markdown structure, link, Mermaid, and page verification for the changed design documents.
- Run `git diff --check`.

## Open Questions

None.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T03:27:50Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: Existing Root Dev Orchestrator task 019faeed-f816-7d43-819d-814bad4e309c for this exact work item.

Normalized Objective: Centralize universally and conditionally applicable Agent skill routing in a General Agent Skills design and shared configuration, remove duplicated role and diagram declarations, regenerate derived artifacts, and preserve the narrower universal role-schema skill boundaries.

Dispatch Time: 2026-08-07T03:27:50Z

Intended Root Role: Dev Orchestrator

Launch Result: Started

Canonical Execution: 019faeed-f816-7d43-819d-814bad4e309c

Last Contact: 2026-08-07T03:27:50Z; existing canonical task confirmed by parent Coordinator.

Next Reconciliation At: 2026-08-07T03:42:50Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019faeed-f816-7d43-819d-814bad4e309c

Evidence: The parent Coordinator restored this same canonical task to Starting in commit `6eb6800707e5f24d09daec3db0b5773070643421`. Candidate `555764d4` and its 29 focused tests plus freshness, YAML, and diff evidence remain preserved. The canonical task reacquired exact Work Item ID activity=work claim `centralize-general-agent-skill-routing-work-019faeed-resume` and exact provider-path claim `centralize-general-agent-skill-routing-running-path-019faeed-resume`; it has not repeated implementation or any accepted green gate.

Observed At: 2026-08-08T16:28:31Z

Started At: 2026-08-08T16:28:17Z

Deadline or Expires At: 2026-08-08T20:28:31Z

Next Action: Dev Backlog Coordinator determines the lifecycle disposition and coordinates correction of the three recorded review findings. Do not start verification or delivery unless a corrected candidate receives an accepted independent review.

Next Reconciliation At: 2026-08-08T16:43:31Z

## Independent Review Evidence

Reviewed Candidate: `555764d4`

Reviewer: Fresh Methodology Artifact Reviewer task `/root/review_general_skill_routing`

Review Result: BLOCKED

Review Scope: Documentation and methodology consistency, shared conditional routing, role-source declarations, Agent-group documentation, generated synchronization visible in the immutable candidate, and consistency with the object-oriented Agent and Skill model.

Findings:

1. Medium: `design/agents/general-agent-skills.md` treats Agent-wide applicability as a Skill Group even though `design/object-oriented-agent-and-skill-model.md` defines a Skill Group as a cohesive methodology capability. Model this as a distinct cross-cutting applicability view or explicitly extend the governing model.
2. Medium: `design/object-oriented-skill-group-models.md` retains stale nine-group, fifty-skill, and seven-design counts while the candidate registry contains ten groups, fifty-two skills, and eight Agent-oriented designs.
3. Low: `design/agents/backlog-management.md`, `design/agents/documentation-methodology.md`, and `design/agents/main-branch-delivery.md` lack the General Agent Skills link promised by the new design.

Accepted Review Evidence: YAML routing, removal of direct role declarations, generated root guidance, manifest entries, and representative generated adapters were otherwise synchronized. The reviewer did not rerun the preserved 29 tests or any accepted freshness, YAML, or diff gate.

## Holding Pause Evidence

Pause Authority: User-directed immediate stop for low-token conservation

Preserved Candidate: 555764d4

Preserved Evidence: 29 focused tests plus freshness, YAML, and diff checks

Canonical Task: 019faeed-f816-7d43-819d-814bad4e309c

Branch: main

Worktree: /Users/martinbechard/dev/dev-methodology

Stopped Child Inventory: None

Implementation Path Release Event: d61a5c54-2cc7-488d-8901-543a63933489

Work Handoff Release Event: 2b56c35b-08a6-44e1-a993-8a39ed7139bd

Resumption Condition: The parent Coordinator must move this item from Holding to Ready, then from Ready to Starting for this same canonical task. The root task must then move it from Starting to Running before any review or further work.

## Ready Resumption Evidence

Transition: Holding -> Ready

Resumption Authority: Explicit user directive received by parent Coordinator on 2026-08-08.

Owner: Unowned

Canonical Task: 019faeed-f816-7d43-819d-814bad4e309c

Next Action: Parent Coordinator records Ready -> Starting for the preserved canonical task; no implementation, review, verification, or integration work is authorized by this transition.

## Current Starting Handoff Evidence

Starting Recorded At: 2026-08-08T16:23:23Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: Existing Root Dev Orchestrator task 019faeed-f816-7d43-819d-814bad4e309c for this exact work item.

Normalized Objective: Centralize the General Agent Skills design and shared conditional routing while preserving the retained candidate, focused evidence, and canonical task identity.

Launch Result: Started

Canonical Execution: 019faeed-f816-7d43-819d-814bad4e309c

Last Contact: 2026-08-08T16:23:23Z; existing canonical task confirmed by parent Coordinator.

Next Reconciliation At: 2026-08-08T16:38:23Z
