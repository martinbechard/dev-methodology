<!--
Copyright (c) 2025 Martin Bechard [martin.bechard@DevConsult.ca]
This software is licensed under the MIT License.
File path: README.md
Credit: Human/AI methodology
1-line summary: Entry point for the reusable development documentation and project wiki skill bundle.
Witty remark: A map is better when it knows where the roads actually are.
-->

# Development Methodology Bundle

## Purpose

This repository distributes portable Agent Skills for software project documentation, project wiki maintenance, backlog flow, structured design and review, careful coding, multi-agent coordination, and structure-aware code search.

Use the installed skills as the operating surface. The repository README is only the entry point for installing and refreshing the bundle.

The core methodology keeps one shared wiki-compatible page contract and five document shapes:

1. Project wiki page
2. Functional specification
3. Architecture
4. High-level design
5. Module design

The shared page contract starts every durable page with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes. Specialized documents keep those sections first, then add their own sections.

## Repository Shape

- skills contains the portable Agent Skills.
- skills/development-methodology/assets/templates contains the reusable TODO-driven template assets.
- adapters contains runtime-specific metadata that is copied only by matching installer adapters.
- scripts/install-skills.py installs the bundled skills through adapter profiles for generic Agent Skills, Codex, Gemini CLI, Claude Code, and JetBrains Junie CLI.
- scripts/refresh-shared-skills.py refreshes the machine-wide shared skill installs from this source repository.
- scripts contains regression tests for installer behavior and bundle content.
- AGENTS.md contains repo-local maintenance directives for agents working on this source repository.

Reusable templates live inside the development-methodology skill assets so there is one distribution surface for agents. Target projects may copy individual template files when they need local editable documents, but the methodology itself is delivered through skills.

## One-Time Skill Setup

Run this from the repository root on a machine that should receive the development methodology skills. The default adapter installs to AGENTS_HOME/skills or ~/.agents/skills.

```bash
python3 scripts/install-skills.py
```

To install for a specific runtime, choose an adapter:

```bash
python3 scripts/install-skills.py --adapter codex
python3 scripts/install-skills.py --adapter gemini
python3 scripts/install-skills.py --adapter claude
python3 scripts/install-skills.py --adapter junie
```

The generic, codex, and gemini adapters default to AGENTS_HOME/skills or ~/.agents/skills. The claude adapter defaults to CLAUDE_HOME/skills or ~/.claude/skills. The junie adapter defaults to ~/.junie/skills, matching JetBrains Junie user-scope skill discovery. Use --dest to override the destination for any adapter, including project-scope .junie/skills or a folder passed to Junie CLI with --skill-location.

The installer skips existing skills by default. To replace installed copies with this repository's bundled versions, run:

```bash
python3 scripts/install-skills.py --replace
```

To inspect the plan without copying files, run:

```bash
python3 scripts/install-skills.py --dry-run
```

Refresh or restart the target agent runtime after installing skills if it does not detect new skill files automatically.

Junie support follows JetBrains documentation for [Agent skills](https://junie.jetbrains.com/docs/agent-skills.html) and [CLI parameters](https://junie.jetbrains.com/docs/parameters.html). JetBrains documents project-scope skills under .junie/skills, user-scope skills under ~/.junie/skills, and additional skill folders through the Junie CLI --skill-location option.

## Shared Skill Refresh

This repository is the source for shared project skills on this machine. After changing source skills, refresh the shared installs before using the bundle from other projects.

```bash
python3 scripts/refresh-shared-skills.py
```

The refresh covers the shared AGENTS_HOME or ~/.agents install, the direct ~/.codex install, and the Claude install. To inspect the refresh plan without replacing files, run:

```bash
python3 scripts/refresh-shared-skills.py --dry-run
```

Each shared destination keeps an ownership manifest named .dev-methodology-install.json. During shared refresh, prune mode removes obsolete skills that this repository previously installed and leaves unowned local skills alone. If a destination has no ownership manifest, the refresh writes one and skips pruning for that run. Run a refresh before planned renames or deletions so later cleanup has an ownership baseline.

Runtime agent metadata packaged inside an owned skill is refreshed and pruned with that skill. Future standalone agent definition folders should be added to the ownership manifest before any prune path is allowed to remove them.

Before renaming or deleting a source skill, sweep this repository for the old skill id. Update or remove references in skill files, companion-skill lists, adapter metadata, role definitions, dispatch profiles, aggregate workflow examples, design documents, README content, scripts, and tests before refreshing shared installs.

When a source skill is renamed or deleted, use the dry run to confirm that the old owned skill is reported as obsolete before running the real refresh.

## Bundled Skill Inventory

The wiki and development-wiki skills are:

- project-wiki
- project-wiki-query
- project-wiki-research
- project-wiki-topic-writer
- project-wiki-topic-verifier
- code-project-wiki

The documentation methodology skills are:

- development-methodology
- documentation-bootstrap
- documentation-reverse-engineering
- documentation-page-verifier

The artifact review skills are:

- review-project-wiki
- review-functional-spec
- review-architecture
- review-high-level-design
- review-module-design

The development practice skills are:

- careful-coding
- ast-grep
- create-backlog
- manage-backlog
- fix-explanation
- structured-explanation
- structured-design
- review-structured
- agent-claim
- agent-work-merge

The stack and project-domain skill packs are:

- typescript-esm
- typescript-strict
- electron-main
- electron-preload
- react-vite-renderer
- nextjs-app-router
- react-server-components
- node-cli
- api-routes
- clerk-auth
- postgres-drizzle
- langgraph
- tailwind-design-system
- jest
- vitest
- playwright
- harness-implementation
- tool-runtime-implementation
- plan-engine-implementation
- local-model-integration

## Applying This Bundle To A Project

1. Install or refresh the bundle on the target machine.
2. In the target repository, use documentation-bootstrap for first-time setup.
3. Use development-methodology when creating or revising functional specs, architecture, high-level designs, module designs, or wiki-compatible documentation.
4. Use documentation-reverse-engineering when an existing codebase needs a source-backed documentation set.
5. Use code-project-wiki when docs/wiki needs code-aware maintenance, commit-range review, Related Code upkeep, or Related Tests upkeep.
6. Use the artifact-specific review skill before finishing a project wiki page, functional specification, architecture document, high-level design, or module design.
7. Use documentation-page-verifier as the shared verifier for mixed, unknown, or custom documentation artifacts.
8. Use the project-wiki family for docs/wiki setup, topic writing, topic verification, wiki-backed answers, and raw research.

## Neutral Target Project Layout

- [documentation-root]/functional
- [documentation-root]/architecture
- [documentation-root]/high-level
- [documentation-root]/modules
- docs/wiki
- raw/wiki-fragments
- raw/processed

The placeholder [documentation-root] means the documentation root chosen by the target project. Projects may choose different folders when they already have established documentation locations, but each project should keep a clear home for each documentation type.

The project wiki should live at docs/wiki. It is a synthesized navigation and understanding layer, not the highest source of truth. Code and tests remain authoritative for actual behavior. Functional and technical documents can live under docs/wiki as wiki page subclasses or remain in their project documentation folders with wiki pages linking to them.

## Verification

Before publishing changes to this bundle, run:

```bash
python3 scripts/validate-agent-skills.py skills
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
python3 scripts/refresh-shared-skills.py
```
