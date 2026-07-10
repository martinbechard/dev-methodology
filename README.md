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

Project agent and skill setup starts with AGENTS-PLAN.yaml as the reviewable planning artifact. The create-agents-plan skill creates root and nested plans that explain which role agents and skills apply to a project, then that validated plan drives durable routing guidance in AGENTS.md. Claude Code projects also receive a thin CLAUDE.md beside each applicable AGENTS.md so Claude imports the same project guidance without duplicating it.

The core methodology keeps one shared wiki-compatible page contract and six document shapes. Each document shape has a focused creation skill, a reusable template asset, and an artifact review skill:

1. Project wiki page: create-project-wiki, project-wiki-template.md, review-project-wiki
2. Functional specification: create-functional-spec, functional-spec-template.md, review-functional-spec
3. Architecture: create-architecture, architecture-template.md, review-architecture
4. High-level design: create-high-level-design, high-level-design-template.md, review-high-level-design
5. Module design: create-module-design, module-design-template.md, review-module-design
6. Unit test plan: create-unit-test-plan, unit-test-plan-template.md, review-unit-test-plan

The shared page contract starts every durable page with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes. Specialized documents keep those sections first, then add their own sections.

## Repository Shape

- skills contains the portable Agent Skills.
- Specialized technology and domain skills own setup-time activation metadata in detection.yaml beside SKILL.md.
- skills/detect-technology-skills contains the setup workflow, generated detector mirror, and generated portable technology registry.
- skills/development-methodology/assets/templates contains the reusable TODO-driven template assets.
- Keep Codex openai.yaml metadata beside each source SKILL.md when a skill needs Codex app metadata, invocation policy, or tool dependencies.
- scripts/install-skills.py installs the bundled skills through adapter profiles for generic Agent Skills, Codex, Gemini CLI, Claude Code, and JetBrains Junie CLI.
- agents/role-schema.yaml defines the canonical customer-independent role schema.
- agents/model-profiles.yaml defines semantic simple, default, advanced, and advanced-long model profiles without provider identifiers.
- adapters/[runtime]/model-profiles.yaml maps semantic profiles to concrete models, reasoning effort, and context settings for each harness.
- agents/roles contains canonical role files grouped by methodology maintenance, project setup, wiki activities, and normal development use.
- generated/adapters contains ready-to-copy native agent definitions. The current milestone generates Codex and Claude definitions from the same canonical roles.
- design/generated/technology-skill-detection-registry.js exposes the same detection registry for documentation and the future interactive agent-skill explorer.
- scripts/openai_metadata.py refreshes derived Codex interface fields from SKILL.md while preserving hand-authored policy and dependencies.
- scripts/refresh-shared-skills.py refreshes the machine-wide shared skill installs from this source repository.
- scripts contains regression tests for installer behavior and bundle content.
- AGENTS.md contains repo-local maintenance directives for agents working on this source repository.

Reusable templates live inside the development-methodology skill assets so there is one distribution surface for agents. Target projects may copy individual template files when they need local editable documents, but the methodology itself is delivered through skills.

## Generated Methodology Documentation

```bash
python3 scripts/build-skill-docs.py
```

The script reads each bundled SKILL.md file, the adjacent Codex openai.yaml metadata, the ordered design/skill-categories.yaml catalog, agents/role-schema.yaml, agents/model-profiles.yaml, adapter model mappings, and the canonical role files. It writes design/generated/skill-definitions.js, design/generated/role-definitions.js, and native agent definitions for the supported runtime adapters.

Canonical roles use three skill-loading paths. A skill entry without a condition is a fixed role skill and always loads. A skill entry with a condition is request-specific; generated agent instructions use the form Use the skill-name skill when condition, while telling the agent to inspect the requested outcome and available evidence when wording is ambiguous. Technology and domain skills remain outside role assignment: Project Agent Setup detects them once and writes unconditional folder loadouts into AGENTS-PLAN.yaml and AGENTS.md.

