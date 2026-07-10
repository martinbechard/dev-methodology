---
name: create-agents-plan
description: Use when creating or substantially rewriting an AGENTS-PLAN.yaml project agent and skill setup plan from the development-methodology agents-plan-template.yaml asset, including root and nested plan placement, role agents, folder technology loadouts, file contracts, proprietary validation notes, and customer-safe examples.
metadata:
  category: documentation-methodology
---

# Create Agents Plan

Use this skill to create or substantially rewrite an AGENTS-PLAN.yaml artifact. The artifact explains how a project should organize role agents, folder technology loadouts, AGENTS.md operational guidance, nested guidance, and validation evidence.

## Template

Use skills/development-methodology/assets/templates/agents-plan-template.yaml as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one root AGENTS-PLAN.yaml when the project needs a reviewable setup plan for agents and skills.

Create nested AGENTS-PLAN.yaml files only when a subfolder has distinct technology, runtime ownership, data boundaries, verification commands, or agent loadouts that would distract from root-level routing.

Create or update AGENTS-PLAN.yaml before writing AGENTS.md guidance. AGENTS-PLAN.yaml is the setup and validation artifact that explains what AGENTS.md should contain, why the roles and skills were chosen, and where project-specific evidence belongs. AGENTS.md is the operational reference that agents actually load after the plan has been validated. When the target uses Claude Code, create a thin CLAUDE.md beside each applicable AGENTS.md that imports the colocated guidance instead of duplicating it.

## Workflow

1. Inspect the target repository before writing. Read README files, AGENTS.md files, package metadata, build configuration, source roots, tests, docs, wiki pages, procedures, backlog files, and current worktree status.
2. Classify the project family, application tiers, technology stacks, documentation surfaces, runtime boundaries, data boundaries, and verification commands.
3. Identify the role agents needed for the project. Prefer shared reusable roles such as Development Orchestrator, Project Agent Setup Agent, Coding Agent, Code Review Agent, QA And Verification Agent, Documentation Writer, Wiki Query Agent, and specialist reviewer roles only when the project evidence requires them.
4. Map each tier, technology, folder, or workflow to the reusable skills it needs.
5. As Project Agent Setup, use detect-technology-skills and its generated registry once for representative folder scopes. Review source paths, owning manifests, configuration, and build evidence.
6. Record deterministic technology_skill_loadouts and folder bindings, including source evidence, missing required skills, exclusive conflicts, and explicit no-variant results.
7. Decide whether the root AGENTS-PLAN.yaml is sufficient or whether one or more subfolders need nested AGENTS-PLAN.yaml files.
8. Copy the template into each required location and replace every TODO with source-backed project content.
9. Keep proprietary project validation notes inside the target project repository. Do not copy private project names, internal implementation details, customer data, secrets, or non-public workflows into distributable examples.
10. Use fictitious names, synthetic paths, and generic behavior for customer-safe examples.
11. After the plan is validated, run scripts/render-agents-technology-skills.py and create or update root and nested AGENTS.md files with unconditional folder skill-loading instructions.
12. When Claude Code is used, create thin CLAUDE.md bridge files that import the colocated AGENTS.md without copying its rules.
13. Say Not yet identified for related sources, tests, commands, or roles that do not exist yet.
14. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use documentation-page-verifier on every created or materially rewritten AGENTS-PLAN.yaml file.
2. Search each AGENTS-PLAN.yaml for unresolved TODO markers that are not intentional.
3. Confirm every role, skill loadout, folder route, validation command, and file contract has source evidence or an open question.
4. Run setup-time detection for representative folders in every declared tier. Confirm each result matches the planned loadout and every required skill is available.
5. Confirm AGENTS.md contains unconditional folder skill-loading instructions, does not tell ordinary agents to rerun detection, and matches AGENTS-PLAN.yaml.
6. Confirm root and nested AGENTS-PLAN.yaml files do not duplicate broad guidance that belongs in root AGENTS.md.
7. Confirm every planned AGENTS.md exists and matches the validated routing plan.
8. When Claude Code is used, confirm every applicable AGENTS.md has a thin colocated CLAUDE.md import and that no guidance is duplicated between them.
9. Confirm customer-shareable examples are fictitious and proprietary examples remain only inside their target repositories.
10. Run project wiki status and lint when docs/wiki exists and the plan references wiki pages.
11. Run the target project build when code, imports, generated artifacts, or project metadata changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
