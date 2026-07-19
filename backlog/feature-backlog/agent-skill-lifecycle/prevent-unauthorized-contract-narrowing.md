# Prevent Unauthorized Contract Narrowing

Status: Ready

Type: Defect

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

## Notes

- Do not prohibit necessary validation; require authority for validation that rejects otherwise supported inputs.
- Prefer preserving the broader accepted contract over introducing speculative restrictions.
