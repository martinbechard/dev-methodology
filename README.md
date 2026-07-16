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

The [Documentation Templates page](design/documentation-templates.html) describes all seven distributed template assets, their creation and review routes, and the project wiki repository and topic-page formats.

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

The script reads each bundled SKILL.md file, the distributed methodology templates, adjacent Codex openai.yaml metadata, the ordered design/skill-categories.yaml catalog, agents/role-schema.yaml, agents/model-profiles.yaml, adapter model mappings, adapter-owned skill sources, and conceptual agent definition sources. It writes design/generated/skill-definitions.js, design/generated/template-definitions.js, design/generated/role-definitions.js, native definitions under generated/adapters, and agent-generation-manifest.json. The [Generic Agent Definitions Source page](design/generic-agent-definitions-source.html) owns portable skill sources, conceptual agent definition properties, native packaging, and adapter mappings. The [Agentic Configuration page](design/agentic-configuration.html) explains how the resulting runtime files provide relevant context while an agentic coding tool generates code.

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
- Exact files, directory trees, repository-wide ownership, and exclusive resources use distinct scope forms.
- A claim can atomically extend its narrow scope as new files or resources become necessary.
- Overlap returns exact conflict pairs; a blocked extension leaves the live claim unchanged.
- Dirty state without a claim enters explicit recovery instead of accepting more anonymous work.
- A modifying claim is released only after verification, commit or explicit no-change, clean worktree status, and runtime-resource cleanup or handoff.

Separate worktrees may commit to their unique branches without a global commit resource. Integration uses a target-specific resource such as merge:integration:main only while updating that shared target branch.

The live registry remains authoritative. Coordination outcomes also append to a repository-global event journal under the Git common directory. The default maintenance policy keeps today and yesterday as hot UTC JSON Lines files, archives older complete days losslessly, and writes compact daily summaries. Native reports use only that journal and the live registry; they do not parse agent transcripts.

The bundled command implements primary, isolation, wait, recovery, extension, heartbeat, status, release, journal maintenance, and contention reporting:

```bash
python3 skills/agent-claim/scripts/claim.py --help
```

Dev Orchestrator owns the root task claim and child handoffs. Dev Merge Coordinator accepts committed clean contributions, acquires the target-specific integration resource, owns shared regeneration and integration verification, commits the combined result, and releases the integration claim only from a clean worktree.

## Scoped Target Deployment

The build and maintenance workflow does not install skills or agents automatically. The installer acts only when explicitly invoked. Use --scope user to select the adapter's standard user directories or --scope project to select its standard directories under the current project. Explicit --dest and --agents-dest values override the corresponding scoped defaults.

Cleanup is enabled by default and removes obsolete bundle-owned artifacts recorded in the destination ownership manifest. Use --cleanup false to retain them. The earlier --prune-owned remains accepted as a deprecated compatibility alias for enabled cleanup. Cleanup never removes unowned skills or agents. Use --replace when refreshing existing bundle-owned files.

A non-dry-run refresh stages complete destination trees and ownership manifests beside the live destinations before changing them. Skills and optional native agents commit as one in-process transaction. A handled staging or destination-swap failure restores every previously live destination when rollback succeeds. If rollback cannot fully restore the destinations, the installer retains the transaction backups and reports their locations for recovery. A successful commit removes the transaction backups.

The matching adapter skill source is merged only when that adapter is selected. The Codex command therefore installs the shared skills plus codex-harness-directives; Claude Code, Gemini CLI, and Junie CLI deployments do not receive that Codex-only skill. A caller that supplies a custom generic source may also supply an explicit adapter source with --adapter-skills-source.

Deploy the Codex bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --scope user \
  --install-agents \
  --replace
```

Deploy the Claude Code bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter claude \
  --scope user \
  --install-agents \
  --replace
```

Deploy the Gemini CLI bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter gemini \
  --scope user \
  --install-agents \
  --replace
```

Deploy the Junie CLI bundle globally:

```bash
python3 scripts/install-skills.py \
  --adapter junie \
  --scope user \
  --install-agents \
  --replace
```

Deploy the Codex bundle to the current project instead:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --scope project \
  --install-agents \
  --replace
```

### Preferred MCP Operations Layer

Codex and Junie can use mcp-agent-ops as the preferred deterministic interface for claims, skill catalog reads, technology detection, skill validation, YAML verification, and Markdown link checks. The distributed scripts remain portability fallbacks only when the tool is absent or its server cannot initialize or connect before request dispatch. A valid structured result such as WAIT, BLOCKED, NO_VARIANT, a validation finding, or a path and authorization rejection is not a transport failure and must not be retried through a fallback.

Install mcp-agent-ops 0.2.3 or newer from its verified release wheel before configuring either host. Follow the companion project's [verified release installation procedure](https://github.com/martinbechard/mcp-agent-ops#install-the-latest-release), including checksum verification and the installed identity checks. The bundle installer deploys only skills and generated agents; it never edits host MCP configuration or installs an external executable.

