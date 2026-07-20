---
name: manage-backlog
description: Migration-only bridge from the retired manage-backlog identifier to manage-file-work-items. Use only when an existing governed caller still names manage-backlog during the bounded cross-bundle migration.
metadata:
  category: development-practice
---

# Manage Backlog Migration Bridge

manage-backlog is retired as an independent behavior owner. Load and apply [manage-file-work-items](../manage-file-work-items/SKILL.md) for every file-provider inventory, lifecycle, recovery, completion, failure, or archive request. This bridge supplies no management or transition procedure of its own.

Do not add new callers. Existing PROJECT.yaml files and generated guidance must migrate to provider file plus manage-file-work-items. Remove this bridge after the separately governed caller migration is complete and generator freshness succeeds without the legacy identifier.
