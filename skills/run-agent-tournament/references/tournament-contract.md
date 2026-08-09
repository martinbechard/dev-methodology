<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 4223bf9b-eda1-4473-b949-f9bdc398696d
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

# Tournament Contract

This contract makes a comparative evaluation attributable, resumable, and auditable. Freeze it before consequential execution. The calling task owns domain content and the mechanism that performs live calls.

Use the provider-neutral [example configuration](../assets/tournament.example.yaml) as a shape reference. Replace every placeholder and resolve every pending state before live execution.

## Frozen Contract

Record each field below in one versioned configuration. Store stable references and digests for external artifacts.

| Area | Required fields |
| --- | --- |
| Identity | Tournament identifier, contract version, mode, decision, owner, and evidence location. |
| Attribution | Role under test, factors allowed to vary, held constants, and either one-factor attribution or an explicit multi-factor limitation. |
| Task | Fixed task contract, prompt or request construction, candidate responsibility boundary, and success conditions. |
| Candidates | Stable label, exact runtime configuration or configuration reference, availability, varied value, and pricing state. |
| Cases | Case identifier, input reference and digest, byte-equivalence method, reviewed ground-truth reference and digest, and representative-use limitation. |
| Output | Strict output schema reference and digest, schema validator, runtime schema support, transport contract, and capture location. |
| Scoring | Domain-owned scorer and version, exact matching keys, metrics, aggregation, metric direction, and handling of missing or invalid evidence. |
| Ranking | Ordered objectives, accuracy equivalence, cost-equivalence tolerance, speed tie-break boundary, final tie-breakers, and unpriced-candidate policy. |
| Stages | Ordered stages, candidate source, cases, repeats, completion rule, advancement count, and tie handling. |
| Execution | Caller-owned call mechanism, live authorization, budget, stop conditions, availability result, and expected call count. |
| Pricing | Usage-field meanings, pricing unit, authoritative source, source date or version, per-category rates, and unpriced state. |
| Safety | Allowed data classification, prohibited data, approved sensitive-data use, candidate exposure, retention boundary, and redaction rules. |
| Verification | Independent preflight checks, material-decision reviewer or deterministic verifier, and required report evidence. |

Do not start live execution while a required field is missing or materially ambiguous. Plan-only work may mark a field as pending and state the assumption used to complete the plan.

### Attribution Controls

Use the same task contract, prompt construction, fixtures, schema, scorer, stage rules, and evidence capture for every candidate in a comparison.

Hold each rendered case input byte-equivalent across candidates. Record the input digest used by each run. If a runtime adds candidate-specific wrappers, separate those wrappers from the case bytes and declare the resulting limitation.

Vary one factor at a time. If multiple factors must vary, list each factor and state that the tournament cannot attribute the result to one factor alone.

