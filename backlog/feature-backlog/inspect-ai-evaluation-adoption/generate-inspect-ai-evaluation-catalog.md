# Generate The Inspect AI Evaluation Catalog

Status: Ready

Type: Feature

Provider: file

Work Item ID: generate-inspect-ai-evaluation-catalog

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Generate Inspect tasks and evaluation definitions from the current canonical suite and scenario sources with digest binding, focused regeneration, and stale-output rejection.

## Context

Hand-maintaining parallel catalogs would erase the expected maintenance benefit. Generation begins only after the executable and reporting contracts stabilize.

Estimated complexity is High. Estimated generation is 220,000–400,000 tokens, or 1.22–2.22 total agent-hours, across 12–20 turns. Estimated non-model runtime is 1–3 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 7 of that proposal.

## Requirements

- Treat existing suite.yaml and scenarios.yaml files as canonical during this phase.
- Generate Inspect definitions through one supported generator rather than hand editing projections.
- Bind generated tasks to conceptual-role, native-adapter, skill, fixture, scenario, scorer, and verifier identities as applicable.
- Support one-suite and complete-catalog regeneration.
- Reject stale, mixed-version, duplicate, missing, or malformed projections.
- Encode the capability routing decisions from earlier phases.
- Update focused catalog documentation and tests.

## Acceptance Criteria

- Selected and complete generation are deterministic and fresh.
- A source change makes the affected projection detectably stale.
- Generated files contain no independent policy that is absent from canonical sources.
- Ordinary scenario addition requires less duplicated work than the current architecture.
- Independent generated-artifact review accepts source-to-output consistency.

## Dependencies

integrate-inspect-ai-reporting-evidence. Unblock when the stabilized execution, routing, governed-result, and evidence schemas are accepted.

Derived Queue Evidence: Stored lifecycle remains Ready. Series order derives effective Holding behind a healthy predecessor or effective Blocked behind the first genuinely Blocked predecessor; do not rewrite this record for either derived state.

## Verification

- Run selected and full generation twice and compare exact outputs.
- Exercise stale-source, duplicate, missing-fixture, and unsupported-capability cases.
- Run focused generator, catalog, source-to-output, and diff checks.

## Open Questions

- Should Inspect definitions remain generated permanently, or become canonical only after complete migration and a separate authority decision?
