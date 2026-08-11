# Fix Future Ideas Evaluation Projection

Status: Starting

Type: Defect

Provider: file

Work Item ID: fix-future-ideas-evaluation-projection

Completion: main-branch

Owner: Unowned pending accepted execution

## Summary

Restore the focused backlog-steward evaluation documentation check for the `future-ideas-capture-and-promotion` scenario without changing unrelated methodology behavior.

## Context

Independent verification of `create-direct-mcp-development-planning-skill` ran a broader evaluation-document test and found one failure in the backlog-steward scenario row. The failing test method and scenario input are byte-identical to the verified candidate base, so the defect is outside that delivery.

## Source Evidence

Dev Verifier confirmed on 2026-08-11 that `scripts.test_agent_skill_evaluation_docs.AgentSkillEvaluationDocumentationTests.test_backlog_steward_rows_publish_neutral_resource_coordination_variants` fails for the `future-ideas-capture-and-promotion` scenario. The verifier reproduced the failure with Python 3.11 and confirmed that the implicated test and scenario input were unchanged from base commit `d737842859165bded535a02c8be19efff41e28ad`.

## Requirements

- Determine whether the scenario source, evaluation projection, or focused expectation is stale.
- Correct only the source of the mismatch and its directly affected generated projection or focused expectation.
- Preserve the intended neutral resource-coordination variants for the backlog-steward scenario.
- Use repository-authorized generators for generated outputs.
- Do not change a correct canonical contract only to make a stale test pass.

## Acceptance Criteria

- The focused backlog-steward evaluation-document test passes with a repository-supported Python 3.11 or newer interpreter.
- The `future-ideas-capture-and-promotion` scenario row contains the intended neutral resource-coordination variants.
- Directly affected generated evaluation documentation is source-current.
- Focused regression and Git diff checks pass.

## Dependencies

None.

## Verification

- Run `/opt/homebrew/bin/python3.11 -m unittest -v scripts.test_agent_skill_evaluation_docs.AgentSkillEvaluationDocumentationTests.test_backlog_steward_rows_publish_neutral_resource_coordination_variants`.
- Run the affected evaluation-document generator freshness check.
- Run focused source/projection consistency checks and `git diff --check`.
- Obtain fresh independent source review and verification before delivery.

## Open Questions

- Which authoritative scenario or projection input currently disagrees with the focused expectation?

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T20:20:49Z

Coordinator: Codex task 019ff271-bb29-7cd2-95da-7b4b9766a1e6

Normalized Objective: Reconcile the future-ideas-capture-and-promotion scenario source, generated evaluation projection, and focused expectation; correct only the authoritative mismatch and directly affected projection or assertion; then complete focused review, verification, main-branch delivery, provider closure, and cleanup.

Intended Root Role: Dev Orchestrator

Launch Result: Requested

Canonical Execution: None

Last Contact At: 2026-08-11T20:20:49Z

Next Reconciliation At: 2026-08-11T20:35:49Z
