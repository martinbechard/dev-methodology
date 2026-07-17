# Agent Test Suite Protocol

## Purpose

This tree evaluates one conceptual agent at a time. Test scenarios come from the complete canonical agent definition rather than from an attempt to exercise every assigned skill independently.

The existing evaluation runner, disposable workspaces, evidence receipts, deterministic checks, Judge contracts, and containment reporting remain the execution substrate. Agent suites own scenario selection, orchestration, and agent-level acceptance.

## Source Authority

Use the following authority order when a suite contract disagrees with another artifact:

1. The canonical conceptual agent definition under agents/roles.
2. The generated native agent selected for the harness.
3. This common protocol.
4. The agent suite manifest and scenario catalog.
5. The shared and suite-specific project skills.

Freeze the canonical definition digest and native adapter digest before a run. A result is stale when either digest changes.

Keep every fixture synthetic. Do not place personal information, customer information, company-confidential information, credentials, private source material, or production data in a fixture, prompt, capture, or result.

## Suite Structure

Each direct child folder named in suite-index.yaml represents one agent under test and must contain:

- suite.yaml with hardcoded target, project-agent, project-skill, dependency, concurrency, and evidence contracts.
- scenarios.yaml with scenarios derived from the target agent definition.
- agents/supervisor.toml.
- agents/judge.toml.
- One suite-specific skill package shared by the supervisor and Judge.

The skills folder at this root contains methods shared by agents in more than one suite. Do not copy those methods into individual agent definitions.

## Orchestration And Concurrency

- The root coordinator may launch at most four suite supervisors concurrently.
- Each supervisor may have exactly one active child agent at a time.
- A supervisor invokes children sequentially: target agent, deterministic evidence worker when needed, Judge, then any correction owner.
- A supervisor never runs the target agent and Judge concurrently.
- The normal ceiling is nine active agents: one root coordinator, four supervisors, and four supervisor children.
- One active child may create one additional nested agent only when the canonical target workflow requires that dependency and the suite manifest allows it. This temporary tenth agent must finish before another nested dependency starts.
- A supervisor may not bypass the limit by launching background agents, duplicate Judges, or speculative fixture workers.
- The root coordinator owns cross-suite scheduling. A suite supervisor owns only its suite run.

## Supervisor Protocol

The supervisor must:

1. Read the hardcoded suite manifest and selected scenario.
2. Compare the scenario with the current canonical agent definition and stop as stale if the contract has drifted.
3. Resolve every fixed and conditional target skill against the frozen task and allowed writes. Stage every applicable skill before target invocation. A missing applicable skill is a critical preflight BLOCKED result; the target must not work around it.
4. Freeze the fixture, task, allowed inputs, allowed writes, applicable target skills, expected state transitions, and deterministic acceptance gates.
5. Invoke the standard generated target agent named by the suite. Do not replace it with a generic worker.
6. For Codex, require underscore-safe project-agent names and verify each spawned thread against the staged agent name and developer instructions. A task label, child path, or polished final response is not identity evidence.
7. Permit only the dependencies listed by the suite and only when the canonical target workflow requires them.
8. Capture the target transcript, final response, changed artifacts, commands, state transitions, delegation events, identity evidence, and cleanup evidence.
9. Run deterministic gates before invoking the Judge. Missing or mismatched project-agent identity is a critical failure that skips semantic judgment.
10. Give the Judge a fresh context containing only governed evidence and the acceptance contract.
11. Record PASS, FAIL, BLOCKED, or STALE with exact evidence and remaining risk.

The supervisor coordinates and classifies. It must not award semantic credit to its own target run.

## Scenario Design Protocol

Derive scenarios from the target definition's responsibility, mutation policy, instructions, examples, assigned skills, output contract, model stages, agent dependencies, and terminal outcomes.

Prioritize agent-level value:

- A representative successful outcome.
- A material boundary, refusal, or no-change path.
- A dependency, verification, or failure-recovery path when the definition contains one.
- Output-contract completeness and terminal-status integrity in every scenario.

Do not create one scenario per skill. Include an assigned skill only when it materially affects the observable target-agent behavior in the selected scenario. Technology variants are representative coverage, not an exhaustive matrix.

## Judge Protocol

- The Judge is read-only and independent from the target run.
- Deterministic critical failures are terminal and skip semantic judgment.
- The Judge evaluates only the frozen scenario contract, canonical definition, governed evidence, and allowed authoritative sources.
- The Judge must not infer actions from polished prose when the required trace, artifact, command, state, or delegation evidence is absent.
- The Judge reports dimension-level evidence, critical failures, final verdict, and residual uncertainty.
- The Judge does not edit the fixture, candidate output, scenario, rubric, or expected result.

## Mutation And Claims

Apply the existing evaluation runner's disposable-workspace and evidence-root boundaries. Any repository mutation outside a disposable run requires a normal repository claim. Suite agents must not write into another suite's folder or evidence area.

For Codex runs, stage only the hardcoded supervisor, target, allowed dependencies, and Judge under the isolated CODEX_HOME agents directory. Enable multi-agent identity support and retain session metadata that binds each child to its custom agent name and loaded developer instructions. Project-folder discovery or a matching task name alone does not satisfy the identity gate.

Mutation scenarios require a disposable permission profile that permits the declared workspace and its Git metadata while denying writes outside the fixture and runner-owned evidence roots. The ordinary workspace-write sandbox is insufficient when the target contract requires claim and commit operations under the Git directory.

Fixture and result cleanup is part of completion. A run cannot pass with an owned process, port, browser profile, worktree, claim, or temporary credential still active.

## Status Vocabulary

- PASS means every critical deterministic gate passed and the required semantic Judge accepted the run.
- FAIL means the governed evidence demonstrates a target-agent contract violation.
- BLOCKED means the run could not reach a verdict because a required dependency, harness feature, fixture capability, or approved authority was unavailable.
- STALE means a governed source, adapter, scenario, fixture, rubric, or evidence digest no longer matches the run.

Do not relabel BLOCKED or STALE as PASS or FAIL.
