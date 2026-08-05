# Enforce Dependency-Aware File Work-Item Lifecycle

Status: Blocked

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/enforce-dependency-aware-file-work-item-lifecycle.md

Work Item ID: enforce-dependency-aware-file-work-item-lifecycle

Completion: direct-main

Owner: Unowned

## Summary

Make file-backed work-item creation, promotion, reporting, and dependency reconciliation use one lifecycle rule: `Ready` means dispatchable with every hard prerequisite satisfied, while queued work with an unmet dependency is `Blocked` until that dependency resolves.

## Context

The current file-backed workflow contradicts itself. `create-file-work-item` creates directly authorized work as `Ready` without first resolving dependencies, `manage-file-work-items` defines `Ready` as having no unmet prerequisites, `codex-workitem-coordination` compensates with downstream effective-eligibility filtering, and `scripts/generate-backlog-report.py` reports the invalid state only after creation. This permits lifecycle metadata to claim that work is runnable when its declared hard prerequisites make dispatch unsafe.

The correction must resolve dependencies at each boundary that can assign `Ready`, reject invalid `Ready` records, and promote dependency-blocked records when their exact prerequisite condition becomes true. Existing active records created under the contradictory rule must be reconciled without rewriting historical terminal evidence.

## Source Evidence

The user requested this defect in the active Codex task on 2026-08-05 and specified: resolve declared dependencies when an item is created, promoted, or moved to `Ready`; use `Ready` only when no hard prerequisite remains; use `Blocked` for queued dependency waits; promote such items when prerequisites are satisfied; reject `Ready` with unmet dependencies; update the relevant skill definitions, report validation, and focused evaluations; and correct existing active records that violate the rule.

## Requirements

- Resolve every declared hard dependency before creation, promotion, or lifecycle transition assigns `Ready`.
- Assign `Ready` only when every declared hard prerequisite is satisfied.
- Assign `Blocked` when authorized queued work has an unmet hard dependency, and record the dependency, blocker owner, and exact evidence-based unblock condition.
- Reconcile dependency-blocked records to `Ready` when their prerequisites reach the required terminal state.
- Reject or correct any attempted `Ready` record with an unmet hard dependency at the mutation boundary rather than relying on downstream effective-eligibility filtering.
- Remove compensating lifecycle ambiguity from `codex-workitem-coordination` while retaining ordinary dispatch sequencing and overlap coordination.
- Make `scripts/generate-backlog-report.py` validate the canonical lifecycle rule and report genuine malformed or stale records without serving as the first enforcement boundary.
- Correct active nonterminal file-backed items that currently say `Ready` while declaring an unmet hard dependency; do not rewrite completed, failed, or historical lifecycle evidence merely for wording.
- Keep dependency resolution based on opaque Work Item IDs so movement between provider folders does not break references.

## Acceptance Criteria

- Creation with no unmet hard dependency produces `Ready`; creation with an unmet hard dependency produces `Blocked` with an exact unblock condition.
- Promotion and ordinary lifecycle transitions cannot produce `Ready` while a declared hard dependency remains unmet.
- Dependency reconciliation moves a correctly blocked item to `Ready` after the prerequisite satisfies its recorded condition.
- Focused negative tests fail if any creation, promotion, or transition path permits `Ready` with an unmet hard dependency.
- The backlog report and focused evaluator fixtures agree on the same lifecycle states and do not need a separate effective-eligibility interpretation.
- Every existing active `Ready` item with an unmet hard dependency is moved to `Blocked` in a path-limited provider transaction, while terminal archives remain unchanged.
- Generated skill documentation is current, all three governed skills validate, focused report and work-item lifecycle tests pass, and `git diff --check` passes.

## Dependencies

- align-work-item-creation-provider-skills

## Verification

- Run the supported skill validator on all three governed canonical sources.
- Run focused creation and management contract tests, including `evals/agent-tests/dev-backlog-steward/test_contract.py` and the directly affected bundle-content cases.
- Run `scripts/test_generate_backlog_report.py` with positive and negative dependency-state fixtures.
- Run the focused Codex work-item coordination evaluation cases that cover dispatch eligibility and dependency reconciliation.
- Generate the backlog report against the reconciled active inventory and confirm no `Ready` item has an unmet hard dependency.
- Regenerate supported skill documentation and run its freshness check.
- Run `git diff --check` and inspect the exact provider-path changes used to reconcile existing active records.

## Open Questions

Determine whether an unmet dependency should be represented solely in the canonical `Dependencies` section plus the ordinary Blocked disposition fields, or whether one additional normalized dependency-state field is necessary for deterministic reporting. Prefer the existing shape unless focused implementation evidence proves it insufficient.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-file-work-item/SKILL.md
- skills/manage-file-work-items/SKILL.md
- skills/coordinate-codex-work-items/SKILL.md

### Allowed Dependent Artifacts

- scripts/generate-backlog-report.py
- scripts/test_generate_backlog_report.py
- scripts/test_bundle_content.py
- evals/agent-tests/dev-backlog-coordinator
- evals/agent-tests/dev-backlog-steward
- evals/agent-tests/dev-backlog-watchdog
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- design/generated/skill-definitions.js
- design/agent-and-skill-evaluations.html
- Directly related generated adapters, focused fixtures, and active provider records required to keep the approved definitions and active lifecycle inventory coherent

### Approval Resolution

Approved at creation on 2026-08-05 by the user's direct request in the active Codex task to create this work item and implement the stated coherent dependency-based lifecycle across the relevant skill definitions, report validation, and focused tests. The coordination package had already been renamed; source discovery therefore resolves that approved function to the live canonical path `skills/coordinate-codex-work-items/SKILL.md`, not the retired `skills/codex-workitem-coordination/SKILL.md`. Approval is limited to the three governed canonical paths listed above. Any additional governed definition requires new explicit user approval.

## Notes

This item is created as `Blocked`, not `Ready`, because `align-work-item-creation-provider-skills` is an active crisis-chain item that modifies `skills/create-file-work-item/SKILL.md`. Its exact unblock condition is that the dependency reaches a terminal successful disposition on current `main`, leaving the shared creation-skill surface available for fresh reconciliation. The Dev Backlog Coordinator owns that dependency-chain sequencing. This source-overlap prerequisite must not be replaced with concurrent implementation or downstream effective-eligibility filtering.
