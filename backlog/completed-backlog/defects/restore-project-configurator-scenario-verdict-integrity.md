# Restore Project Configurator Scenario Verdict Integrity

Status: Completed

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator task 019f7dfe-6b43-7402-8776-813473e71069 under parent Dev Backlog Coordinator task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: restore-project-configurator-verdict-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T00:50:55.174511Z from clean baseline commit 353273d2806b7109033ec3954e7a7394126d4db5.
- Scope boundary: this claim owns only the Running transition and primary index resource and is released after its clean commit. Project Configurator suite artifacts, tests, review, verification, and integration require a separate canonical isolated claim.

## Execution Record

- Canonical Dev Orchestrator task: 019f7dfe-6b43-7402-8776-813473e71069
- Branch: accepted source branch codex/restore-project-configurator-verdict-integrity; delivery is integrated on main
- Worktree: /Users/martinbechard/.codex/worktrees/c9fc/dev-methodology
- Current phase: Completed and archived
- Accepted candidate commit: 1ed42a6e8bb2f1e9807415056089a3e29bd98f2e
- Integrated main commit: ded845bf39f8f21c1cb9a2b250141a38ab8c5c5c
- Integration or completion wait: None
- Claim attempts: Integration acquired on the first attempt at event 758e3985-2a6f-472d-a394-3f93f181cb08 and released at event f20ccca5-f409-44c9-b06e-ef78cfc1f29d; task-record claim acquired at event 1171342f-f007-4691-a3f4-7ce376ac4e33
- Open issues: None

## Completion Evidence

- Canonical Dev Orchestrator task: 019f7dfe-6b43-7402-8776-813473e71069 under parent Dev Backlog Coordinator task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Accepted candidate commit: 1ed42a6e8bb2f1e9807415056089a3e29bd98f2e.
- Integrated main commit: ded845bf39f8f21c1cb9a2b250141a38ab8c5c5c.
- Integration claim: integrate-project-configurator-verdict-integrity acquired at event 758e3985-2a6f-472d-a394-3f93f181cb08 and released normally at event f20ccca5-f409-44c9-b06e-ef78cfc1f29d.
- Task-record commit: 4e5b84517b187908ac6bee81b914fd078cdb7e25.
- Task-record claim acquired at event 1171342f-f007-4691-a3f4-7ce376ac4e33 and released normally at event feffd81b-e556-4c6a-8dbf-29e1c2ce7b37.
- Fresh independent post-integration review covered exactly the seven files changed by the integration diff from c0e3bbe9d0ba43322c50489c566d4f9704fa9e88 through ded845bf39f8f21c1cb9a2b250141a38ab8c5c5c. The reviewer reported no findings, no open questions, and an ACCEPT verdict. The reviewed files remained byte-identical on the then-current main commit 2978cb2340c55cb18d4b49c97732d28c152094bd.
- The 14 Project Configurator suite-local unittest cases passed in 0.157 seconds.
- Project Configurator validate-only scheduling passed with the Codex harness, one suite, one supervisor job, and no model or live scenario execution.
- Global evaluation catalog validation passed with CATALOGS VALID.
- Git diff validation passed. The task-owned validate-only summary was preserved externally at /private/tmp/project-configurator-verdict-postintegration-edEvgq/summary.json, its accidental primary copy was removed, and primary status returned clean before terminal claim acquisition.
- No broad, full, or live suite was run during post-integration closeout.
- Terminal backlog claim restore-project-configurator-verdict-terminal-backlog acquired in PRIMARY mode from clean main 7b79a959c11d057ea969be4f1e6a6c962964b672 at event 67fa9b49-cf79-46ae-928e-18b6b0d0391a for exactly the active source path and completed defect destination. Its normal release event is reported in the terminal handoff after the clean archive commit.

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
