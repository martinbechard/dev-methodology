---
name: file-based-backlog
description: Route backlog creation, inventory, lifecycle, recovery, and archival through repository files. Use when applicable project guidance selects file-based-backlog for the active scope or the user explicitly asks to record or manage work in the repository backlog.
metadata:
  category: development-practice
---

# File-Based Backlog

Use repository files as the authoritative work queue and durable lifecycle record.

## Selection

- Apply this skill only when applicable project guidance or the request selects file-based-backlog.
- When no backlog process is selected and durable backlog work is required, ask the user rather than defaulting to repository files.
- Use the repository's configured backlog location. When no location is configured, apply the standard typed folders defined by create-backlog and manage-backlog.

## Operations

- Apply create-backlog when converting a request or finding into a new typed item.
- Apply manage-backlog when inventorying, claiming, resuming, blocking, completing, failing, or archiving items.
- Acquire the required file claim before creating or changing backlog artifacts.
- Preserve source references, acceptance criteria, dependencies, verification expectations, delivery evidence, and lifecycle state in the repository.
- Keep implementation commits separate from unrelated backlog maintenance.

## Boundaries

- Do not create or update hosting-service issues as a duplicate queue.
- Do not infer completion from a commit, stopped process, or pull-request link without the delivery evidence required by the item.
- Do not create a new item when an existing active item represents the same work.

## Result

Return the item path, type, state, ownership, dependencies, delivery evidence, and next runnable action.
