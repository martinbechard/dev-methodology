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

Use the repository skill sources and generated adapters as the operating surface. Working on this bundle does not require copying its skills or agents into user-home runtime folders.

Project agent and skill setup starts with one PROJECT.yaml at the project root as the reviewable configuration artifact. The create-project-configuration skill records every role, skill loadout, folder route, and root or nested AGENTS.md placement in that one project-wide configuration. Claude Code projects also receive a thin CLAUDE.md beside each applicable AGENTS.md so Claude imports the same project guidance without duplicating it.

The core methodology keeps one shared wiki-compatible page contract and six document shapes. Each document shape has a focused creation skill, a reusable template asset, and an artifact review skill:

1. Project wiki page: project-wiki-create, project-wiki-template.md, project-wiki-review
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
- agents/roles contains canonical role files grouped by Dev Activities, Wiki Activities, Project Setup, and Methodology Maintenance.
- generated/adapters contains ready-to-copy native agent definitions and agent-generation-manifest.json. The current milestone generates Codex and Claude definitions from the same canonical roles.
- design/generated/technology-skill-detection-registry.js exposes the same detection registry for documentation and the future interactive agent-skill explorer.
- scripts/openai_metadata.py refreshes derived Codex interface fields from SKILL.md while preserving hand-authored policy and dependencies.
- scripts contains regression tests for installer behavior and bundle content.
- AGENTS.md contains repo-local maintenance directives for agents working on this source repository.

Reusable templates live inside the development-methodology skill assets so there is one distribution surface for agents. Target projects may copy individual template files when they need local editable documents, but the methodology itself is delivered through skills.

## Generated Methodology Documentation

```bash
python3 scripts/build-skill-docs.py
```

The script reads each bundled SKILL.md file, the adjacent Codex openai.yaml metadata, the ordered design/skill-categories.yaml catalog, agents/role-schema.yaml, agents/model-profiles.yaml, adapter model mappings, and the canonical role files. It writes design/generated/skill-definitions.js, design/generated/role-definitions.js, native agent definitions for the supported runtime adapters, and generated/adapters/agent-generation-manifest.json.

The agent generation manifest is the deterministic forensic inventory for a build. It maps every canonical role source to its Codex and Claude output path and expected SHA-256 digest, with exact role and adapter counts. It deliberately omits timestamps so a no-op build remains clean. Installer manifests in each runtime agent destination record the later installation time and installed digests.

Canonical roles use three skill-loading paths. A skill entry without a condition is a fixed role skill and always loads. A skill entry with a condition is request-specific; generated agent instructions use the form Use the skill-name skill when condition, while telling the agent to inspect the requested outcome and available evidence when wording is ambiguous. Technology and domain skills remain outside role assignment: Project Configurator detects them once and writes unconditional folder loadouts into PROJECT.yaml and AGENTS.md.

Canonical roles request modelProfile and may assign modelStages for work such as low-cost evidence extraction followed by advanced synthesis. Provider model identifiers stay in adapter mappings. Every supported adapter must map every canonical profile.

Model stage fields describe intended dispatch stages; generated single-agent definitions do not execute those stages by themselves. A staged evaluation must capture separate evidence-worker and synthesis invocations before the behavior is marked verified.

Build the portable technology detection registry and installed detector mirror before generating role and documentation views:

```bash
python3 scripts/build-technology-detection.py
```

The detection build validates every specialized technology and domain skill, rejects generic fixed-role skills and task-time fields in detection metadata, rejects detected skills in canonical fixed role loadouts, writes the portable YAML registry, and verifies that the installed detector mirror matches the canonical script.

Project Configurator selects representative folder scopes and runs detection once. Agent role, task wording, prompt keywords, read confirmation, and optional local commands are not detection inputs. Accepted source-backed loadouts are recorded in PROJECT.yaml and rendered as unconditional folder skill-loading guidance in AGENTS.md.

Detection is scope-safe in mixed repositories. Every definition names the skill it selects and expresses activation as explicit any-of and all-of clauses over file extensions, same-file path and extension matches, owning manifests, dependencies, content markers, or parsed source imports. A skill activates only when one complete any-of branch succeeds, and the matched artifacts become its source evidence. Parsed Python imports ignore comments and string literals. Dependency and configuration evidence comes from the nearest owning package or project manifest, so sibling modules and root workspace dependencies cannot activate stacks for an independently owned child package.

