---
name: dev-methodology-repository-maintenance
description: Maintain this repository's portable skill bundle, conceptual agent definitions, generated artifacts, design documentation, tests, and release workflow without losing repository-specific rules.
metadata:
  category: project-maintenance
---

# Dev Methodology Repository Maintenance

Use this project skill when changing the dev-methodology repository.

## Repository Purpose

This repository maintains portable Agent Skills and conceptual agent definitions. The files under skills and agents are distributable product sources. Keep repository-only maintenance rules in this project skill.

Keep this skill concise. Put a long repository procedure in a root file whose name starts with procedure- and reference that file here.

## Multi-Item Coordination

When the user asks one parent task to coordinate several user-visible backlog tasks, use codex-workitem-coordination through Dev Backlog Coordinator.

Keep backlog mutations with Dev Backlog Steward. Keep each work item's artifact delivery with Dev Orchestrator. Use design/orchestrated-development-lifecycle.html for the communication sequence.

## Source Boundaries

- README.md is the human-facing bundle entry point.
- PROJECT.yaml is the source for generated project guidance.
- AGENTS.md is generated operational guidance.
- .agents/skills contains skills used only to maintain this repository.
- skills contains portable skills distributed to other projects and machines.
- agents contains customer-independent conceptual agent schemas and source definitions.
- detection.yaml beside a technology or domain skill owns setup-time detection metadata.
- adapters contains runtime-specific source metadata.
- generated/adapters contains generated native agent definitions. Regenerate these files from their conceptual sources.
- backlog contains the primary-worktree-only typed work queue and User Action Required state. Private worktrees omit it.
- .worktrees contains ignored operational checkouts under the primary worktree. Resolve this directory from the primary worktree, never from another linked checkout.
- design contains explanations of the skill and agent model.
- scripts contains installation, refresh, generation, validation, and regression support.

Do not put repository-specific procedures in distributed skills.

## Before Editing

- Inspect Git and the live claim registry before changing files.
- Read README.md when changing bundle structure, installation, skill inventory, adapter behavior, or verification workflow.
- Read each distributed skill before changing it.
- Preserve unrelated local changes and untracked files.
- Keep the change within the user's requested scope.

## Distributed Skill Maintenance

When adding, renaming, deleting, or materially changing a distributed skill:

- Update its source under skills.
- Keep its frontmatter name aligned with its directory name.
- Keep agents/openai.yaml beside the skill when Codex metadata, invocation policy, or tool dependencies are required.
- Run scripts/openai_metadata.py skills after changing a skill name or description.
- Run scripts/build-technology-detection.py after changing detection metadata or activation criteria.
- Update README.md when the public inventory, setup, verification, or bundle purpose changes.
- Update affected design HTML.
- Update the focused catalog assertions in scripts/test_bundle_content.py.
- Search for the old skill identifier before and after a rename or deletion.
- Name review checklists review-checklist-[review-target].md.
- Name completed artifact checklists artifact-name.review-checklist-[review-target].md.

## Conceptual Agent Maintenance

When adding, renaming, deleting, or materially changing a conceptual agent definition:

- Update its source under agents/roles.
- Keep its filename field aligned with its source filename.
- Use only bundled skill identifiers in its skills list.
- Run scripts/build-skill-docs.py to regenerate documentation data and native adapters.
- Update README.md and affected design HTML when policy, runtime support, installation, or customization behavior changes.
- Do not edit design/generated or generated/adapters by hand.

## README And Design

Keep README.md aligned with:

- repository structure;
- install and refresh commands;
- ownership and pruning behavior;
- bundled skill inventory;
- target-project setup;
- verification commands.

Keep these design pages aligned with the current skill and agent model:

- design/agent-and-skill-definitions.html;
- design/agentic-configuration.html;
- design/skills-modularization.html;
- design/generic-agent-definitions-source.html;
- design/agent-skill-specialization-examples.html;
- design/orchestrated-development-lifecycle.html;
- design/documentation-templates.html.