Canonical roles request modelProfile and may assign modelStages for work such as low-cost evidence extraction followed by advanced synthesis. Provider model identifiers stay in adapter mappings. Every supported adapter must map every canonical profile.

Model stage fields describe intended dispatch stages; generated single-agent definitions do not execute those stages by themselves. A staged evaluation must capture separate evidence-worker and synthesis invocations before the behavior is marked verified.

Build the portable technology detection registry and installed detector mirror before generating role and documentation views:

```bash
python3 scripts/build-technology-detection.py
```

The detection build validates every specialized technology and domain skill, rejects generic fixed-role skills and task-time fields in detection metadata, rejects detected skills in canonical fixed role loadouts, writes the portable YAML registry, and verifies that the installed detector mirror matches the canonical script.

Project Agent Setup selects representative folder scopes and runs detection once. Agent role, task wording, prompt keywords, read confirmation, and optional local commands are not detection inputs. Accepted source-backed loadouts are recorded in AGENTS-PLAN.yaml and rendered as unconditional folder skill-loading guidance in AGENTS.md.

Detection is scope-safe in mixed repositories. File extensions and globs form the scoped selector group; owning manifests, dependencies, and content markers form the project-signal group. A detected variant with both groups needs evidence from both. Dependency and configuration evidence comes from the nearest owning package or project manifest, so sibling modules and root workspace dependencies cannot activate stacks for an independently owned child package.

The generated [agent and skill hierarchy](design/agent-skill-hierarchy.svg) shows model profiles, every canonical role, fixed generic skill edges, and the specialized skills available for setup-time folder detection. Regenerate it with:

```bash
python3 scripts/build-agent-skill-hierarchy.py
```

The generated [agent, skill, technology, and test coverage checklist](design/agent-skill-test-coverage-checklist.md) inventories every canonical agent and bundled skill, shows specialized activation coverage, and distinguishes declarations and manual observations from independently verified behavior. Regenerate it with:

```bash
python3 scripts/build-support-checklist.py
```

Role cards, scenario examples, skill inventories, loadout tables, and runtime definitions are generated from canonical data rather than maintained independently in HTML. Canonical role examples show a scenario purpose, invocation, and plausible response. Each skill entry in canonical role YAML nests a justification that explains why the role needs the skill, and each output contract entry nests a purpose that explains why the output exists. The generated role modal displays those explanations with the enlarged pills, and native adapters render them as comments. The generator rejects canonical roles that reference missing skill IDs.

Use maintain-methodology-documentation when changing skills, roles, categories, adapters, or design pages. That skill owns the canonical-source update, regeneration, stale-output check, validation, and diff-review workflow.

Each skill frontmatter metadata block names its category id. The category file owns category order and display labels.

The HTML design pages use the generated static data to open formatted skill definitions from skill badges. The Edit button uses an editor URL scheme when the page can infer the repository root from a local file URL or from a repoRoot query parameter.

Use the check mode before publishing documentation changes.

```bash
python3 scripts/build-skill-docs.py --check
```

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

Install generated native agent definitions with the supported Codex or Claude adapter:

