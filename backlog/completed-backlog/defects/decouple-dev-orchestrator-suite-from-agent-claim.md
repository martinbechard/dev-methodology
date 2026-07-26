# Decouple The Dev Orchestrator Evaluation From Claim Files

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/decouple-dev-orchestrator-suite-from-agent-claim.md

Completion: direct-main

## Problem

The Dev Orchestrator evaluation supports projects that do not use claims.

The evaluator currently fails such a project when its Git metadata already contains an
empty claim registry or claim-event history. Those repository-wide files can predate the
evaluation. Their presence does not prove that the evaluated scenario used the claim
helper.

## Required Change

When resource coordination is `none`:

- Allow a pre-existing claim registry.
- Allow pre-existing claim-event history.
- Reject an actual claim-helper invocation by the evaluated scenario.
- Reject claim evidence reported by the evaluated scenario.

When resource coordination is `agent-claim`, preserve the existing claim checks.

## Acceptance Criteria

- A no-claim scenario passes when an empty registry already exists.
- A no-claim scenario passes when claim-event history already exists.
- A no-claim scenario still fails when its target or child invokes the claim helper.
- A no-claim scenario still fails when its handoff evidence includes claim-release data.
- The agent-claim companion case still passes.

## Scope

- `evals/agent-tests/runner.py`
- `evals/agent-tests/dev-orchestrator/test_fixtures.py`

The suite configuration already makes `agent-claim` conditional. No skill, conceptual
agent, generated adapter, scenario, or fixture configuration change is needed.

## Prior Attempts

Earlier candidates tried to classify many command forms and bind them to repository claim
files. They were rejected and must not be reused.

This implementation starts from current main. It distinguishes scenario activity from
pre-existing repository files.

## Verification

- Run the focused Dev Orchestrator fixture tests.
- Run Python compilation.
- Run `git diff --check`.

## Delivery Mode

The user directed temporary single-task delivery without claims or delegated agents.

## Completion Evidence

- Implementation commit: `63cd4fe1`.
- A no-claim scenario now ignores pre-existing repository claim files.
- An actual claim-helper invocation by the target or a child still fails.
- Claim-release data remains invalid in no-claim scenario evidence.
- The agent-claim companion case remains covered by the focused fixture suite.
- All 27 focused Dev Orchestrator fixture tests passed.
- Python compilation and `git diff --check` passed.
- No claim was acquired.
- No publication was needed because no distributed skill or agent definition changed.
