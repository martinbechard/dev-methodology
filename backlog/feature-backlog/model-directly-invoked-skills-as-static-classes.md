# Model Directly Invoked Skills As Static Classes

Status: Ready

Type: Feature

Provider: file

Work Item ID: model-directly-invoked-skills-as-static-classes

Completion: main-branch

## Summary

Extend the object-oriented Agent and Skill model with Static Classes for skills that callers invoke directly outside Agent definitions. Use the private Backlog Dispatcher skill and its invocation of the Dev Backlog Coordinator as the primary example, and align the dispatch-process documentation with the current Codex root-task launch constraint.

## Context

The design currently models Agents, Skills, Skill Groups, and related definition relationships. It does not give directly invoked operational skills a distinct object-oriented representation when those skills are not dependencies of an Agent definition.

The project-private `.agents/skills/backlog-dispatcher/SKILL.md` is such an entry point. It coordinates caller-owned runtime operations and invokes the Dev Backlog Coordinator Role, but it is not itself a portable Agent definition. Current Codex coordination also requires the caller-owned root task to perform work-item task creation. This runtime constraint explains why Backlog Dispatcher remains a Skill rather than an Agent.

Official OpenAI documentation supports only the broader public claims that Codex work can run as separate tasks or threads and that Skills package reusable instructions and workflows. Unless stronger official evidence is found, the root-only task-launch constraint must be described as current observed Codex runtime or harness behavior, not as a general OpenAI platform guarantee.

## Source Evidence

On 2026-08-12, after restarting Codex and completing the resource-claim repair, the user requested: add Static Classes to `design/object-oriented-agent-and-skill-model.md` for directly invoked skills outside Agent definitions; use the private Backlog Dispatcher as an example that invokes the Dev Backlog Coordinator; update the dispatch-process documentation to explain that Codex tasks can start other tasks only from root and therefore Backlog Dispatcher is a Skill rather than an Agent; and verify the claim in official OpenAI documentation.

Relevant repository sources are `design/object-oriented-agent-and-skill-model.md`, `design/agents/work-item-dispatching-and-delivery.md`, `.agents/skills/backlog-dispatcher/SKILL.md`, `skills/coordinate-codex-tasks/SKILL.md`, and the applicable conceptual Agent role definitions. Relevant official sources include OpenAI's Codex product documentation about multiple tasks or threads and Skills as reusable workflow packages.

## Requirements

- Define Static Class semantics and notation for a Skill that callers invoke directly without instantiating or attaching it to an Agent definition.
- Distinguish Static Classes from Agent dependencies, request-triggered skill loading, `AGENTS.md` provider selection, Interface Skills, Provider Skills, and Skill Groups.
- Use private Backlog Dispatcher as the primary worked example. Show that it invokes the Dev Backlog Coordinator Role while leaving caller-owned root task creation with the authorized runtime dispatcher.
- Explain why Backlog Dispatcher is modeled and placed as a project-private Skill rather than as an Agent.
- Preserve the boundary between project-private `.agents/skills` content and portable distributable skills or Agent definitions.
- Update `design/object-oriented-agent-and-skill-model.md` and the canonical dispatch-process documentation, including diagrams, terminology, navigation, examples, and cross-links that those documents own.
- Inspect `design/agents` and the complete `design/orchestrated-development-lifecycle.html` before choosing the final model and wording.
- Verify every OpenAI-platform statement against current official OpenAI documentation.
- Attribute only source-supported public behavior to OpenAI. Label the root-only task-launch constraint as observed current Codex runtime or harness behavior unless an official OpenAI source states that exact constraint.
- Update generated projections only through their canonical source and supported generator when repository discovery proves that a changed canonical source owns them.
- Apply the configured document-provenance contract to every changed maintained document.

## Acceptance Criteria

- The object-oriented model defines Static Class in a way that is consistent with the existing Agent, Skill, Interface Skill, Provider Skill, and Skill Group model.
- The model contains a clear Backlog Dispatcher example that invokes Dev Backlog Coordinator without representing Backlog Dispatcher as an Agent.
- The dispatch-process documentation explains the caller-owned root task boundary and the resulting Skill-versus-Agent design choice.
- Statements attributed to OpenAI have direct citations to current official OpenAI documentation; runtime-specific observations are clearly identified and are not overstated as public guarantees.
- Private placement and portable publication boundaries remain consistent with `.agents/skills/backlog-dispatcher/SKILL.md` and current project guidance.
- All affected navigation, links, diagrams, terminology, generated artifacts, and provenance are consistent and current.
- Fresh independent review finds no loss of lifecycle authority, runtime ownership, or object-model distinctions.

## Dependencies

None.

## Verification

- Run the repository-supported checks for changed design Markdown and HTML artifacts, links, navigation, provenance, and generated freshness.
- Verify any regenerated output by exact source-to-projection comparison through its supported generator.
- Check every external citation against the current official OpenAI source and confirm that the cited text supports the associated claim.
- Run focused regression tests for any changed design generator, catalog, or documentation projection.
- Run Git diff whitespace validation.
- Obtain fresh independent document-topic review, methodology-artifact review, and documentation verification before delivery.

## Open Questions

None. The implementer must resolve notation and exact document ownership from repository design authority without changing the requested semantics.

## Notes

The official OpenAI sources presently identified support separate Codex task or thread execution and reusable Skills. They do not presently establish the stronger root-only task-launch rule. Treat that distinction as a required truthfulness boundary during delivery.
