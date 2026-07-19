# Enforce Documentation Template Conformance

Status: Ready

Type: Defect

## Summary

Require Dev Documentation Writer to produce complete canonical methodology artifacts on the first bounded contribution attempt.

## Context

The Project Bootstrapper missing-configuration evaluation required a new module design derived from the canonical module design template. Dev Documentation Writer initially omitted required template sections, including Implementation Readiness, and described boundary tests that were absent from the fixture. Repeated correction consumed the contribution budget before the integrated project could reach an accepted steady state.

The complete evaluation did not edit the distributed Dev Documentation Writer or documentation creation skills.

## Evidence

- evals/agent-tests/project-bootstrapper/scenarios.yaml defines the missing-configuration multi-contribution contract.
- evals/agent-tests/project-bootstrapper/fixtures/missing-configuration contains the frozen bootstrap fixture.
- skills/create-module-design and its canonical template define the required module design structure.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the bounded correction failure.
- The live run required two documentation corrections because the first drafts omitted canonical headings and asserted tests not present in the fixture.

## Requirements

- Load and apply the canonical artifact template before drafting the requested document.
- Emit every required heading and readiness section in template order unless the template explicitly marks it optional.
- Ground test, verification, and implementation statements in supplied repository evidence.
- Do not invent boundary tests, completed verification, or implementation state.
- Make a deterministic template-conformance check part of the writer handoff.
- Add focused coverage for complete first-attempt module design generation.

## Acceptance Criteria

- A missing module design contains every canonical required section on the first bounded contribution attempt.
- Implementation Readiness is present and evidence-backed.
- Test descriptions match files and commands present in the fixture.
- The Project Bootstrapper missing-configuration scenario no longer spends correction rounds on template omissions or invented tests.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused template-conformance tests for Dev Documentation Writer.
- Compare the generated module design headings with the canonical template.
- Run the Project Bootstrapper missing-configuration scenario and inspect contribution count, reviewer evidence, and cleanup.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- This item concerns source-faithful completeness, not prose length.
