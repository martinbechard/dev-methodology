# Restore Project Configurator Scenario Verdict Integrity

Status: Running

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: restore-project-configurator-verdict-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T00:50:55.174511Z from clean baseline commit 353273d2806b7109033ec3954e7a7394126d4db5.
- Scope boundary: this claim owns only the Running transition and primary index resource and is released after its clean commit. Project Configurator suite artifacts, tests, review, verification, and integration require a separate canonical isolated claim.

## Summary

Restore source-faithful Project Configurator Judge verdicts for technology-routing canonical completeness and mutation agreement and for invalid-configuration repository inspection and non-repetition.

## Context

The corrected full Project Configurator run passed the valid-configuration-reuse scenario and all deterministic repository gates. Two broader scenarios still failed at the independent Judge boundary even though their deterministic checks passed.

For technology-routing, the Judge reported a noncanonical and incomplete PROJECT.yaml, omitted mandatory sections, missing conceptual definitions, and a mutation agreement incorrectly marked inapplicable. For invalid-configuration, the target correctly returned BLOCKED and deterministic checks passed, but the Judge reported that the target admitted it had not inspected the repository and repeated supervisor assertions instead of supplying independent source-backed reasoning.

These failures are outside the bounded preserve-authoritative-configuration-evidence implementation. This defect records them together because they share the Project Configurator scenario and Judge evidence contract, without authorizing a governed definition change.

## Evidence

- Retained full run evidence: /private/tmp/preserve-authoritative-config-corrected-full.Y2DU9B.
- The full runner completed without an infrastructure or cleanup failure.
- valid-configuration-reuse returned PASS in the same full run.
- technology-routing passed deterministic routing and worktree-ignore checks, then failed the independent Judge for canonical completeness, conceptual-definition coverage, and mutation-agreement classification.
- invalid-configuration correctly returned BLOCKED and passed deterministic checks, then failed the independent Judge for absent repository inspection and repeated supervisor assertions.
- Final verifier claim preserve-authoritative-config-corrected-live-verify released normally at event cc7b6370-3f49-4ed0-a7a6-178cf9ab654e.

## Requirements

- Require technology-routing output to preserve the canonical PROJECT.yaml structure and every scenario-mandated section.
- Require the technology-routing evidence packet to include the required conceptual definitions and a source-faithful mutation agreement disposition.
- Prevent mutation agreement from being marked inapplicable when the scenario contract requires its evaluation.
- Require invalid-configuration reasoning to cite observable repository inspection before returning BLOCKED.
- Require the invalid-configuration Judge packet to distinguish independent target reasoning from repeated supervisor assertions.
- Keep deterministic scenario gates and independent Judge gates aligned without weakening either boundary.
- Add focused fixtures and assertions for each reported failure mode.

## Acceptance Criteria

- technology-routing produces a canonical complete PROJECT.yaml with all mandatory sections and required conceptual-definition evidence.
- technology-routing records the correct mutation-agreement applicability and disposition.
- invalid-configuration still returns BLOCKED without unauthorized mutation and shows source-backed repository inspection.
- The invalid-configuration Judge verdict rejects repetition-only reasoning and accepts independent repository-backed reasoning.
- Both scenarios pass their deterministic and independent Judge gates repeatably.
- Applicable repository tests, generated-output freshness checks, and Git diff validation pass.

## Dependencies

None.

## Verification

- Run focused fixture and contract tests for technology-routing canonical completeness, conceptual definitions, and mutation agreement.
- Run focused fixture and contract tests for invalid-configuration repository inspection and non-repetition.
- Run both Project Configurator scenarios and inspect target output, Judge packets, claim lifecycle, commits, and cleanup.
- Run applicable repository validation and generated-output freshness checks.
- Run git diff --check.

## Notes

- This Ready defect records broader Project Configurator regressions discovered while verifying preserve-authoritative-configuration-evidence.
- The existing preserve-configurator-runtime-bridges feature covers generated runtime bridge imports and is not a duplicate of this scenario-verdict defect.
- No governed agent definition, skill definition, generated definition, User Action Required item, or artifact mutation is authorized by this backlog-only creation step.
