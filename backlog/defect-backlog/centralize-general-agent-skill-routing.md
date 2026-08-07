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

Phase: General Agent Skills routing and design alignment

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

Evidence: The canonical task accepted the existing implementation, loaded the applicable methodology, file-placement, explanation, and work-item lifecycle skills, logged the defect, and acquired the exact Work Item ID activity=work claim before repository implementation.

Observed At: 2026-08-07T03:29:07Z

Started At: 2026-08-07T03:29:07Z

Deadline or Expires At: Governed by the active work-item claim and parent coordination policy.

Next Action: Centralize project-wide conditional skill routing, create the General Agent Skills design, remove duplicated role and Agent-group declarations, regenerate derived artifacts, and verify the synchronized result.

Next Reconciliation At: 2026-08-07T03:44:07Z
