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

Project agent and skill setup starts with one PROJECT.yaml at the project root as an intermediate, reviewable intent log. Project Configurator records every selected conceptual agent definition, skillset, folder route, and root or nested AGENTS.md placement in that one project-wide configuration before rendering operational guidance. A maintainer may edit PROJECT.yaml to request a correction; Project Configurator reconciles the edit with repository evidence and bundle constraints before regenerating the guidance. Claude Code projects also receive a thin CLAUDE.md beside each applicable AGENTS.md so Claude imports the same project guidance without duplicating it.

The core methodology keeps one shared wiki-compatible page contract and six document shapes. Each document shape has a focused creation skill, a reusable template asset, and an artifact review skill:

1. Project wiki page: project-wiki-create, project-wiki-template.md, project-wiki-review
2. Functional specification: create-functional-spec, functional-spec-template.md, review-functional-spec
3. Architecture: create-architecture, architecture-template.md, review-architecture
4. High-level design: create-high-level-design, high-level-design-template.md, review-high-level-design
5. Module design: create-module-design, module-design-template.md, review-module-design
6. Unit test plan: create-unit-test-plan, unit-test-plan-template.md, review-unit-test-plan

The shared page contract starts every durable page with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes. Specialized documents keep those sections first, then add their own sections.

Normal planned development proceeds top down from accepted functional specifications and architecture through create-high-level-design and review-high-level-design, then through create-module-design and review-module-design, and finally through ordinary implementation agents with the project-routed technology skills. The design skills use PLANNED_DEVELOPMENT mode, account for every applicable requirement, and block downstream work when a critical identity, security, public-response, state-ownership, validation, transaction, asynchronous, or failure-timing contract remains unresolved.

Project-specific evaluation skills may freeze inputs and compare completed candidates with hidden reference artifacts, but they do not create production designs or code and do not add project-specific development rules to the generation context. Accepted upstream specifications and designs remain valid production inputs even when a separate reverse-engineering process originally produced them.

## Repository Shape

- skills contains the portable Agent Skills.
- Specialized technology and domain skills own setup-time activation metadata in detection.yaml beside SKILL.md.
- skills/detect-technology-skills contains the setup workflow, generated detector mirror, and generated portable technology registry.
- skills/development-methodology/assets/templates contains the reusable TODO-driven template assets.
- Keep Codex openai.yaml metadata beside each source SKILL.md when a skill needs Codex app metadata, invocation policy, or tool dependencies.
- scripts/install-skills.py installs the bundled skills through adapter profiles for generic Agent Skills, Codex, Gemini CLI, Claude Code, and JetBrains Junie CLI.
- agents/role-schema.yaml defines the customer-independent conceptual agent definition schema.
- agents/model-profiles.yaml defines semantic simple, default, advanced, and advanced-long model profiles without provider identifiers.
- adapters/[runtime]/model-profiles.yaml maps semantic profiles to concrete models, reasoning effort, and context settings for each harness.
- adapters/[runtime]/skills/[skill-name]/SKILL.md contains directives that belong only to that runtime. The installer includes these skills only with the matching adapter.
- agents/roles contains conceptual agent definition sources grouped by Dev Activities, Wiki Activities, Project Setup, and Methodology Maintenance.
- generated/adapters contains ready-to-copy native agent definitions and agent-generation-manifest.json. Codex, Claude Code, Gemini CLI, and Junie CLI definitions are generated from the same conceptual sources.
- design/generated/technology-skill-detection-registry.js exposes the same detection registry for documentation and the future interactive agent-skill explorer.
- scripts/openai_metadata.py refreshes derived Codex interface fields from SKILL.md while preserving hand-authored policy and dependencies.
- scripts contains regression tests for installer behavior and bundle content.
- AGENTS.md contains repo-local maintenance directives for agents working on this source repository.

Reusable templates live inside the development-methodology skill assets so there is one distribution surface for agents. Target projects may copy individual template files when they need local editable documents, but the methodology itself is delivered through skills.

## Generated Methodology Documentation

```bash
python3 scripts/build-skill-docs.py
```

The script reads each bundled SKILL.md file, adjacent Codex openai.yaml metadata, the ordered design/skill-categories.yaml catalog, agents/role-schema.yaml, agents/model-profiles.yaml, adapter model mappings, adapter-owned skill sources, and conceptual agent definition sources. It writes design/generated/skill-definitions.js, design/generated/role-definitions.js, native definitions under generated/adapters, and agent-generation-manifest.json. The [Generic Agent Definitions Source page](design/generic-agent-definitions-source.html) owns portable skill sources, conceptual agent definition properties, native packaging, and adapter mappings. The [Agentic Configuration page](design/agentic-configuration.html) explains how the resulting runtime files provide relevant context while an agentic coding tool generates code.

