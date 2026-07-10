---
name: create-functional-spec
description: Use when creating or substantially rewriting a functional specification artifact from the development-methodology functional-spec-template asset, including actors, entry points, workflows, states, edge cases, acceptance behavior, and verification evidence.
metadata:
  category: artifact-creation
---

# Create Functional Specification

Use this skill to create or substantially rewrite one functional specification artifact. The artifact describes observable behavior from the actor's point of view and links the code, tests, and source material that define the behavior.

## Template

Use skills/development-methodology/assets/templates/functional-spec-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one functional specification that defines:

- Parent workflow.
- Actors.
- Entry points.
- Scope.
- User-facing concepts.
- Workflows.
- Workflow diagram when useful.
- States and rules.
- Edge cases.
- Verification blocks.

Use project-wiki-topic-writer instead when the task is a durable wiki topic page that summarizes existing functional knowledge without owning the functional specification.

Use documentation-reverse-engineering when the user asks to derive a set of functional specifications from an existing codebase.

## Workflow

1. Inspect the target repository before writing. Read product requirements, README files, agent instructions, procedures, routes, UI surfaces, commands, integrations, services, tests, backlog files, existing docs, wiki pages, and current worktree status.
2. Identify the actor goal, entry points, states, permissions, visible outcomes, and verification evidence.
3. Copy the functional specification template into the target documentation location when a new artifact is needed.
4. Replace each TODO with behavior grounded in authoritative source material.
5. Keep the shared page contract sections first.
6. Write workflow steps from the actor's point of view.
7. Include disabled states, error states, empty states, unavailable states, confirmation behavior, redirects, persistence outcomes, and important negative behavior when source evidence supports them.
8. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use review-functional-spec on the completed artifact.
2. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every workflow, state group, edge case, and acceptance claim has source evidence or a clearly recorded open question.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
