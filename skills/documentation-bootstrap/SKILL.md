---
name: documentation-bootstrap
description: Use when applying the development methodology bundle to a target repository for the first time, choosing documentation roots, templates, AGENTS guidance, or wiki setup.
metadata:
  category: documentation-methodology
---

# Documentation Bootstrap

Use this skill for the first meaningful setup of the development methodology in a target repository. The output is a source-backed setup recommendation and a complete project-local documentation structure that agents and humans can maintain consistently.

## Full Project Documentation Default

When bootstrap includes reverse engineering for a repository, application, or project, treat the entire codebase as in scope. Do not ask the user to select a documentation breadth or offer a representative, sampled, minimal, or tiered documentation set. Use documentation-reverse-engineer to inventory every meaningful module, create and review the module documents, group the complete module set into high-level designs, derive architecture from the complete high-level-design set, document all observable workflows, and integrate the result into README and wiki hubs.

Only use a narrower boundary when the user explicitly names it. Record what remains outside that boundary and do not report the project as fully documented or fully reverse engineered.

## Inputs

- Target repository root.
- Existing AGENTS instructions, README files, procedures, design folders, docs folders, wiki folders, backlog folders, and build or test commands.
- Installed development-methodology and project-wiki family skills.
- User preferences for documentation roots, wiki ownership, automation, or local template copies.

## Setup Recommendation

Before editing, inspect the repository and present a concise setup recommendation when the project shape is not obvious. Include:

- Documentation root candidates.
- Wiki root recommendation, normally docs/wiki unless an established convention exists.
- Functional, architecture, high-level design, and module design locations.
- Whether the project needs local editable template copies or can use installed skill assets directly.
- Project wiki setup needs, including raw/wiki-fragments and raw/processed.
- AGENTS.md guidance needed for future agents.
- Verification commands and gaps.

Proceed directly when the user already specified these choices or the repository convention is clear.

## Bootstrap Workflow

1. Inspect the target repository before creating files. Apply the project instructions already in context, then read README files, task-relevant procedures, package metadata, build scripts, existing docs, existing wiki pages, backlog folders, and current git status when present.
2. Choose documentation roots that fit existing conventions. Prefer a single documentation root with functional, architecture, high-level, and modules subfolders when the project has no convention. This keeps the structure compact; it does not reduce artifact coverage.
3. Confirm docs/wiki as the wiki root unless the project has a stronger established location.
4. Use development-methodology to select template assets for initial documents.
5. Copy only template files that will become active project documents or project-owned templates.
6. Use project-wiki setup guidance for docs/wiki initialization, schema, topic index, glossary, open decisions, known defects, and maintenance log.
7. Add or update AGENTS.md guidance so future agents check docs/wiki first, save unsynthesized wiki knowledge under raw/wiki-fragments, use project-wiki skills for wiki work, and commit wiki changes with the source or documentation changes that made them necessary.
8. Keep runtime-specific commands in project guidance only when the project actually depends on that runtime.
9. When reverse engineering is in scope, require the documentation coverage manifest and every pass completion gate from documentation-reverse-engineer before bootstrap can advance or report completion.
10. Record unresolved ownership, source authority, verification, or automation questions in Open Questions instead of guessing.

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