The generation manifest is the deterministic build inventory: it records each conceptual agent definition source, every generated Codex, Claude Code, Gemini CLI, and Junie CLI path, each adapter-owned skill source and digest, and aggregate counts without timestamps. Codex generation enables and instructs every mutation-capable agent to load codex-harness-directives. Read-only Codex agents and every non-Codex adapter remain unchanged, so Codex-only directives do not leak into portable conceptual definitions.

Build the portable technology detection registry and installed detector mirror before generating conceptual agent definition and documentation views:

```bash
python3 scripts/build-technology-detection.py
```

The detection build validates the specialized metadata and refreshes the portable registry plus installed detector mirror. [Technology Skills](design/skills-modularization.html) explains always-used and rule-selected agent skills, detector inputs, activation semantics, proof boundaries, and setup-time technology bindings.

The generated [interactive agent and skill hierarchy](design/agent-and-skill-definitions.html#hierarchy-title) is published with the conceptual agent definition catalog, which owns its interaction instructions and scope. Regenerate the SVG with:

```bash
python3 scripts/build-agent-skill-hierarchy.py
```

The generated [agent, skill, technology, and test coverage checklist](design/agent-skill-test-coverage-checklist.md) inventories every agent and bundled skill, shows specialized activation coverage, and distinguishes declarations and manual observations from independently verified behavior. Regenerate it with:

```bash
python3 scripts/build-support-checklist.py
```

Conceptual agent definition cards, the skill catalog, and the agent-and-skill diagram are generated from conceptual definition and skill source data rather than maintained independently in HTML. Agent examples show a scenario purpose, invocation, and plausible response. Each skill entry in a conceptual definition YAML source nests a justification that explains why the agent needs the skill, each output contract entry nests a purpose that explains why the output exists, and agentDependencies names any fixed direct agent-to-agent use shown by the diagram. The generated definition modal displays the skill and output explanations with the enlarged pills, and native adapters render them as comments. The generator rejects conceptual definitions that reference missing skill IDs or agent dependencies.

Within the linked HTML design set, the documentation index assigns one owner to each substantive topic. Sibling HTML pages use navigation summaries and links instead of maintaining parallel explanations. The generated diagram and generated cards are the intentional duplicate views of conceptual-definition-to-skill relationships. The diagram can also reveal agent-to-agent dependencies without treating dynamic task-time routing as a fixed dependency.

Use maintain-methodology-documentation when changing skills, conceptual agent definitions, categories, adapters, or design pages. That skill owns source updates, regeneration, stale-output checks, validation, and diff review. Skill authoring and review share skill-authoring, while conceptual agent definition creation and review share agent-role-authoring so instruction structure, authority, state transitions, examples, agent dependencies, and outputs are defined once.

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

Deploy unchanged generic bundles to explicit user-level runtime directories so they are available across projects. Use replace and prune-owned when refreshing a bundle-owned installation.

The matching adapter skill source is merged only when that adapter is selected. The Codex command therefore installs the shared skills plus codex-harness-directives; Claude Code, Gemini CLI, and Junie CLI deployments do not receive that Codex-only skill. A caller that supplies a custom generic source may also supply an explicit adapter source with --adapter-skills-source.

Deploy the Codex bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --dest ~/.codex/skills \
  --install-agents \
  --agents-dest ~/.codex/agents \
  --replace \
  --prune-owned
```

Deploy the Claude Code bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter claude \
  --dest ~/.claude/skills \
  --install-agents \
  --agents-dest ~/.claude/agents \
  --replace \
  --prune-owned
```

Deploy the Gemini CLI bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter gemini \
  --dest ~/.gemini/skills \
  --install-agents \
  --agents-dest ~/.gemini/agents \
  --replace \
  --prune-owned
```

Deploy the Junie CLI bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter junie \
  --dest ~/.junie/skills \
  --install-agents \
  --agents-dest ~/.junie/agents \
  --replace \
  --prune-owned
```

The installer never infers AGENTS_HOME, CODEX_HOME, CLAUDE_HOME, or a user-home destination. Use --dry-run to inspect an explicit deployment, --replace to update bundle-owned copies, and --prune-owned to remove obsolete owned artifacts at that target.

Use project-level skill and agent directories only when the project needs customized definitions, deliberate project-only scoping, or a checked-in team configuration. An unchanged generic bundle belongs in the runtime's user-level directories.

The same explicit-destination rule applies to every adapter, including Gemini CLI and Junie CLI.

Each explicit destination keeps an ownership manifest named .dev-methodology-install.json. Ownership manifests record content digests. Replacement, pruning, and cleanup refuse to discard a customized owned artifact without discrepancy analysis and explicit approval. Unowned skills and agents are never removed.

Remove bundle-owned artifacts from an explicit skills destination and optional agent destination with:

```bash
python3 scripts/install-skills.py \
  --dest /explicit/skills/destination \
  --agents-dest /explicit/agents/destination \
  --remove-owned
```

Before renaming or deleting a source skill, sweep this repository for the old skill id. Update or remove references in skill files, companion-skill lists, Codex metadata, conceptual agent definitions, dispatch profiles, aggregate workflow examples, design documents, README content, scripts, and tests before regenerating the derived outputs.

After changing skill names or descriptions, run the metadata sync before validation:

```bash
python3 scripts/openai_metadata.py skills
```

## Customer Deployment And Customization

Customer maintainers may edit an installed skill or native agent definition directly. Keep the original skill and agent names stable so definition-owned skillsets, companion-skill references, and project guidance continue to resolve. Optional provenance should remain minimal: record the original name and whether the installed definition replaces the generic one.

For a requested customized-copy update, use an agent-assisted three-way discrepancy analysis between the old generic definition, the installed customer definition, and the new generic definition. The user decides which differences to keep, merge, replace, or remove.

After that analysis and explicit user approval, --replace-customized may be combined with --replace to apply the approved replacement.

## Agent Responsibility Boundaries

Wiki work remains separate from general documentation, coding, review, backlog, and project setup. The generated [Core Agent and Skills](design/agent-and-skill-definitions.html) page owns catalog views of current conceptual agent definitions and skill definitions, including responsibilities, assigned skills, output contracts, examples, model profiles, repository mutation policies, and agent-skill relationships. [Technology Skills](design/skills-modularization.html) explains technology-agnostic agent skills and setup-bound technology extensions. The [orchestrated development lifecycle](design/orchestrated-development-lifecycle.html) owns bootstrap, normal planned design progression, complete source-backed documentation, execution, review, verification, integration, claim release, and execution evidence.

Whole-project reverse engineering finishes after project configuration and exact path coverage, one reviewed module design per meaningful responsibility, complete reviewed HLD grouping, reviewed architecture, reviewed functional workflow coverage, and verified README/wiki navigation. Sampling may be useful for later project-owned experiments, but it never reduces the shared documentation coverage contract.

## Bundled Skill Inventory

README.md is the required human-facing inventory of bundled skill names. The generated catalog owns their definitions and relationships; this list does not restate either.

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
- agent-role-authoring
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
- java-design
- spring-boot
- spring-boot-design
- spring-data-jpa
- spring-boot-testing
- liquibase
- jhipster-project
- jhipster-domain-modeling
- jhipster-persistence
- jhipster-testing
- jhipster-security
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

The jhipster skill family targets Java and Spring Boot applications generated with JHipster. Setup-time detection requires JHipster evidence at the nearest owning project boundary before it adds the project skill or any concern-specific JHipster skill.

The optional tool variants are:

- ast-grep

The Codex-only adapter skill is:

- codex-harness-directives

## Review Skill Checklist Convention

Every review skill uses a reference checklist named review-checklist-[review-target].md under that skill's references folder. For example, review-architecture uses review-checklist-architecture.md.

Review checklists are evidence-capture templates. Each checklist question requires status, the objective question, quoted evidence from the artifact or source material, and an assessment grounded in that quote.

When a review skill runs, it saves a completed review checklist next to the reviewed artifact using this form: artifact-name.review-checklist-[review-target].md. For example, a coding review of test.ts saves test.ts.review-checklist-coding.md.

Artifact-specific review skills pass the artifact, source evidence, and completed review checklist to documentation-page-verify. The verifier uses the completed checklist evidence to complete the shared page-contract, source-authority, link, diagram, and steady-state assessment.

## Applying This Bundle To A Project

Invoke Project Bootstrapper once and describe the desired steady state:

1. Use the repository bundle sources and matching generated runtime adapter.
2. Review the resulting PROJECT.yaml, root or nested AGENTS.md guidance, and verification commands. [Technology Skills](design/skills-modularization.html) explains setup-time detection and folder skillsets.
3. Use documentation-bootstrap and documentation-reverse-engineer when the project needs a source-backed documentation baseline. Whole-project reverse engineering covers every meaningful module by default: inventory and review module designs first, group the complete set into high-level designs, derive architecture from those groups, cover all observable workflows, and expose the complete hierarchy through README and wiki hubs. Narrower coverage is valid only when the user explicitly names the boundary.
4. For normal planned development, treat accepted functional specifications and architecture as the upstream authority. Create and review the HLD, create and review its module designs, then implement with the ordinary coding agent and project-routed technology skills. A missing high-impact contract blocks dependent work instead of being filled with an unsupported assumption.
5. Follow the [orchestrated development lifecycle](design/orchestrated-development-lifecycle.html) for the owning execution, independent review, integrated verification, commit, and claim-release gates.

Separately requested deployment still requires caller-supplied destinations under Explicit Target Deployment.

## Neutral Target Project Layout

- [documentation-root]/functional
- [documentation-root]/architecture
- [documentation-root]/high-level
- [documentation-root]/modules
- [documentation-root]/module-coverage.md
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
python3 scripts/validate-agent-skills.py adapters/codex/skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
```
