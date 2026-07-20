# Ignore Unrelated Noop Events In Agent Suite Identity Attribution

Status: Running

Type: Defect

## Current Execution Ownership

- Canonical Dev Orchestrator task: 019f7e52-1c6d-7cc2-bf96-3edd212462a8.
- Parent Dev Backlog Coordinator task: 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Worktree: /Users/martinbechard/.codex/worktrees/12da/dev-methodology.
- Phase: implement the bounded identity-attribution correction, obtain fresh independent review, run focused deterministic verification, integrate directly into main, and complete this work item.
- Verification boundary: focused runner and identity-attribution tests only; no live or full agent-catalog run unless affected-surface evidence requires escalation.

## Summary

Keep Agent Suite identity attribution scoped to the target and Judge lifecycle so an unrelated immediately closed default or noop event cannot convert a semantically passing scenario into an infrastructure failure.

## Context

The corrected focused Project Configurator valid-configuration-reuse run produced a target PASS, an independent Judge PASS, all authoritative evidence gates, a valid claim lifecycle, a commit, and clean teardown. The aggregate runner still exited with an infrastructure failure because its supervisor identity audit observed both default and project_configurator_suite_supervisor after the coordinator accidentally created and immediately closed an unrelated default noop event during tool discovery.

The attribution boundary must exclude unrelated immediately closed default or noop events while preserving every target, Judge, and expected supervisor identity requirement. This is harness infrastructure work, not permission to weaken scenario identity checks or alter governed agent or skill definitions.

## Evidence

- Retained focused run evidence: /private/tmp/preserve-authoritative-config-corrected-focused.LqJWZx.
- The valid-configuration-reuse target and independent Judge both returned PASS in that retained run.
- The runner recorded identities default and project_configurator_suite_supervisor and classified the otherwise passing run as an infrastructure failure.
- The unrelated default event was created and immediately closed outside the target and Judge lifecycle during coordinator tool discovery.
- Final verifier claim preserve-authoritative-config-corrected-live-verify released normally at event cc7b6370-3f49-4ed0-a7a6-178cf9ab654e.

## Requirements

- Attribute supervisor identity only from events that belong to the evaluated suite lifecycle.
- Ignore an unrelated default or noop event only when evidence proves it was immediately closed and did not participate in the target, Judge, or expected supervisor execution.
- Preserve strict target identity, Judge identity, expected supervisor identity, and unexpected participating-identity failures.
- Keep identity evidence observable in retained run results so exclusions can be independently audited.
- Add deterministic regression coverage for one unrelated immediately closed default noop beside a valid target and Judge lifecycle.
- Add adversarial coverage proving a default identity that participates in target, Judge, or supervisor work still fails attribution.

## Acceptance Criteria

- A passing target and Judge lifecycle is not failed solely because an unrelated immediately closed default or noop event exists outside that lifecycle.
- Every participating target, Judge, and supervisor identity remains subject to the existing strict gates.
- Retained evidence records both the excluded event and the exact reason it was outside the evaluated lifecycle.
- Focused harness tests cover the accepted exclusion and the participating-default rejection boundary.
- Applicable repository tests and Git diff validation pass.

## Dependencies

None.

## Verification

- Run focused identity-attribution tests with an unrelated immediately closed default noop event.
- Run adversarial tests where a default identity participates in target, Judge, or supervisor execution.
- Inspect retained identity evidence and exclusion reasons.
- Run the applicable Agent Suite runner tests and repository validation.
- Run git diff --check.

## Notes

- This Ready defect records an independently classified technical follow-up from the accepted preserve-authoritative-configuration-evidence verification.
- No governed agent definition, skill definition, generated definition, scenario contract, or User Action Required scope is authorized by this item.
