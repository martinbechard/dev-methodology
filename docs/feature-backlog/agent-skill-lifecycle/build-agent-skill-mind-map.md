# Build The Agent And Skill Mind Map

Status: Blocked

Type: Feature

## Summary

Build an interactive mind map for exploring canonical agents, fixed-role skills, detected technology skills, loading mechanisms, model profiles, harness adapters, activation evidence, and verification status.

## Context

The repository already generates role, skill, detection, hierarchy, and evaluation data, but the current views do not provide one explorable relationship model. The visualization must consume the stable detector and evidence schemas rather than encode relationships manually.

See the series [index](index.md).

## Requirements

- Generate one joined explorer data contract from canonical roles, skill catalog, technology detection registry, model profiles, adapters, evaluation cases, and verified receipts.
- Show fixed-role edges separately from detected-folder edges.
- Show Claude preload, Claude dynamic Skill-tool loading, Codex instruction-driven loading, optional availability overrides, and any verified app-server injection evidence.
- Provide filters for role, skill category, technology, capability, folder scope, harness, model profile, loading mode, declaration status, and verified behavior.
- Link agent nodes to canonical role files and generated adapters.
- Link skill nodes to SKILL.md and detection metadata.
- Link evidence status to evaluation cases and receipts.
- Make missing, unsupported, blocked, manual, declared, and verified states visually distinct.
- Keep the view usable with the current catalog size and keyboard accessible.
- Generate data; do not duplicate the catalog in hand-authored page code.

## Acceptance Criteria

- A user can start from an agent and identify every fixed and potentially detected skill.
- A user can start from a skill and identify roles, technologies, loading modes, and verification evidence.
- TypeScript, Spring Boot, Python, and FastAPI paths are distinguishable.
- Manual observations cannot appear as verified behavior.
- Filtering to one harness shows its actual preload or dynamic-loading semantics.
- All links resolve and all generated data freshness checks pass.
- The visualization works without network access.

## Dependencies

- replace-router-with-setup-detector
- verify-codex-skill-activation

## Verification

- Run generated-data freshness tests.
- Validate every displayed node and edge against canonical source data.
- Test keyboard navigation and representative filters.
- Inspect the page at desktop and narrow viewport widths.
- Perform an independent comparison against the support checklist and hierarchy.

## Notes

- Do not begin implementation against the obsolete routing registry.
- Wireframes and interaction sketches may be prepared before dependencies complete, but final data binding must use the detector and verified evidence schemas.
