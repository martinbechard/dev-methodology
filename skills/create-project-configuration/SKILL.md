---
name: create-project-configuration
description: Use when creating or substantially rewriting the single root PROJECT.yaml project configuration from the development-methodology project-template.yaml asset, including conceptual agent definitions, folder technology skillsets, nested AGENTS.md guidance, file contracts, proprietary validation notes, and customer-safe examples.
metadata:
  category: documentation-methodology
---

# Create Project Configuration

Use this skill to create or substantially rewrite a PROJECT.yaml artifact. The artifact explains how a project should organize conceptual agent definitions, folder technology skillsets, AGENTS.md operational guidance, nested guidance, and validation evidence.

## Template

Use skills/development-methodology/assets/templates/project-template.yaml as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create exactly one PROJECT.yaml at the project root when the project needs a reviewable configuration for agents and skills. The root file owns the configuration for the entire project, including every subfolder scope.

Do not create nested PROJECT.yaml files. When a subfolder has distinct technology, runtime ownership, data boundaries, verification commands, or agent skillsets, record that scope in the root PROJECT.yaml and create nested AGENTS.md guidance when normal work in that subtree needs a narrower operational contract.

Create or update PROJECT.yaml before writing AGENTS.md guidance. PROJECT.yaml is the setup and validation artifact that explains what AGENTS.md should contain, why the conceptual agent definitions and skills were chosen, and where project-specific evidence belongs. AGENTS.md is the operational reference that the harness supplies after the configuration has been validated. When the target uses Claude Code, create a thin CLAUDE.md beside each applicable AGENTS.md that imports the colocated guidance instead of duplicating it.

Treat PROJECT.yaml as an intermediate, reviewable intent log between repository inspection and generated operational guidance. A maintainer may edit it to correct a selected conceptual agent definition, folder skillset, route, or guidance placement. On the next setup run, Project Configurator must treat those edits as requested configuration intent, reconcile them with current repository evidence and bundle constraints, preserve valid corrections, and report a blocking conflict or open question instead of silently replacing an unsupported edit.

Generic repository-mutation behavior belongs to conceptual agent definitions and the agent-claim skill. Do not reproduce that procedure in PROJECT.yaml or AGENTS.md. Record a coordination_overrides mapping only when the target repository has source-backed nondefault claim-registry, branch, worktree, exclusive-resource, or integration requirements; omit it when the bundle defaults apply.

## Workflow

1. Inspect the target repository before writing. Inspect existing AGENTS.md artifacts, then read README files, package metadata, build configuration, source roots, tests, docs, wiki pages, task-relevant procedures, backlog files, and current worktree status.
2. Classify the project family, application tiers, technology stacks, documentation surfaces, runtime boundaries, data boundaries, and verification commands.
3. Identify the conceptual agent definitions needed for the project. Prefer shared reusable definitions such as Development Orchestrator, Project Configurator, Coding Agent, Code Review Agent, QA And Verification Agent, Documentation Writer, Wiki Query Agent, and specialist reviewers only when the project evidence requires them.
4. Map each tier, technology, folder, or workflow to the reusable skills it needs.
5. As Project Configurator, inspect the technology skills actually exposed by the target runtime, then use detect-technology-skills and its generated registry once for representative folder scopes. Review source paths, owning manifests, configuration, and build evidence.
6. Review each detector candidate for pertinence to the analyzed folder. Reject owning-manifest overreach when the folder's source, configuration, runner, or runtime responsibility belongs to another technology, and record the rejection evidence.
7. Record deterministic technology_skill_loadouts and folder bindings, including source evidence, runtime availability, rejected candidates, missing required skills, exclusive conflicts, and explicit no-variant results. For a scope with no pertinent specialized skill, record `NO_VARIANT` plus a general-model-training fallback; do not invent a skill or omit the scope. Keep a detected required-but-unavailable skill `BLOCKED`.
8. Decide which subfolders need nested AGENTS.md guidance and record every decision in the root PROJECT.yaml.
9. Verify that every selected conceptual agent definition declares repositoryMutation and that the installed or bundled native definition can load agent-claim whenever that policy is required or conditional. Treat a missing conceptual agent definition, skill, or command as BLOCKED instead of compensating with copied project instructions.
10. Record only source-backed project-specific coordination_overrides. Omit the mapping when the bundle defaults apply.
11. Copy the template once to the project root and replace every TODO with source-backed project content.
12. When an existing PROJECT.yaml contains maintainer edits, treat them as requested configuration intent. Reconcile each edit with current source evidence and bundle constraints, preserve valid corrections, and record a blocking conflict or open question instead of silently replacing an unsupported edit.
13. Keep proprietary project validation notes inside the target project repository. Do not copy private project names, internal implementation details, customer data, secrets, or non-public workflows into distributable examples.
14. Use fictitious names, synthetic paths, and generic behavior for customer-safe examples.
15. After the configuration is validated, run scripts/render-agents-technology-skills.py with PROJECT.yaml and create or update root and nested AGENTS.md files with unconditional folder skill-loading instructions.
16. When Claude Code is used, create thin CLAUDE.md bridge files that import the colocated AGENTS.md without copying its rules.
17. Say Not yet identified for related sources, tests, commands, or conceptual agent definitions that do not exist yet.
18. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use documentation-page-verify on the created or materially rewritten root PROJECT.yaml file.
2. Search PROJECT.yaml for unresolved TODO markers that are not intentional.
3. Confirm every conceptual agent definition, skillset, folder route, validation command, and file contract has source evidence or an open question.
4. Run setup-time detection for representative folders in every declared tier. Confirm each result matches the planned skillset, every selected skill is exposed by the target runtime, every required skill is available, and every no-variant scope explicitly falls back to general model training.
5. Confirm AGENTS.md contains unconditional folder skill-loading instructions or an explicit general-model-training fallback, does not tell ordinary agents to rerun detection, and matches PROJECT.yaml.
6. Confirm every selected conceptual agent definition's repositoryMutation declaration agrees with its definition-owned, conditional, or absent agent-claim skillset. Confirm the required conceptual definitions, skill, and atomic command are available to the target runtime, and confirm generic claim procedure text was not copied into PROJECT.yaml or AGENTS.md.
7. Confirm the project contains exactly one PROJECT.yaml at its root and that it records every nested AGENTS.md placement decision.
8. Confirm every planned AGENTS.md exists and matches the validated routing plan.
9. When Claude Code is used, confirm every applicable AGENTS.md has a thin colocated CLAUDE.md import and that no guidance is duplicated between them.
10. Confirm maintainer edits to PROJECT.yaml were preserved when valid or reported with the evidence and constraint that blocks them.
11. Confirm customer-shareable examples are fictitious and proprietary examples remain only inside their target repositories.
12. Run project wiki status and lint when docs/wiki exists and the plan references wiki pages.
13. Run the target project build when code, imports, generated artifacts, or project metadata changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