Configure Codex at user or trusted-project scope in config.toml. Custom subagents inherit parent MCP configuration when they omit an agent-specific server table, so the generated conceptual agents do not duplicate this connection definition.

For a user-scope Codex deployment, the MCP skill root is the resolved absolute path to ~/.agents/skills. The detection registry must be below that same installed root. For a project-scope or explicit-destination deployment, use the resolved selected destination instead. Keeping the installer destination and MCP root identical prevents the host and the MCP catalog from loading different bundle versions.

```toml
[mcp_servers.mcp-agent-ops]
enabled = true
required = false
command = "/absolute/path/to/mcp-agent-ops"
startup_timeout_sec = 15.0
tool_timeout_sec = 60.0

[mcp_servers.mcp-agent-ops.env]
MCP_AGENT_OPS_SKILL_ROOTS = "/absolute/path/to/user-home/.agents/skills"
MCP_AGENT_OPS_DETECTION_REGISTRY = "/absolute/path/to/user-home/.agents/skills/detect-technology-skills/references/technology-skill-detection-registry.yaml"
MCP_AGENT_OPS_WORKSPACE_ROOTS = "/absolute/path/to/allowed/projects"
```

Earlier Codex bundle deployments may be manifest-owned under ~/.codex/skills. Migrate by deploying the current Codex bundle to user scope, changing both MCP paths to ~/.agents/skills, and starting a new host session or calling skill_refresh. After skill_list confirms the new catalog, remove only the legacy bundle-owned copy with:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --dest ~/.codex/skills \
  --remove-owned
```

The legacy cleanup preserves independent and customized unowned content in ~/.codex/skills.

Configure Junie in the user or project mcp.json file. A generated Junie agent without an mcpServers allowlist can use the servers configured for its session.

```json
{
  "mcpServers": {
    "mcp-agent-ops": {
      "command": "/absolute/path/to/mcp-agent-ops",
      "args": [],
      "env": {
        "MCP_AGENT_OPS_SKILL_ROOTS": "/absolute/path/to/user-home/.junie/skills",
        "MCP_AGENT_OPS_DETECTION_REGISTRY": "/absolute/path/to/user-home/.junie/skills/detect-technology-skills/references/technology-skill-detection-registry.yaml",
        "MCP_AGENT_OPS_WORKSPACE_ROOTS": "/absolute/path/to/allowed/projects"
      }
    }
  }
}
```

Use the operating-system path separator when more than one root is required. Every model-supplied repository, project, worktree, verification, and validation path must be absolute and resolve beneath a configured root. A configured skill symlink may target another location only when that resolved target is also configured as a skill root.

The server reuses one immutable catalog snapshot. After an explicit deployment updates installed skills, start a new host session or call skill_refresh. Normal routing must not reread skills already preloaded by the host. When selected skill content is not yet in context, load the complete selected set with one skill_load call and retrieve only required supporting resources with skill_resource_load.

See the [Codex MCP configuration reference](https://learn.chatgpt.com/docs/extend/mcp) and [Junie MCP configuration reference](https://junie.jetbrains.com/docs/junie-cli-mcp-configuration.html) for the host-owned configuration surfaces.

Host approval policy remains user-owned. The evaluation runner's automatic approval of thirteen exact MCP operations and its Git-lifecycle permissions are isolated evaluation policy and are not copied into normal Codex or Junie host configuration.

An MCP evaluation requires one call-bearing MCP process stream. A completed call in any additional process stream invalidates the exact-once session evidence instead of being ignored.

Every required operation must also carry its expected privacy-safe semantic outcome. An outcome-less completed call is not semantic evidence. The integration case accepts VALID from skill_validate and CATALOG from skill_refresh; FINDINGS, EMPTY, and missing outcomes fail the deterministic tool contract.

The installer derives destinations only when --scope user or --scope project is supplied. Without a scope, provide --dest and, when installing agents, --agents-dest. Use --dry-run to inspect a deployment, --replace to update bundle-owned copies, and --cleanup false only when obsolete owned artifacts must be retained.

Use project-level skill and agent directories only when the project needs customized definitions, deliberate project-only scoping, or a checked-in team configuration. An unchanged generic bundle belongs in the runtime's user-level directories.

The same scoped-default and explicit-override rules apply to every adapter, including Gemini CLI and Junie CLI.

Each destination keeps an ownership manifest named .dev-methodology-install.json. Ownership manifests record content digests. Replacement, cleanup, and removal refuse to discard a customized owned artifact without discrepancy analysis and explicit approval. Unowned skills and agents are never removed.

Remove bundle-owned artifacts from an explicit skills destination and optional agent destination with:

```bash
python3 scripts/install-skills.py \
  --adapter codex \
  --scope user \
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
- quarkus
- quarkus-design
- quarkus-persistence
- quarkus-testing
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

