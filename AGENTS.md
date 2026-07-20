# Dev Methodology Repository Instructions

## Purpose

This file is the repo-local operating contract for maintaining this repository.

Do not move these directives into a distributed skill unless the rule is reusable outside this repository. The distributed skills under skills are the product this repository ships. This AGENTS.md file describes how to maintain that product.

Keep these instructions simple. If a maintenance rule needs a long explanation, prefer a root procedure file whose name starts with procedure- and link it from here.

## Codex Multi-Item Coordination

When the user explicitly asks one parent task to coordinate multiple user-visible Codex backlog tasks, use the [codex-workitem-coordination skill](skills/codex-workitem-coordination/SKILL.md) through Dev Backlog Coordinator. Keep backlog mutations with Dev Backlog Steward and per-item artifact delivery with Dev Orchestrator. The [orchestrated development lifecycle](design/orchestrated-development-lifecycle.html) owns the communication sequences; do not copy that procedure into repository-local guidance.

## Source Boundaries

- README.md is the human-facing entry point for the bundle.
- AGENTS.md is the agent-facing maintenance contract for this repository.
- skills contains portable Agent Skills distributed to other projects and machines.
- agents contains the customer-independent conceptual agent definition schema and source definitions.
- detection.yaml beside a specialized technology or domain skill is the source for setup-time detection metadata and activation evidence.
- adapters contains runtime-specific metadata for those distributed skills.
- generated/adapters contains generated native agent definitions and must be regenerated from conceptual agent definition sources rather than edited manually.
- backlog contains this repository's primary-worktree-only typed work queue and user-action-required state; isolated agent worktrees omit it.
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

## Work-Item Workflow Skill References

Project Configurator owns these independent selectors. Workflow skills are referenced by name only and are never inlined; their procedures stay in the selected skill definitions. Technology skill inlining is a separate mechanism below.

- Default provider file: create with create-file-work-item; manage with manage-file-work-items.
- Default completion direct-main: use complete-work-item-direct-main.

Most-specific matching folder pattern wins independently for provider and completion overrides. A folder override changes only its own selector.

When a selector is UNSET, the pertinent agent asks at the stated operation boundary and does not infer either value from repository or hosting evidence, files, remotes, templates, plugins, or available tools.

## Agent And Skill Definition Approval

Every change to an agent definition or skill definition requires explicit, scope-specific user approval before mutation. Record the user's direction, the exact definition scope it authorizes, and the approval evidence in the work lifecycle. Silence, unrelated prior approval, and broad repository mutation authority are insufficient.

Repository access, a failing test, a repair assignment, general write authority, review work, verification work, and a desire to make validation pass do not authorize a definition change.

The harness-loaded directive is the project authority boundary. Before mutating a governed canonical source, run the supported pre-mutation check with an approval record that cites existing explicit user direction:

```bash
python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change path/to/definition --approval-record path/to/approval-record.yaml
```

The check validates the configured path boundary, exact scope, basis, and provenance record. It does not enforce filesystem permissions, create approval, or let an agent manufacture user-direction provenance.

Governed canonical definition surfaces:

- Conceptual agent definitions: agents/roles/**/*.role.yaml.
- Agent definition schemas and model inputs: agents/role-schema.yaml, agents/model-profiles.yaml, adapters/*/model-profiles.yaml.
- Distributed skill definitions: skills/*/SKILL.md.
- Adapter-owned skill definitions: adapters/*/skills/*/SKILL.md.
- Skill definition metadata: skills/*/agents/openai.yaml, adapters/*/skills/*/agents/openai.yaml.

Generated definition mirrors are source-owned and must never be edited directly:

- generated/adapters/**, design/generated/role-definitions.js, design/generated/skill-definitions.js.

Supported source-category to generated-mirror relationships:

- Conceptual agent definitions: generated/adapters/**, design/generated/role-definitions.js.
- Agent definition schemas and model inputs: generated/adapters/**, design/generated/role-definitions.js.
- Distributed skill definitions: generated/adapters/**, design/generated/skill-definitions.js.
- Adapter-owned skill definitions: generated/adapters/**, design/generated/skill-definitions.js.
- Skill definition metadata: generated/adapters/**, design/generated/skill-definitions.js.
- Regenerate a mirror only when it is listed for the approved canonical source category. Cross-family role-to-skill and skill-to-role documentation regeneration is blocked. A supported regeneration does not require a second approval.

When a test fails, investigate whether the test, fixture, assertion, or expected result is incorrect before proposing a definition change. Ordinary authorized implementation changes and corrections to incorrect tests remain allowed when they do not alter a governed definition.

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

Before finishing changes to this repository, select the lowest verification tier supported by the affected surfaces and risks. The verification plan must identify those surfaces and map every check to a concrete risk. Record why the task selected a higher tier whenever it escalates beyond the lowest applicable tier.

Escalate only when affected-surface evidence, a failed focused check, a shared generator or runner change, or a final-campaign requirement justifies it.

### Tier 1: Small Bounded Skill Or Catalog Changes

For bounded skill wording, metadata, detection, or catalog additions:

- Run the exact governed-definition approval check before mutation when the changed source is governed.
- Validate the changed source and metadata.
- Run focused behavior, detection, and bundle tests that exercise the changed surface.
- Run applicable generator freshness checks without regenerating unrelated output.
- Run git diff --check.
- Obtain an independent review of the exact change.

Do not require the full scripts regression, project-wiki regression, or live agent catalog solely because a skill was added or changed.

### Tier 2: Generated Definition Changes

For generated-definition changes:

- Run focused tests for the approved canonical source.
- Regenerate only the supported mirrors from approved sources.
- Run the relevant generator freshness checks.
- Run git diff --check.
- Obtain an independent review of the exact source and generated diff.

### Tier 3: Shared Infrastructure Changes

For shared runner, claim engine, cleanup, installer, generator framework, or other broad infrastructure changes, run the full applicable deterministic regression and appropriate live verification. Keep the checks tied to the affected execution paths and declared risks.

### Tier 4: Campaign Or Release Gates

Run the full scripts, project-wiki, and agent catalog regression as a campaign final-state gate, a release gate, or an evidence-backed broad-impact gate. It is not the default per-item gate. The final campaign full-agent-catalog gate remains required.

The full deterministic repository regression is:

```bash
python3 scripts/validate-agent-skills.py skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
```

For wiki or OKF changes at a tier that requires the affected wiki surface, also run:

```bash
python3 skills/project-wiki/scripts/wiki_ops.py status
python3 skills/project-wiki/scripts/wiki_ops.py lint
python3 skills/project-wiki/scripts/wiki_ops.py okf-validate
```

For any tracked-file change, run:

```bash
git diff --check
```

Do not rerun an unchanged expensive full suite after integration when the integrated bytes are identical to an independently reviewed contribution and fresh pre-integration full evidence exists. Run focused post-integration checks plus integrity and provenance checks instead.

Reproduce an unrelated baseline failure on the baseline and route it as a warning or follow-up. Do not use an unrelated confirmed baseline failure to keep an otherwise bounded item open.

If a build script is introduced later, run the repository build after code, imports, generated artifacts, or project metadata changes.

## Commit Expectations

- Commit coherent verified repository-maintenance work before completion.
- Do not include unrelated untracked files in the commit.
- Include README.md, AGENTS.md, design HTML, tests, Codex metadata, and explicit deployment behavior in the same change when they are part of the same catalog or workflow update.
