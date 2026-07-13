---
name: code-project-wiki
description: Use when maintaining docs/wiki for a code repository, syncing recent commits, updating Related Code or Related Tests, or recording skipped wiki updates.
metadata:
  category: wiki-and-knowledge
---

# Code Project Wiki

Use this skill for code-aware project wiki maintenance. The project-wiki skill remains the wiki engine; this skill adds repository-specific synchronization rules around code, tests, commits, procedures, and documentation.

## Required Companion Skills

- Use project-wiki for setup, status, lint, page schema, and wiki operations.
- Use project-wiki-topic-write when editing durable topic pages.
- Use project-wiki-topic-verify before finishing topic page changes.
- Use project-wiki-query for wiki-backed project questions.
- Use project-wiki-research when new external or raw research must be captured before synthesis.

## Operating Model

The wiki is a synthesized navigation and understanding layer. Code and tests remain authoritative for actual behavior. Functional specifications, procedures, architecture, high-level designs, module designs, and backlog files supply intent and workflow context.

Daily or commit-range sync should inspect recent repository changes as source material, then update wiki pages only when project understanding changed.

Update the wiki when changes affect:

- User-visible behavior.
- Design intent.
- Code ownership.
- Runtime boundaries.
- Verification evidence.
- Procedures.
- Known defects.
- Open decisions.
- Documentation routes or source authority.

Record a skipped commit or skipped file group when no durable wiki update is needed.

## Commit Sync Workflow

1. Determine the commit range from the wiki maintenance log, a small wiki state file, or the user's requested range.
2. Save a raw scan artifact with commit ids, messages, changed files, and initial classification when the project has a raw workflow.
3. Classify changed files as functional document, technical document, source code, test, configuration, migration, procedure, backlog, wiki page, generated artifact, or unrelated.
4. Read changed source files, tests, functional documents, technical documents, procedures, and backlog files before editing wiki pages.
5. Treat commit messages as discovery hints, not sufficient authority.
6. Use project-wiki suggestions or repository search to map changed files to likely wiki pages.
7. Update existing pages before creating new pages.
8. Create a new durable page only when the changed concept can recur or change independently.
9. Update Related Code and Related Tests when source ownership or verification changed.
10. Record open questions instead of guessing when code and documents disagree.
11. Run leaf-linking, wiki lint, and topic verification before completion.
12. Record the processed commit range, changed wiki pages, skipped commits, and verification results.

## Related Code And Tests Upkeep

Related Code should point to project-relative files, folders, scripts, configuration, migrations, or generated-artifact sources that directly support the page's claims.

Related Tests should point to project-relative unit, integration, end-to-end, smoke, lint, validation, or manual verification evidence. Use Not yet identified only after checking likely test roots and project metadata.

When a code change moves ownership, changes a test path, or adds missing verification, update the affected wiki pages in the same coherent commit as the source or documentation change when possible.

## Local Source Links

A local source link inside docs/wiki may help navigation in some repositories. It is a local convenience, not a portable citation.

If a project uses a local source link:

- Record the link path in wiki maintenance guidance.
- Add the linked path to git ignore rules so it is not tracked.
- Keep wiki page citations project-relative wherever possible.

## Verification

Before finishing:

1. Run project wiki status.
2. Run leaf-linking after creating or updating durable leaf pages.
3. Run project wiki lint.
4. Run project-wiki-topic-verify on changed durable topic pages.
5. Run OKF validation when the project uses OKF-compatible pages.
6. Recheck raw queues when the maintenance task included raw fragments or processed moves.
7. Report changed pages, skipped commits or file groups, verification commands, and unresolved questions.
