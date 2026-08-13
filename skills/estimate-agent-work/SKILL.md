---
name: estimate-agent-work
description: Estimate AI-delivered engineering work in complexity, generated tokens, autonomous turns, agent-hours, separate non-model runtime, expected parallelism, and wall-clock time without presenting human person-days as the primary effort measure.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: af7e6f78-ef7b-494a-a0dd-f4925cd7603d
Created-UTC: 2026-08-13T10:15:05Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: medium
Task-ID: 019ffa3d-191f-7343-aaeb-2499de1ad605
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Estimate Agent Work

Estimate the AI effort and elapsed time for an accepted engineering scope. Keep the estimate
explicit enough to revise when evidence changes. This skill estimates delivery; it does not own
backlog priority, architecture, scope acceptance, dispatch, resource allocation, or acceptance.

## Required Inputs

- The accepted outcome, boundaries, dependencies, and verification expectations.
- Known repository, integration, environment, and coordination constraints.
- An assumed or observed generated-output throughput with its model, reasoning profile,
  harness, and execution environment. Use `default_generated_tokens_per_second: 50` only when
  no better scoped observation is available, and label it as an assumption.
- Known non-model waits and whether each one blocks the dependency critical path.

Do not treat an assumed throughput as a universal model rate or delivery promise. Input and
cached tokens affect context pressure and can affect monetary cost, but do not convert them
through the generated-output throughput rate.

## Score Complexity

Score the whole accepted scope at one fixed level. Explain the strongest range drivers across
reasoning uncertainty, integration breadth, verification burden, correction risk, and
coordination depth.

| Level | Reasoning uncertainty | Integration breadth | Verification burden | Correction risk | Coordination depth |
| --- | --- | --- | --- | --- | --- |
| 1 — Low | Known solution and local facts | One isolated boundary | One focused check | Small reversible correction | One owner and no handoff |
| 2 — Moderate | Some discovery or choice | Several related files or one integration | Focused tests plus a nearby regression | Bounded rework is plausible | One planned handoff or dependency |
| 3 — High | Material unknowns or design tradeoffs | Several components, generators, or runtimes | Multiple test layers or environments | Review can require meaningful redesign | Multiple ordered owners or shared resources |
| 4 — Very high | Novel, ambiguous, or adversarial reasoning | Cross-system or migration-scale effects | Broad, live, security, or platform verification | Expensive rollback or repeated correction risk | Several dependent agents, approvals, or external parties |

Do not average away one dominant risk. Use a range wide enough for unresolved factors and name
what evidence would narrow it.

## Estimate Generated-Token Effort

Estimate implementation generation, including hidden reasoning when the runtime reports or
budgets it as generated output. Report a low and high range. Keep live-evaluation consumption
separate even when the same model executes both activities.

Use these formulas for both range bounds:

```text
generated_tokens_per_agent_hour = generated_tokens_per_second × 3,600
agent_hours = implementation_generated_tokens ÷ generated_tokens_per_agent_hour
```

With the default planning assumption, `50 × 3,600 = 180,000` generated tokens per agent-hour.
Record whether the throughput is `assumed` or `observed`; an observed override applies only to
the recorded model, reasoning profile, harness, and execution environment.

Input and cached tokens are not generated-token effort. Record them only as context or optional
cost inputs. Do not combine implementation generation with live-evaluation input, cached, or
generated tokens.

## Estimate Autonomous Turns

A turn is one checkable work cycle: obtain or change evidence, perform a bounded action, and
inspect the result before selecting the next action. Estimate a low and high turn count from the
dependency graph, likely correction loops, and required handoffs. A turn is not a user-message
count and turns are not equal-duration time units.

## Separate Runtime And Parallelism

Report each non-model runtime range separately:

- `tool_runtime`
- `build_runtime`
- `test_runtime`
- `browser_runtime`
- `live_evaluation_runtime`
- `external_service_runtime`
- `approval_runtime`
- `other_runtime`

For each range, record one disposition: `blocking` when it extends its dependency path,
`parallelizable` when it overlaps another interval on that path, or `off_critical_path` when it
belongs only to a path that does not set delivery duration. Also record its dependency `path`
and an `overlap_group` for intervals that run concurrently. Within one path, add serial intervals
and take the maximum duration of intervals in the same overlap group. Do not double-count a wait
merely because more than one workstream observes it.

