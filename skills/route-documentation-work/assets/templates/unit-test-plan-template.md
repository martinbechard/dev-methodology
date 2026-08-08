<!--
{{COPYRIGHT}}
Artifact-ID: {{ARTIFACT_ID}}
Created-UTC: {{CREATED_UTC}}
Creating-Agent: {{CREATING_AGENT}}
Runtime: {{RUNTIME}}
Dispatched-Model: {{DISPATCHED_MODEL}}
Reasoning-Effort: {{REASONING_EFFORT}}
Task-ID: {{TASK_ID}}
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# TODO Unit Test Plan

## Current Understanding

> This section gives implementers and reviewers a shared reason for the plan before they choose test cases. Test authors and reviewers use it during planning and maintenance to identify the unit, behavior, testing need, and current understanding.

TODO: Describe the unit, behavior, and reason a durable test plan is needed.

## Authoritative Sources

> This section keeps planned tests aligned with intended behavior rather than assumptions. Test authors and reviewers use it during discovery and dispute resolution to link controlling contracts, designs, code, defects, and guidance and state how conflicts are handled.

TODO: Link behavior contracts, designs, source code, callers, dependencies, defects, existing tests, and project guidance.

TODO: Record how conflicts between intended and current behavior are handled.

## Related Code

> This section lets test authors locate the implementation boundary and collaborators whose behavior the plan exercises. Test authors use it while designing or updating tests to link the exact code surfaces in scope.

TODO: Link the implementation boundary and direct collaborators, or say Not yet identified.

## Related Tests

> This section prevents duplicate coverage and exposes where unit evidence connects to broader verification. Test authors and reviewers use it during planning and review to map existing tests, fixtures, snapshots, and configuration in a navigable form.

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

> This section preserves why the testing work exists and which delivery outcomes depend on it. Coordinators and test authors use it during prioritization and review to link the defects, features, or test work that the plan supports.

TODO: Link related defects, features, or test work, or say Not yet identified.

## Related Wiki Pages

> This section gives test authors fast access to the behavior and design context needed to judge expected results. Test authors and reviewers use it during scenario design and maintenance to link relevant specifications, designs, and known defects.

TODO: Link related functional, architecture, high-level, module, or known-defect pages, or say Not yet identified.

## Open Questions

> This section exposes uncertainty before it becomes an arbitrary test assumption. Test authors and reviewers use it during discovery and review to record unresolved behavior, boundary, dependency, fixture, or coverage decisions.

TODO: Record unresolved behavior, boundary, dependency, fixture, or coverage questions.

## Maintenance Notes

> This section helps future maintainers know when test intent or coverage must be reconsidered. Test maintainers use it after relevant changes or reviews to record the triggers that can make this plan stale.

TODO: Record what changes require this plan to be rechecked.

## Unit Boundary

> This section prevents tests from exercising an accidental or overly broad subject. Test authors and module owners use it when selecting the test seam to define the unit, entry points, responsibilities, callers, state, and external boundaries.

TODO: Name the unit, entry points, responsibilities, callers, state, and external boundaries.

## Test Strategy

> This section makes the evidence level intentional, helping reviewers distinguish unit concerns from integration or end-to-end concerns. Test authors and reviewers use it before writing scenarios to define observable behavior, isolation, fixtures, and excluded test levels.

TODO: Describe the observable test boundary, fixture approach, isolation policy, and what belongs in integration or end-to-end tests instead.

## Boundary Doubles

> This section prevents test doubles from hiding the contracts and risks they are meant to isolate. Test authors and reviewers use it when a unit crosses boundaries to identify each required double, the contract it represents, and its purpose without prescribing a library.

TODO: Describe each required stub, fake, spy, or mock by boundary contract and purpose without mandating a library.

## Scenarios

> This section turns required behavior and risks into implementable, reviewable examples. Test authors and reviewers use it during test creation and coverage review to define stable scenarios with sources, setup, actions, expected results, and applicability.

For each scenario provide a stable identifier, source reference, setup, action, expected result, and applicability notes.

### TODO Scenario Identifier And Name

> This subsection gives one behavior a stable reference so implementation, reviews, failures, and coverage maps can discuss the same case. Test authors use it for each scenario by copying the subsection and replacing the heading and fields with its source, setup, action, expected result, and applicability.

- Source: TODO
- Setup: TODO
- Action: TODO
- Expected result: TODO
- Applicability: TODO

## Coverage Map

> This section reveals whether important responsibilities and failure paths have evidence or remain explicit gaps. Test reviewers and maintainers use it during review and maintenance to map requirements, invariants, risks, failures, and transitions to scenario identifiers.

TODO: Map responsibilities, invariants, risks, failures, and state transitions to scenario identifiers or explicit gaps.

## Verification

> This section makes completion reproducible for implementers and reviewers instead of relying on an unrecorded local run. Implementers and reviewers use it when executing the plan to list focused and broader commands and the evidence expected from them.

TODO: List the focused and broader commands expected during implementation and review, or say Not yet identified.
