# Document External Terminal Cleanup

Status: Ready

Type: Feature

Provider: file

Work Item ID: document-external-terminal-cleanup

Completion: main-branch

## Summary

Align lifecycle documentation, Dev Orchestrator and Dev Backlog Coordinator role sources, generated adapters, and focused tests with the externally executed terminal-cleanup invariant.

## Context

The immediate `enforce-external-terminal-cleanup` item is deliberately limited to three skill sources. Durable design explanations, conceptual role responsibilities, generated projections, and their regression coverage need a separate delivery boundary.

## Source Evidence

On 2026-08-12, the user separately requested one Ready file-provider backlog item for later documentation, role, and generated-output updates. The user named `design/agents/work-item-dispatching-and-delivery.md`, `design/orchestrated-development-lifecycle.html`, the Dev Orchestrator and Dev Backlog Coordinator role sources, and mechanically required adapters and tests.

## Requirements

- Update `design/agents/work-item-dispatching-and-delivery.md` and `design/orchestrated-development-lifecycle.html` with the terminal evidence, Coordinator authorization, root Dispatcher cleanup, archive-last, returned-outcome, and capacity-reconciliation sequence.
- Update the Dev Orchestrator and Dev Backlog Coordinator conceptual role sources to preserve the same ownership boundary.
- Regenerate every supported adapter mechanically from the changed canonical role sources.
- Regenerate `design/generated/skill-definitions.js` after the immediate skill-source item lands, and verify it contains the delivered external-cleanup contract.
- Add or update only the focused tests and generated projections proven necessary by source ownership.
- Reconcile current skill text before writing so documentation and roles describe the delivered executable contract rather than a predicted version.
- Preserve the distinction between terminal delivery eligibility and completed external cleanup.

## Acceptance Criteria

- Documentation and role sources consistently prohibit Dev Orchestrator from removing its active worktree or checked-out branch and from archiving its active task.
- The documented sequence ends with root Dispatcher task archival and returned outcomes before Coordinator capacity reconciliation.
- Codex, Claude, Gemini, and Junie adapters exactly match the supported generator output for both roles.
- Focused regression tests cover role ownership, ordering, generated freshness, and terminology.
- Fresh independent documentation, role-definition, generated-artifact, and verification gates accept the result.

## Dependencies

None.

## Verification

- Run supported conceptual-agent generation and exact source-to-adapter comparison.
- Run focused role, Codex task-control, work-item coordination, lifecycle-document, provenance, and bundle-content tests.
- Verify maintained-document links, navigation, provenance, and generated freshness.
- Run Git diff whitespace validation.
- Obtain fresh independent artifact review and verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml

### Allowed Dependent Artifacts

- generated/adapters/codex/agents/dev-orchestrator.toml
- generated/adapters/codex/agents/dev-backlog-coordinator.toml
- generated/adapters/claude/agents/dev-orchestrator.md
- generated/adapters/claude/agents/dev-backlog-coordinator.md
- generated/adapters/gemini/agents/dev-orchestrator.md
- generated/adapters/gemini/agents/dev-backlog-coordinator.md
- generated/adapters/junie/agents/dev-orchestrator.md
- generated/adapters/junie/agents/dev-backlog-coordinator.md
- design/agents/work-item-dispatching-and-delivery.md
- design/orchestrated-development-lifecycle.html
- design/generated/skill-definitions.js
- Mechanically required focused test files and generator-owned projections proven by repository discovery.

### Approval Resolution

Approved at creation. On 2026-08-12, the user explicitly requested later updates to the two named design documents, Dev Orchestrator and Dev Backlog Coordinator role sources, and mechanically required adapters and tests. This approval does not include additional governed skill or Agent definition sources.

## Notes

This Ready item is a distinct later delivery. Coordinate its exact design and role paths against the immediate skill item at mutation and integration boundaries; do not merge the two canonical executions.

The immediate source-only item intentionally leaves `design/generated/skill-definitions.js` stale because the user separated generated documentation updates into this later item. Treat the exact `build-skill-docs.py --check` delta caused only by those three delivered skill sources as accepted input to this item, not as evidence that the immediate item may mutate the projection.
