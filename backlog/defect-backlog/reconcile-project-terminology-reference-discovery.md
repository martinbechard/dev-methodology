# Reconcile Project Terminology Reference Discovery

Status: Ready

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
