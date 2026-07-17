---
name: agent-scenario-design
description: Derive a compact high-value scenario set from one canonical conceptual agent definition without turning every assigned skill into a separate test obligation.
metadata:
  category: evaluation
---

# Agent Scenario Design

Use this project skill when creating or refreshing scenarios for one agent-owned suite.

## Inputs

- Canonical conceptual agent definition.
- Generated native adapter selected for the harness.
- Existing executable fixtures and governed Judge checks.
- Current suite manifest and prior evidence.

## Workflow

1. Extract the agent responsibility, repository mutation policy, decisions, workflow, delegation, review, failure handling, completion rules, examples, skills, output contract, and model stages.
2. Identify the few behaviors whose failure would most harm an end user.
3. Define a representative success scenario.
4. Define a material boundary, refusal, no-change, or blocked scenario.
5. Define a dependency, verification, correction, or recovery scenario when the role contract contains that path.
6. For every scenario, state the task, fixture, initial state, required behavior, forbidden behavior, allowed dependencies, deterministic gates, semantic rubric, expected outputs, and terminal status.
7. Reuse an existing synthetic fixture when it proves the contract. Propose a new fixture only when the current fixtures cannot expose a material role behavior.
8. Mark scenarios stale when the role or native adapter digest changes.

## Coverage Rule

Evaluate the agent contract, not the size of its skill list. Select a skill probe only as a diagnostic control for a scenario whose observable behavior depends on that skill. A representative technology path is sufficient unless the agent definition itself promises technology-specific behavior.

## Result

Return the scenario catalog change, role-contract traceability, fixture decision, Judge plan, and any important role behavior deliberately deferred.
