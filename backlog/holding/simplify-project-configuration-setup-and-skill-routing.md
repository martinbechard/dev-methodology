# Simplify Project Configuration Setup And Skill Routing

Status: Holding

Type: Feature

Provider: file

Provider Reference: backlog/holding/simplify-project-configuration-setup-and-skill-routing.md

Completion: direct-main

## Summary

Give Project Configurator a concise Basic or Advanced setup dialogue, use clear Persistence and Commit terminology, let the user confirm detected technologies, default core and technology skills to by-reference delivery, create only the selected empty documentation structure during setup, and document the dependency boundary between conceptual agents, core skills, PROJECT.yaml, AGENTS.md, technology skills, and persistence-specific workflow skills.

## Context

Project setup currently asks for provider and completion without defaults, supports only the hybrid specifications-and-wiki documentation mode, selects technology skills automatically, defaults generated core and folder technology guidance to inline content, and carries concurrency infrastructure without a persisted single-agent versus concurrent-tasking choice.

The desired setup is intentionally smaller. Basic setup hides choices that have safe defaults but displays each hidden decision as Set with its resolved value. Advanced setup exposes the project-dependent choices with defaults. Technology detection remains source-backed, but its detected candidates and evidence are shown to the user for confirmation. Setup creates the selected documentation folders only and does not perform source reverse engineering.

The skill architecture must remain layered. Conceptual agent definitions own only reusable technology-agnostic core skills. PROJECT.yaml records project selections. Generated agent definitions refer to their core skills. Root or nested AGENTS.md guidance refers to the selected folder technology skills. Technology skills provide the technology-specific tools, commands, and rules used to realize the generic workflows described by core skills. Provider-specific persistence skills are selected through project workflow configuration and must not become direct Dev Coder dependencies.

## Source Evidence

- On 2026-07-20 and 2026-07-21, the user refined the proposed setup canvases and directed creation of this draft work item.
- The user selected Basic as the setup default, Concurrent tasking as the user-facing concurrency term, Persistence instead of Provider, and Commit instead of Completion.
- The user required Basic setup to display hidden decisions as Set with their resolved value, ask whether to create the Wiki, show scraped technology detections for user selection, and default both core and technology skills to by-reference delivery.
- The user limited setup documentation work to creating empty Wiki or specification folders and explicitly excluded reverse engineering from setup.
- The user required the implementation and HTML documentation to explain the relationship between agent definitions, core skills, PROJECT.yaml, AGENTS.md, and technology skills, with no direct Dev Coder dependency on provider-specific skills.
- Current implementation anchors include skills/create-project-configuration/SKILL.md, skills/development-methodology/assets/templates/project-template.yaml, scripts/build-skill-docs.py, scripts/render-agents-technology-skills.py, agents/role-schema.yaml, and agents/roles/dev-activities/dev-coder.role.yaml.

## Creation Evidence

- Creation authority: explicit user request to create a draft work item implementing the refined setup contract.
- Creation time: 2026-07-21T04:07:00Z.
- Backlog claim: draft-project-configuration-setup-choices-019f8130.
- Claim acquisition event: 6caa0b9c-0632-47ed-b6f9-cec29295af25.
- Claim scope: repository-root backlog on the primary main worktree only.

## Draft State

This item remains in Holding while its exact governed definition scope and final selector schema are reviewed. It must not be dispatched as unattended Ready work until the applicable skill and conceptual-agent definition paths receive explicit scope-specific approval under repository policy.

## Requirements

### Setup Mode And Presentation

- Make Setup mode the first setup question with Basic as its default and Advanced as the alternative.
- Persist the selected setup mode in the root PROJECT.yaml so later configuration runs preserve the project-owned choice.
- In Basic mode, do not render controls for decisions that are fixed by the Basic profile.
- For every hidden Basic decision, render a concise Set label and the resolved value so the user can inspect what the configurator chose.
- Never show a disabled or irrelevant Concurrent capacity control. Show it only after Advanced setup selects Concurrent tasking Yes.
- Keep repository-derived facts distinct from project-owned choices. Label confirmed detector results as detected and user-selected rather than presenting them as hidden defaults.

### Basic Setup Contract

- Set Concurrent tasking to No.
- Do not activate claim acquisition, worktree isolation, concurrent capacity, or merge coordination solely because the bundle contains those capabilities.
- Set Persistence to none.
- Set Commit to direct-main.
- Ask whether to create the Wiki, with Yes as the default.
- Run technology detection, show the detected technology candidates and their evidence, and require the user to confirm which candidates apply.
- Set core skill delivery to by reference.
- Set technology skill delivery to by reference.
- Display the hidden resolved values for Concurrent tasking, Persistence, Commit, core skill delivery, and technology skill delivery.

### Advanced Setup Contract

