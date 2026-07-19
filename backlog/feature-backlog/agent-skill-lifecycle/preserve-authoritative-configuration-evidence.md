# Preserve Authoritative Configuration Evidence

Status: Ready

Type: Defect

## Summary

Prevent Project Configurator from corrupting valid source evidence while reconciling stale paths, and require detector evidence to retain its declared scalar shape in generated guidance.

## Context

The Project Configurator valid-configuration reuse scenario supplied authoritative task and README evidence that a Python package had moved from worker-old to worker. The target correctly relocated stale nested guidance and produced a working worker route, but rewrote PROJECT.yaml to claim that the package moved from worker to worker.

The same run stored detector evidence as a YAML mapping where the configuration contract expected the detector's string evidence. Generated AGENTS.md guidance consequently contained Python-dictionary syntax instead of the source-backed detector text.

The independent Judge accepted role identity, claim lifecycle, routing, bridges, protected inputs, executable tests, commits, and cleanup. It returned FAIL because the final committed configuration contradicted unchanged authoritative sources and overclaimed evidence preservation. The complete evaluation did not edit the distributed Project Configurator skills.

## Evidence

- evals/agent-tests/project-configurator/scenarios.yaml defines the valid-configuration reuse contract.
- evals/agent-tests/project-configurator/fixtures/valid-configuration-reuse contains the frozen authoritative task, README, stale route, and executable worker test.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The focused run retained the candidate history, source digests, target session, Judge session, and claim journal in its result evidence.

## Requirements

- Treat accepted task, README, and existing valid configuration evidence as authoritative inputs that must not be semantically rewritten without stronger source authority.
- Distinguish old and new path values when reconciling a move, and verify the final provenance statement against the frozen sources.
- Preserve the declared scalar shape of detector evidence from detection output through PROJECT.yaml and generated AGENTS.md guidance.
- Reject mapping or collection serialization where a detector evidence field requires a string.
- Require the final review to compare changed evidence statements with their source text, not only validate YAML syntax and route references.
- Add deterministic and Judge coverage for source-evidence contradictions and evidence-shape drift.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A move from worker-old to worker remains represented exactly that way after configuration reuse.
- Valid existing source evidence is retained unless an accepted stronger source authorizes its replacement.
- Detector evidence is a scalar string in PROJECT.yaml and renders as plain source-backed text in AGENTS.md.
- The valid-configuration reuse scenario passes repeatably with protected inputs unchanged.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for Project Configurator source selection, reconciliation, and evidence serialization.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Project Configurator valid-configuration reuse scenario.
- Inspect the final PROJECT.yaml provenance, generated AGENTS.md evidence, independent Judge verdict, and cleanup evidence.
- Run repository unit tests and Git diff validation.

## Notes

- Structural validity is insufficient when a generated configuration statement contradicts an unchanged authoritative source.
- Do not flatten arbitrary mappings silently; validate the detector contract at the boundary that consumes its evidence.