Record live-evaluation consumption separately with its own input, cached, generated-token, and
runtime ranges. Do not relabel live-evaluation consumption as implementation generation.

Calculate:

```text
total_agent_hours = sum(all implementation-generation agent-hours)
path_delivery_hours = path_generated_effort_agent_hours + path_non_model_runtime_hours
wall_clock_duration_hours = max(path_delivery_hours for every dependency path)
```

The generated-effort critical path is the path with the greatest implementation-generation
agent-hours. The delivery critical path is the path with the greatest combined generated effort
and path runtime. They can be different. When reporting `critical_path_agent_hours`, name the
selected path and include only its generated effort. Never select a generation-only path and
then add runtime from another path.

Report `expected_parallelism` as the expected concurrent agent count or a bounded range and name
which workstreams and waits can overlap. Parallelism does not reduce total agent-hours. It can
reduce wall-clock time only when the dependency graph permits overlap.

## State Uncertainty And Confidence

State the assumptions, low- and high-range drivers, evidence gaps, and a confidence of `low`,
`medium`, or `high`. Prefer ranges to point values. Widen the range for unresolved integration,
environment, review, or correction risk.

Do not use person-days as the primary AI effort measure. If a stakeholder needs a human-calendar comparison, label it as a separate derived
communication aid rather than model effort.

Only include monetary cost when current prices are supplied or verified. Identify the price
source and effective date, preserve provider-specific input, cached, output, and live-evaluation
categories, and keep cost distinct from generated-token effort and elapsed time.

## Estimation Procedure

1. Confirm the accepted scope, dependencies, delivery gates, and missing evidence.
2. Select one complexity level and explain every factor that sets or widens the range.
3. Estimate implementation generated tokens and autonomous turns by dependency-ordered workstream.
4. Record the throughput value, evidence kind, model, reasoning profile, harness, and environment.
5. Convert each implementation range to agent-hours and sum total effort.
6. Calculate every path's generated effort and runtime, including serial and overlapping intervals.
7. Select wall-clock duration from the longest combined delivery path, name its generated-only `critical_path_agent_hours`, and separately identify a different generated-effort critical path when applicable.
8. Record separate live-evaluation consumption, uncertainty, confidence, and optional price-backed cost.
9. Return the reusable shape with compact arithmetic and the evidence that would change it.

## Serial Example

One workstream is estimated at 180,000–360,000 implementation generated tokens, or 1.0–2.0
generated-effort agent-hours at the assumed 50 generated tokens per second. It needs 3–5
autonomous turns and 0.5–0.5 hours of serial blocking test runtime on the same path. With
`expected_parallelism: 1`, total and critical-path agent-hours are both 1.0–2.0, and the combined
path produces 1.5–2.5 wall-clock hours. A live evaluation
may separately consume 100,000 input tokens, 20,000 cached tokens, 40,000 generated tokens, and
0.25 runtime hours; none of those tokens are implementation generated-token effort.

## Parallel Example

Two independent workstreams total 360,000–540,000 implementation generated tokens, or 2.0–3.0
total agent-hours. Each path has 1.0–1.5 generated-effort agent-hours. On each path, 0.25–0.5
hours of overlapping build runtime and 0.25–0.5 hours of overlapping test runtime share one
overlap group, so they contribute 0.25–0.5 hours rather than 0.5–1.0 hours. With
`expected_parallelism: 2`, the longest combined path is 1.25–2.0 wall-clock hours. Parallelism
does not reduce total agent-hours: the estimate remains 2.0–3.0.

## Asymmetric Path Example

The generation-heavy path A has 1.5 generated-effort agent-hours and 0.25 hours of path runtime,
for 1.75 delivery hours. The runtime-heavy path B has 0.75 generated-effort agent-hours and 1.5
hours of path runtime, for 2.25 delivery hours. Path B is therefore the 2.25-hour delivery
critical path and reports `critical_path_agent_hours: 0.75`, while path A remains the separate
generated-effort critical path. A 0.5-hour external-service wait overlaps a 0.5-hour test wait in
the same path overlap group and is not double-counted; together they contribute 0.5 hours.

## Reusable Estimate Shape

