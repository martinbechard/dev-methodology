---
name: create-backlog
description: Migration-only bridge from the retired create-backlog identifier to create-file-work-item. Use only when an existing governed caller still names create-backlog during the bounded cross-bundle migration.
metadata:
  category: development-practice
---

# Create Backlog Migration Bridge

create-backlog is retired as an independent behavior owner. Load and apply [create-file-work-item](../create-file-work-item/SKILL.md) for every file-provider creation request. This bridge supplies no creation, placement, claim, or provider-selection procedure of its own.

Do not add new callers. Existing PROJECT.yaml files and generated guidance must migrate to provider file plus create-file-work-item. Remove this bridge after the separately governed caller migration is complete and generator freshness succeeds without the legacy identifier.
