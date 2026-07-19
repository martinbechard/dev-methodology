# Preserve Authoritative Configuration Evidence

Status: Completed

Type: Feature

## Completion Evidence

- Running lifecycle: Dev Backlog Steward recorded Running ownership in commit 1ee72be549619d0eb3fe3e0a769d1d97865d6ba4 and released the exact-file lifecycle claim at event 9fab37c3-8870-4000-a110-cdec87092744.
- Accepted renderer implementation: source commit a612fe255c96b28582433b5ff0390bed6a621832 and correction commit 6b5390436a03aaede4ec33ac4764f2067d133908 were independently reviewed and verified. The corrected behavior was integrated on main as e2e7a47e212df38852af802d4312c410c3c1ca2f.
- Accepted Project Configurator evaluation contract: source commit 0fc48bdf435983dfc7409eb2f678613d6dca6a92 and correction commit c0fcca5ab7d0093f04e98fbe5df490281acaee88 were independently reviewed and verified. The corrected contract was integrated on main as 5d48cfb85853fa12e2e81adbb62385f8362594a7.
- Reviews: fresh renderer code review, Project Configurator methodology artifact review, correction reviews, and final post-integration code and artifact reviews all accepted the bounded contributions with no remaining in-scope findings.
- Deterministic verification: focused renderer tests passed 6 of 6, detector tests passed 64 of 64, Project Configurator fixture tests passed 10 of 10, Agent Suite runner tests passed 56 of 56, repository script tests passed 456 of 456, project-wiki tests passed 17 of 17, all applicable validators and generated-output freshness checks passed, and Git diff validation passed.
- Semantic acceptance: the exact valid-configuration-reuse behavior passed independently in the retained focused run at /private/tmp/preserve-authoritative-config-corrected-focused.LqJWZx and in the retained full run at /private/tmp/preserve-authoritative-config-corrected-full.Y2DU9B. The full runner completed cleanly and valid-configuration-reuse returned PASS.
- Aggregate disposition: accepted with WARN because the remaining aggregate failures were proven outside this bounded implementation. Identity attribution follow-up is recorded in [Ignore Unrelated Noop Events In Agent Suite Identity Attribution](../../defect-backlog/ignore-unrelated-noop-events-in-agent-suite-identity-attribution.md). Broader Project Configurator scenario follow-up is recorded in [Restore Project Configurator Scenario Verdict Integrity](../../defect-backlog/restore-project-configurator-scenario-verdict-integrity.md).
- Evidence cleanliness: disposable repository-local validate-only output was classified, its summary digest was recorded as eea420f6a93cd8aae51cbbf498b22baeaebac5d31c61ffda612faf4092d7381c, retained external evidence was preserved, the disposable directory was removed, and the repository script suite then passed 456 of 456 from a clean primary worktree.
- Scope boundary: no governed agent definition, skill definition, generated definition, README, design document, root PROJECT.yaml or AGENTS.md, or scripts/test_bundle_content.py was changed by this feature.
- Terminal lifecycle: Dev Backlog Steward acquired PRIMARY backlog-only claim preserve-authoritative-configuration-evidence-terminal-completed at event a32bf0dd-e7f7-4010-9a99-09bf5d037718 from clean commit 01db43bba1b733ae5b991eb97f26b2a730330663. The claim is released immediately after this completion archive commit is clean.

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: preserve-authoritative-configuration-evidence-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T11:49:14.428147Z from clean baseline commit f476be76d01c978a24ea58d47999b659fba24dd4.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Project source, evaluation artifacts, generated outputs, verification, and integration remain gated on a later ARTIFACT GO.

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
