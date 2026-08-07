# Centralize General Agent Skill Routing

Status: Ready

Type: Defect

Provider: file

Work Item ID: centralize-general-agent-skill-routing

Completion: main-branch

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
