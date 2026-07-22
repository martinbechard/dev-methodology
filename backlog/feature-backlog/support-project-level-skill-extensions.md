# Support Project-Level Skill Extensions

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/support-project-level-skill-extensions.md

Completion: direct-main

## Discovery Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f85c8-62c2-71d0-bab4-861e863d03ed
- Worktree: /Users/martinbechard/.codex/worktrees/9052/dev-methodology
- Branch: codex/support-project-level-skill-extensions
- Starting main: 2624b5b25ba6e5548051d7b9953933b1e57b3f87
- Phase: Bounded schema, renderer, and exact governed-scope discovery completed; the recorded exact approval permits Ready-state dispatch within the stated scope.
- Started: 2026-07-21
- Running-record claim: start-project-skill-extensions-019f85c8, acquired event 294844ff-d66c-4452-bb44-9d6d1be019de.
- Open issues: No user-action issue remains. Implementation must stay within the approved exact scope.
- Accepted candidate: Pending.

## Delivery Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: /root/process_backlog/orch_project_skill_extensions
- Artifact claim: project-skill-extensions-20260722
- Branch: codex/project-skill-extensions-20260722
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/project-skill-extensions-20260722
- Starting main: 13ea3ffe92fe7a8352f33b4f618f39f212322ba3
- Phase: Lifecycle Running committed; ARTIFACT GO pending.
- Candidate: Pending.
- Accepted commit: Pending.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Delivery evidence: Pending.
- Claim pressure: README.md is currently owned by deploy-explicit-project-20260722. Start on proven non-overlapping scopes; serialize any later README.md or scripts/test_bundle_content.py extension rather than waiting idle or polling.

## User Action Required

### Question For The User

Do you approve changing exactly skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md, together with their supported generated skill mirrors and the directly related non-governed project template, renderer, focused validation and bundle tests, README, and skills-modularization design documentation, to implement backlog/feature-backlog/support-project-level-skill-extensions.md?

### Why User Input Is Required

The evidence-backed design requires changes to two governed skill definitions. Repository policy requires exact path-specific approval before mutation.

### Options And Tradeoffs

- Approve the exact two-skill scope: implement the ordered project-level extension mechanism and its directly related surfaces.
- Narrow the scope by naming allowed paths: preserve excluded behavior as blocked follow-up work.
- Defer: retain the discovery result without implementation.

### Resolution

Approved on 2026-07-22. The user answered "ok authorized" immediately after the exact Question For The User recorded above in the parent conversation. Provenance: parent coordination conversation for this backlog transition. The approval covers exactly skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md, their supported generated skill mirrors, and the directly related non-governed surfaces named in that question.

### Unattended Work Boundary

Ready-state work may proceed only within the exact approved scope. Any governed path or related surface outside the recorded question requires separate scope-specific approval. Preserve the resolved ordered-list schema and root-only reference rendering contract.

### Discovery Evidence

- Canonical task: 019f85c8-62c2-71d0-bab4-861e863d03ed.
- Clean branch/worktree: codex/support-project-level-skill-extensions at /Users/martinbechard/.codex/worktrees/9052/dev-methodology, based on 2624b5b25ba6e5548051d7b9953933b1e57b3f87.
- Schema decision: one ordered project_skill_extensions list accepts bundled identifiers and explicit registered-skill mapping entries; normalized skill id controls duplicate, availability, unknown, and definition-owned conflict checks.
- Rendering decision: one final Project Skill Extensions reference-only section is rendered in root AGENTS.md only; nested AGENTS.md files, technology loadouts, and workflow selectors remain independent.
- Exact governed manifest: skills/create-project-configuration/SKILL.md and skills/development-methodology/SKILL.md.
- Directly related non-governed surfaces: skills/development-methodology/assets/templates/project-template.yaml, scripts/render-agents-technology-skills.py, scripts/test_technology_detection.py, scripts/test_bundle_content.py, README.md, and design/skills-modularization.html.
- UAR routing claim: route-project-skill-extensions-approval, acquired event bf5b9715-7427-4e1d-b290-1e865248ecfb.

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
