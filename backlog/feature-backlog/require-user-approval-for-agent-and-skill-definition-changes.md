# Require User Approval For Agent And Skill Definition Changes

Status: Ready

Type: Feature

## Summary

Require explicit user approval before any agent definition or skill definition is changed. Preserve ordinary authority to change implementation code and tests, but prevent testing, repair, review, verification, and maintenance agents from rewriting definitions merely to make a test pass when the test or fixture may be incorrect.

## Context

The user explicitly authorized this feature after clarifying the intent of a prior Proposed restriction. The restriction is an authority boundary, not a general freeze on implementation or test maintenance: when a test fails, agents must investigate whether the product definition or the test is wrong and may repair an incorrect test within ordinary task authority, but they must not change an agent or skill definition without explicit user approval.

PROJECT.yaml is the repository's canonical project configuration and reviewable intent log. The Project Configurator and create-project-configuration workflow own reconciliation of that configuration with repository evidence and deterministic AGENTS.md guidance. The root AGENTS.md is the operational contract supplied to agents, so the directive must be recorded canonically in PROJECT.yaml and rendered into AGENTS.md through the supported Project Configurator/rendering path rather than maintained as divergent hand-written policy.

Repository evidence identifies these governed definition surfaces:

- agents/roles/**/*.role.yaml contains the canonical conceptual agent definition sources.
- skills/*/SKILL.md contains canonical distributed skill definitions, including skill instructions, frontmatter identity, and description.
- adapters/*/skills/*/SKILL.md contains adapter-owned skill definitions that are distributed only for the matching runtime.
- Adjacent skill metadata such as skills/*/agents/openai.yaml is governed when a requested change alters the skill's exposed identity, description, invocation policy, or tool dependencies.
- agents/role-schema.yaml, agents/model-profiles.yaml, and adapter mappings are supporting definition-model inputs. A change to them requires approval when it changes the meaning or generated representation of an agent definition.
- generated/adapters/**, design/generated/role-definitions.js, design/generated/skill-definitions.js, and generated/adapters/agent-generation-manifest.json are derived mirrors. They are regenerated from approved canonical sources and are never edited directly. Regeneration that only reflects an already approved source-definition change does not require a second approval.

Ordinary implementation source, test code, test fixtures, documentation unrelated to a definition, and generated outputs unrelated to agent or skill definitions remain outside this approval boundary unless the requested change would itself alter a governed definition.

## Requirements

- Add one canonical project-level directive to PROJECT.yaml stating that every change to an agent definition or skill definition requires explicit user approval.
- State in the directive that repository access, a failing test, a repair assignment, or a desire to make validation pass does not constitute approval to change a definition.
- State that a testing or repair agent must consider and investigate whether a failing test, fixture, assertion, or expected result is incorrect before proposing a definition change.
- Preserve the distinction between governed definition changes and ordinary authorized implementation or test changes. Do not require separate user approval merely to correct an incorrect test when the correction does not change a governed definition.
- Make approval specific and auditable. The lifecycle evidence must identify the user's approval and the exact definition scope it authorizes; silence, unrelated prior approval, and broad repository mutation authority are insufficient.
- Inspect and use the live PROJECT.yaml schema and Project Configurator contract. Extend the canonical configuration and renderer only as needed so the directive has one source of truth and a deterministic operational representation.
- Regenerate AGENTS.md through the supported Project Configurator and scripts/render-agents-technology-skills.py path. Do not hand-edit a policy copy that can drift from PROJECT.yaml, and do not discard unrelated maintained AGENTS.md sections while rendering the configured directive.
- Apply the approval gate to canonical conceptual agent sources, canonical distributed and adapter-owned skill sources, and definition-affecting metadata or schema inputs identified in Context.
- Keep generated mirrors source-owned. Regenerate generated/adapters, design/generated agent and skill data, and the generation manifest through their supported generators only when an approved source change requires them; never patch generated definitions directly.
- Add focused regression coverage for configuration validation, deterministic AGENTS.md rendering, governed-path classification, approval evidence, and the incorrect-test decision boundary.
- Preserve existing repository privacy, claims, work-item, generation, review, verification, commit, and deployment contracts.
- Use narrow implementation claims that exclude backlog scope. Use separate brief primary-only backlog claims for lifecycle transitions and final archival.
- Obtain fresh independent review of the changed project configuration, renderer, tests, and generated AGENTS.md result. Obtain fresh independent verification after accepted corrections are integrated.
- Refresh the installed user-scope bundle and MCP skill catalog under a separate shared-install claim only if the delivered change modifies distributable skill or agent artifacts. Record a truthful not-required result when the change remains project-local.

## Acceptance Criteria

- PROJECT.yaml contains the canonical directive that every agent-definition or skill-definition change requires explicit user approval.
- AGENTS.md deterministically contains the matching operational directive after the supported Project Configurator/rendering workflow runs, without a divergent hand-maintained policy or loss of unrelated repository guidance.
- A proposed edit under agents/roles/**/*.role.yaml is rejected or blocked without recorded explicit user approval and is permitted when matching approval evidence is supplied.
- A proposed edit under skills/*/SKILL.md or adapters/*/skills/*/SKILL.md is rejected or blocked without recorded explicit user approval and is permitted when matching approval evidence is supplied.
- Definition-affecting changes through adjacent skill metadata, the conceptual-agent schema or model profile, or adapter mappings cannot bypass the approval boundary.
- Direct edits to generated/adapters/** and generated agent or skill documentation mirrors remain prohibited; approved definition changes update those outputs only through regeneration.
- A failing test does not authorize a definition rewrite. Focused evidence proves that the workflow evaluates whether the test, fixture, assertion, or expected result is incorrect and can repair an incorrect test without changing a definition.
- The approval rule does not block ordinary authorized implementation changes or test corrections that do not alter a governed agent or skill definition.
- Approval evidence is scope-specific and auditable, and tests reject silence, unrelated approvals, generic repository-write authority, and approval for a different definition surface.
- Focused renderer, configuration, and policy tests pass, followed by the complete validation suite required by AGENTS.md and git diff --check.
- Fresh independent review reports no unresolved authority-boundary, source-of-truth, generated-output, or regression-coverage findings.
- Fresh independent verification confirms the canonical configuration, generated AGENTS.md directive, negative no-approval cases, positive matching-approval cases, incorrect-test case, ordinary-change case, and generated-mirror protections.
- Any required installed-bundle replacement and MCP skill refresh completes under a separate claim with installed-source evidence, or lifecycle evidence records why deployment was not required.
- The final backlog archive records exact implementation, review, verification, integration, deployment-or-not-required, claim-release, and commit evidence before Status: Completed is archived.

## Dependencies

None.

## Verification

- Add unit tests for parsing and validating the canonical PROJECT.yaml directive, including missing, malformed, and contradictory values.
- Add focused tests for scripts/render-agents-technology-skills.py proving the directive renders deterministically into AGENTS.md and preserves required maintained guidance.
- Add policy tests covering each canonical governed source family, definition-affecting metadata or schema inputs, and direct generated-mirror edits.
- Add negative tests proving no approval, unrelated approval, generic write authority, a failing test, and a test-repair assignment do not authorize a definition change.
- Add positive tests proving explicit approval for the exact agent or skill definition scope authorizes the requested source change and its supported regenerated mirrors.
- Add a regression scenario where the test expectation is incorrect; verify the test is repaired and the agent or skill definition remains unchanged.
- Add a control scenario where ordinary implementation or test source changes proceed under normal task authority because no governed definition is changed.
- Run the focused Project Configurator, AGENTS.md renderer, bundle-content, and agent-test policy suites.
- Run every skill and bundle validation command required by AGENTS.md, the project-wiki unit suite, and git diff --check.
- Have an independent reviewer inspect the diff and an independent verifier rerun the focused and repository-level checks from fresh evidence.
- If distributable artifacts change, run the user-scope replacement dry run, perform the approved install under a separate claim, refresh the MCP catalog, and verify installed manifests and source digests.

## Notes

- User authority for this feature is the explicit direction to add this project-level approval requirement. It does not pre-approve future changes to any particular agent or skill definition.
- When a future task needs a definition change, ask for approval that names or unambiguously bounds the affected definition before mutation.
- Test repair must preserve source truth. Passing tests are evidence only when their expectations are correct; definition rewrites are not an acceptable shortcut around suspect tests.
- Keep backlog creation, Ready-to-Running transition, and Completed archival as separate brief primary-only lifecycle claims. Never hold backlog scope together with artifact, generator, install, or integration resources.
