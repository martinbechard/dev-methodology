# Reconcile Dev Coder Native Skill Binding With Suite Manifest

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/reconcile-dev-coder-native-skill-binding-with-suite-manifest.md

Completion: direct-main

## Lifecycle Start

- Owner: Dev Orchestrator
- Canonical Thread And Task Identity: 019f9907-b5f0-7d72-8647-a7aae10dcda4
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Branch: codex/reconcile-dev-coder-suite-binding-019f9907
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/f0c1/dev-methodology
- Phase: correction attempt 1
- Coordination Evidence: Backlog claim reconcile-dev-coder-suite-binding-running-019f9907 acquired on primary main at 2026-07-25T11:29:47.398158Z; acquisition journal event eb6dd5b3-d1e1-4e17-91ed-341d4e873e22.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Reconcile the Dev Coder suite required-skill contract with its native skill-binding evaluation.
- Dispatched At: 2026-07-25T11:26:23Z
- Intended Root Role: Dev Orchestrator
- Discovered Ordinary Source Scope: evals/agent-tests/dev-coder/suite.yaml; evals/agent-tests/dev-coder/skills/dev-coder-suite-contract/SKILL.md; evals/agent-tests/dev-coder/test_fixtures.py. No governed or generated mutation is indicated.
- Runtime Thread And Task Id: 019f9907-b5f0-7d72-8647-a7aae10dcda4.

## Reservation Coordination Evidence

- Backlog Claim: reserve-dev-coder-suite-binding-20260725 acquired on primary main at 2026-07-25T11:26:23.901358Z; acquisition journal event d2728b4c-d898-4d25-aaf4-8a7fc1f9ede3.

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

## Correction Attempt 1 Plan — 2026-07-25

- Authorization: Parent-authorized correction plan for this canonical Running item. Status remains Running; Owner remains Dev Orchestrator; Canonical Thread And Task Identity, Parent Coordination Thread, Canonical Branch, and Canonical Worktree remain unchanged.
- Rejected Candidate: c0916072a3ee9af8207b41257e0f971c225a2716.
- Fresh Review: REJECT.
- Medium Finding: The suite-wide claim contract must preserve enabled ownership release or an explicit handoff. Release-only evidence remains only in scenarios that require it.
- High Finding: The suite.yaml source digest requires a candidate-owned supported generated documentation refresh.
- Authorized Correction Scope: evals/agent-tests/dev-coder/suite.yaml; evals/agent-tests/dev-coder/skills/dev-coder-suite-contract/SKILL.md; evals/agent-tests/dev-coder/test_fixtures.py; and design/agent-and-skill-evaluations.html.
- Generated Documentation Boundary: design/agent-and-skill-evaluations.html may be produced only by scripts/build-agent-skill-evaluation-docs.py after the source correction. Focused coverage changes may occur only inside the existing evals/agent-tests/dev-coder/test_fixtures.py.
- Exclusions: No governed source, generated adapter, other generated mirror, backlog implementation, or other path is authorized.
- Next Runnable Action: Dev Orchestrator performs correction attempt 1 within the exact authorized scope, obtains fresh review, and preserves required verification and delivery evidence before any lifecycle transition.

## Completion — 2026-07-25

- Completion Disposition: READY for lifecycle COMPLETED under the direct-main contract.
- Completed Phase: direct-main delivery, independent review, verification, integration observation, and terminal file-provider archival are complete.
- Accepted Source Commit: 6d61b5abb94b11cfa6be0a9f02fd000f672ecad3 (fresh review ACCEPT with no material findings).
- Independent Verification: PASS. The accepted evidence includes the four fixture cases, Dev Coder validate-only, suite-skill validation, evaluation-document freshness, 26 evaluation-document tests, build-skill-docs check, focused role-policy check, and diff check.
- Integration Evidence: c0916072a3ee9af8207b41257e0f971c225a2716 was integrated as c095a7867270580a7a722adbe48dea840b99f4a4; 6d61b5abb94b11cfa6be0a9f02fd000f672ecad3 was integrated as 4bab2a264c5327c2a5e66b3499c391eb6ae82f54. Commit bc67dec01fa95c20200d59a34199aa86bbea9a51 refreshed only the supported evaluation HTML and is an ancestor of the observed main tip.
- Delivered Paths: evals/agent-tests/dev-coder/suite.yaml; evals/agent-tests/dev-coder/skills/dev-coder-suite-contract/SKILL.md; evals/agent-tests/dev-coder/test_fixtures.py; design/agent-and-skill-evaluations.html.
- Main Observation: primary main was clean at 0e1432e1561d11b957609164e013d6d8205e0c65. Both integration commits c095a7867270580a7a722adbe48dea840b99f4a4 and 4bab2a264c5327c2a5e66b3499c391eb6ae82f54, and the evaluation HTML refresh bc67dec01fa95c20200d59a34199aa86bbea9a51, are reachable from that observed main tip.
- Integration Coordination Release: integration claim acquired journal event bb6f30c2-abd1-4333-be70-f0806a1ccd3 and released journal event e59e8bd2-72c9-48dc-94fe-fc098f99b5f3.
- Separate Defects: newly exposed all-suite defects were recorded independently: Project Bootstrapper is completed, and Dev Merge Coordinator remains Ready at canonical task 0e1432e1. They are not part of this completion.
- Terminal Provider Transaction: backlog claim complete-dev-coder-suite-binding-019f9907 acquired on primary main at 2026-07-25T12:21:42.125887Z; acquisition journal event 79102887-045b-4f30-bba4-e4cabc9a23a3. This archive path is the terminal provider reference.
- Cleanup Eligibility: the delivered candidate and primary worktrees were clean before this transaction, the delivery is preserved on main, and the canonical delivery worktree/branch are eligible for normal cleanup after this terminal transaction's claim is released.
