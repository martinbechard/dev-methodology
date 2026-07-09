---
name: create-agents-plan
description: Use when creating or substantially rewriting an AGENTS-PLAN.yaml project agent and skill routing plan from the development-methodology agents-plan-template.yaml asset, including root and nested plan placement, role agents, skill loadouts, folder routing, file contracts, proprietary validation notes, and customer-safe examples.
---

# Create Agents Plan

Use this skill to create or substantially rewrite an AGENTS-PLAN.yaml artifact. The artifact explains how a project should organize role agents, skill loadouts, AGENTS.md routing references, nested guidance, and validation evidence.

## Template

Use skills/development-methodology/assets/templates/agents-plan-template.yaml as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one root AGENTS-PLAN.yaml when the project needs a reviewable setup plan for agents and skills.

Create nested AGENTS-PLAN.yaml files only when a subfolder has distinct technology, runtime ownership, data boundaries, verification commands, or agent loadouts that would distract from root-level routing.

Create or update AGENTS-PLAN.yaml before writing AGENTS.md routing guidance. AGENTS-PLAN.yaml is the setup and validation artifact that explains what AGENTS.md should contain, why the roles and skills were chosen, and where project-specific evidence belongs. AGENTS.md is the operational routing reference that agents actually load after the plan has been validated.

## Workflow

1. Inspect the target repository before writing. Read README files, AGENTS.md files, package metadata, build configuration, source roots, tests, docs, wiki pages, procedures, backlog files, and current worktree status.
2. Classify the project family, application tiers, technology stacks, documentation surfaces, runtime boundaries, data boundaries, and verification commands.
3. Identify the role agents needed for the project. Prefer shared reusable roles such as Development Orchestrator, Project Agent Setup Agent, Coding Agent, Code Review Agent, QA And Verification Agent, Documentation Architect, Wiki Query Agent, and specialist reviewer roles only when the project evidence requires them.
4. Map each tier, technology, folder, or workflow to the reusable skills it needs.
5. Decide whether the root AGENTS-PLAN.yaml is sufficient or whether one or more subfolders need nested AGENTS-PLAN.yaml files.
6. Copy the template into each required location and replace every TODO with source-backed project content.
7. Keep proprietary project validation notes inside the target project repository. Do not copy private project names, internal implementation details, customer data, secrets, or non-public workflows into distributable examples.
8. Use fictitious names, synthetic paths, and generic behavior for customer-safe examples.
9. Say Not yet identified for related sources, tests, commands, or roles that do not exist yet.
10. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use documentation-page-verifier on every created or materially rewritten AGENTS-PLAN.yaml file.
2. Search each AGENTS-PLAN.yaml for unresolved TODO markers that are not intentional.
3. Confirm every role, skill loadout, folder route, validation command, and file contract has source evidence or an open question.
4. Confirm root and nested AGENTS-PLAN.yaml files do not duplicate broad guidance that belongs in root AGENTS.md.
5. Confirm customer-shareable examples are fictitious and proprietary examples remain only inside their target repositories.
6. Run project wiki status and lint when docs/wiki exists and the plan references wiki pages.
7. Run the target project build when code, imports, generated artifacts, or project metadata changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
