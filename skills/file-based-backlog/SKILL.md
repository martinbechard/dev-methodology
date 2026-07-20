---
name: file-based-backlog
description: Migration-only bridge from the retired file-based-backlog selector to create-file-work-item and manage-file-work-items. Use only when an existing governed caller still names file-based-backlog during the bounded cross-bundle migration.
metadata:
  category: development-practice
---

# File Based Backlog Migration Bridge

file-based-backlog is retired as an independent selector and behavior owner. For an already selected file provider, load create-file-work-item for creation and manage-file-work-items for inventory or lifecycle work. This bridge supplies no provider selection, routing, claim, creation, or management procedure of its own.

Do not add new callers or use this identifier as a PROJECT.yaml value. Migrate project intent to provider file and generated guidance to the matching canonical create or manage skill. Remove this bridge after the separately governed caller migration is complete and generator freshness succeeds without the legacy identifier.
