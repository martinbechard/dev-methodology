# Execute Lifecycle Operations as Skills and Use Provider-Owned Work Item IDs

Status: Completed

Type: Feature

Priority: High

Provider: file

Work Item ID: execute-lifecycle-operations-as-skills-and-use-provider-owned-work-item-ids

Completion: direct-main

Owner: Unowned

## Summary

Execute bounded work-item lifecycle operations directly through provider-selected skills in the authorized Coordinator or Orchestrator context, without requiring a Dev Backlog Steward child for each atomic transition. Simplify the generic persistence contract to use one opaque Work Item ID whose representation, resolution, storage, and stable archival mapping are owned by the selected provider.

## Context

The current lifecycle workflow commonly delegates short deterministic transitions, such as Ready to Starting, Starting to Running, and Running to Completed, to a separate Dev Backlog Steward task. That extra execution context can lose or complicate the caller's authorization, writable-worktree access, command approvals, staged-state evidence, and atomic mutation sequence. The result has been avoidable handoffs, permission failures, commit races, expired settlement windows, and recovery work.

The generic persistence model also exposes Provider Reference and provider-path terminology. This conflates a backlog item's logical identity with a provider-specific storage location. In the file provider, moving an item from an active queue to an archive changes its path even though the logical item is unchanged. Remote providers have different identifiers and storage behavior that generic lifecycle logic should not parse.

The desired model keeps delivery and persistence as separate phases while allowing the same authorized root agent to execute each phase through the appropriate skill. The selected provider owns ID representation, lookup, concurrency protection, mutation, publication or commit behavior, terminal organization, and continued resolution after archival.

## Source Evidence

On 2026-08-05, the user directly requested a high-priority work item from the attached proposal titled "Execute Backlog Lifecycle Operations as Skills and Use Provider-Owned Work Item IDs." The proposal explicitly requires direct lifecycle-skill execution in the owning Coordinator or Orchestrator context, removal of mandatory Steward-child dispatch for atomic transactions, an opaque provider-owned Work Item ID, stable identity across archival, preserved claims, and continued separation between Commit delivery and backlog persistence.

## Requirements

- Define the generic Backlog Item contract around one opaque Work Item ID and remove Provider Reference as a generic input, output, schema field, prompt field, and example concept.
- Require generic lifecycle logic to pass Work Item ID without parsing provider-specific syntax or inferring paths, URLs, issue numbers, or keys.
- Define the provider interface for inventory, read, transition, reconcile, complete, fail, and report operations using Work Item ID.
- Make each provider own Work Item ID representation, uniqueness scope, resolution, storage, concurrency, mutation, publication, terminal organization, collision handling, and diagnostic location reporting.
- Ensure Work Item ID remains stable and resolvable across lifecycle transitions and active-to-terminal movement.
- Define and implement a stable file-provider identity that is not changed merely because the backing file moves between active and archive folders.
- Keep GitHub, GitLab, Jira, and Azure DevOps identifier interpretation inside their respective provider implementations.
- Direct an authorized Dev Backlog Coordinator to apply the selected work-item management skill itself for bounded Coordinator-owned lifecycle operations, including Starting reservations.
- Direct an authorized Dev Orchestrator to apply the selected work-item management skill itself for bounded Orchestrator-owned lifecycle operations, including Starting to Running and terminal completion after delivery is READY.
- Remove any requirement to create a Dev Backlog Steward child solely to execute one atomic lifecycle transaction.
- Retain a Dev Backlog Steward role only for work that benefits from independent backlog-wide context, such as inventory reconciliation, normalization, multi-item archival audits, provider-wide recovery, or sustained queue maintenance; retire the role if no such independent responsibility remains.
- Preserve explicit transition authority checks, provider-selected concurrency protection, exact mutation scope, provider-specific commit or publication evidence, and cleanup.
- Keep Commit delivery separate from lifecycle persistence: Commit must not mutate backlog lifecycle state, and completion may run only after Commit returns READY.
- Inventory current Provider Reference and provider-path uses, classify their purpose, migrate generic identity uses to Work Item ID, and retain provider locations only inside provider implementations or diagnostic evidence.
- Migrate existing active and archived records without changing their logical identity or making them undiscoverable.
- Update focused lifecycle tests, provider tests, agent evaluations, generated adapters, and design documentation to express the new execution and identity model.
- Reconcile overlapping requirements in the active object-oriented skill-group work-item series. Do not implement conflicting lifecycle or provider-identity contracts concurrently, and supersede obsolete requirements rather than layering both models.

## Acceptance Criteria

