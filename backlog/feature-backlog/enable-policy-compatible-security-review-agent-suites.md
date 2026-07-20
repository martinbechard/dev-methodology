# Enable Policy Compatible Security Review Agent Suites

Status: Running

Type: Feature

## Running Ownership

- Owner: Dev Orchestrator for the exact item under parent task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: policy-security-review-backlog.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T03:07:05.914008Z from clean baseline commit 361488356d9a3fef1a30202a46f6a1589cc17fa6.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Dev Security Reviewer suite-local scenarios, route-selection contract and fixtures, deterministic tests, review, verification, and integration require a separate canonical isolated claim.

## Summary

Provide a policy-compatible execution route for synthetic Dev Security Reviewer scenarios so security-review behavior can be evaluated without bypassing Codex safeguards or losing semantic Judge evidence.

## Context

The material-findings scenario asks the Dev Security Reviewer to trace a synthetic cross-tenant read path. The generated Codex adapter selects a Sol-backed model while its Codex harness directives prohibit that model family from cybersecurity work. The target therefore produced no prioritized security finding, critical output gates failed, and the Judge was skipped.

This is a harness routing conflict rather than missing product authority. The separate missing-authority scenario correctly remains BLOCKED when deployed authorization policy evidence is absent.

The classification is recorded in [Classify Agent Suite Blocking Resources](../completed-backlog/analyses/classify-agent-suite-blocking-resources.md), and the authoritative run evidence is preserved in [Complete Agent Suite Results](../../evals/agent-tests/results/2026-07-17-complete-agent-suites.md).

## Requirements

- Select a supported model, harness, or deterministic evaluator route that is permitted to perform the bounded synthetic security-review scenario.
- Preserve the canonical Dev Security Reviewer role, application-security guidance, read-only boundary, fixture identity, and expected output contract.
- Keep Codex safeguard routing explicit and never bypass it through rephrasing, prompt splitting, hidden delegation, or an affected fallback model.
- Validate the selected route before target dispatch and report a distinct infrastructure blocker when no permitted route is available.
- Bind target and Judge identities, staged definitions, fixture digests, tool traces, and verdict evidence to the retained result.
- Require the material-findings target to trace input through route, middleware, authorization, query, and missing negative coverage; prioritize the finding by exploitability; and state residual risk.
- Preserve justified-clean-review as a no-material-finding scenario grounded in positive and negative evidence.
- Preserve missing-authority as a safe BLOCKED scenario that does not infer deployed policy behavior.

## Acceptance Criteria

- The material-findings scenario executes through a route permitted for the declared synthetic security-review scope.
- The target returns prioritized findings, affected files and evidence, and residual risk without modifying the fixture.
- Deterministic identity, read-only, evidence-reference, output-contract, and finding-priority gates pass.
- A fresh independent Judge evaluates the semantic result instead of being skipped for the current model-policy conflict.
- The scenario records its expected semantic terminal result without a test-infrastructure BLOCKED classification.
- justified-clean-review continues to reject invented findings and unsupported global-security claims.
- missing-authority continues to request bounded governing evidence and remains safely BLOCKED.
- No safeguard, capability declaration, or Judge gate is weakened to obtain a passing suite.

## Dependencies

None.

## Verification

- Run the focused material-findings scenario and inspect route selection, target evidence, deterministic gates, Judge invocation, and cleanup.
- Run justified-clean-review and missing-authority through the same routing decision and confirm their distinct semantic outcomes.
- Force an unavailable or prohibited route and verify dispatch stops before cybersecurity work begins.
- Add deterministic tests for supported, prohibited, unavailable, and malformed routing evidence.
- Run the Dev Security Reviewer suite, runner tests, generated-adapter freshness checks when affected, applicable bundle validation, and Git diff validation.

## Notes

- The work chooses a compliant evaluation route; it does not relax the Codex cybersecurity safeguard.
- Keep synthetic fixture findings separate from claims about any real deployed system.
