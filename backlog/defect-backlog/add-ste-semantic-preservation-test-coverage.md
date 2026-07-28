# Add STE semantic-preservation test coverage

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/add-ste-semantic-preservation-test-coverage.md

Completion: direct-main

## Summary

Make the STE technical-writing tests reject semantic changes to identifiers, configuration values, and ownership. Add a negative activation fixture that proves ordinary communication and non-document artifacts do not activate the STE contract.

## Context

Candidate a83eae77b1e5a0001d79995a5687043c81ef0abf delivered the STE technical-documentation standard. Its focused test module, scripts/test_ste_technical_writing.py, protects identifiers and owners in helper code. However, the negative test asserts only normative force and one condition.

An independent Dev Code Reviewer removed the protected-value and owner checks from the candidate. The mutation still passed one test with this evidence: testsRun: 1, failures: 0, errors: 0, mutant: protected-and-owner-checks-removed.

The current feature item requires tests to reject changed identifiers, configuration values, ownership, conditions, and normative force. It also requires focused boundary tests that prove STE applies to technical documentation but not to ordinary communication or non-document artifacts. This defect attaches to the current STE delivery and does not change that feature's lifecycle.

## Source Evidence

On 2026-07-28, an independent Dev Code Reviewer confirmed that candidate a83eae77b1e5a0001d79995a5687043c81ef0abf has insufficient semantic-preservation tests. The reviewer removed protected-value and owner checks, then observed a passing mutation result: testsRun: 1, failures: 0, errors: 0, mutant: protected-and-owner-checks-removed.

The confirmed defect violates the acceptance criterion in backlog/feature-backlog/establish-ste-technical-documentation-standard.md that tests reject changed identifiers, configuration values, ownership, conditions, or normative force. The same feature item requires focused boundary tests for ordinary communication and non-document artifacts.

## Requirements

- Add separate negative test cases or assertions for a changed identifier, a changed configuration value, and a changed owner.
- Add a negative activation fixture that shows STE does not activate for ordinary communication or a non-document artifact.
- Keep the tests focused on semantic-preservation and activation-boundary behavior.
- Preserve the existing STE feature scope and do not change its lifecycle from this defect item.

## Acceptance Criteria

- A mutation that changes an identifier causes the focused test to fail.
- A mutation that changes a configuration value causes the focused test to fail.
- A mutation that changes ownership causes the focused test to fail.
- A negative activation fixture proves that STE does not apply to ordinary communication or a non-document artifact.
- The focused STE test module passes after the added cases are in place.
- Independent review confirms that the added tests detect the reported mutation gap.

## Dependencies

None.

## Verification

- Run the focused test module:

```text
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.11 -m unittest -v scripts.test_ste_technical_writing
```

- Demonstrate that each reported semantic mutation is rejected by its corresponding negative case or assertion.
- Obtain independent Dev Code Reviewer confirmation of the test coverage.
- Run git diff --check for the delivery diff.

## Open Questions

None.

## Notes

This defect is attached to the current STE delivery at backlog/feature-backlog/establish-ste-technical-documentation-standard.md. The original coder owns the runnable next action. This defect record authorizes no dispatch, implementation ownership, or lifecycle transition for the parent feature.
