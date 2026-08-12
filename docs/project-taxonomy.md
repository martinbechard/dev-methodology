<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: a8efba1b-a0f1-4943-8354-9d71ffd17c7d
Created-UTC: 2026-08-12T15:26:35Z
Creating-Agent: Project Organiser
Runtime: Codex
Dispatched-Model: gpt-5.6-terra
Reasoning-Effort: medium
Task-ID: /root/add_archive_taxonomy_rule
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Project Taxonomy

This document is the repository placement authority for new, maintained files and directories.

## Conventions

- Use lowercase kebab-case filenames unless a category defines a fixed name or a tool requires another format.
- Keep established root filenames, such as README.md, PROJECT.yaml, AGENTS.md, and terminology.md.
- Use a YYYY-MM-DD date prefix for dated operational archive folders.
- Keep generated output separate from hand-maintained source. Change the generator or source for generated output.
- Follow an established adjacent test location when its source category has one. This taxonomy defines no repository-wide test-mirroring rule.

## Top-Level Folder Principles

- Repository-root authority files define repository purpose, configuration, agent guidance, and shared terminology.
- Product source directories contain portable skills, conceptual Agent definitions, and adapter source.
- Project-maintenance directories contain repository-specific skills, scripts, tests, documentation, and evaluation fixtures.
- Generated directories contain deterministic outputs. Do not hand-edit generated output.
- Operational directories contain backlog state, claims, linked worktrees, or other runtime state. Keep them separate from product source.
- Retained inactive operational evidence belongs in the dated .archive hierarchy. Temporary and cache directories do not contain durable evidence.

## Categories

### README.md

- Purpose: Human-facing bundle entry point, repository map, setup guidance, and verification reference.
- Signals: Repository-wide explanation for maintainers and users of the distributed bundle.
- Filename pattern: Fixed filename README.md.

### PROJECT.yaml

- Purpose: Authoritative project configuration for generated guidance, resource coordination, and technology-skill routing.
- Signals: Root configuration that records selected project policies and repository understanding.
- Filename pattern: Fixed filename PROJECT.yaml.

### AGENTS.md

- Purpose: Generated operational guidance for Agents that work in this repository.
- Signals: Root guidance derived from PROJECT.yaml and selected project skills.
- Filename pattern: Fixed filename AGENTS.md; generated output.

### terminology.md

- Purpose: Project terminology standard for maintained technical prose.
- Signals: Preferred-term definitions that apply to repository-authored language.
- Filename pattern: Fixed filename terminology.md.

### .agents/skills/

- Purpose: Repository-private skills used to maintain this repository.
- Signals: Maintenance guidance that must not become part of the distributed skill bundle.
- Filename pattern: One skill per lowercase-kebab-case directory with SKILL.md.

### skills/

- Purpose: Portable Agent Skills distributed to projects and supported harnesses.
- Signals: Customer-independent reusable skill sources, templates, references, and optional detection metadata.
- Filename pattern: One skill per lowercase-kebab-case directory with SKILL.md; detection.yaml only when setup-time detection applies.

### agents/

- Purpose: Customer-independent conceptual Agent schemas and definitions.
- Signals: Role, model-profile, and schema source used to generate harness-specific Agent configurations.
- Filename pattern: Lowercase-kebab-case or established schema filenames; preserve fixed filenames where present.

### adapters/

- Purpose: Runtime-specific source metadata and adapter-owned sources.
- Signals: Source material that maps conceptual bundle definitions to a supported Agent harness.
- Filename pattern: Runtime and artifact names follow the adapter contract.

### generated/

- Purpose: Deterministic generated artifacts, including native Agent configurations.
- Signals: Output recreated from canonical source by a repository generator.
- Filename pattern: Generator-owned; do not hand-edit.

### design/

- Purpose: Maintained explanations of the skill, Agent, configuration, and documentation models.
- Signals: Repository design documentation and supporting presentation data.
- Filename pattern: Descriptive lowercase-kebab-case Markdown or HTML filenames; generated content belongs in design/generated/.

### docs/

- Purpose: Repository operational documentation that is not the bundle entry point or a design page.
- Signals: Placement authorities, maintenance references, and other durable repository documentation.
- Filename pattern: Descriptive lowercase-kebab-case Markdown filenames; project-taxonomy.md is fixed for the placement authority.

### scripts/

- Purpose: Repository maintenance, installation, generation, validation, and regression tooling.
- Signals: Executable support for bundle maintenance and deterministic output production.
- Filename pattern: Descriptive lowercase-kebab-case Python filenames; related tests follow established script-local patterns.

### evals/

- Purpose: Evaluation suites, fixtures, and controlled sample projects.
- Signals: Inputs and expected outcomes used to assess Agent or methodology behavior.
- Filename pattern: Descriptive lowercase-kebab-case directories and files; preserve fixture-specific conventions.

### backlog/

- Purpose: Primary-worktree work-item queue, lifecycle records, user-action state, and completed outcomes.
- Signals: Typed planning and coordination records governed by the selected persistence workflow.
- Filename pattern: Provider-defined work-item filenames and established lifecycle directories.

### .archive/<YYYY-MM-DD>-<topic>/

- Purpose: Retained, inactive operational artifacts, including cleanup scripts, reports, inventories, and decision evidence.
- Signals: An artifact is no longer active source, generated output, backlog state, or live runtime state, but its retained evidence remains useful.
- Filename pattern: The folder name is a UTC or repository-relevant date in YYYY-MM-DD format, a hyphen, and a lowercase-kebab-case topic. Keep descriptive filenames inside the dated folder.

### .agent-ops/

- Purpose: Shared operational coordination state, including resource-claim records and journals.
- Signals: Runtime-managed state created or maintained by the configured coordination helper.
- Filename pattern: Helper-owned operational filenames; do not add product source here.

### .worktrees/

- Purpose: Ignored linked worktrees for isolated Agent work.
- Signals: Temporary operational checkouts rooted in the primary worktree.
- Filename pattern: Claim-owned worktree directories.

### .github/

- Purpose: GitHub repository automation and collaboration configuration.
- Signals: Hosting-platform workflows, templates, and metadata.
- Filename pattern: GitHub-defined filenames and directories.

### legacy_procedures/

- Purpose: Retained legacy repository procedures that are not current distributed skills.
- Signals: Historical procedure material kept separate from active source and current maintenance guidance.
- Filename pattern: Preserve existing descriptive filenames; do not place new current procedures here.

## Change Log

- 2026-08-12: Added the repository taxonomy and the dated .archive category for retained inactive operational artifacts.
