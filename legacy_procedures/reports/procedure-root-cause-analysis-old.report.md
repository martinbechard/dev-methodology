# Root Cause Analysis Procedure Migration Report

## Source

Source procedure: [procedure-root-cause-analysis-old.md](../procedure-root-cause-analysis-old.md)

## Purpose And Scope

The procedure turns a test failure or observed defect into an inspectable diagnosis before implementation. Its durable intent is to separate observations from suspected causes, identify the evidence needed to confirm a cause, account for recurring failures, and select a fix that addresses the causal mechanism rather than merely satisfying the immediate assertion.

It is a diagnostic workflow, not a universal implementation format. The procedure's fixed table and mandatory approval stop are useful only when the requester wants an RCA or diagnosis-first handoff.

## Durable Guidance Worth Keeping

- State the observed symptom precisely, including the expected-versus-actual result, relevant error output, logs, inputs, and the affected boundary.
- Keep evidence, suspected source locations, hypotheses, and unresolved questions distinct. A suspected cause is not a root cause until the supporting evidence is sufficient.
- For each material unknown, name the least-invasive confirmation: inspect the relevant code or configuration, reproduce with a focused test, inspect logs, or add temporary tracing.
- Check whether the issue is new or a recurrence. For a recurrence, examine the previous fix, its assumptions, and the path it failed to cover.
- Use Five Whys as an optional probing technique when it reveals a causal chain; do not use it to manufacture certainty or replace evidence.
- Propose a fix principle and its verification, then assess whether it addresses the causal boundary and relevant variants rather than only the reported symptom.
- Keep diagnostic instrumentation and proposed changes narrow, reversible, and tied to a stated confirmation need.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Separate facts, hypotheses, unknowns, and an answer | [structured-explanation](../../skills/structured-explanation/SKILL.md) | Strong: its item model explicitly separates evidence, conjecture, gaps, and conclusions. It does not supply a defect-investigation sequence or remediation test. | Reuse as the reasoning and report format for an RCA skill; no generic-model change is required. |
| Record the source responsible for each fact or hypothesis | [ast-grep](../../skills/ast-grep/SKILL.md) and [structured-explanation](../../skills/structured-explanation/SKILL.md) | Partial: ast-grep supports structural discovery, and structured-explanation requires concrete evidence, but neither routes an investigation from symptom to candidate boundary. | Include source discovery and evidence citation in the proposed RCA skill. |
| Reproduce a test failure, inspect output, and run focused checks | [jest](../../skills/jest/SKILL.md), [vitest](../../skills/vitest/SKILL.md), and [playwright](../../skills/playwright/SKILL.md) | Partial: each covers its own execution surface and failure evidence, without a framework-neutral root-cause workflow. | Route from the proposed skill to the applicable runner; retain runner-specific commands in those skills. |
| Treat unexplained failures as work, make scoped changes, and verify success | [careful-coding](../../skills/careful-coding/SKILL.md) | Partial: it requires explicit assumptions, small changes, and verified goals, but it does not require confirmation of a causal explanation before remediation. | Keep it as the change-safety companion; add no RCA table or Five Whys requirement to this general coding skill. |
| Explain what changed and assess conformance after a fix | [fix-explanation](../../skills/fix-explanation/SKILL.md) | Partial and downstream: it explains an implemented patch and classifies its type, rather than establishing the pre-implementation diagnosis. | Use after implementation when an explanation of the applied fix is requested. |
| Diagnose a test or acceptance failure | [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml) | Partial: the role runs checks and reports results, but lacks a causal-analysis and confirmation-plan contract. | Add the proposed skill after it exists. |
| Investigate a long-running local failure with logs and runtime boundaries | [Runtime Diagnostician](../../agents/roles/development-use/runtime-diagnostician.role.yaml) | Partial: the role already has reproduction, evidence, and a narrow fix path, but lacks explicit recurrence analysis and causal-confirmation discipline. | Add the proposed skill after it exists. |
| Implement a verified fix | [Coding Agent](../../agents/roles/development-use/coding-agent.role.yaml) | Adjacent: it implements and tests scoped changes, rather than owning a diagnosis-first workflow. | Do not add by default; load the RCA skill when coding work begins from an unresolved defect investigation. |

