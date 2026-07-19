---
name: github-issues-backlog
description: Route backlog creation, triage, lifecycle updates, recovery, and completion through GitHub issues. Use when applicable project guidance selects github-issues-backlog for the active scope or the user explicitly asks to create or manage GitHub issues as the project backlog.
metadata:
  category: development-practice
---

# GitHub Issues Backlog

Use GitHub issues as the authoritative backlog without creating duplicate repository backlog files.

## Inputs And Authority

- Resolve the target repository, issue or new-item intent, item type, requirements, acceptance criteria, dependencies, labels, and verification expectations.
- Use the configured repository and issue conventions. Ask when the target repository or required convention is missing.
- Create, edit, label, assign, close, reopen, or comment on issues only when the request or authorized workflow permits that external change.
- Require an available authenticated GitHub issue interface. Report BLOCKED when it is unavailable rather than falling back to local files.

## Operations

- Search open and recently closed issues for the same work before creating a new issue.
- Create one issue for one independently actionable outcome. Use issue links or task lists for related work when repository convention permits them.
- Preserve requirements, acceptance criteria, dependencies, verification expectations, and source evidence in the issue.
- Record claims or active ownership through the repository's configured labels, assignees, project fields, or comments.
- Link implementation branches and pull requests without treating their existence as completion.
- Close an issue only when its configured delivery evidence is satisfied. Record blocked or failed outcomes without misreporting them as complete.

## Boundaries

- GitHub issues are hosting-service records, not Git objects.
- Do not create repository backlog files as a shadow copy unless the user explicitly asks for an export.
- Do not expose sensitive findings, private data, credentials, or proprietary evidence in an issue whose visibility is not appropriate.
- Do not alter unrelated labels, milestones, assignments, project fields, or issue text.

## Result

Return the issue link, type, state, ownership, dependencies, delivery evidence, and next runnable action.