Runner and coordinator behavior are different factors. Use separate tournaments when they are different roles. A coordinator tournament must use frozen runner evidence as described in [Coordinator Proof](#coordinator-proof).

## Dry-Run Matrix

Before each live authorization, enumerate every invocation that the authorization covers. Use one row for each candidate, case, and repeat combination.

Each row records:

- stage and matrix-row identifier;
- candidate label and configuration digest;
- case identifier, exact input digest, schema digest, and ground-truth digest;
- repeat number and seed or nondeterminism control when applicable;
- prior-evidence state;
- intended action as execute or reuse;
- expected live calls as zero or one;
- estimated usage or cost when credible, otherwise unknown;
- data-safety classification and authorization reference.

Sum expected live calls for the authorization scope. State future-stage formulas separately when advancing candidate identities are not yet known. Freeze a new exact matrix after advancement and before authorizing that stage.

The dry run also proves that every candidate is available and every row uses the same case bytes. A plan or dry run never makes a live model call.

## Independent Preflight

Validate tournament infrastructure independently from candidate quality before spending credits or exposing data.

1. Read every fixture and verify its digest, encoding, and declared case identifier.
2. Verify that reviewed ground truth covers every case and uses the scorer's exact keys.
3. Validate the strict output schema with an independent valid and invalid sample.
4. Confirm that the selected runtime supports the schema features before candidate execution.
5. Exercise transport and output capture without treating the result as a scored candidate run.
6. Verify evidence paths, write authority, usage capture, clocks, and stop behavior.
7. Verify candidate availability, accepted pricing state, budget, live authorization, and data-safety authority.
8. For a coordinator tournament, validate every frozen runner hash before any coordinator call.

A schema keyword rejected by the runtime, transport failure, or capture failure is infrastructure evidence. It is not evidence of model accuracy.

## Per-Run Evidence And Validity

Give every invocation a stable run identifier. Preserve original evidence even when a later retry succeeds.

Each run records:

- tournament, contract, stage, matrix-row, candidate, case, and repeat identifiers;
- exact candidate configuration and its digest;
- exact rendered case input or durable reference and digest;
- fixture, ground-truth, schema, scorer, and frozen dependency digests;
- raw candidate response and captured output artifact;
- usage events with total input, cached input, and output separated;
- transport events, exit status, stderr or equivalent failure evidence;
- start and end observations plus elapsed wall time;
- validity state, invalid reason, schema findings, and candidate-responsibility decision;
- domain score, metric components, and scorer version;
- pricing source, arithmetic inputs, estimated cost, and pricing status;
- authorization and data-safety classification without secrets or sensitive payload duplication.

A reusable completed run satisfies all of these conditions:

- it matches the frozen candidate, case, repeat, configuration, input, schema, and dependency digests;
- transport completed and the required output artifact exists;
- the captured output passes the frozen schema;
- the evidence needed for scoring, usage, timing, and audit is complete.

Record infrastructure, transport, schema, and missing-artifact failures as invalid. Do not convert them into false negatives or zero scores. The only exception is a frozen task contract that explicitly assigns the specific failure to candidate responsibility. Retain the invalid evidence and the reason for that exception.

## Advancement And Repeats

Advance candidates only after the current stage has complete valid evidence under its frozen completion rule. Apply the exact aggregation, ranking, advancement count, and tie rule from the contract.

For each stage, preserve:

- the eligible candidates and required matrix rows;
- excluded or invalid runs and their disposition;
- aggregate metric inputs and results;
- the complete stage ranking;
- the frozen rule that selected each advancing candidate;
- an independent audit result when the decision is material.

A wide round, smaller semifinal, and multi-case final are a useful optional shape. The caller may choose another valid shape. Include a clean control when it tests a meaningful domain failure mode.

Use repeated leading-candidate trials when variance can affect the decision. Freeze repeat counts before that stage. A single run per case is screening evidence. Its report must say that variance is unmeasured and must not claim statistical proof.

## Default Ranking And Cost

Use the caller's accepted ranking policy. When no policy exists, offer this default and freeze acceptance before execution:

1. Create exact accuracy tiers from highest to lowest. Do not infer an accuracy-equivalence tolerance.
2. Compare estimated cost only among candidates in the same accuracy tier.
3. Starting with the cheapest remaining priced candidate, place every candidate costing no more than 115 percent of that candidate in one equivalent-cost band.
4. Order candidates within an equivalent-cost band by lower total wall-clock time.
5. Apply the frozen final tie-breaker only after accuracy, cost band, and speed.

Calculate uncached input as follows:

```text
uncached input = max(total input - cached input, 0)
```

Calculate estimated cost using the source's declared rate unit:

```text
estimated cost =
  uncached input * uncached-input rate
  + cached input * cached-input rate
  + output * output rate
```

Apply the source's divisor or unit conversion exactly once. Never charge cached input at both cached and uncached rates. Preserve raw usage and unrounded arithmetic. Declare any display rounding separately.

Never infer a price from another candidate, provider, model family, or token proxy. Keep an unpriced candidate in the accuracy results with its usage evidence. Do not assert cost superiority between priced and unpriced candidates. Mark any winner or ordering that depends on the missing price as provisional unless the frozen contract contains another accepted comparison rule.

Speed never overrides a higher accuracy tier or a cheaper non-equivalent cost band.

## Resume And Deterministic Rescore

Resume evaluates the dry-run matrix against retained evidence. Reuse only a completed schema-valid run that matches every frozen digest. A completed invalid run does not satisfy its matrix row. Rerun that row only when the frozen retry rule, live authorization, budget, and stop conditions permit it.

Never overwrite an earlier run. Link a retry to the original run and retain both validity decisions.

Deterministic rescore uses retained raw responses, usage, timing, ground truth, schemas, and scorer inputs. It makes zero live calls. Record the scorer, ranking policy, or price-card revision that changed and preserve the earlier result.

Do not label work as a rescore when it changes candidate output, case bytes, prompt bytes, or another frozen execution input. That change requires a new contract version and, if executed, new live authority.

For resume and rescore, report:

- matrix rows reused, missing, invalid, retried, or excluded;
- live calls planned and actually made;
- original and current scorer, ranking, or pricing versions;
- changed results and unchanged conclusions;
- evidence digests that prove no candidate call occurred during deterministic rescore.

## Coordinator Proof

Run coordinator candidates separately from runner candidates. Freeze one runner dossier before the coordinator tournament.

The dossier manifest records:

- the runner identity and exact configuration digest;
- every runner report identifier, durable reference, byte length, and cryptographic digest;
- the ordered dossier or rendered coordinator-input digest;
- the hash algorithm and canonicalization rule, if any;
- the validator that checks the manifest.

Prefer hashing the exact report bytes. If canonicalization is necessary, freeze and version its algorithm.

Verify the manifest before each coordinator invocation and after evidence capture. Record the same runner and dossier digests for every coordinator candidate. A mismatch invalidates the affected coordinator run and stops advancement until the attribution boundary is restored.

## Verification And Audit

Verification checks the frozen contract against evidence rather than trusting a report summary.

Verify:

- one-factor control or the declared multi-factor limitation;
- byte-equivalent case inputs and candidate configuration identity;
- independent fixture, ground-truth, schema, runtime-support, transport, and capture preflight;
- dry-run row coverage and planned versus actual live-call counts;
- per-run validity and exclusion of invalid runs from accuracy scoring;
- resume reuse of only matching completed schema-valid runs;
- zero live calls during deterministic rescore;
- scorer arithmetic, usage semantics, cached-input subtraction, prices, cost bands, and tie-breakers;
- stage completeness, rankings, advancement, repeats, and frozen runner proof;
- authorization, budget, stop conditions, data safety, and evidence retention;
- report claims against raw evidence and declared limitations.

Use an independent reviewer or deterministic verifier for advancement, scoring, and winner selection when the decision is material. Record the verifier identity, scope, evidence version, findings, and disposition.

## Final Report

The report contains:

- tournament identifier, contract version, mode, decision, role under test, and varied factors;
- constants, candidates, cases, schema, scorer, stages, repeats, and actual live-call count;
- winner, complete final ranking, stage rankings, advancement evidence, and selection rationale;
- accuracy and other declared metrics with misses and case-level evidence;
- raw usage, pricing state, pricing sources, estimated cost arithmetic, cost bands, and provisional status;
- elapsed time and the boundary within which speed affected ranking;
- invalid runs, retries, exclusions, infrastructure findings, and missing evidence;
- resume or rescore reuse evidence and zero-call proof when applicable;
- runner dossier identity and hashes for a coordinator tournament;
- data-safety disposition and retained-evidence location;
- independent audit result;
- limitations, representative-use boundary, variance evidence, confidence, and unresolved uncertainty;
- selected runtime configuration and its mapping to a semantic model profile.

Provider identifiers may appear in runtime evidence and adapter mappings. Keep reusable conceptual agent definitions provider-neutral.

## Caller-Owned Boundaries

The caller or domain evaluation package owns the task, fixtures, reviewed ground truth, strict output schema, scoring semantics, runtime commands, live-call mechanism, and evidence storage implementation. This contract defines methodology and required evidence only.