Separately requested deployment uses the user or project defaults, or caller-supplied destination overrides, under Scoped Target Deployment.

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

## Agent And Skill Evaluations

The evals directory owns synthetic fixtures, complete agent and skill coverage declarations, workflow packs, Judge definitions, sandbox profiles, evidence receipts, and concise results. Evaluation support targets Codex and Junie. Other generated adapters remain part of the distributable bundle but are outside this evaluation harness.

Operational commands and receipt requirements are documented in [evals/README.md](evals/README.md). The generated [agent and skill coverage checklist](design/agent-skill-test-coverage-checklist.md) reports declarations, fixtures, execution, Judge outcome, Judge calibration, security containment, and stale evidence separately.

Evaluation coverage has four distinct layers:

1. Structural checks validate every skill, conceptual agent definition, generated adapter, detection rule, and catalog reference.
2. Skill probes declare the applicable trigger, negative trigger, observable behavior, Judge plan, workflow associations, and matched skill-omission and wrong-skill controls for every bundled skill.
3. Agent scenarios declare happy-path and boundary behavior, repository mutation authority, output-contract fields, supported harnesses, and Judge plans for every conceptual agent definition.
4. Workflow packs evaluate code delivery, documentation and methodology, project setup, wiki lifecycle, and backlog work across their required independent handoffs.

Deterministic Judges run before semantic judgment and own executable checks, schemas, trace identity, skill reads, mutation boundaries, command results, state transitions, and source or fixture hashes. A Model Judge is used only when exact checks cannot decide semantic quality. Calibration metrics can be computed now, but promotion to a calibrated Model Judge is disabled until every sample has provenance-bound Model and Human Judge artifacts for the exact harness, prompt, model, reasoning profile, rubric, and calibration set. Raw Judge outcome and calibration status remain separate. A deterministic critical failure skips Model Judge execution.

Fixtures are prepared once per content digest, dependency inputs, platform, architecture, and toolchain. A trusted fixture-preparation step may install dependencies while populating the integrity-checked prepared snapshot; live harness execution refuses install hooks. Before a live clone, the runner checks the full prepared-tree digest while holding the cache-key lock. Each run receives a disposable copy-on-write workspace when the platform supports it and a full disposable copy otherwise. Transient dependency, build, cache, and version-control trees do not participate in source hashing or source copying. The prepared cache is not claimed as filesystem-immutable, and external dependency-cache mounts are not implemented.

Ordinary Codex and Junie cases run in the local tier. This tier isolates reproducibility and host state; it is not a hostile-code sandbox. Both receive a disposable workspace, controlled configuration and environment, isolated evidence, bounded output and time, cleanup, and a complete mutation audit. Personal configuration and credentials are not inherited. Any explicitly approved authentication variable must contain a dedicated evaluation credential, and its value is redacted from retained captures and printed diagnostics. The host runner does not rerun model-modified verification code; required command outcomes come from captured harness evidence. Codex applies either its native read-only or workspace-write sandbox, or the exact evaluator-owned permission profile used by the MCP Git-lifecycle case. That profile denies the host home and evidence root, disables network access, preserves staged agent and configuration trees as read-only, and grants writes only to the disposable workspace, its Git metadata, and the unique temporary directory; other system paths remain read-only. Junie receives a pinned executable plus unique JUNIE_HOME, HOME, cache, temporary, and event locations, and a successful run must produce one non-empty terminal result event. Its MCP case allows ordinary read-only commands, Git add and Git commit, and the same thirteen exact mcp-agent-ops operations; unmatched actions still require approval. This is capability routing rather than filesystem containment. Junie session-ledger events can prove the named custom agent started and finished, but they do not carry the adapter digest, so exact-definition attribution remains unverified and is never inferred from the task prompt.

The prepared-snapshot cache, copy-on-write workspaces, transient-tree pruning, cleanup, and local Codex and Junie execution paths are implemented. All seven current cases are ordinary local cases and are runnable through both harnesses. Selected cases currently execute serially. Bounded parallel case execution, the externally-contained tier for explicitly high-risk cases, read-only dependency mounts or copy-on-write delta enumeration, and warm-worker pooling remain follow-on components.

Model-visible context is allow-listed and recorded before invocation. Evaluation-only references, expected findings, Judge prompts, and calibration answers remain outside the evaluated workspace. Canonical Model Judge artifacts bind the selected case, run, harness, candidate output, and governed evidence by digest. Receipts classify executed, Judge-passed, security-contained, Judge calibration, and stale-by-digest independently. Local execution and a Judge pass do not imply security containment. The legacy verified field remains for receipt compatibility only.

## Verification

Before publishing changes to this bundle, run:

```bash
python3 scripts/validate-agent-skills.py skills
python3 scripts/validate-agent-skills.py adapters/codex/skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 scripts/run-agent-skill-evals.py --validate-catalogs
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
```