```yaml
estimate:
  complexity:
    level: 2
    factors:
      reasoning_uncertainty: "bounded discovery"
      integration_breadth: "one generator and its projections"
      verification_burden: "focused and repository checks"
      correction_risk: "review may require one bounded revision"
      coordination_depth: "implementation, review, verification"
  throughput:
    default_generated_tokens_per_second: 50
    value_generated_tokens_per_second: 50
    evidence_kind: assumed # assumed or observed
    model: "recorded model or unknown"
    reasoning_profile: "recorded profile or unknown"
    harness: "recorded harness or unknown"
    execution_environment: "recorded environment or unknown"
  paths:
    path-a:
      generated_tokens: {low: 180000, high: 360000}
      generated_effort_agent_hours: {low: 1.0, high: 2.0}
      autonomous_turns: {low: 3, high: 5}
    path-b:
      generated_tokens: {low: 90000, high: 135000}
      generated_effort_agent_hours: {low: 0.5, high: 0.75}
      autonomous_turns: {low: 1, high: 2}
  live_evaluation:
    input_tokens: {low: 0, high: 0}
    cached_tokens: {low: 0, high: 0}
    generated_tokens: {low: 0, high: 0}
    runtime_hours: {low: 0.0, high: 0.0}
  non_model_runtime:
    tool_runtime: {low: 0.0, high: 0.0, disposition: off_critical_path, path: path-b, overlap_group: null, overlaps_with: []}
    build_runtime: {low: 0.25, high: 0.5, disposition: parallelizable, path: path-a, overlap_group: compile-and-test, overlaps_with: [test_runtime]}
    test_runtime: {low: 0.25, high: 0.5, disposition: parallelizable, path: path-a, overlap_group: compile-and-test, overlaps_with: [build_runtime]}
    browser_runtime: {low: 0.0, high: 0.0, disposition: off_critical_path, path: path-b, overlap_group: null, overlaps_with: []}
    live_evaluation_runtime: {low: 0.0, high: 0.0, disposition: off_critical_path, path: path-b, overlap_group: null, overlaps_with: []}
    external_service_runtime: {low: 0.0, high: 0.0, disposition: off_critical_path, path: path-b, overlap_group: null, overlaps_with: []}
    approval_runtime: {low: 0.0, high: 0.0, disposition: blocking, path: path-a, overlap_group: null, overlaps_with: []}
    other_runtime: {low: 0.0, high: 0.0, disposition: off_critical_path, path: path-b, overlap_group: null, overlaps_with: []}
  path_summaries:
    path-a:
      generated_effort_agent_hours: {low: 1.0, high: 2.0}
      serial_runtime_hours: {low: 0.0, high: 0.0}
      overlap_runtime_hours: {low: 0.25, high: 0.5}
      non_model_runtime_hours: {low: 0.25, high: 0.5}
      combined_delivery_hours: {low: 1.25, high: 2.5}
    path-b:
      generated_effort_agent_hours: {low: 0.5, high: 0.75}
      serial_runtime_hours: {low: 0.0, high: 0.0}
      overlap_runtime_hours: {low: 0.0, high: 0.0}
      non_model_runtime_hours: {low: 0.0, high: 0.0}
      combined_delivery_hours: {low: 0.5, high: 0.75}
  total_agent_hours: {low: 1.5, high: 2.75}
  generated_effort_critical_path: {path: path-a, agent_hours: {low: 1.0, high: 2.0}}
  delivery_critical_path: {path: path-a, combined_hours: {low: 1.25, high: 2.5}}
  critical_path_agent_hours: {path: path-a, low: 1.0, high: 2.0}
  expected_parallelism: {low: 1, high: 1, overlap: []}
  wall_clock_duration_hours: {low: 1.25, high: 2.5}
  uncertainty:
    assumptions: []
    low_range_drivers: []
    high_range_drivers: []
    evidence_that_would_change_estimate: []
  confidence: medium
  monetary_cost: null # include a priced breakdown only with supplied or verified current prices
```

## Result

Return the complexity decision, implementation generated-token and autonomous-turn ranges,
throughput metadata, total and critical-path agent-hours, expected parallelism, separate runtime
and live-evaluation ranges, wall-clock range, uncertainty, confidence, and any price-backed cost.
Name material unknowns and the evidence that would narrow or revise the estimate.
