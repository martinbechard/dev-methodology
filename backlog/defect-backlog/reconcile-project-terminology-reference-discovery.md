# Reconcile Project Terminology Reference Discovery

Status: Starting

Type: Defect

Provider: file

Work Item ID: reconcile-project-terminology-reference-discovery

Completion: main-branch

## Summary

Restore configured mcp-agent-ops discovery and publication verification for the direct project-root `terminology.md` reference.

## Context

The configured reference provider successfully refreshes revision `89b418948b1bcfdc656fce1c2e50e8bc1fcc12126b6b1c21627e97d7d0e9c13c`, but its published names omit the tracked direct project-root `terminology.md`. A revision-matched `reference_load` therefore returns `reference_not_found`. This is a valid ABSENT result for ordinary terminology application, but it cannot satisfy post-mutation publication verification because no returned digest can match the changed target.

The preserved Work Item `replace-evaluation-oracle-terminology-with-judge` is Blocked with accepted candidate `6f8e617c2fdb36bac1dbb46a77410e384505437d` until this capability is restored.

## Requirements

- Reproduce refresh and revision-matched load from the configured dev-methodology project context.
- Diagnose the configured project-root discovery path before changing configuration or implementation.
- Make the smallest authoritative correction in Project Configurator source, project configuration, or mcp-agent-ops, according to the diagnosed owner.
- Preserve configured user-reference roots, path-free scope labels, immutable snapshot behavior, allowed workspace boundaries, and `reference_not_found` semantics for genuinely absent references.
- Do not use filesystem fallback or arbitrary user-home search as publication proof.
- If mcp-agent-ops changes, verify and publish/install the supported package through its own repository and release workflow before project-runtime verification.
- Preserve the Oracle terminology candidate and do not reimplement its source changes.

## Acceptance Criteria

- `reference_refresh` in a fresh configured dev-methodology runtime publishes a revision whose names include `terminology.md`.
- Revision-matched `reference_load` returns the direct project scope and the validated SHA-256 digest of the tracked target without exposing a physical path.
- Genuine ABSENT behavior still returns only `reference_not_found` when neither configured project nor user scope contains the reference.
- Workspace-root, aggregation, ordering, deduplication, skipped-root, immutable-snapshot, and path-redaction contracts remain intact.
- Focused Project Configurator and mcp-agent-ops reference discovery/publication tests pass.
- Fresh independent review and verification accept the correction and installed-runtime evidence.

## Dependencies

None.

## Verification

- Run focused reference refresh/load tests at the owning source boundary.
- Verify the configured project context and fresh-runtime catalog revision after any required publication/install/restart boundary.
- Confirm revision equality and target digest equality.
- Run applicable configuration rendering, typing, lint, package, and Git diff checks.
- Obtain independent source and runtime verification.

## Open Questions

None.

## Notes

- This is the finish-lane recovery item for `replace-evaluation-oracle-terminology-with-judge`.
- Ordinary terminology application may continue with ABSENT status; mutation publication cannot.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T13:54:14Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `7322557a0e5841b2a432a6fdb1db7dc80feabf33` on primary `main`.
- Priority: Mandatory finish-lane recovery for the preserved Blocked Oracle terminology candidate.
- Capacity: Replaces the slot released by `replace-evaluation-oracle-terminology-with-judge` entering Blocked. Active usage remains four of five.
- Overlap: Diagnose before mutation. Do not touch Oracle candidate paths, active Project Configurator receipt files, provider-terminology paths, Index alignment paths, or unrelated plan artifacts. Any mcp-agent-ops source work must use its repository's own provider, claims, review, release, and publication boundary.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: Work Item `start-terminology-reference-discovery-work-item`; event `c3b646c6-3be4-4ad1-8d90-e94fba536ddf`. Provider `start-terminology-reference-discovery-provider`; event `cc4ae5c5-884c-4f05-ba21-3dfafa5e8929`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T13:55:15Z.
- Codex Task ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Conversation ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Project Terminology Reference Discovery`.
- Initial Action: The visible root starts one Dev Orchestrator subagent for this authoritative Work Item and owns required Codex title and subagent messaging.
- Creation Outcome: Unique direct `threadId` and host success in the saved dev-methodology project, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: Work Item `adopt-terminology-reference-discovery-task`; event `18b6eb70-c19b-4dbe-99ac-37877f84e211`. Provider `adopt-terminology-reference-discovery-provider`; event `60cc1726-3cd2-4396-a536-74dc3d84d2c9`.
