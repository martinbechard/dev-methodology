---
name: create-project-configuration
description: Use when creating or substantially rewriting the single root PROJECT.yaml project configuration from the development-methodology project-template.yaml asset, including role agents, folder technology loadouts, nested AGENTS.md guidance, file contracts, proprietary validation notes, and customer-safe examples.
metadata:
  category: documentation-methodology
---

# Create Project Configuration

Use this skill to create or substantially rewrite a PROJECT.yaml artifact. The artifact explains how a project should organize role agents, folder technology loadouts, AGENTS.md operational guidance, nested guidance, and validation evidence.

## Template

Use skills/development-methodology/assets/templates/project-template.yaml as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create exactly one PROJECT.yaml at the project root when the project needs a reviewable configuration for agents and skills. The root file owns the configuration for the entire project, including every subfolder scope.

Do not create nested PROJECT.yaml files. When a subfolder has distinct technology, runtime ownership, data boundaries, verification commands, or agent loadouts, record that scope in the root PROJECT.yaml and create nested AGENTS.md guidance when normal work in that subtree needs a narrower operational contract.

Create or update PROJECT.yaml before writing AGENTS.md guidance. PROJECT.yaml is the setup and validation artifact that explains what AGENTS.md should contain, why the roles and skills were chosen, and where project-specific evidence belongs. AGENTS.md is the operational reference that the harness supplies after the configuration has been validated. When the target uses Claude Code, create a thin CLAUDE.md beside each applicable AGENTS.md that imports the colocated guidance instead of duplicating it.

## Workflow

1. Inspect the target repository before writing. Inspect existing AGENTS.md artifacts, then read README files, package metadata, build configuration, source roots, tests, docs, wiki pages, task-relevant procedures, backlog files, and current worktree status.
2. Classify the project family, application tiers, technology stacks, documentation surfaces, runtime boundaries, data boundaries, and verification commands.
3. Identify the role agents needed for the project. Prefer shared reusable roles such as Development Orchestrator, Project Agent Setup Agent, Coding Agent, Code Review Agent, QA And Verification Agent, Documentation Writer, Wiki Query Agent, and specialist reviewer roles only when the project evidence requires them.
4. Map each tier, technology, folder, or workflow to the reusable skills it needs.
5. As Project Agent Setup, use detect-technology-skills and its generated registry once for representative folder scopes. Review source paths, owning manifests, configuration, and build evidence.
6. Record deterministic technology_skill_loadouts and folder bindings, including source evidence, missing required skills, exclusive conflicts, and explicit no-variant results.
7. Decide which subfolders need nested AGENTS.md guidance and record every decision in the root PROJECT.yaml.
8. Record the repository-global agent coordination contract: atomic claim registry, optimistic clean-primary selection, isolated worktree policy, overlap blocking, recovery, release, and completion evidence.
9. Copy the template once to the project root and replace every TODO with source-backed project content.
10. Keep proprietary project validation notes inside the target project repository. Do not copy private project names, internal implementation details, customer data, secrets, or non-public workflows into distributable examples.
11. Use fictitious names, synthetic paths, and generic behavior for customer-safe examples.
12. After the configuration is validated, run scripts/render-agents-technology-skills.py with PROJECT.yaml and create or update root and nested AGENTS.md files with unconditional folder skill-loading instructions and the concise agent-claim trigger.
13. When Claude Code is used, create thin CLAUDE.md bridge files that import the colocated AGENTS.md without copying its rules.
14. Say Not yet identified for related sources, tests, commands, or roles that do not exist yet.
15. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use documentation-page-verify on the created or materially rewritten root PROJECT.yaml file.
2. Search PROJECT.yaml for unresolved TODO markers that are not intentional.
3. Confirm every role, skill loadout, folder route, validation command, and file contract has source evidence or an open question.
4. Run setup-time detection for representative folders in every declared tier. Confirm each result matches the planned loadout and every required skill is available.
5. Confirm AGENTS.md contains unconditional folder skill-loading instructions, does not tell ordinary agents to rerun detection, and matches PROJECT.yaml.
6. Confirm AGENTS.md tells every modifying agent to use agent-claim and that PROJECT.yaml records a repository-global registry plus primary, isolation, overlap, recovery, release, and completion rules.
7. Confirm the project contains exactly one PROJECT.yaml at its root and that it records every nested AGENTS.md placement decision.
8. Confirm every planned AGENTS.md exists and matches the validated routing plan.
9. When Claude Code is used, confirm every applicable AGENTS.md has a thin colocated CLAUDE.md import and that no guidance is duplicated between them.
10. Confirm customer-shareable examples are fictitious and proprietary examples remain only inside their target repositories.
11. Run project wiki status and lint when docs/wiki exists and the plan references wiki pages.
12. Run the target project build when code, imports, generated artifacts, or project metadata changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