## Coverage Assessment

The current bundle covers the building blocks but not the complete portable contract: turn a symptom into evidence-labelled candidate causes, choose and perform confirmations, distinguish a verified root cause from an open hypothesis, inspect failed prior fixes, and define a mechanism-level validation plan. This is a material but bounded gap. It warrants one focused development-practice skill, not a new diagnostic role.

## Precise Suggested Additions

### New Root Cause Analysis Skill

Create a development-practice skill named root-cause-analysis. Its description should trigger for diagnosing a failing test, bug, regression, unexpected runtime behavior, or recurring defect when the user needs a supported causal explanation and a fix path.

Its workflow should be:

1. Define the symptom, expected behavior, actual behavior, reproduction command or scenario, scope, and available evidence.
2. Build a compact evidence ledger. For each material item, record the fact, evidence source, suspected boundary, hypothesis, confidence, and unknown or confirmation needed. Use structured-explanation item types when a narrative report is clearer than a table.
3. Inspect the relevant code, configuration, tests, fixtures, logs, and recent or prior fix history before adding instrumentation. Use ast-grep for structural discovery when it makes the search more reliable.
4. Confirm or reject each leading hypothesis with the smallest adequate observation. Prefer existing evidence and focused reproduction; make temporary tracing or test changes reversible and state what they are meant to prove.
5. Name a root cause only when the evidence establishes the causal mechanism. Otherwise return the leading hypothesis, confidence, and next confirmation rather than an invented conclusion.
6. For a recurrence, explain which previous assumption, boundary, variant, or verification gap allowed the issue to persist. Use Five Whys only if it clarifies this chain.
7. Propose the smallest fix principle that removes the mechanism, identify the affected code or configuration boundary, and define focused and proportionate broader verification. State residual risks and variants explicitly.

The skill should route focused execution to Jest, Vitest, or Playwright as applicable; route long-running, process-, log-, or exclusive-resource failures to Runtime Diagnostician; and pair implementation work with Careful Coding and, after a patch, Fix Explanation. A full source-file rewrite is never a required RCA output.

### Agent Role Changes

- QA And Verification Agent: add root-cause-analysis with the rationale that it converts unexplained test and acceptance failures into evidence-backed diagnosis, confirmation, and verification plans.
- Runtime Diagnostician: add root-cause-analysis with the rationale that it makes causal confidence, recurring failures, and the next least-invasive confirmation explicit.
- Do not create a dedicated RCA agent. The necessary ownership already belongs to verification and runtime diagnosis; Coding Agent can load the skill selectively when it is asked to diagnose before modifying code.

## Guidance To Omit Or Narrow

- Omit the universal instruction to use this exact procedure for all future troubleshooting. Routing should depend on whether the task needs RCA depth.
- Do not require a nine-column table for every diagnosis. Retain its information categories, but allow a compact evidence ledger or structured-explanation report when the failure is small.
- Do not call a speculative source location or explanation a fact. Source is evidence only when it directly supports the stated claim.
- Do not require Five Whys in every investigation, or assume five iterations establish a root cause. It is a prompt for deeper inquiry, not proof.
- Narrow the instruction to wait for human approval before implementation: stop after diagnosis only when the user requested analysis, a proposed plan, or an approval gate. Otherwise follow the user's authorized implementation scope.
- Omit the instruction to generate complete files after approval. Make the smallest scoped patch and present normal diffs or changed-file summaries; full-file output is not safer and can create noisy, error-prone merges.
- Do not prescribe HTML attribute descriptions, test-only inputs, or particular console-output fields. These are examples of evidence, not portable required columns.

## Conclusion

Preserve the procedure's evidence-first diagnosis, explicit confirmation needs, recurrence analysis, and mechanism-level fix validation. The existing skills provide important components, especially structured-explanation, runner skills, careful-coding, and fix-explanation, but no skill coordinates them into root-cause analysis. Add one concise root-cause-analysis skill to QA And Verification Agent and Runtime Diagnostician, use it selectively with Coding Agent, and do not add a separate agent or revive the fixed table and full-file-output rules as universal policy.