- Ask whether Concurrent tasking is enabled, with No as the default.
- Ask Concurrent capacity only when Concurrent tasking is Yes, with 3 as the default.
- Ask for Persistence, with file as the default. Supported choices remain none, file, GitHub, GitLab, Azure DevOps, and Jira unless a separately accepted provider contract changes them.
- Ask for Commit independently, with direct-main as the default. Supported choices remain direct-main and feature-branch unless a separately accepted commit contract changes them.
- Ask for Documentation using Wiki, specs, or both, with both as the default.
- Run technology detection, show every detected candidate with its evidence and conflicts, and let the user confirm the applicable set.
- Ask whether core skills and technology skills are inline or by reference. Keep both defaults by reference and present them together as one Skill loading question group.
- Preserve unsupported Persistence selections as explicit blocked choices rather than silently falling back.

### Persistence And Commit Terminology

- Use Persistence as the user-facing and canonical project-configuration term that selects none or the durable work-item storage provider.
- Keep none as an explicit Persistence option.
- Use Commit as the user-facing and canonical project-configuration term that selects direct-main or feature-branch delivery.
- Keep Persistence and Commit independent.
- Provide deterministic migration and compatibility handling for existing workflow_selection.provider and workflow_selection.completion values without silently changing recorded project intent.
- Do not expose folder overrides during ordinary Basic or Advanced installation. Preserve existing compatible override behavior only as an advanced hand-edited configuration capability if it remains necessary.

### Documentation Setup Boundary

- Support exactly the installation choices Wiki, specs, and both for documentation structure.
- Basic setup asks only whether to create the Wiki and does not introduce a specifications question.
- Create only the selected empty folder structure and repository-required placeholders.
- Do not inspect the project to generate source-derived module designs, high-level designs, architecture, functional specifications, or Wiki synthesis during setup.
- Do not invoke documentation reverse engineering as part of Project Configurator setup.
- Keep reverse engineering as a later explicit workflow that consumes the accepted configuration and selected documentation roots.
- Do not expose independent review as an installation choice. Review requirements remain owned by the later workflow that performs the work.

### Agent, Core Skill, Guidance, And Technology Skill Link

- Define conceptual agent definitions as owners of required and conditional technology-agnostic core skill identifiers only.
- Prohibit technology-specific skill identifiers in conceptual agent definition skill lists.
- Keep core skills generic. Their workflows refer to technology-neutral capabilities and tool purposes rather than specific language, framework, database, test runner, or provider implementations.
- Generate native agent definitions with references to their selected core skills when by-reference delivery is selected. Do not copy the complete core skill bodies into those definitions in the default setup.
- Record selected conceptual agents, core skill delivery, detected and user-confirmed technologies, technology skill delivery, Persistence, Commit, documentation choice, and Concurrent tasking in PROJECT.yaml.
- Render root and nested AGENTS.md guidance from the accepted PROJECT.yaml. Under by-reference delivery, name the applicable technology skills for each folder without copying their complete definitions.
- Use the selected technology skills to supply the concrete technology-specific tools, commands, conventions, review criteria, and verification rules needed by the generic core workflows for the matching folder.
- Ensure ordinary coding, review, diagnosis, and verification agents consume the applicable AGENTS.md technology-skill references and do not rerun setup-time detection.
- Keep persistence-specific create and manage skills behind the Persistence selection and its owning workflow router or backlog role.
- Prohibit direct dependencies from Dev Coder to create-file-work-item, manage-file-work-items, create-github-work-item, manage-github-work-items, create-gitlab-work-item, manage-gitlab-work-items, Azure DevOps placeholders, Jira placeholders, or later provider-specific equivalents.
- Let Dev Coder depend only on its generic implementation and delivery core skills. Pass normalized work and persistence evidence through the orchestrator or backlog owner rather than teaching Dev Coder every provider.
- Keep technology selection and persistence selection as separate mechanisms. Selecting a technology must not add persistence skills to an agent, and selecting Persistence must not add technology skills to a conceptual agent definition.

### Generated Guidance And Compatibility

- Replace the current inline-by-default setup output with by-reference defaults for both core and technology skill delivery.
- Retain explicit inline as an Advanced option for runtimes or projects that deliberately want self-contained generated instructions.
- Preserve fixed versus conditional core skill semantics when delivery changes from inline to by reference.
- Preserve root and nested AGENTS.md precedence and thin Claude bridge behavior.
- Preserve existing valid PROJECT.yaml intent during migration and report unsupported or conflicting legacy values with exact paths and remediation.
- Remove stale user-facing Provider, Completion, inline-by-default, automatic-technology-selection, and setup-time-reverse-engineering wording from maintained examples and generated guidance.

### HTML And Entry Documentation

- Update design/skills-modularization.html to own the complete agent definition to core skill to PROJECT.yaml to AGENTS.md to technology skill relationship, including by-reference defaults and the prohibition on technology skills in conceptual agent definitions.
- Update design/agent-and-skill-definitions.html so its diagram and explanatory text distinguish core agent-skill relationships from setup-selected folder technology skills and do not imply provider-specific Dev Coder dependencies.
- Update design/agentic-configuration.html to show how PROJECT.yaml selections render into root and nested AGENTS.md references across supported harnesses.
- Update design/orchestrated-development-lifecycle.html so project setup creates configuration and empty documentation structure without running reverse engineering, and later workflows consume the accepted setup.
- Update design/generic-agent-definitions-source.html when generated core-skill reference behavior or adapter examples change.
- Update README.md because the public setup flow, configuration choices, and default skill-delivery behavior change.
- Regenerate only source-owned generated documentation data and native adapter mirrors supported by the approved canonical source categories.

