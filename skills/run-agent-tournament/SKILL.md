---
name: run-agent-tournament
description: Plan, run, resume, rescore, audit, and report controlled tournaments among agent definitions, semantic model profiles, provider models, reasoning efforts, or prompts under one fixed task contract. Use for comparative selection from repeatable evidence; do not use for ordinary single-model testing.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: f0a1243f-b56a-4e10-9817-bf4f060c6aaf
Created-UTC: 2026-08-09T04:41:52Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe4cb-b4f3-7563-8ece-a60e567aae29
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Run Agent Tournament

An agent tournament compares two or more candidates under one fixed task contract. Use it to make a controlled selection from repeatable evidence. Keep ordinary single-model testing with the calling task.

## Modes

- Plan-only defines the decision, controls, candidate matrix, stages, and dry-run matrix. It needs no live-run authorization. Mark every unresolved planning assumption.
- Live execution runs an authorized frozen contract and preserves the complete evidence for each invocation.
- Resume reuses only completed schema-valid runs. It executes another attempt only through the frozen retry policy.
- Deterministic rescore recomputes validity, scores, costs, rankings, or reports from retained evidence. It makes zero live calls and preserves auditable caller-owned proof of that fact.
- Audit and report verify an existing tournament and communicate its result. They do not add live calls without a separate authorized execution mode.

Read [Tournament Contract](references/tournament-contract.md) completely when you freeze, execute, resume, deterministically rescore, audit, or report a tournament. Do not load the reference only to decide whether this skill applies or to outline an unfrozen plan.

## Clarify Material Gaps

Before live execution, ask the smallest useful set of questions when a missing answer can change attribution, validity, ranking, cost, or data exposure. Explain why each answer changes the experiment.

Material gaps include:

- the decision, role under test, varied factor, or held constants;
- the candidates, availability, fixtures, reviewed ground truth, output schema, or scoring semantics;
- the ranking policy, equivalence tolerances, tie-breakers, stages, retry policy, variance policy, repeats, or advancement rules;
- live-run authority, budget, pricing treatment, evidence location, or stop conditions;
- the data-safety boundary for candidate inputs.

Concise clarification examples include:

- Are we selecting the runner or the coordinator? Holding the other role constant is necessary for attribution.
- No reviewed ground truth is available. Should planning propose synthetic fixtures for approval, or should it use designated real tasks?
- One candidate is unpriced. Should its cost-dependent result remain provisional, or does an accepted comparison rule apply?

Separate runner and coordinator tournaments when they are distinct roles. For a coordinator comparison, freeze the runner reports and their hashes before any coordinator call.

Planning may use explicit non-blocking assumptions. Never carry an assumption silently into paid or otherwise consequential execution. Missing reviewed ground truth may produce a fixture proposal for approval, but it stops live calls.

## Run The Tournament

1. Select the mode and state the decision that the tournament will support.
2. Resolve material gaps or stop before live calls.
3. Freeze the complete contract, including retry and variance policies. Enumerate every authorized invocation in a dry-run matrix.
4. State a live-call maximum that includes live preflight and allowed retries. Obtain explicit authority for consequential execution.
5. Validate fixtures, ground truth, runtime schema support, transport, and output capture independently from candidate output quality. Make transport and capture preflight with zero live model calls, or enumerate and authorize each live preflight invocation in the matrix.
6. Hold each case input byte-equivalent across candidates. Vary one factor at a time unless the contract declares each varying factor and the attribution limitation.
7. Execute or resume the frozen matrix within its authorization, budget, retry limits, and call maximum. Preserve exact configuration, raw output, usage, transport evidence, timing, validity, and score evidence.
8. Rank and advance candidates only through the frozen rules. Repeat leading candidates when variance matters.
9. Obtain an independent audit when the selection is material.
10. Report the decision, complete ranking, invalid runs, evidence limits, confidence, and any provisional status.

## Default Ranking

Require an explicit ranking policy. If the caller supplies none, offer this default for acceptance:

1. Rank exact accuracy first. Do not infer an accuracy-equivalence tolerance.
2. Compare cost only within the same accuracy tier.
3. Treat costs within exactly 15 percent of the cheaper candidate as equivalent.
4. Compare wall-clock time only within an equivalent-cost band.

Calculate usage cost without charging cached input twice:

```text
uncached input = max(total input - cached input, 0)
```

Price uncached input, cached input, and output separately. Never invent a missing price. Keep an unpriced candidate visible with its accuracy and usage evidence. Mark a winner or ordering as provisional when it depends on an unavailable price and no accepted comparison rule resolves it.

If unknown cost prevents ordering a tied accuracy tier, report a partial unresolved ranking. Stop affected advancement or winner selection until the caller accepts a rule or supplies the price. A uniquely higher-accuracy unpriced candidate remains the accuracy leader because that lead does not depend on cost.

## Validity And Evidence

Classify infrastructure, transport, schema, and missing-artifact failures as invalid runs. Do not score them as candidate inaccuracy unless the frozen task contract explicitly assigns that failure to the candidate.

Retain enough evidence to reproduce validity, scoring, cost arithmetic, stage ranking, advancement, and selection. Keep invalid evidence instead of hiding it. A one-run-per-case result is screening evidence with unmeasured variance, not statistical proof.

Require a frozen variance metric, aggregation, acceptable limit, maximum repeats, and advance-or-stop disposition. A screening-only policy forbids a definitive winner while variance is unmeasured or remains unstable.

For deterministic rescore, retain proof from the caller-owned execution boundary. Use a disabled call mechanism or complete invocation ledger or telemetry for the rescore window. Unchanged evidence digests support this proof but do not replace it.

Before a model call, confirm that no fixture contains unauthorized PII or company-confidential information. If sensitive material is necessary, require explicit authority for its use and candidate exposure.

## Result

Return:

- the frozen contract and dry-run call count;
- per-run validity, scores, usage, cost, and elapsed time;
- per-stage rankings and advancement evidence;
- the winner and complete or explicitly partial ranking, including unresolved unpriced ties;
- misses, invalid runs, limitations, variance evidence, confidence, and provisional status;
- retry attempts, live-preflight calls, actual calls, the authorized maximum, and zero-call rescore proof;
- independent audit evidence for a material decision;
- a semantic model-profile handoff for the selected configuration.

Keep provider identifiers in runtime configuration, evidence, or adapter mappings. Do not place them in reusable conceptual agent definitions.

## Non-Goals

- Do not define the domain task, fixtures, ground truth, output schema, or scoring semantics.
- Do not provide runtime commands or a live-call mechanism.
- Do not prescribe a provider, model family, reasoning effort, prompt, or tournament shape.
- Do not treat synthetic fixtures as proof of real-world completeness.
- Do not replace domain reviewers, ground-truth owners, or independent verification.
- Do not install, deploy, publish, or activate the selected configuration.
