# AGENTS-PLAN

## Current Understanding

TODO: Summarize the project purpose, current development stage, and why agent and skill routing is needed.

## Authoritative Sources

TODO: List the source files, documentation files, procedures, package metadata, build configuration, and existing AGENTS.md files inspected for this plan.

## Project Scope And Boundaries

TODO: Identify the repository boundary, product or service boundary, private data boundary, and any sibling repositories that should not be mixed into this plan.

## Project Taxonomy

TODO: Classify the project family, primary runtime, application tiers, technology stacks, and documentation surfaces.

Use application tiers for separable technical guidance. For a web application, record front-end, API, static pages, database, background jobs, local tooling, and documentation tiers as applicable.

## Root AGENTS.md Routing Reference

TODO: Explain what the root AGENTS.md should tell agents before they work in this repository.

Include repository-wide rules, privacy constraints, build and test commands, documentation locations, and the project taxonomy terms that the skills router should use.

## Role Agent Set

TODO: Define the project roles that should exist for this repository.

For each role, record:

- Role name.
- Purpose.
- Work it owns.
- Work it must hand off.
- Skills it normally loads.
- Validation it must run before completion.

## Skill Loadouts

TODO: Map each technology, tier, or recurring workflow to the skills that should be loaded.

Keep skills reusable and portable. Keep project-specific rules in AGENTS.md or in this AGENTS-PLAN.md file until they are promoted into a reusable skill.

## Folder Routing

TODO: Map repository folders to roles, tiers, skills, and verification commands.

For each folder or path pattern, record:

- Folder or pattern.
- Tier or workflow.
- Primary role.
- Required skills.
- Source evidence.
- Verification commands.
- Whether a nested AGENTS-PLAN.md is needed.

## Nested AGENTS-PLAN Files

TODO: List any subfolders that need their own AGENTS-PLAN.md because they contain a distinct technology, runtime, data boundary, or verification workflow.

Create a nested plan only when the local guidance is specific enough that loading it with every root-level task would be distracting.

## Documentation And File Contracts

TODO: Explain which durable files agents should consult or maintain, and why each file exists.

Include AGENTS.md, AGENTS-PLAN.md, README.md, design documents, docs/wiki pages, procedures, backlog files, test plans, and generated artifacts when they exist.

## Validation Plan

TODO: Define how this project validates agent setup.

Include:

- Commands that confirm syntax, build, tests, lint, docs, and wiki checks.
- How to verify that each role loads the expected skills.
- How to verify that private or proprietary examples remain inside the target repository.
- How to verify that customer-shareable examples stay fictitious.

## Customer-Safe Example Shape

TODO: If this project needs customer-facing examples, describe them with fictitious names, synthetic paths, and generic product behavior.

Do not copy private project names, customer names, internal workflows, private architecture, secrets, or non-public data into customer-safe examples.

## Proprietary Validation Notes

TODO: Keep project-specific validation observations here when this AGENTS-PLAN.md lives inside a private project repository.

Do not move these notes into the distributable bundle unless they have been generalized and stripped of private context.

## Open Questions

TODO: List unknowns that affect routing, role boundaries, privacy handling, or verification.

## Maintenance Notes

TODO: Record how this AGENTS-PLAN.md should be kept aligned with AGENTS.md, skills, adapter metadata, README content, design documents, and project folder changes.