### Tests And Evaluation

- Add focused schema and renderer tests for Basic and Advanced setup decisions, defaults, hidden Set values, conditional Concurrent capacity, Persistence, Commit, documentation structure, and by-reference skill delivery.
- Add tests proving Basic output contains no Concurrent tasking or capacity control while still reporting Concurrent tasking Set to No.
- Add tests proving Basic asks for Wiki and technology confirmation but does not ask for specifications, Persistence, Commit, or skill delivery.
- Add tests proving Advanced shows the expected grouped questions and reveals Concurrent capacity only after Concurrent tasking Yes.
- Add an invariant test that conceptual agent definitions contain no technology-specific skills.
- Add an invariant test that Dev Coder contains no provider-specific persistence create or manage skills.
- Add generated-adapter tests proving by-reference core skills remain fixed or conditional as declared without copied skill bodies.
- Add AGENTS.md renderer tests proving by-reference technology skills are routed at the correct folder scope without copied skill bodies.
- Add Project Configurator evaluation scenarios for Basic setup and Advanced setup with multiple detected technologies, rejected candidates, user selection, Wiki-only folder creation, specifications-only folder creation, and both.
- Update bundle-content and generated-freshness assertions for the accepted schema, wording, documentation, and adapter behavior.

## Acceptance Criteria

- A new project can complete Basic setup after the initial mode question, the Wiki question, and technology confirmation; every other Basic decision is displayed as Set with its resolved value rather than shown as a control.
- Basic setup never shows Concurrent capacity and does not activate claim or worktree behavior for ordinary single-agent work.
- Advanced setup exposes Concurrent tasking, Persistence, Commit, Documentation, technology confirmation, and Skill loading with the specified defaults and conditional behavior.
- Setup creates only the selected empty documentation folder structure and never runs source reverse engineering.
- Detection results are shown with evidence and the user's confirmed technology selection is persisted.
- Core and technology skills default to by-reference delivery in both setup modes, while Advanced can explicitly select inline delivery.
- Every conceptual agent definition lists only technology-agnostic core skills.
- Dev Coder has no direct provider-specific persistence skill dependency.
- Generated agent definitions refer to core skills, and applicable AGENTS.md guidance refers to folder technology skills, with PROJECT.yaml providing the reviewed link between them.
- Generic core workflows remain usable across stacks because folder technology skills provide their concrete tool and command bindings.
- Existing valid Provider and Completion configuration migrates deterministically to Persistence and Commit without losing project intent.
- The relevant HTML design pages and README consistently explain the implemented setup and skill-linking model.
- Focused tests, generated-output freshness checks, Project Configurator evaluations, applicable validators, Git diff validation, and independent review pass.

## Dependencies

None.

## Proposed Governed Definition Scope

The likely governed source scope includes skills/create-project-configuration/SKILL.md and any other distributed skill definitions whose behavior must change after source inspection. Conceptual agent definitions should change only if live validation finds technology or persistence-provider dependencies that violate the accepted boundary. Before implementation, record the exact governed skill and conceptual-agent definition paths and run the required pre-mutation approval checks with explicit scope-specific user approval.

Supported generated mirrors, templates, renderer code, tests, evaluation fixtures, README.md, and design HTML are included only when owned by an approved canonical source change or when they are ordinary non-governed implementation and documentation surfaces.

## Verification

- Validate the final PROJECT.yaml schema and both Basic and Advanced setup examples.
- Run focused Project Configurator, agent-generation, technology-detection, AGENTS.md renderer, bundle-content, and documentation tests.
- Run the exact governed-definition approval check before each approved skill or conceptual-agent definition mutation.
- Regenerate only supported mirrors and run their freshness checks.
- Verify all conceptual role skill lists against the technology detection registry.
- Verify Dev Coder dependencies against every current persistence-provider skill identifier.
- Verify Basic and Advanced question visibility and Set-value reporting through deterministic setup fixtures.
- Verify Wiki, specs, and both create only the selected empty directory structure and do not invoke reverse engineering.
- Review every changed HTML page against the accepted implementation and run applicable page validation.
- Run Git diff validation and obtain an independent review of the exact source, generated, test, and documentation changes.

## Notes

- Folder overrides are deliberately excluded from the ordinary setup dialogue because they are not needed to choose the project-wide defaults.
- Independent review is deliberately excluded from installation choices because it belongs to the later workflow being performed.
- This item does not authorize reverse engineering, provider implementation, or unrelated technology-skill creation.
- The setup canvases used during refinement are design aids and are not authoritative repository artifacts.
