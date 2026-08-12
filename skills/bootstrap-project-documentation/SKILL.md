---
name: bootstrap-project-documentation
description: Use when applying the development methodology bundle to a target repository for the first time, choosing documentation roots, templates, AGENTS guidance, or wiki setup.
metadata:
  category: documentation-methodology
---

# Bootstrap Project Documentation

Use this skill for the first meaningful setup of the development methodology in a target repository. The output is a source-backed setup recommendation and a complete project-local documentation structure that agents and humans can maintain consistently.

## Configuration Setup Boundary

When Project Configurator invokes this skill during setup, create only the selected empty documentation roots and repository-required placeholders. Basic setup asks only whether to create the Wiki: Yes selects wiki and No selects none, which creates no documentation root. Advanced setup choices are wiki, specifications, and both. Do not inspect source to create module designs, high-level designs, architecture, functional specifications, or wiki synthesis, and do not invoke reverse-engineer-project-documentation. Reverse engineering remains a later explicit workflow that consumes the accepted PROJECT.yaml.

## Full Project Documentation Default

When bootstrap includes reverse engineering for a repository, application, or project, treat the entire codebase as in scope. Do not ask the user to select a documentation breadth or offer a representative, sampled, minimal, or tiered documentation set. Use reverse-engineer-project-documentation to inventory every meaningful module, create and review the module documents, group the complete module set into high-level designs, derive architecture from the complete high-level-design set, document all observable workflows, and integrate the result into README and wiki hubs.

The project configuration pass from reverse-engineer-project-documentation precedes documentation work. It creates or reconciles `PROJECT.yaml`, inventories the target runtime's available technology skills, and owns matching root and nested `AGENTS.md` routing. A scope with no pertinent specialized skill uses the recorded general-model-training fallback and remains in coverage.

Only use a narrower boundary when the user explicitly names it. Record what remains outside that boundary and do not report the project as fully documented or fully reverse engineered.

## Inputs

- Target repository root.
- Existing AGENTS instructions, README files, procedures, design folders, docs folders, wiki folders, backlog folders, and build or test commands.
- Installed route-documentation-work and project-wiki family skills.
- User preferences for documentation roots, wiki ownership, automation, or local template copies.

## Setup Recommendation

Before editing, inspect the repository and present a concise setup recommendation when the project shape is not obvious. Include:

- Documentation root candidates.
- Wiki root recommendation, normally docs/wiki unless an established convention exists.
- Functional, architecture, high-level design, and module design locations.
- Whether the project needs local editable template copies or can use installed skill assets directly.
- Project wiki setup needs, including raw/wiki-fragments and raw/processed.
- Documentation mode selection. Use hybrid-specifications-and-wiki for a full structured-specification and wiki bootstrap unless the project already records another supported mode.
- AGENTS.md guidance needed for future agents.
- Verification commands and gaps.

Proceed directly when the user already specified these choices or the repository convention is clear.

## Bootstrap Workflow

1. Inspect the target repository before creating files. Apply the project instructions already in context, then read README files, task-relevant procedures, package metadata, build scripts, existing docs, existing wiki pages, backlog folders, and current git status when present.
2. Choose documentation roots that fit existing conventions. For specifications or both, create or recognize separate categories in docs/project-taxonomy.md or the project-named placement taxonomy for durable Markdown architecture, HLD, and component design before any design artifact is written. When the project has no stronger convention, use docs/architecture/ARC-NNN-slug.md, docs/design/high-level/HLD-NNN-slug.md, and docs/design/components/CD-NNN-slug.md. Never place architecture in the HLD category to compensate for a missing architecture category.
3. Record the authority direction as architecture to HLD to component design, require each child to reference its parent, and prohibit circular authority references. If docs/architecture also contains a fixed structured workflow output such as architecture-design.yaml, record that generated or phase-specific artifact as a separate taxonomy entry with its own owner and lifecycle.
4. Confirm docs/wiki as the wiki root unless the project has a stronger established location.
5. During ordinary setup, persist only the selected project_setup.documentation value and do not require documentation_mode.
6. When a later explicit documentation workflow will keep structured module, high-level, architecture, and functional specifications authoritative while using README and docs/wiki for navigation and synthesis, select hybrid-specifications-and-wiki and persist it under documentation_mode so downstream agents do not reconstruct the selection from conversational context. For a legacy PROJECT.yaml without that later-workflow field, infer the value only when both structured specification roots and docs/wiki already exist or the workflow is establishing that full hierarchy. Otherwise obtain the project-owned selection before documentation work. Treat an unsupported documentation mode or a missing value without safe migration evidence as BLOCKED only at this later documentation boundary.
7. During configuration setup, create only the selected empty roots, required taxonomy categories, and required placeholders. During a later explicit documentation workflow, use route-documentation-work to select template assets for active documents.
8. Copy template files only during that later document-creation workflow or when the user explicitly requests project-owned templates.
9. Use project-wiki setup guidance for docs/wiki initialization, schema, topic index, glossary, open decisions, known defects, and maintenance log.
10. Add or update AGENTS.md guidance so future agents check docs/wiki first, save unsynthesized wiki knowledge under raw/wiki-fragments, use project-wiki skills for wiki work, and commit wiki changes with the source or documentation changes that made them necessary.
11. Keep runtime-specific commands in project guidance only when the project actually depends on that runtime.
12. When reverse engineering is in scope, require the project configuration gate, documentation coverage manifest, and every pass completion gate plus final top-down semantic reconciliation from reverse-engineer-project-documentation before bootstrap can advance or report completion.
13. Record unresolved ownership, source authority, verification, or automation questions in Open Questions instead of guessing.

## Local Template Policy

Installed skills are the reusable methodology source. Target repositories should not receive a full copy of this bundle by default.

Copy individual templates only when:

- A new document is being created from that template.
- The project explicitly wants local editable starter templates.
- The target runtime cannot access installed skill assets and the user accepts a project-local copy.

When local templates are copied, place them under the target project's chosen documentation root and treat them as project-owned assets.

## Verification

Before finishing:

1. Run project wiki status and lint when docs/wiki exists.
2. Run OKF validation when wiki pages changed.
3. Run agent-skill validation when skill files changed.
4. Run repository build or documentation checks only if setup changed code, imports, generated artifacts, project metadata, or documented commands.
5. Search for unresolved TODO markers outside intentionally copied templates.
6. Report the documentation root, wiki root, local templates copied, AGENTS.md guidance changed, verification commands run, and unresolved questions.
7. When a later explicit documentation workflow is configured, confirm PROJECT.yaml contains its validated documentation mode, including the legacy missing-field migration result when applicable, and report that persisted value. For ordinary setup, confirm only the selected project_setup.documentation value.
8. For specifications or both, confirm the taxonomy contains distinct architecture, HLD, and component-design categories, their filename prefixes, their parent-child authority direction, and any separately owned fixed structured architecture outputs.
