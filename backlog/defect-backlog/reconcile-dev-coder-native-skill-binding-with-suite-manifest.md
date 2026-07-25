# Reconcile Dev Coder Native Skill Binding With Suite Manifest

Status: Ready

Type: Defect

Owner: Unassigned

Provider: file

Provider Reference: backlog/defect-backlog/reconcile-dev-coder-native-skill-binding-with-suite-manifest.md

Completion: direct-main

## Authority Reconciliation

Read-only authority evidence confirms that no governed canonical mutation is currently indicated. The portable Dev Coder role intentionally omits agent-claim, scripts/test_role_mutation_policy.py explicitly protects mutation roles and native contracts from loading agent-claim, and PROJECT.yaml -> AGENTS.md owns project-selected resource-coordination injection.

This defect is ordinary evaluation-contract drift in evals/agent-tests/dev-coder/suite.yaml and its associated suite scenarios, fixtures, and tests. Delivery must reconcile that evaluated contract without hand-editing generated/adapters/codex/agents/dev-coder.toml and without mutating a governed role or skill definition.

If later discovery genuinely requires a governed definition, this same item must transition to User Action Required with an exact approval manifest before any such mutation. Do not infer approval or use a generated adapter edit as a substitute.

## Reconciliation Evidence

- Portable-role evidence: agents/roles/dev-activities/dev-coder.role.yaml makes resource coordination conditional on the project-selected policy and does not load agent-claim.
- Native-contract evidence: scripts/test_role_mutation_policy.py asserts that mutation roles and their native contracts do not load agent-claim.
- Project injection evidence: PROJECT.yaml selects resource coordination independently, and generated AGENTS.md guidance owns the selected coordination procedure.
- Backlog Claim: reconcile-dev-coder-suite-contract-drift-019f9801 acquired on primary main at 2026-07-25T06:55:16.147805Z; acquisition journal event 14ea1ff2-834c-4287-87a6-76ee891740da.

## Summary

Reconcile the Dev Coder evaluation suite's required skill binding with the generated Codex native agent so the current-main validate-only catalog check succeeds without weakening the governed-definition approval boundary.

## Context

At current main commit f88312697e0522adbb39d3b59d897fefc1b9b8e1, the exact baseline command below fails in _validate_suite with ValueError: dev-coder native agent does not include required skill agent-claim.

The Dev Coder suite manifest at evals/agent-tests/dev-coder/suite.yaml lists agent-claim under target.requiredSkills. The generated native agent at generated/adapters/codex/agents/dev-coder.toml lists the definition-owned skills it loads, but does not include agent-claim. The runner checks each manifest-required skill as a substring of the generated native developer instructions.

This is distinct from backlog/defect-backlog/enforce-suite-catalog-path-containment-in-evaluation-runner.md, which covers suite-index path containment, and backlog/defect-backlog/enforce-agent-claim-lifecycle-evidence-in-runner-resource-scenarios.md, which covers lifecycle-evidence validation.

## Source Evidence

- The user supplied the confirmed current-main baseline at commit f88312697e0522adbb39d3b59d897fefc1b9b8e1 on 2026-07-25.
- Baseline command:

  ```text
  /Users/martinbechard/.pyenv/versions/3.11.10/bin/python3 evals/agent-tests/runner.py --harness codex --validate-only
  ```

- Observed failure: _validate_suite raises ValueError: dev-coder native agent does not include required skill agent-claim.
- Fresh record-time inspection confirmed the required manifest entry in evals/agent-tests/dev-coder/suite.yaml, the missing binding in generated/adapters/codex/agents/dev-coder.toml, and the runner check in evals/agent-tests/runner.py.

## Requirements

- Reconcile the effective Dev Coder suite required-skill contract and generated/native Codex agent skill binding so they agree on whether agent-claim is required.
- Preserve Dev Coder's repository-mutation and resource-coordination semantics; do not remove a required behavior merely to make validation pass.
- Treat conceptual role definitions, distributed skill definitions, metadata, and generated adapter mirrors as governed surfaces where applicable.
- Before mutating a governed canonical source, obtain explicit, scope-specific user approval and pass the required definition-change pre-mutation check.
- Regenerate native output only from an approved canonical source; do not edit generated adapter output by hand.

## Acceptance Criteria

- The Dev Coder suite manifest and the generated Codex native Dev Coder agent express the same required skill set for the evaluated contract.
- The baseline validate-only command succeeds for the Dev Coder validation path without this missing-skill error.
- Focused regression coverage detects a future mismatch between a suite-required skill and the generated native agent's declared instructions.
- Any governed canonical mutation has recorded, exact user approval and a successful pre-mutation check; generated mirrors are refreshed only through the supported generator.
- The containment and lifecycle-evidence defects remain separate and unchanged by this delivery unless independently authorized.

## Dependencies

None.

## Verification

- Run the exact baseline command using the repository-supported Python 3.11 interpreter.
- Run focused Dev Coder suite-manifest, native-agent, and runner validation tests.
- Run relevant generated-definition and skill-document freshness checks.
- Run git diff --check and obtain fresh independent review.

## Coordination Evidence

- Backlog claim record-dev-coder-native-skill-binding-019f9801 acquired on primary main at 2026-07-25T06:49:15.650342Z; acquisition journal event 54713d74-b7fa-46c6-a0bf-9ddbf3016cd8.

## Notes

This transaction records the defect only. It does not authorize implementation, governed-definition mutation, generated-output edits, or changes to either separate active runner defect.
