# Preserve Configurator Runtime Bridges

Status: Completed

Type: Defect

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-9fa4-7ee0-b603-44c2bf61b85d.
- Worktree: /Users/martinbechard/.codex/worktrees/8490/dev-methodology.
- Branch: codex/preserve-configurator-runtime-bridges, fully integrated on main.
- Phase: Completed and archived; eligible for parent worktree and merged-branch cleanup.
- Accepted candidate commit: c67ab49ca59a9d9492dc3ac70f4147b50fb847e2.
- Integrated main commit: 88b2a13ccd9162187aea8bde089ccc9e8e296b8b.
- Integration wait: None. The exact integration claim succeeded on its first attempt.
- Completion wait: None. The exact source and destination backlog claim succeeded on its first attempt.
- Open issues: None for the delivered item. The live scenario runner has a separate shared response-schema defect recorded below.

## Completion Evidence

- Candidate c67ab49ca59a9d9492dc3ac70f4147b50fb847e2 changed seven evaluation-only files. It did not mutate a governed canonical agent or distributed skill definition and did not regenerate a mirror.
- Fresh independent review found two correctable evaluation-test gaps in earlier candidates. The final fresh-context review accepted c67ab49ca59a9d9492dc3ac70f4147b50fb847e2 with no priority findings after both corrections were committed.
- Main commit 88b2a13ccd9162187aea8bde089ccc9e8e296b8b integrates the accepted bytes after semantic reconciliation confirmed that current main had no changes on the seven owned paths.
- Integration claim preserve-configurator-runtime-bridges-integration-8490 acquired the seven exact project paths plus merge:integration:main at event 71044bee-b659-4b9a-9dff-bdab2705d736 and released cleanly at event 0f880de2-aa14-4fb6-a6d4-e9f7fb80e360.
- The Project Configurator fixture suite passed 17 tests on three consecutive corrected-candidate runs and again after integration.
- The focused agent-suite structure test and conceptual-role contract test passed. Evaluation catalog validation returned CATALOGS VALID, and Agent Skill validation passed.
- Technology detection, methodology documentation data, agent and skill hierarchy, and support-checklist freshness checks passed after integration. Git diff validation passed and main was clean.
- A focused live technology-routing attempt retained evidence at /private/tmp/dev-methodology-configurator-bridges-8490-run1/summary.json. It stopped before supervisor or target dispatch because the shared response schema omitted handoffReceipts from a required-array declaration. Status was infrastructure-failed and workspace cleanup was clean. The accepted candidate does not change the runner or response schema, so this unrelated baseline infrastructure failure is a warning rather than an item blocker; no live scenario verdict was claimed.
- Terminal backlog claim preserve-configurator-runtime-bridges-completion-8490 acquired exactly this active source path and backlog/completed-backlog/defects/preserve-configurator-runtime-bridges.md at event 70d4f72f-4cae-4909-8f9e-f37238e17f4c. Its archive commit and release event are reported in the terminal handoff.

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