The generated [interactive agent and skill hierarchy](design/agent-skill-hierarchy.svg) lets users select a canonical role to isolate its fixed and request-specific skill edges, or select a skill to reveal every canonical role using it. Double-clicking an item opens the same generated definition modal used by the role cards and skill catalog, and closing a definition opened from the map returns to the map. The hierarchy omits setup-time stack and domain skills because canonical roles do not link to them; the complete inventory remains in the skill catalog. Regenerate it with:

```bash
python3 scripts/build-agent-skill-hierarchy.py
```

The generated [agent, skill, technology, and test coverage checklist](design/agent-skill-test-coverage-checklist.md) inventories every canonical agent and bundled skill, shows specialized activation coverage, and distinguishes declarations and manual observations from independently verified behavior. Regenerate it with:

```bash
python3 scripts/build-support-checklist.py
```

Role cards, scenario examples, skill inventories, loadout tables, and runtime definitions are generated from canonical data rather than maintained independently in HTML. Canonical role examples show a scenario purpose, invocation, and plausible response. Each skill entry in canonical role YAML nests a justification that explains why the role needs the skill, and each output contract entry nests a purpose that explains why the output exists. The generated role modal displays those explanations with the enlarged pills, and native adapters render them as comments. The generator rejects canonical roles that reference missing skill IDs.

Use maintain-methodology-documentation when changing skills, roles, categories, adapters, or design pages. That skill owns the canonical-source update, regeneration, stale-output check, validation, and diff-review workflow. Skill authoring and review share skill-authoring so harness boundaries, portability, dependencies, and concision are defined once.

Each skill frontmatter metadata block names its category id. The category file owns category order and display labels.

The HTML design pages use the generated static data to open formatted skill definitions from skill badges. The Edit button uses an editor URL scheme when the page can infer the repository root from a local file URL or from a repoRoot query parameter.

Use the check mode before publishing documentation changes.

```bash
python3 scripts/build-skill-docs.py --check
```

## Agent Claims And Worktrees

Every modifying agent uses agent-claim before changing repository files or exclusive runtime state. Claim acquisition is atomic and repository-global across linked Git worktrees.

- The first independent writer may claim a clean primary worktree.
- A later non-overlapping writer receives a dedicated branch and linked worktree.
- Overlapping file or exclusive resource claims wait or coordinate.
- Dirty state without a claim enters explicit recovery instead of accepting more anonymous work.
- A modifying claim is released only after verification, commit or explicit no-change, clean worktree status, and runtime-resource cleanup or handoff.

The bundled command implements primary, isolation, wait, recovery, heartbeat, status, and release decisions:

```bash
python3 skills/agent-claim/scripts/claim.py --help
```

Dev Orchestrator owns the root task claim and child handoffs. Dev Merge Coordinator accepts committed clean contributions, owns shared regeneration and integration verification, commits the combined result, and releases the integration claim only from a clean worktree.

## Explicit Target Deployment

The build and maintenance workflow does not install skills or agents into user-home runtime folders. The installer exists only for an explicitly requested deployment or packaging operation, and every destination must be supplied by the caller.

Deploy the Codex bundle to explicit target-project directories:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --dest /path/to/target/.agents/skills \
  --install-agents \
  --agents-dest /path/to/target/.codex/agents
```

Deploy the Claude bundle to explicit target-project directories:

```bash
python3 scripts/install-skills.py \
  --adapter claude \
  --dest /path/to/target/.claude/skills \
  --install-agents \
  --agents-dest /path/to/target/.claude/agents
```

The installer never infers AGENTS_HOME, CODEX_HOME, CLAUDE_HOME, or a user-home destination. Use --dry-run to inspect an explicit deployment, --replace to update bundle-owned copies, and --prune-owned to remove obsolete owned artifacts at that target.

The same explicit-destination rule applies to the generic, Gemini, and Junie adapters, including --adapter junie.

Each explicit destination keeps an ownership manifest named .dev-methodology-install.json. Ownership manifests record content digests. Replacement, pruning, and cleanup refuse to discard a customized owned artifact without discrepancy analysis and explicit approval. Unowned skills and agents are never removed.

Remove bundle-owned artifacts from an explicit skills destination and optional agent destination with:

```bash
python3 scripts/install-skills.py \
  --dest /explicit/skills/destination \
  --agents-dest /explicit/agents/destination \
  --remove-owned
