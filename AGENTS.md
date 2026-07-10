# Dev Methodology Repository Instructions

## Purpose

This file is the repo-local operating contract for maintaining this repository.

Do not move these directives into a distributed skill unless the rule is reusable outside this repository. The distributed skills under skills are the product this repository ships. This AGENTS.md file describes how to maintain that product.

Keep these instructions simple. If a maintenance rule needs a long explanation, prefer a root procedure file whose name starts with procedure- and link it from here.

## Source Boundaries

- README.md is the human-facing entry point for the bundle.
- AGENTS.md is the agent-facing maintenance contract for this repository.
- skills contains portable Agent Skills distributed to other projects and machines.
- agents contains the canonical customer-independent role schema and role definitions.
- adapters contains runtime-specific metadata for those distributed skills.
- generated/adapters contains generated native agent definitions and must be regenerated from canonical roles rather than edited manually.
- design contains the HTML explanations of the skill and agent model.
- scripts contains installer, refresh, validation, and regression-test support.

Do not create separate skill files for repo-local maintenance procedures. Keep repo-local procedures in AGENTS.md or in root procedure files.

## Before Editing

- Inspect the live repository state before changing files.
- Read README.md when changing bundle structure, install behavior, skill inventory, adapter behavior, or verification workflow.
- Read the relevant skill files before changing distributed skill content.
- Preserve unrelated local changes and untracked files.
- Keep changes scoped to the requested maintenance work.

## Skill Catalog Maintenance

When adding, renaming, deleting, or materially changing a distributed skill:

- Update the source skill under skills.
- Keep the skill frontmatter name aligned with the skill directory name.
- Keep Codex openai.yaml metadata beside each source SKILL.md when a skill needs Codex app metadata, invocation policy, or tool dependencies.
- Run scripts/openai_metadata.py skills after skill name or description changes so derived Codex interface fields stay aligned while policy and dependencies remain hand-authored.
- Update README.md when the public skill inventory, setup flow, verification flow, or bundle purpose changes.
- Update the design HTML files that describe skills, agents, role maps, specialization strategy, operating model, or examples whenever the catalog, role model, adapter model, or examples change.
- Update scripts/test_bundle_content.py so the bundle regression tests describe the current catalog.
- Sweep the repository for old skill ids before and after renames or deletions.
- Refresh shared installs after source skill changes.
- Keep review skill checklists named review-checklist-[review-target].md, and keep completed checklist guidance aligned with artifact-name.review-checklist-[review-target].md.

When adding, renaming, deleting, or materially changing a canonical role:

- Update the source role under agents/roles.
- Keep its filename field aligned with the role source filename.
- Use only bundled skill IDs in the skills list.
- Run scripts/build-skill-docs.py so role documentation data and native adapters are regenerated together.
- Update README.md and the relevant design HTML when role policy, runtime support, installation, or customization behavior changes.
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

- design/agent-role-skill-map.html
- design/agent-skill-specialization-examples.html
- design/agent-skill-specialization-strategy.html
- design/agentic-development-operating-model.html

If a change affects the skill catalog, adapter shape, role naming, dispatch profile examples, or agent specialization story, update the relevant HTML files in the same change.

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
python3 scripts/build-skill-docs.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
python3 scripts/refresh-shared-skills.py
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

- Commit verified repository-maintenance work when the change is coherent and the worktree allows a clean scoped commit.
- Do not include unrelated untracked files in the commit.
- Include README.md, AGENTS.md, design HTML, tests, Codex metadata, and shared-install refresh effects in the same change when they are part of the same catalog or workflow update.
