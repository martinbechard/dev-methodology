# Prevent Unauthorized Contract Narrowing

Status: Completed

Type: Defect

## Approval Resolution

The user approved the exact three-skill governed definition scope.

## Approved Scope

Do you approve changing only skills/code-discovery/SKILL.md, skills/careful-coding/SKILL.md, and skills/test-driven-development/SKILL.md to prevent unsupported public-contract narrowing, together with their supported generated skill-definition mirrors and directly related non-governed evaluation/test coverage?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Ok”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, the user's direct reply on 2026-07-20 to the exact question above.

The decision gate is resolved. Delivery completion still requires the exact governed pre-mutation checks, implementation, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Current Execution

- Canonical Dev Orchestrator task: 019f7fbe-d91d-7e10-85a2-55f4729f3bed.
- Worktree: /Users/martinbechard/.codex/worktrees/52a3/dev-methodology.
- Phase: approved scoped implementation, focused verification, independent review, integration, completion, and cleanup.
- Running ownership was recorded after feature-branch completion released its terminal backlog claim; the replacement task supersedes the archived approval-boundary task without changing the approved definition scope.

## Summary

Prevent implementation agents from adding stricter public input constraints than the authoritative task and existing contract support.

## Context

The Dev Coder executable TypeScript scenario required an asynchronous coupon lookup that accepts percentage results in the inclusive range from 0 through 100. The target added a whole-number-only constraint, documented it as part of the public behavior, and added a test that rejected 12.5 percent.

The independent Judge found the implementation, regression suite, verification, claim lifecycle, commit, and cleanup otherwise complete. It returned FAIL because integer-cent calculations and rounding requirements did not authorize rejecting an in-range fractional percentage. The target had converted an implementation preference into a narrower dependency contract.

The target loaded code-discovery, careful-coding, test-driven-development, TypeScript, TypeScript Strict, TypeScript ESM, and the other declared implementation skills. The complete evaluation did not edit those distributed skills.

## Evidence

- evals/agent-tests/dev-coder/scenarios.yaml requires scoped behavior without unrelated pricing changes.
- evals/projects/typescript-order-pricing contains the frozen task, public boundary, and executable tests.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The target explicitly chose a whole-number percentage rule before implementation even though the supplied authority defined only the inclusive numeric range.

## Requirements

- Require implementation agents to distinguish explicit contract constraints from implementation conveniences and inferred preferences.
- Preserve every value allowed by the authoritative public contract unless the user or a stronger accepted source authorizes narrowing it.
- Keep rounding and representation decisions internal when they do not require a public input restriction.
- Require uncertain material public constraints to remain open decisions or blockers instead of silently becoming validation rules.
- Add deterministic or Judge coverage for unsupported input-domain narrowing.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- An inclusive numeric range accepts supported fractional values unless explicit authority requires integers.
- Internal integer-cent arithmetic does not add a whole-number percentage restriction at the dependency boundary.
- Tests do not encode invented validation rules as required behavior.
- A genuinely ambiguous material public constraint produces an explicit decision request when implementation cannot safely preserve the broader contract.
- The Dev Coder TypeScript behavior scenario passes repeatably without unauthorized contract narrowing.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for the changed discovery, careful-coding, and implementation contracts.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Dev Coder TypeScript behavior scenario with fractional in-range, boundary, invalid, rounding, and dependency-failure cases.
- Inspect the public types, implementation, regression assertions, independent Judge verdict, and cleanup evidence.
- Run repository unit tests and Git diff validation.

## Completion Evidence

- Delivery: main commit d24b3f442a897108238ec65cbbaf0d0bfb4b5a3e implements the approved scope.
- Review: independent methodology review passed with no findings.
- Focused verification: exact skill validation, build-skill-docs freshness, support-checklist freshness, focused fixtures (2/2), validate-only TypeScript scenario, source/generated integrity, and Git diff validation passed.
- Integration: main fast-forwarded from 1a58d26 to d24b3f4 under integration claim event 4458f88e-afcb-4e21-b3ad-e4031f9f4ecd; that claim released cleanly in event 0d0cfaae-3432-403b-802f-adc71966d9a9. The integrated tree is 5a12dd3203c12473c503d8ccc83462ddc19b084c with stable patch ID 28513d8a4f490354c483856899454fabdb9be843.
- Cleanup: primary and managed worktrees were clean at d24b3f4; the private branch was deleted after its managed worktree detached at the preserved integrated commit.
- Baseline warning: build-agent-skill-hierarchy --check reports the pre-existing stale design/agent-skill-hierarchy.svg from clean base; it was reproduced unchanged and is non-blocking for this item.

## Notes

- Do not prohibit necessary validation; require authority for validation that rejects otherwise supported inputs.
- Prefer preserving the broader accepted contract over introducing speculative restrictions.