```

Before renaming or deleting a source skill, sweep this repository for the old skill id. Update or remove references in skill files, companion-skill lists, Codex metadata, role definitions, dispatch profiles, aggregate workflow examples, design documents, README content, scripts, and tests before regenerating the derived outputs.

After changing skill names or descriptions, run the metadata sync before validation:

```bash
python3 scripts/openai_metadata.py skills
```

## Customer Deployment And Customization

The build produces customer-independent skills, canonical roles, support scripts, documentation data, and native agent definitions. Project Bootstrapper works from those repository artifacts without populating user-home runtime folders. When the user separately requests a packaged deployment, the caller chooses explicit target directories and the installer performs repeatable copying, validation, ownership tracking, pruning, dry-run reporting, and cleanup.

Customer maintainers may edit an installed skill or agent definition directly. Keep the original skill and agent names stable so role loadouts, companion-skill references, and project guidance continue to resolve. Optional provenance should remain minimal: record the original name and whether the installed definition replaces the generic one.

Customized files must not be silently overwritten. A requested update uses an agent-assisted three-way discrepancy analysis between the old generic definition, the installed customer definition, and the new generic definition. The user decides which differences to keep, merge, replace, or remove.

After that analysis and explicit user approval, --replace-customized may be combined with --replace to apply the approved replacement.

## Wiki Activities

Wiki responsibilities are isolated from general documentation, coding, review, backlog, and project-setup roles. The dedicated wiki category contains:

- Wiki Architect for initial wiki structure, ownership, federation, source workflow, and setup verification.
- Wiki Query Responder for wiki-first answers and bounded research handoffs.
- Wiki Researcher for on-demand raw research reports.
- Wiki Source Collector for approved raw-only public source windows.
- Wiki Writer for ordinary durable topic, hub, digest, and code-aware maintenance.
- Wiki Ingester for raw-to-processed synthesis.
- Wiki Topic Verifier for independent topic-page acceptance.
- Wiki Artifact Reviewer for project-wiki methodology artifacts and their completed review checklists.

Project Bootstrapper is the one-command setup entry point. It reuses an existing PROJECT.yaml without rerunning Project Configurator or technology detection. When PROJECT.yaml is absent, it runs Project Configurator before documentation work. It then delegates each selected non-wiki artifact to Dev Documentation Writer, routes every artifact through the matching independent reviewer until accepted, uses the wiki roles when the project selects docs/wiki, and finishes with integrated verification through Dev Verifier.

Dev Documentation Writer owns functional specifications, architecture, high-level designs, module designs, unit test plans, and README or custom-entry-document integration during reverse engineering. Dev Artifact Reviewer owns the matching non-wiki artifact reviews and applies the shared page verifier when a custom document has no artifact-specific checklist. Work that needs durable wiki context or changes is handed to the appropriate wiki activity role instead of loading wiki skills into a general role.

## Bundled Skill Inventory

The wiki and development-wiki skills are:

- project-wiki
- project-wiki-query
- project-wiki-research
- project-wiki-create
- project-wiki-review
- project-wiki-topic-write
- project-wiki-topic-verify
- code-project-wiki

The documentation methodology skills are:

- development-methodology
- documentation-bootstrap
- documentation-reverse-engineer
- documentation-page-verify
- create-project-configuration
- maintain-methodology-documentation
- skill-authoring
- name-methodology-artifacts

The artifact creation skills are:

- create-functional-spec
- create-architecture
- create-high-level-design
- create-module-design
- create-unit-test-plan

The artifact review skills are:

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
- organise-project-files
- create-backlog
- manage-backlog
- fix-explanation
- structured-explanation
- structured-design
- review-structured-artifact
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
- typescript
- python
- fastapi
- java
- spring-boot
- sql
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
- agent-harness
- tool-runtime
- plan-engine
- local-model-integration

The optional tool variants are:

- ast-grep

## Review Skill Checklist Convention

Every review skill uses a reference checklist named review-checklist-[review-target].md under that skill's references folder. For example, review-architecture uses review-checklist-architecture.md.

Review checklists are evidence-capture templates. Each checklist question requires status, the objective question, quoted evidence from the artifact or source material, and an assessment grounded in that quote.

Dev Artifact Reviewer always loads review-structured-artifact for the generic base checklist and finding synthesis, then adds the matching artifact-specific review skill for the requested document type. The artifact-specific checklist supplements the generic checklist rather than replacing it.

Methodology Maintainer and Methodology Artifact Reviewer both load skill-authoring. It prevents distributed skills from telling ordinary agents to rediscover or reread harness-loaded instruction files while preserving explicit AGENTS.md creation, update, validation, rendering, review, and harness-investigation tasks.

Code review follows the same evidence philosophy without one massive universal review skill. The Dev Code Reviewer applies the fixed-role and folder technology skills supplied for the review scope, completes the applicable focused evidence checklists, and then synthesizes findings from the evidence packet. It does not rerun technology detection. Stage declarations do not prove staged execution; verification requires captured worker and synthesis invocations.

Code Comments is a fixed skill for Dev Coder and Dev Code Reviewer. It governs mandatory headers for code artifacts, public construct documentation, concise rationale comments, and review evidence that checks implementation behavior against documented intent. Non-trivial comment blocks use Structured Explanation discipline. Configuration and other non-code files are outside the mandatory header rule.

When a review skill runs, it saves a completed review checklist next to the reviewed artifact using this form: artifact-name.review-checklist-[review-target].md. For example, a coding review of test.ts saves test.ts.review-checklist-coding.md.

Artifact-specific review skills pass the artifact, source evidence, and completed review checklist to documentation-page-verify. The verifier uses the completed checklist evidence to complete the shared page-contract, source-authority, link, diagram, and steady-state assessment.

## Applying This Bundle To A Project

Invoke Project Bootstrapper once and describe the desired steady state. The Bootstrapper owns the remaining setup sequence:

1. Work from the repository bundle sources and matching generated runtime adapter without creating duplicate user-home installations.
2. Check for project-root PROJECT.yaml. When it exists, reuse its validated roles, folder skill loadouts, routing, and verification commands without invoking Project Configurator or rerunning detection. When it is absent, delegate configuration to Project Configurator; it inspects the target, runs technology detection once for representative folder scopes, creates PROJECT.yaml, renders root and nested AGENTS.md guidance, and validates the routing before documentation begins. Reconfigure an existing PROJECT.yaml only when the user explicitly asks.
3. Use documentation-bootstrap and documentation-reverse-engineer to identify the smallest durable documentation set supported by live code, configuration, tests, procedures, and existing documentation.
4. Delegate each template-owned non-wiki artifact to Dev Documentation Writer with one matching creation route. Use its README or custom-document integration route for entry documents that must preserve an established format. Use Wiki Architect and Wiki Writer when the selected project convention includes docs/wiki.
5. Send non-wiki documents to Dev Artifact Reviewer, project-wiki methodology artifacts to Wiki Artifact Reviewer, and ordinary wiki topic pages to Wiki Topic Verifier. Return findings to the owning writer and repeat until the artifact passes or a specific human decision prevents correction.
6. Delegate integrated build, test, lint, documentation, link, wiki, and setup checks to Dev Verifier. Reopen correctable work rather than reporting an avoidable incomplete setup.
7. Finish with the configured routing, accepted documentation and review evidence, exact verification results, and only genuinely unresolved decisions.

The Bootstrapper does not stop after a recommendation, partial document set, or agent handoff while safe project-local work remains. Separately requested deployment still requires caller-supplied destinations.

Bootstrap is resumable. Existing valid configuration, accepted documents, and completed review evidence are reused rather than recreated. A failed correction returns to its owning writer with the reviewer evidence; the same unresolved finding is not retried indefinitely, and accepted independent work remains available for a later resume.

## Neutral Target Project Layout

- [documentation-root]/functional
- [documentation-root]/architecture
- [documentation-root]/high-level
- [documentation-root]/modules
- PROJECT.yaml
- [technology-subfolder]/AGENTS.md when a subfolder needs distinct operational guidance
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
```
