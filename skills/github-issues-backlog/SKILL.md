---
name: github-issues-backlog
description: Compatibility route for existing guidance that still selects github-issues-backlog. Dispatch creation to create-github-work-item and every inventory or lifecycle operation to manage-github-work-items without creating a shadow file queue.
metadata:
  category: development-practice
---

# GitHub Issues Backlog

This package is a transition route for current generated and configured callers that still name github-issues-backlog. The separately approved selector and role migration will move those callers to create-github-work-item for creation and manage-github-work-items for inventory, ownership, lifecycle, recovery, and terminal updates.

## Routing

- Load create-github-work-item when the requested operation may create one durable GitHub issue. That skill owns duplicate detection and creation.
- Load manage-github-work-items for lookup, inventory, selection, ownership, lifecycle, recovery, delivery evidence, reconciliation, close, or reopen operations.
- Load both only when one explicit request genuinely contains creation followed by management. Preserve the created or matched issue identity across the handoff.
- Return the selected skill's observed provider result. Do not reproduce its procedure or mutate GitHub independently in this compatibility package.

## Boundaries

- Use this route while applicable generated or configured guidance still selects github-issues-backlog, or when an explicit request names this legacy identifier. Do not claim that selector or role migration is complete until its separately governed sources have changed.
- GitHub issues remain the sole durable authority. Never create a repository backlog file, cached issue mirror, or fallback queue.
- Return BLOCKED when the authenticated GitHub provider interface, repository authority, required capability, or mutation permission is unavailable.
- A GitHub issue is the work item. A pull request is only a delivery reference, and publication alone never completes the issue.

## Result

Return the canonical replacement skill used, repository, issue number and URL, observed lifecycle state, ownership, dependencies, delivery evidence, and next action.
