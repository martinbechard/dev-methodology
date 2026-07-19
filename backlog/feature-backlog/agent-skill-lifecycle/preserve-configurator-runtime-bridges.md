# Preserve Configurator Runtime Bridges

Status: Ready

Type: Defect

## Summary

Require Project Configurator to emit functional harness bridges and preserve canonical fixed and conditional skill ownership when generating project guidance.

## Context

The Project Configurator technology-routing scenario correctly detected distinct service, user-interface, and infrastructure routes, preserved protected inputs, committed its work, and released its claim. The generated root and nested Claude guidance files contained prose instead of the required functional import of the corresponding agent guidance.

The same generated PROJECT.yaml made documentation-bootstrap fixed, made agent-claim conditional, and omitted organise-project-files. Canonical Project Configurator ownership fixes agent-claim and makes organise-project-files and documentation-bootstrap conditional. The deterministic critical gate returned FAIL. A later focused run passed, showing that the behavior is nondeterministic rather than an unavoidable fixture limitation. The complete evaluation did not edit the distributed Project Configurator skills.

## Evidence

- evals/agent-tests/project-configurator/scenarios.yaml defines the technology-routing bridges and canonical skill ownership contract.
- evals/agent-tests/project-configurator/fixtures/technology-routing contains the frozen multi-folder routing project.
- agents/roles defines Project Configurator fixed and conditional skill ownership.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the failed complete-run checkpoint and the passing focused rerun.
- The failed output used prose Claude guidance instead of a functional agent-guidance import at every configured boundary.

## Requirements

- Generate the exact functional Claude-to-agent-guidance import required by each configured root and nested boundary.
- Validate bridge behavior from file content rather than accepting descriptive prose.
- Preserve agent-claim as a fixed Project Configurator skill.
- Preserve organise-project-files and documentation-bootstrap as conditional Project Configurator skills.
- Reject missing, duplicated, or reclassified canonical skills in PROJECT.yaml.
- Add deterministic and Judge coverage for every generated harness bridge and role-owned skill set.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- Root and nested Claude guidance files contain functional imports of the corresponding agent guidance.
- Project Configurator fixed and conditional skill sets exactly match the canonical conceptual role.
- Technology-specific routing remains distinct for service, user-interface, and infrastructure folders.
- Protected source evidence remains unchanged and the generated project configuration is committed cleanly.
- The Project Configurator technology-routing scenario passes repeatably across multiple runs.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for root and nested runtime bridge generation.
- Compare generated PROJECT.yaml skill ownership directly with the canonical Project Configurator role.
- Run the technology-routing scenario multiple times and inspect bridge content, route status, target output, independent Judge verdict, claim lifecycle, and cleanup.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- A prose statement that agent guidance exists is not a functional harness bridge.
- Do not copy technology skills into the fixed role-owned set; keep setup-time folder detection distinct.