```bash
python3 scripts/install-skills.py --adapter codex --install-agents
python3 scripts/install-skills.py --adapter claude --install-agents
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

The refresh covers the shared AGENTS_HOME or ~/.agents skill install, the direct ~/.codex skill and agent install, and the Claude skill and agent install. To inspect the refresh plan without replacing files, run:

```bash
python3 scripts/refresh-shared-skills.py --dry-run
```

Each shared destination keeps an ownership manifest named .dev-methodology-install.json. During shared refresh, prune mode removes obsolete skills that this repository previously installed and leaves unowned local skills alone. If a destination has no ownership manifest, the refresh writes one and skips pruning for that run. Run a refresh before planned renames or deletions so later cleanup has an ownership baseline.

Ownership manifests record content digests. If an owned skill or agent changed after installation, replacement or pruning stops and reports that discrepancy analysis is required. After the old generic, installed customer, and new generic definitions have been compared and the user approves replacement, rerun the installer with both --replace and --replace-customized.

Runtime agent metadata packaged inside an owned skill is refreshed and pruned with that skill.

Standalone generated agents use a separate ownership manifest in the runtime agent folder. Pruning removes only agent files previously owned by this bundle and preserves unowned local agent definitions.

Before renaming or deleting a source skill, sweep this repository for the old skill id. Update or remove references in skill files, companion-skill lists, Codex metadata, role definitions, dispatch profiles, aggregate workflow examples, design documents, README content, scripts, and tests before refreshing shared installs.

After changing skill names or descriptions, run the metadata sync before validation:

```bash
python3 scripts/openai_metadata.py skills
```

When a source skill is renamed or deleted, use the dry run to confirm that the old owned skill is reported as obsolete before running the real refresh.

## Customer Machine Installation And Customization

The build produces customer-independent skills, canonical roles, support scripts, documentation data, and native agent definitions. On a customer machine, the Project Bootstrap Agent selects the applicable adapter and uses deterministic scripts to copy the generic skills, agents, and support files into the runtime user scope. The agent decides what applies; scripts perform repeatable copying, validation, ownership tracking, pruning, and dry-run reporting.

Customer maintainers may edit an installed skill or agent definition directly. Keep the original skill and agent names stable so role loadouts, companion-skill references, and project guidance continue to resolve. Optional provenance should remain minimal: record the original name and whether the installed definition replaces the generic one.

Customized files must not be silently overwritten. A requested update uses an agent-assisted three-way discrepancy analysis between the old generic definition, the installed customer definition, and the new generic definition. The user decides which differences to keep, merge, replace, or remove.

## Wiki Activity Agents

Wiki responsibilities are isolated from general documentation, coding, review, backlog, and project-setup roles. The dedicated wiki category contains:

- Wiki Setup Agent for initial wiki structure, ownership, federation, source workflow, and setup verification.
- Wiki Query Agent for wiki-first answers and bounded research handoffs.
- Wiki Research Agent for on-demand raw research reports.
- Public Source Collector for approved raw-only public source windows.
- Wiki Writer Agent for ordinary durable topic, hub, digest, and code-aware maintenance.
- Wiki Ingest Agent for raw-to-processed synthesis.
- Wiki Topic Verifier for independent topic-page acceptance.
- Wiki Artifact Reviewer for project-wiki methodology artifacts and their completed review checklists.

Documentation Writer owns functional specifications, architecture, high-level designs, module designs, and unit test plans. Artifact Review Agent owns the matching non-wiki artifact reviews. Work that needs durable wiki context or changes is handed to the appropriate wiki activity role instead of loading wiki skills into a general role.

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
- create-agents-plan
- maintain-methodology-documentation

The artifact creation skills are:

- create-project-wiki
- create-functional-spec
- create-architecture
- create-high-level-design
- create-module-design
- create-unit-test-plan

The artifact review skills are:

- review-project-wiki
- review-functional-spec
- review-architecture
- review-high-level-design
- review-module-design
- review-unit-test-plan

The development practice skills are:

- detect-technology-skills
- code-discovery
- test-strategy
- end-to-end-verification
- application-security
- user-experience-review
- prompt-contracts
- careful-coding
- code-comments
- create-backlog
- manage-backlog
- fix-explanation
- structured-explanation
- structured-design
- review-structured
- agent-claim
- agent-work-merge
- code-review-evidence
- test-driven-development
- code-execution-tracing
- root-cause-analysis
- runtime-evidence-collection

The stack and project-domain skill packs are:

- typescript-esm
- typescript-strict
- typescript-coding
- python-coding
- fastapi
- java-coding
- spring-boot
- sql-coding
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

The optional tool variants are:

- ast-grep

## Review Skill Checklist Convention

Every review skill uses a reference checklist named review-checklist-[review-target].md under that skill's references folder. For example, review-architecture uses review-checklist-architecture.md.

Review checklists are evidence-capture templates. Each checklist question requires status, the objective question, quoted evidence from the artifact or source material, and an assessment grounded in that quote.

Code review follows the same evidence philosophy without one massive universal review skill. The Code Review Agent reads the root and nearest AGENTS.md, loads every fixed-role skill and folder technology skill declared for the review scope, completes the applicable focused evidence checklists, and then synthesizes findings from the evidence packet. It does not rerun technology detection. Stage declarations do not prove staged execution; verification requires captured worker and synthesis invocations.

Code Comments is a fixed skill for Coding Agent and Code Review Agent. It governs mandatory headers for code artifacts, public construct documentation, concise rationale comments, and review evidence that checks implementation behavior against documented intent. Non-trivial comment blocks use Structured Explanation discipline. Configuration and other non-code files are outside the mandatory header rule.

When a review skill runs, it saves a completed review checklist next to the reviewed artifact using this form: artifact-name.review-checklist-[review-target].md. For example, a coding review of test.ts saves test.ts.review-checklist-coding.md.

Artifact-specific review skills pass the artifact, source evidence, and completed review checklist to documentation-page-verifier. The verifier uses the completed checklist evidence to complete the shared page-contract, source-authority, link, diagram, and steady-state assessment.

## Applying This Bundle To A Project

1. Use the Project Bootstrap Agent to detect the runtime and install the matching generic skills and generated native agents.
2. In the target repository, use documentation-bootstrap for first-time setup.
3. Use create-agents-plan to create AGENTS-PLAN.yaml when the project needs role agents, skill loadouts, folder routing, nested plan placement, or customer-safe example planning; generate AGENTS.md and thin CLAUDE.md bridge files where Claude Code is used.
4. As Project Agent Setup, use detect-technology-skills once for representative folder scopes, record source-backed loadouts in AGENTS-PLAN.yaml, and render unconditional folder skill-loading instructions into AGENTS.md.
5. Use development-methodology to choose the non-wiki documentation artifact type and apply the request-specific skill conditions, loading only the creation or review skill needed for the current job.
6. Use documentation-reverse-engineering when an existing codebase needs a source-backed documentation set.
7. Use Wiki Setup Agent for initial wiki creation or substantial restructuring, including the create-project-wiki artifact route when that durable contract is needed.
8. Use Wiki Writer Agent when docs/wiki needs ordinary topic maintenance, code-aware synchronization, commit-range review, Related Code upkeep, or Related Tests upkeep.
9. Use Wiki Ingest Agent for raw-source synthesis and Wiki Topic Verifier for the independent acceptance loop.
10. Use Wiki Query Agent for wiki-backed answers, Wiki Research Agent for bounded on-demand research, and Public Source Collector for approved raw-only collection windows.
11. Use create-functional-spec, create-architecture, create-high-level-design, create-module-design, or create-unit-test-plan when Documentation Writer creates one non-wiki methodology artifact from its template.
12. Use the matching non-wiki artifact review skill through Artifact Review Agent before finishing a functional specification, architecture document, high-level design, module design, or unit test plan.
13. Use Wiki Artifact Reviewer before accepting a project-wiki methodology artifact.
14. Use documentation-page-verifier as the shared verifier for mixed, unknown, or custom documentation artifacts.

## Neutral Target Project Layout

- [documentation-root]/functional
- [documentation-root]/architecture
- [documentation-root]/high-level
- [documentation-root]/modules
- AGENTS-PLAN.yaml
- [technology-subfolder]/AGENTS-PLAN.yaml when a subfolder has distinct technology, data, runtime, or verification guidance
- docs/wiki
- raw/wiki-fragments
- raw/processed

The placeholder [documentation-root] means the documentation root chosen by the target project. Projects may choose different folders when they already have established documentation locations, but each project should keep a clear home for each documentation type.

The project wiki should live at docs/wiki. It is a synthesized navigation and understanding layer, not the highest source of truth. Code and tests remain authoritative for actual behavior. Functional and technical documents can live under docs/wiki as wiki page subclasses or remain in their project documentation folders with wiki pages linking to them.

## Verification

Before publishing changes to this bundle, run:

```bash
python3 scripts/validate-agent-skills.py skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
python3 scripts/refresh-shared-skills.py
```
