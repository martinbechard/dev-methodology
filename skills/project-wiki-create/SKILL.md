---
name: project-wiki-create
description: Use when creating or substantially rewriting a project wiki methodology artifact from the development-methodology project-wiki-template asset, including wiki setup, authority order, base page contract, page subclassing, update workflow, automation, and verification guidance.
metadata:
  category: wiki-and-knowledge
---

# Project Wiki Create

Use this skill to create or substantially rewrite one project wiki methodology artifact. The artifact explains how a target repository's project wiki is structured, sourced, maintained, and verified.

## Template

Use skills/development-methodology/assets/templates/project-wiki-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one project wiki artifact that defines:

- Wiki root, required root pages, and ownership.
- Source authority order.
- Shared base page contract.
- Page subclassing rules.
- Diagram policy.
- Topic page and code page expectations.
- Local source link policy.
- Daily commit sync, update workflow, automation, and verification.
- Related methodology skills, procedures, and existing wiki pages.

Use project-wiki instead when the task is ordinary docs/wiki topic creation, topic maintenance, linting, OKF migration, raw ingest, or wiki operation work that does not need this methodology artifact.

Use documentation-bootstrap first when the repository has not chosen documentation roots or wiki ownership yet.

## Workflow

1. Inspect the target repository before writing. Read its README files, task-relevant procedures, docs, wiki root, raw folders, scripts, tests, backlog files, and current worktree status.
2. Identify whether the artifact describes existing behavior, intended behavior, or a known mix of both.
3. Copy the project wiki template into the target documentation location when a new artifact is needed.
4. Replace each TODO with the current source-backed rule for that target repository.
5. Keep the shared page contract sections first.
6. Link project-relative files at the point where the prose depends on them.
7. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
8. Remove only sections that genuinely do not apply.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use project-wiki-review on the completed artifact.
2. Use documentation-page-verify with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists.
4. Run OKF validation when topic pages changed.
5. Search the artifact for unresolved TODO markers that are not intentional.
6. Confirm every source-backed claim links to its source or states Not yet identified.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
