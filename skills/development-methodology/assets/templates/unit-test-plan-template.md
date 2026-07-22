<!--
Copyright (c) 2025 Martin Bechard [martin.bechard@DevConsult.ca]
This software is licensed under the MIT License.
File path: skills/development-methodology/assets/templates/unit-test-plan-template.md
1-line summary: Template for a source-backed unit test plan.
-->

# TODO Unit Test Plan

## Current Understanding

TODO: Describe the unit, behavior, and reason a durable test plan is needed.

## Authoritative Sources

TODO: Link behavior contracts, designs, source code, callers, dependencies, defects, existing tests, and project guidance.

TODO: Record how conflicts between intended and current behavior are handled.

## Related Code

TODO: Link the implementation boundary and direct collaborators, or say Not yet identified.

## Related Tests

TODO: Link existing unit, integration, and end-to-end coverage, or say Not yet identified.

TODO: When three or more implementation, test, fixture, snapshot, or configuration paths share a prefix or span two or more folders, show them once as a fenced text tree rather than repeating full paths in scenario lists.

TODO: Path tree example (replace every synthetic segment, package, and file with complete project paths):

```text
src/
├── main/java/com/example/feature/
│   └── FeatureService.java
└── test/java/com/example/feature/
    ├── FeatureServiceTest.java
    ├── fixtures/FeatureFixtures.java
    └── snapshots/feature-result.json
```

TODO: Refer to tree leaves by short label in scenarios and coverage rows; do not repeat the full common prefix for every test.

TODO: When test groups need different boundary or fixture metadata, split them into named subsections by test group. Put one small fenced text tree in each subsection and its metadata immediately after the tree. Do not put multiline trees in Markdown table cells or simulate them with HTML breaks.

## Related Backlog Items

TODO: Link related defects, features, or test work, or say Not yet identified.

## Related Wiki Pages

TODO: Link related functional, architecture, high-level, module, or known-defect pages, or say Not yet identified.

## Open Questions

TODO: Record unresolved behavior, boundary, dependency, fixture, or coverage questions.

## Maintenance Notes

TODO: Record what changes require this plan to be rechecked.

## Unit Boundary

TODO: Name the unit, entry points, responsibilities, callers, state, and external boundaries.

## Test Strategy

TODO: Describe the observable test boundary, fixture approach, isolation policy, and what belongs in integration or end-to-end tests instead.

## Boundary Doubles

TODO: Describe each required stub, fake, spy, or mock by boundary contract and purpose without mandating a library.

## Scenarios

For each scenario provide a stable identifier, source reference, setup, action, expected result, and applicability notes.

### TODO Scenario Identifier And Name

- Source: TODO
- Setup: TODO
- Action: TODO
- Expected result: TODO
- Applicability: TODO

## Coverage Map

TODO: Map responsibilities, invariants, risks, failures, and state transitions to scenario identifiers or explicit gaps.

## Verification

TODO: List the focused and broader commands expected during implementation and review, or say Not yet identified.
