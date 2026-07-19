# Preserve Integrated Documentation Steady State

Status: Ready

Type: Defect

## Summary

Require Project Bootstrapper and its documentation contributors to remove contribution-phase and future-work wording after the referenced artifacts have been integrated.

## Context

The Project Bootstrapper missing-configuration evaluation successfully created and integrated configuration, module documentation, and wiki contributions. Its final bounded review still found PROJECT.yaml, AGENTS.md, the wiki README, the module catalog, and module pages describing now-present artifacts as absent, excluded, or future work. Links and ownership statements therefore contradicted the final repository state.

The complete evaluation did not edit the distributed Project Bootstrapper, Project Configurator, Dev Documentation Writer, or Wiki Architect skills.

## Evidence

- evals/agent-tests/project-bootstrapper/scenarios.yaml defines the integrated steady-state acceptance contract.
- evals/agent-tests/project-bootstrapper/fixtures/missing-configuration contains the frozen multi-contribution fixture.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the final correction-cap failure.
- The final live review found present wiki pages still labeled as excluded or future contributions and configuration guidance still stating that required documentation was absent.

## Requirements

- Re-read the integrated repository state after every accepted contribution and before final review.
- Replace contribution-phase, absent-artifact, exclusion, and future-work wording when the referenced artifact now exists.
- Keep PROJECT.yaml, AGENTS.md, wiki navigation, module catalogs, manifests, and module pages mutually consistent.
- Resolve links and ownership statements against the final tree rather than an earlier contribution snapshot.
- Assign one contributor explicit ownership of the final cross-artifact steady-state sweep.
- Add deterministic checks for stale phase wording and contradictions about present files.

## Acceptance Criteria

- Final configuration and documentation describe the same integrated repository state.
- No present wiki or module artifact is labeled absent, excluded, or future work.
- Navigation and manifests include every accepted contribution with valid links.
- The Project Bootstrapper missing-configuration scenario reaches final acceptance within its bounded correction policy.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

- Enforce Documentation Template Conformance.

## Verification

- Add focused integration tests that transition a fixture from contribution phase to steady state.
- Search final artifacts for fixture-specific absent, excluded, and future-work markers.
- Run the Project Bootstrapper missing-configuration scenario and inspect every accepted contribution and the final review packet.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- A correct intermediate contribution does not satisfy the final integrated-state contract.