Update the relevant page when a change affects the skill catalog, adapter shape, conceptual agent naming, dispatch examples, or specialization model.

## Markdown

- Do not use inline code formatting in Markdown files.
- Use fenced code blocks for commands and multiline snippets.
- Write steady-state documentation.
- Use generic, portable examples unless a document is intentionally repository-specific.

## Verification

Choose tests from changed behavior and actual dependency paths. Run the smallest relevant test first. A tier identifies the affected surface; it does not trigger a full repository regression.

| Tier | Change event | Required tests | Explicit exclusions |
| --- | --- | --- | --- |
| 1 | Documentation-only change with no executable contract change | Documentation validation for changed files; applicable link or markup checks; git diff --check | No unit suites, agent catalog, browser tests, or unrelated documentation checks |
| 2 | Skill, role, configuration, template, or metadata contract change | Targeted contract tests for changed statements; validation for each changed source; affected generated-output freshness; git diff --check | No full repository suite, project-wiki suite, browser tests, or live-model tests |
| 3 | Generated output changes from an approved source change | Source-targeted tests; supported regeneration; generator freshness; exact source-to-output consistency; git diff --check | No unrelated generators or broad regression suites |
| 4 | Test fixture, expected result, assertion, or test data change | Tests that consume the changed test input; one focused negative case when needed; git diff --check | No unrelated module tests; no production or canonical contract changes merely to satisfy a test |
| 5 | Helper, parser, simulator, runner, installer, or generator implementation change | Targeted unit tests for changed functions and failure boundaries; a targeted integration test only across a real component boundary; git diff --check | No full repository suite solely because the file is shared |
| 6 | Product or methodology implementation change | Unit tests for changed behavior; directly affected component tests; a focused regression for the reported defect; git diff --check | No tests for components that do not consume or depend on changed behavior |
| 7 | Primary-main integration of an accepted candidate | Smallest tests proving integrated bytes and affected behavior; candidate-to-main content mapping; git diff --check | No repetition of unchanged pre-integration tests without integration-sensitive behavior |
| 8 | User-level installation or publication | Targeted installer or publication tests; installed byte or digest comparison; refresh and inspect affected catalog entries | No full repository suite or complete catalog evaluation |
| 9 | Focused testing reveals a distinct cross-component failure | Record the concrete failure and dependency path, then add only the implicated component's targeted tests | No escalation based on file size, location, shared classification, or hypothetical risk |
| 10 | The user requests broader verification | Run exactly the requested scope after stating its expected cost | No additional suites beyond the requested scope |

When a targeted test fails, determine whether the implementation or test is wrong. Correct an incorrect fixture, assertion, expected result, test datum, or test-support file within the current change, then rerun only its consumers. Do not change correct production behavior or a canonical contract to satisfy an incorrect test.

Run broader tests only when the user requests them or a focused failure identifies a concrete dependency.

Correct a trivial unrelated failure immediately without creating a work item when current source makes both the cause and correction unambiguous, the edit is limited to a stale assertion, fixture, test-support value, or documentation statement, no production behavior or governed definition changes, no user-owned bytes overlap, and one focused check can verify the correction in the same bounded turn. Report the incidental correction separately from the primary result.

Record the failure as a distinct defect when any of those conditions is absent, the correction needs investigation or design judgment, the change affects production behavior or a governed definition, the failure recurs after the obvious correction, or focused verification identifies a wider dependency. Do not keep the current item open solely because of a recorded distinct defect.

If this repository later adds a build script, run the build after changing code, imports, generated artifacts, or project metadata.

## Commits

- Commit coherent, verified maintenance work before completion.
- Unrelated changes do not block a scoped commit. Commit only the intended files and leave unrelated changes untouched.
- Exclude unrelated untracked files.
- Keep related README, generated AGENTS.md, design HTML, tests, Codex metadata, and deployment behavior in the same change.