- Generic backlog operations accept Work Item ID and do not require Provider Reference.
- Generic lifecycle logic treats Work Item ID as opaque and contains no provider-specific identifier parsing.
- Every configured provider documents and implements how its Work Item IDs are represented, resolved, collision-checked, and kept stable.
- A file-backed work item retains the same Work Item ID before and after archival, and the file provider resolves it in both states.
- Remote-provider locations and identifiers remain confined to their respective provider implementations.
- An authorized Coordinator completes a bounded Coordinator-owned lifecycle transition directly through the selected management skill without creating a Steward child.
- An authorized Orchestrator completes Starting to Running directly through the selected management skill without creating a Steward child.
- An authorized Orchestrator completes terminal lifecycle persistence directly after Commit returns READY, without Commit itself changing lifecycle state.
- Claims and provider-specific concurrency controls protect only the resources required by the provider operation and remain separate from logical Work Item ID.
- Existing active and archived work items remain discoverable after migration.
- Focused tests prove direct skill execution, stable archival identity, provider-opaque generic logic, transition authority, and delivery-versus-persistence separation.
- Documentation and generated artifacts show WorkItemProvider implementations behind the generic work-item interface and no longer present provider storage locations as generic identity.
- The Dev Backlog Steward contract, if retained, contains no mandatory wrapper role for individual atomic lifecycle transactions.

## Dependencies

None. This item is independently actionable and high priority. It overlaps lifecycle and provider guidance in backlog/feature-backlog/apply-object-oriented-skill-group-design/align-codex-work-item-coordination-skill.md, backlog/feature-backlog/apply-object-oriented-skill-group-design/align-work-item-creation-provider-skills.md, and backlog/feature-backlog/apply-object-oriented-skill-group-design/split-backlog-blockage-and-dispatch-mode-skills.md; those overlaps require sequencing and supersession reconciliation, not completion dependencies.

## Verification

- Run focused contract tests for generic Work Item ID inputs and outputs, provider-owned resolution, stable file-provider identity across archival, and rejection of generic identifier parsing.
- Run focused lifecycle tests proving direct Coordinator and Orchestrator skill execution without Steward-child dispatch.
- Run focused tests proving Commit delivery never mutates lifecycle state and completion occurs only after a READY delivery disposition.
- Run focused tests for each changed provider implementation and its identifier-resolution boundary.
- Regenerate only supported adapters and documentation derived from changed canonical sources, then verify freshness.
- Validate each changed governed skill or conceptual agent definition through the configured validator.
- Run the smallest directly affected agent evaluation scenarios and documentation checks.
- Run git diff checks and verify that existing active and archived items remain resolvable after migration.

## Open Questions

- Which durable identifier representation and lookup mechanism best preserves existing file-backed item identity without requiring generic logic to understand paths?
- Which current Provider Reference occurrences are generic identity, provider routing, storage location, remote identifier, or diagnostic evidence?
- Does the Dev Backlog Steward retain any independent backlog-wide responsibilities after atomic lifecycle operations move into skills?

## Notes

- This work does not remove providers, claim-based concurrency, or independent backlog analysis that genuinely needs a separate execution context.
- This work does not combine Commit delivery with lifecycle persistence.
- This work does not standardize all providers on one identifier format or expose provider-specific locations globally.
- The current file-provider record still uses Provider Reference because that is the live provider contract being replaced by this work item.
- Backlog Crisis Mode was active at creation time. On 2026-08-05, the user explicitly prioritized this item after identifying repeated Dev Backlog Steward commit failures and per-transition handoff waste. The Root Dev Backlog Coordinator adopted it as the current crisis item and executed this lifecycle mutation directly through the selected file-work-item management skill, without a Steward child or claim operation.

## Crisis Execution Evidence

Transition: Ready -> Running.

Execution Owner: Root Dev Backlog Coordinator in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Priority Authority: Direct user instruction on 2026-08-05 to deal with Steward commit failures and wasted lifecycle-transition time.

Current Phase: Source discovery and smallest-complete implementation planning.

Coordination Mode: Backlog Crisis Mode; single-threaded delivery, no claim operations, and one committed crisis item before the next item begins.

## Delivery Evidence

- Direct lifecycle execution and Steward-scope simplification: `7d216a0d`.
- Provider-owned Work Item ID contract, provider boundaries, report migration, focused tests, documentation, and supported generated artifacts: `b9603b48`.
- Focused verification: 113 tests passed across lifecycle coordination, file-provider reporting, exact-path Git behavior, configured-provider ID boundaries, completion contracts, and the work-item template.
- All 13 changed skill definitions passed the configured skill validator with no findings.
- Generated documentation freshness and `git diff --check` passed.
- Completion was recorded directly by the owning Root Dev Backlog Coordinator through the selected file-provider management contract; no Dev Backlog Steward child or claim operation was used.
