# Synchronize Installed Skill Catalog After Provider Renames

Status: Running

Owner: Dev Orchestrator task 019fd919-a1d4-7471-b158-5068c1d7622d

Canonical Conversation: 019fd919-a1d4-7471-b158-5068c1d7622d

Root Agent Task: 019fd919-a1d4-7471-b158-5068c1d7622d

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/synchronize-installed-skill-catalog-after-provider-renames

Worktree: /Users/martinbechard/.codex/worktrees/75c3/dev-methodology

Phase: Installing and verifying the configured user-level methodology bundle

Type: Defect

Provider: file

Work Item ID: synchronize-installed-skill-catalog-after-provider-renames

Completion: direct-main

## Summary

Deploy the current methodology skill identities to the configured user-level installation, remove retired skill directories, refresh the installed catalog, and prove that installed definitions match the authoritative repository sources.

## Context

The repository contains the completed provider-family naming and responsibility changes, but the configured user-level installation remains on the earlier identities. The source checkout contains the current interface and provider skills, including `agent-claim-helper`, `agent-claim-helper-command`, `agent-claim-helper-mcp`, `create-work-item`, `create-work-item-file`, `manage-work-items`, `manage-work-items-file`, `coordinate-work-items`, `coordinate-codex-tasks`, `deliver-work-item`, and `manage-future-ideas`.

The corresponding files were absent from `${HOME}/.agents/skills` during live verification. That installation still contained retired definitions including `agent-claim-command`, `agent-claim-mcp`, `create-file-work-item`, `manage-file-work-items`, and `coordinate-codex-work-items`. As a result, repository guidance and the runtime-visible skill catalog do not describe the same dependency and dispatch model.

## Source Evidence

On 2026-08-06, while answering the user's request to verify whether the naming and responsibility recommendations had been applied, a direct comparison of `skills/*/SKILL.md` with `${HOME}/.agents/skills/*/SKILL.md` found the current repository identities missing from the installation and the retired identities still present. The user previously directed that detected incorrect behavior must always be logged instead of ignored.

## Requirements

- Use the repository installer and recorded core-skill delivery mode to replace the configured user-level methodology installation from authoritative current-main sources.
- Install every current skill and generated native-agent artifact owned by the methodology bundle, including all interface and provider identities introduced by the completed naming and responsibility work.
- Remove retired bundle-owned skill directories without deleting unrelated user-owned or other-bundle content.
- Update the installation ownership manifest and other installation metadata so they describe the installed bytes and selected delivery mode exactly.
- Refresh the runtime skill catalog after the filesystem installation succeeds.
- Reconcile partial or uncertain installation and catalog-refresh outcomes without reporting success from source state alone.
- Preserve the repository source and backlog state; installation is a distinct shared-runtime deployment operation.

## Acceptance Criteria

- The configured user-level skill root contains the current interface and provider skill identities named in this item.
- The installed bundle no longer exposes the retired identities `agent-claim-command`, `agent-claim-mcp`, `create-file-work-item`, `manage-file-work-items`, or `coordinate-codex-work-items`.
- Installed bundle-owned skill and native-agent bytes match the authoritative integrated source and generated artifacts byte for byte.
- The installation ownership manifest contains no orphaned retired paths and matches the installed files and selected core-skill delivery mode.
- A refreshed runtime catalog resolves the current identities and does not resolve the retired identities.
- A fresh runtime inventory agrees with repository `AGENTS.md`, `PROJECT.yaml`, role definitions, and the maintained skill catalog for the renamed families.

## Dependencies

None.

## Verification

- Run the installer dry run and inspect the exact replacement and retirement manifest.
- Acquire the configured `shared-install` resource claim before changing the user-level installation.
- Perform the approved replacement installation and compare installed file digests with current-main sources and generated artifacts.
- Validate the installation ownership manifest and selected core-skill delivery metadata.
- Refresh the runtime skill catalog and record its revision or equivalent immutable result.
- Inspect a fresh runtime skill inventory for every current and retired identity named in this item.
- Run focused installation, catalog, generated-artifact freshness, and stale-name tests.

## Open Questions

None.

## Notes

The completed source work remains valid. This defect concerns deployment parity between that source and the configured user-level runtime, not another rename or redesign of the skill families.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-06T22:01:45Z

Coordinator: Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Normalized Objective: Replace the configured user-level methodology installation from authoritative current-main sources, retire only bundle-owned obsolete skill identities, refresh the runtime catalog, and prove installed bytes, ownership metadata, sizes, timestamps, and identities match the repository.

Launch Result: Not attempted.

Canonical Conversation: None.

Last Contact At: None.

Next Reconciliation At: 2026-08-06T22:16:45Z.

Intended Root Role: Dev Orchestrator.

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fd919-a1d4-7471-b158-5068c1d7622d

Evidence: The canonical root task remains active. It detected a main advance that changed a bundle-owned skill, invalidated the earlier installation snapshot, fast-forwarded the work-item branch to current main commit 851587a3ff4c668500b1adfabffd9617880c48d2, and owns the bounded replacement installation, catalog refresh, fresh independent gates, direct-main observation, and provider closure sequence.

Observed At: 2026-08-06T22:14:36Z

Started At: 2026-08-06T22:04:20Z

Deadline or Expires At: 2026-08-06T23:14:36Z

Next Action: Commit this evidence refresh, hand off the update claims, reacquire outcome ownership, replace the user-level bundle from current main under a new shared-install claim, and restart the independent review and verification gates against the new immutable snapshot.

Next Reconciliation At: 2026-08-06T22:29:36Z
