# Replace Evaluation Oracle Terminology With Judge

Status: Starting

Type: Defect

Provider: file

Work Item ID: replace-evaluation-oracle-terminology-with-judge

Completion: main-branch

## Summary

Use Judge as the preferred term for the evaluator that assesses an Evaluation result. Replace evaluation-related Oracle terminology in maintained sources, fixtures, generated artifacts, and human-facing output without changing evaluation behavior.

## Context

The project already uses Judge for model-based evaluation agents and defines Evaluator agent in terminology.md. Some evaluation fixtures, tests, contracts, comments, errors, and output still use Oracle for the evaluator, expected-result logic, or evaluator-owned files. This mixed vocabulary makes one evaluation role appear to have multiple meanings.

The current primary source scan found evaluation-related Oracle usage in the methodology-design-system review coordinator fixture and the Dev Code Reviewer evaluation suite. Historical records, exact identifiers, retained quotations, and compatibility-sensitive machine fields may require preservation or an explicit migration rather than blind replacement.

## Source Evidence

On 2026-08-12, the user directed: “Terminology: we shouldn't use oracle, we should use judge to mean the evaluator in evaluations. Please create a work item to update the terminology.” This request authorizes creation of this terminology-correction work item.

## Requirements

- Add Judge to terminology.md as the preferred term for the evaluator that applies Evaluation criteria and produces or validates an Evaluation result.
- State the relationship between Judge and Evaluator agent so the terms do not create competing roles.
- Record Oracle as avoided terminology when it means the evaluator in project Evaluations, because observed maintained sources already use that substitution repeatedly.
- Inventory maintained evaluation sources, fixtures, tests, comments, errors, labels, documentation, and generated artifacts for Oracle terminology.
- Replace evaluation-related prose and user-facing labels with Judge or a more precise term such as expected result when Judge is not the intended concept.
- Update canonical sources before regenerating supported derived artifacts.
- Preserve exact historical quotations, immutable evidence, external terminology, and compatibility-sensitive identifiers when renaming would alter source truth or break a contract.
- When a compatibility-sensitive identifier must remain, document the boundary and keep human-facing terminology aligned with Judge.
- Do not change evaluator behavior, evaluation criteria, verdict semantics, or evidence authority as part of the terminology correction.

## Acceptance Criteria

- terminology.md contains one unambiguous Judge entry and an evidence-backed avoided use of Oracle for evaluation evaluators.
- Maintained evaluation prose and user-facing output use Judge instead of Oracle when referring to the evaluator.
- Remaining Oracle occurrences are individually justified as exact historical, external, or compatibility-sensitive uses, or use a distinct non-evaluator meaning.
- Canonical sources and supported generated artifacts are consistent and fresh.
- Existing Evaluation and Judge behavior remains unchanged.
- Focused terminology, evaluation-fixture, generation, and bundle-content checks pass.

## Dependencies

None.

## Verification

- Search maintained project sources for case-insensitive whole-word Oracle occurrences and classify every remaining match.
- Run focused tests for each changed Evaluation fixture or suite.
- Run terminology structure and application checks for terminology.md.
- Regenerate supported outputs when canonical sources change and run affected freshness checks.
- Run git diff --check and obtain independent review of the terminology boundary and preserved identifiers.

## Open Questions

- Which existing Oracle identifiers are compatibility-sensitive and require a staged migration instead of direct renaming?
- Where Oracle currently means deterministic expected-result data rather than an evaluator, should the replacement be expected result, reference result, or another precise term?

## Notes

- This item governs project terminology and its application. It does not rename third-party products or rewrite historical evidence.
- Use Judge only for the evaluation actor or evaluator role. Do not use Judge as a generic synonym for every assertion, comparison function, fixture, or expected-result file.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T11:43:10Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e8923f2cb1fe967806a0542359d15af01d94ac19` on primary `main`.
- Capacity: Slot 2 of 5. Independent terminology/evaluation scope; exclude private Backlog Dispatcher, document provenance, Dev Orchestrator routing, and documentation-template parser paths.
- Transition Claims: `start-replace-evaluation-oracle-terminology-with-judge-work-item`; event `4923f794-562d-422e-a1d2-f7599efbace4`. `start-replace-evaluation-oracle-terminology-with-judge-provider`; event `a1c95fda-d302-4200-a62d-0d469bdfb783`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T11:44:58Z.
- Codex Task ID: `019ffaf0-4bd1-72a1-b66d-335c429a88be`.
- Conversation ID: `019ffaf0-4bd1-72a1-b66d-335c429a88be`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Replace Evaluation Oracle Terminology With Judge`.
- Initial Action: Launch one Dev Orchestrator subagent for this authoritative provider record.
- Creation Outcome: Unique success with no client or pending identity and no retry. The caller decoded a JSON-string tool envelope containing this complete canonical result.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-oracle-judge-visible-task`; event `d3ea8fb8-7d63-49fb-8bf4-67efd74ca7c5`. `adopt-oracle-judge-provider`; event `45ee8b72-6ed6-4fa3-8a8f-470709fffa79`.
