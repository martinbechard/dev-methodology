# Support Project-Level Skill Extensions

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/support-project-level-skill-extensions.md

Completion: direct-main

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Add an explicit PROJECT.yaml extension mechanism for project-selected skills whose references are appended to root AGENTS.md guidance.

## Context

The user proposed this capability during the resource-coordination dialogue on 2026-07-21. Current PROJECT.yaml configuration selects conceptual agents, workflow provider and completion skills, and folder technology skillsets, but it has no general project-level skill extension list.

Resource coordination is one consumer, but the extension mechanism must be generic rather than encoded as a coordination-only workaround.

## Source Evidence

- On 2026-07-21, the user proposed an extensions property in PROJECT.yaml that lets users add skills appended to project-level AGENTS.md guidance.
- The reviewed dialogue agreed to track its exact shape separately from the resource-coordination selector.
- On 2026-07-21, the user explicitly requested creation of work items based on those conversations.

## Requirements

- Define a documented PROJECT.yaml property for project-level skill extensions.
- Accept bundled skill identifiers and any explicitly supported registered-skill form.
- Validate duplicates, unknown identifiers, unavailable skills, and conflicts deterministically.
- Preserve declared order when order affects generated guidance; otherwise define stable canonical ordering.
- Render concise skill references at the end of root AGENTS.md without copying complete skill procedures.
- Keep folder technology-skill inlining and workflow selectors independent from this extension mechanism.
- Define how extensions interact with definition-owned skills so the same skill is not loaded twice.
- Update the project template, Project Configurator procedure, renderer, validation, documentation, and focused tests together.
- Obtain exact, scope-specific approval before changing governed skill definitions.

## Acceptance Criteria

- A project can declare one or more project-level extension skills in PROJECT.yaml.
- Generated root AGENTS.md contains deterministic reference-only guidance for each valid extension.
- Unknown, unavailable, duplicate, and conflicting entries fail with exact field paths and correction guidance.
- Nested AGENTS.md and folder technology skillsets are unchanged unless explicitly configured through their existing mechanisms.
- Existing definition-owned skills are not duplicated in generated instructions.

## Dependencies

None.

## Verification

- Design the exact YAML shape from existing PROJECT.yaml conventions.
- Test empty, single, multiple, duplicate, unknown, unavailable, and definition-owned-duplicate cases.
- Verify generated AGENTS.md placement and stable ordering.
- Run applicable project configuration, renderer, template, bundle, and documentation checks.
- Run Git diff validation and independent methodology review.

## Open Questions

- Should extensions be one ordered list or a mapping that can later carry setup-time validation metadata?
- Are project-level extensions inherited by nested AGENTS.md files or referenced only from the root-loaded contract?
