# Dev Methodology Repository Instructions

## Purpose

This file is the repo-local operating contract for maintaining this repository.

Do not move these directives into a distributed skill unless the rule is reusable outside this repository. The distributed skills under skills are the product this repository ships. This AGENTS.md file describes how to maintain that product.

Keep these instructions simple. If a maintenance rule needs a long explanation, prefer a root procedure file whose name starts with procedure- and link it from here.

## Source Boundaries

- README.md is the human-facing entry point for the bundle.
- AGENTS.md is the agent-facing maintenance contract for this repository.
- skills contains portable Agent Skills distributed to other projects and machines.
- agents contains the customer-independent conceptual agent definition schema and source definitions.
- detection.yaml beside a specialized technology or domain skill is the source for setup-time detection metadata and activation evidence.
- adapters contains runtime-specific metadata for those distributed skills.
- generated/adapters contains generated native agent definitions and must be regenerated from conceptual agent definition sources rather than edited manually.
- backlog contains this repository's primary-worktree-only typed work queue and user-review state; isolated agent worktrees omit it.
- .worktrees contains ignored linked agent checkouts rooted at the primary worktree. It is operational state rather than project source, and agents must never resolve it from another linked worktree.
- design contains the HTML explanations of the skill and agent model.
- scripts contains installer, refresh, validation, and regression-test support.

Do not create separate skill files for repo-local maintenance procedures. Keep repo-local procedures in AGENTS.md or in root procedure files.

## Before Editing

- Inspect the live repository state before changing files.
- Read README.md when changing bundle structure, install behavior, skill inventory, adapter behavior, or verification workflow.
- Read the relevant skill files before changing distributed skill content.
- Preserve unrelated local changes and untracked files.
- Keep changes scoped to the requested maintenance work.

## Technology Skills

Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.

Before acting on files under a matching folder, every agent must apply each inlined skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills.

Folder skillsets:

When configured folder patterns overlap, the most-specific matching pattern wins.

- scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: scripts/build-agent-skill-hierarchy.py and sibling .py files
- skills/project-wiki/scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python package evidence: skills/project-wiki/scripts/project_wiki_ops/__init__.py and sibling .py files
- skills/detect-technology-skills/scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: skills/detect-technology-skills/scripts/detect.py
- evals/projects/python-inventory/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: evals/projects/python-inventory/src/inventory.py; Owning manifest evidence: evals/projects/python-inventory/pyproject.toml requires Python 3.11 or newer
- evals/projects/fastapi-orders/**: apply the inlined fastapi, python skills instructions before acting.
  - fastapi evidence: Owning manifest dependency: evals/projects/fastapi-orders/pyproject.toml declares fastapi; Framework source evidence: evals/projects/fastapi-orders/app/main.py imports FastAPI and declares an application route
  - python evidence: Python source evidence: evals/projects/fastapi-orders/app/main.py

Inlined folder skill instructions:

### Folder pattern: scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: skills/project-wiki/scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: skills/detect-technology-skills/scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: evals/projects/python-inventory/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: evals/projects/fastapi-orders/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: fastapi -----
# FastAPI

Load Python with this skill.

## Application Boundaries

- Keep request and response models explicit and separate persistence or internal domain shapes when their contracts differ.
- Use dependency injection for request-scoped collaborators and cross-cutting policies.
- Translate domain failures to HTTP responses at the API boundary without losing useful causes in logs.
- Keep blocking work out of asynchronous request paths unless it is isolated behind an appropriate executor or synchronous endpoint.
- Put startup and shutdown ownership in lifespan handling.

## Routing And Validation

- Make status codes, response models, validation constraints, authentication requirements, and error bodies observable in the route contract.
- Avoid hidden side effects in dependencies and validators.
- Preserve framework-generated validation behavior unless the API contract intentionally replaces it.

## Verification

- Test routes through the ASGI application boundary with dependency overrides scoped to the test.
- Cover successful responses, invalid input, authorization failure, and translated domain failures.
- Verify asynchronous tests and lifespan behavior with the project's chosen test client and event-loop tooling.
----- END INLINED TECHNOLOGY SKILL: fastapi -----

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----
## Skill Catalog Maintenance

When adding, renaming, deleting, or materially changing a distributed skill:

- Update the source skill under skills.
- Keep the skill frontmatter name aligned with the skill directory name.
- Keep Codex openai.yaml metadata beside each source SKILL.md when a skill needs Codex app metadata, invocation policy, or tool dependencies.
- Run scripts/openai_metadata.py skills after skill name or description changes so derived Codex interface fields stay aligned while policy and dependencies remain hand-authored.
- Run scripts/build-technology-detection.py after detection metadata or specialized activation criteria change.
- Update README.md when the public skill inventory, setup flow, verification flow, or bundle purpose changes.
- Update the design HTML files that describe skills, conceptual agent definitions, agent maps, skills modularization, agentic configuration, or examples whenever the catalog, conceptual definition model, adapter model, or examples change.
- Update scripts/test_bundle_content.py so the bundle regression tests describe the current catalog.
- Sweep the repository for old skill ids before and after renames or deletions.
- Keep review skill checklists named review-checklist-[review-target].md, and keep completed checklist guidance aligned with artifact-name.review-checklist-[review-target].md.

When adding, renaming, deleting, or materially changing a conceptual agent definition:

- Update the conceptual source under agents/roles.
- Keep its filename field aligned with the conceptual definition source filename.
- Use only bundled skill IDs in the skills list.
- Run scripts/build-skill-docs.py so conceptual agent definition documentation data and native adapters are regenerated together.
- Update README.md and the relevant design HTML when conceptual definition policy, runtime support, installation, or customization behavior changes.
- Never edit design/generated or generated/adapters by hand.

## README And Design HTML

README.md must stay aligned with the distributable bundle:

- Repository shape.
- Install and refresh commands.
- Ownership and prune behavior.
- Bundled skill inventory.
- Applying the bundle to target projects.
- Verification commands.

The design HTML files must stay aligned with the current skills and agent model:

- design/agent-and-skill-definitions.html
- design/agentic-configuration.html
- design/skills-modularization.html
- design/generic-agent-definitions-source.html
- design/agent-skill-specialization-examples.html
- design/orchestrated-development-lifecycle.html
- design/documentation-templates.html

If a change affects the skill catalog, adapter shape, conceptual agent definition naming, dispatch profile examples, or agent specialization story, update the relevant HTML files in the same change.

## Markdown Rules

- Do not use inline Markdown code formatting in Markdown files.
- Use fenced code blocks only when command blocks or multi-line snippets are needed.
- Write steady-state documentation. Do not describe content as enhanced, revised, new, or old unless the document is explicitly a change plan.
- Keep examples generic and portable unless the document is intentionally repo-specific.

## Validation

Before finishing changes to this repository, run the relevant checks from the repository root.

For skill or bundle changes, run:

```bash
python3 scripts/validate-agent-skills.py skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
```

For wiki or OKF changes, also run:

```bash
python3 skills/project-wiki/scripts/wiki_ops.py status
python3 skills/project-wiki/scripts/wiki_ops.py lint
python3 skills/project-wiki/scripts/wiki_ops.py okf-validate
```

For any tracked-file change, run:

```bash
git diff --check
```

If a build script is introduced later, run the repository build after code, imports, generated artifacts, or project metadata changes.

## Commit Expectations

- Commit coherent verified repository-maintenance work before completion.
- Do not include unrelated untracked files in the commit.
- Include README.md, AGENTS.md, design HTML, tests, Codex metadata, and explicit deployment behavior in the same change when they are part of the same catalog or workflow update.
