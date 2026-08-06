# Synchronize Installed Skill Catalog After Provider Renames

Status: Completed

Owner: Dev Orchestrator task 019fd919-a1d4-7471-b158-5068c1d7622d (completed)

Canonical Conversation: 019fd919-a1d4-7471-b158-5068c1d7622d

Root Agent Task: 019fd919-a1d4-7471-b158-5068c1d7622d

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/synchronize-installed-skill-catalog-after-provider-renames

Worktree: /Users/martinbechard/.codex/worktrees/75c3/dev-methodology

Phase: Running -> Completed after verified direct-main delivery and terminal provider closure

Completed At: 2026-08-06T22:34:29Z

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/synchronize-installed-skill-catalog-after-provider-renames.md

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

## Historical Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Orchestrator task 019fd919-a1d4-7471-b158-5068c1d7622d

Evidence: Fresh post-refresh Dev Code Reviewer task installed_catalog_review_v2 and Dev Verifier task installed_catalog_verify_v2 are actively evaluating immutable installation evidence sourced from commit 9c2bd564f6cd1502617c45df373df74c4e13f7df. Current main advanced only on the unrelated excluded design/skill-groups/concurrent-tasking.md path; installed bundle source and generated-agent paths remain unchanged.

Observed At: 2026-08-06T22:26:52Z

Started At: 2026-08-06T22:04:20Z

Deadline or Expires At: 2026-08-06T23:26:52Z

Next Action: Commit this delegated-work evidence refresh, hand off the update claims, reacquire outcome ownership, evaluate the two terminal gate results, and proceed to direct-main observation only if both accept the unchanged immutable installation snapshot.

Next Reconciliation At: 2026-08-06T22:41:52Z

## Completion Evidence

- Completion Selector: direct-main.
- Delivery Disposition: READY.
- Accepted Source Commit: 9c2bd564f6cd1502617c45df373df74c4e13f7df.
- Integration Strategy: The accepted source commit was already represented on current main, so no topology-only merge was created.
- Integration Commit And Main Observation: main at f4d1a84e378029a58cbaec68e6d3cec6c7b8b25a. The accepted source commit is an ancestor. A scoped comparison found no later changes under skills, adapters, agents, generated, AGENTS.md, PROJECT.yaml, README.md, or scripts.
- Independent Review: ACCEPTED by fresh post-refresh Dev Code Reviewer task installed_catalog_review_v2. Open questions none and no material candidate risk.
- Independent Verification: VERIFIED by fresh post-refresh Dev Verifier task installed_catalog_verify_v2. The six directly implicated provider-family naming tests, fixture-aware stale inventory, generated documentation freshness, installer cleanup and ownership tests, installed byte comparison, manifest validation, and runtime catalog checks passed.
- Separate Baseline Defect: The older broad stale-name scanner does not account for deliberate negative fixtures. The parent Coordinator recorded distinct Work Item ID make-provider-naming-stale-scan-fixture-aware at commit f4d1a84e378029a58cbaec68e6d3cec6c7b8b25a. This installation-only item made no repository source correction.
- Installed Skill Evidence: Ownership manifest SHA-256 3f743e9554ab62a62147b035683c57036ae7457f7ca2688a702a1a639742c8d7, size 26969 bytes, updated at 2026-08-06T22:15:23.285910+00:00. All 139 owned skill artifacts, 427 files, and 1535527 bytes match authoritative source digests, bytes, sizes, and timestamps.
- Installed Native-Agent Evidence: Ownership manifest SHA-256 537e9c68dbf3b9906eac54abc2459e48d15dea804812aa78470852781bb4718b, size 6252 bytes, updated at 2026-08-06T22:15:24.112051+00:00. All 30 owned native-agent files and 229279 bytes match generated source digests, bytes, sizes, and timestamps. Core-skill delivery is by-reference and agrees with generation metadata.
- Catalog Refresh Evidence: Revision b8cc46bf7444de25526181a44126d42ce9924c780f5e3dcf48fb626b0b05c4b2 contains 147 unique runtime identities. Every current interface and provider identity named by this item resolves with no shadowing, and all five named retired identities are absent.
- Cleanup And Ownership Evidence: The dry run identified only obsolete manifest-owned identities. Replacement removed those owned identities, preserved unrelated unowned content, and left no retired path in the ownership manifest.
- Shared Installation Claims: First reconciliation acquisition event 910b9f1f-0714-4df2-a35c-80a2c486b78b and release event 6ccfe728-70c7-4500-b058-6580c53d50f6. Final current-main replacement acquisition event d5b5cf5f-39ff-4863-b191-bd51649c9765 and verified-stability release event 88423695-db38-4d73-b974-c3275fe11961.
- Terminal Provider Claims: Work Item ID update acquisition event 3fabbd60-84c9-4302-bf7a-cea158ecb7c9 and exact source-plus-destination path acquisition event 608cd435-0312-4544-a936-c58f7417311c. Release events are reported with the committed provider result.
- Unrelated Dirty Main Preservation: Before this terminal transaction, design/skill-groups/concurrent-tasking.md had worktree SHA-256 07daba30dcb343e9928a963b62f006a5673e33cfc6415a29e7811b353af58b1f, index blob da5693414ac0847b7fddce897d53a765811b859d, and binary-diff SHA-256 646413b5e61ea44081cdeb60d24a891dfeef094e1ed1da9772a33fc3ff7a95b7. It remained excluded from claims, staging, edits, tests, and this provider commit.
- Verification Checkout: The work-item checkout was clean at observed main f4d1a84e378029a58cbaec68e6d3cec6c7b8b25a before terminal provider mutation.
- Remote Publication: Not required by the configured direct-main completion contract.
- Terminal Provider Commit: This exact status-and-archive transaction; its immutable commit is reported in the provider result after commit.
- Archive Path: backlog/completed-backlog/defects/synchronize-installed-skill-catalog-after-provider-renames.md.
