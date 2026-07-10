# Root Cause Analysis Procedure Migration Report

## Source

Source procedure: [procedure-root-cause-analysis.md](../procedure-root-cause-analysis.md)

## Purpose And Scope

The procedure investigates one failing unit test at a time, first checking that
the test expresses the intended scenario and then tracing the implementation to
an evidence-backed root-cause and proposed fix. Its durable contribution is a
diagnosis workflow that separates a defective test from a defective product and
does not let a speculative patch substitute for evidence.

It is more than ordinary test execution guidance. The current Jest and Vitest
skills tell an agent to run focused tests and understand failures, while
structured-explanation supplies an evidence vocabulary. None defines the
complete test-failure diagnosis loop or its stop conditions.

## Durable Guidance Worth Keeping

- Capture a minimal failure packet before interpreting the result: focused
  command, failing suite and case, relevant expected-versus-received output,
  input, configuration, and test setup.
- Start with one reproducible failing case from the earliest actionable
  failure, then widen the scope only after it is understood or fixed.
- Validate the test against the relevant requirement, scenario, design, or
  other authoritative contract before changing production code. Check inputs,
  test-double setup, and assertions separately.
- If the test is invalid, correct it to the authoritative contract and rerun
  the diagnosis. Do not use a production fix to satisfy an invalid test.
- Read focused runtime evidence when it exists and associate it with the named
  test execution, rather than treating an undifferentiated log as proof.
- Follow the shortest material execution path, locate the first demonstrated
  divergence between expected and actual behavior, and distinguish observation
  from inference.
- Inspect mock contracts and call history when a mocked boundary could explain
  the divergence. Verify runner-required mock ordering and setup only when it
  applies to the framework and module system in use.
- For non-terminating or runaway executions, look for a repeated evidence
  pattern, identify the loop or state transition involved, and prove the exit
  condition that fails to occur.
- Form a small ranked set of hypotheses, select the simplest one supported by
  evidence, check it against prior failed attempts and authoritative design,
  then propose the narrowest fix.
- Keep diagnosis, approval, implementation, and verification as distinct
  stages. After a source fix, run focused regression checks before widening the
  suite; report residual or environment-blocked failures.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Focused Jest execution and failure output | [Jest](../../skills/jest/SKILL.md) | Partial: it requires focused runs and says failures remain the task, but does not require a reproducible evidence packet or one-case diagnosis. | Add the shared diagnosis workflow below. |
| Equivalent Vitest diagnosis | [Vitest](../../skills/vitest/SKILL.md) | Partial: it supports focused runs and failure diagnosis but has no test-validity or evidence structure. | Add the same runner-neutral workflow. |
| Separate facts, hypotheses, unknowns, and answer | [structured-explanation](../../skills/structured-explanation/SKILL.md) | Partial: the evidence model is complete, but it does not provide test-specific intake, validity checks, or fix gates. | Require it as the report format for non-trivial diagnoses. |
| Validate test inputs, doubles, and assertions against an authoritative scenario | Jest, Vitest, [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml) | Missing | Add a contract-versus-test validity checkpoint before product-code changes. |
| Inspect mock behavior, calls, and ordering | Jest and Vitest | Partial: both discuss mocks and fixtures, but not diagnosis-driven mock-contract inspection. | Add a concise debugging rule; preserve framework-specific ordering only conditionally. |
| Trace the path and find a divergence | proposed [code-execution-tracing report](procedure-code-tracing.report.md) | Partial pending creation: the adjacent report correctly proposes a source- and evidence-labelled tracing skill. | Have the diagnosis skill route to that skill; do not duplicate its detailed trace contract. |
| Minimal source change and focused regression loop | [careful-coding](../../skills/careful-coding/SKILL.md), Jest, and Vitest | Partial: surgical changes and focused checks exist, but they are not linked to a documented diagnosis. | Require the proposed fix to cite the demonstrated divergence and test it first. |
| Diagnose and hand off test evidence | QA And Verification Agent | Partial: its output contract has command results and PASS, WARN, or FAIL, but no root-cause report. | Add a diagnosis artifact when a failure cannot be resolved by a straightforward, directly evidenced correction. |
| Implement an approved diagnosis | [Coding Agent](../../agents/roles/development-use/coding-agent.role.yaml) | Partial: it makes focused changes and tests them, but has no explicit diagnosis input. | Require implementation to preserve the diagnosis evidence and rerun its reproducer. |
| Long-running incident-style reproduction | [Runtime Diagnostician](../../agents/roles/development-use/runtime-diagnostician.role.yaml) | Partial and adjacent: it owns runtime boundaries and logs, not ordinary unit-test RCA. | Escalate only when focused test diagnosis exposes a process, resource, or nondeterministic runtime boundary. |

## Coverage Assessment

The catalog has the necessary pieces but not the orchestration. The material
gap is a reusable, runner-neutral test-failure diagnosis workflow that makes
the test-contract check, evidence labels, divergence finding, hypothesis
selection, and implementation gate explicit. It should compose with the
proposed code-execution-tracing skill rather than absorb its detailed tracing
format.

## Precise Suggested Additions

### New Skill: Test-Failure Diagnosis

Create a development-practice skill named test-failure-diagnosis. Its
description should trigger for a failing unit or integration test that needs an
evidence-backed root-cause analysis before a code or test change.

Its compact workflow should require:

1. Reproduce or record the focused failure and identify the suite, case,
   command, relevant output, input, configuration, fixture, and test doubles.
2. Select one failure to diagnose. Prefer the first actionable failure from a
   focused run; do not conflate unrelated downstream failures.
3. Read the test and its authoritative contract. Classify its inputs, doubles,
   and assertions as conformant, non-conformant, or unverified. Correct a
   demonstrably invalid test before proposing a product-code fix.
4. Write the analysis with structured-explanation. Label run output, logs,
   source, and mock-call history as FACT; label unproven explanations as
   HYPOTHESIS; make missing evidence UNKNOWN.
5. Use code-execution-tracing when source-path analysis is needed. Include only
   the path, state, branches, and side effects material to the failure, and
   state the first evidenced divergence.
6. If a boundary is mocked, inspect the double's contract, configured results,
   relevant calls, reset or restoration behavior, and framework-specific import
   or setup order. Do not apply a universal ordering rule across runners.
7. For timeout, recursion, runaway write, or repeated-event failures, isolate
   the repeated sequence and the missing or ineffective exit condition from
   evidence; otherwise omit loop analysis.
8. Rank at most five evidence-supported hypotheses, propose the smallest fix,
   check it against the contract and earlier attempts, and state the exact
   reproducer and regression checks required after approval.
9. Stop at the recommendation when approval is required by the user or local
   repository policy. Otherwise implement only the approved or clearly
   authorized fix, rerun the reproducer, then widen verification in proportion
   to the changed scope.

The skill should link to Jest or Vitest for runner operations,
structured-explanation for the report format, code-execution-tracing for
detailed path analysis, and careful-coding for the patch. It needs no scripts
or bundled reference material initially: the target repository supplies the
authoritative contracts, logs, and test configuration.

### Jest

Add these guidance bullets:

- When a focused Jest failure needs investigation, capture the failing command,
  case, relevant output, fixture or configuration, and test-double setup. Check
  inputs, doubles, and assertions against the applicable contract before
  changing product code.
- During diagnosis, inspect the mock contract and relevant call history when a
  mock could explain the failure. Verify mock setup order only as required by
  the repository's Jest, transform, and module-loading configuration.

### Vitest

Add these guidance bullets:

- When a focused Vitest failure needs investigation, capture the failing
  command, case, relevant output, fixture or configuration, and test-double
  setup. Check inputs, doubles, and assertions against the applicable contract
  before changing product code.
- During diagnosis, inspect the mock contract and relevant call history when a
  mock could explain the failure. Follow the repository's Vitest and module
  loading semantics instead of importing Jest ordering rules.

### Agent Roles

- QA And Verification Agent: for a non-trivial test failure, produce or review
  the evidence packet, test-validity classification, demonstrated divergence,
  unresolved unknowns, and the focused regression command. Add
  test-failure-diagnosis and, once created, code-execution-tracing to its skill
  list.
- Coding Agent: when implementing from an RCA, limit the patch to the supported
  cause, preserve the reproducer, and rerun it before broader checks. Add
  test-failure-diagnosis and code-execution-tracing only if this diagnostic work
  is expected to be a routine part of the role; otherwise allow explicit
  loading to keep its default context smaller.
- Runtime Diagnostician: do not add the new skill by default. Its scope begins
  only after a test failure demonstrates a runtime, process, resource, or
  nondeterministic boundary that cannot be resolved within the focused test
  loop.

No dedicated root-cause-analysis agent is recommended. Diagnosis belongs with
the existing verification and coding roles; the new skill supplies the missing
repeatable contract.

## Guidance To Omit Or Narrow

- Omit the fixed Tracer module, trace.log file, max-writes error, and instruction
  to remove a tracer mock. They encode a former application's observability
  architecture. A repository that depends on instrumentation must document its
  own diagnostic prerequisites locally.
- Omit fixed RCA filenames, deletion of a prior report, test-plan filenames,
  source folders, and design-document paths. The report location and authority
  hierarchy must come from the target repository.
- Narrow first failed suite to first actionable failure from a focused run. Test
  runners can emit setup, discovery, parallel, or cascading failures whose
  textual order does not establish causality.
- Narrow the demand to copy only an it block and scenario text. Cite or extract
  the minimal contract and setup evidence needed for the question; verbatim
  copying is neither required nor always useful.
- Omit mandatory line-by-line simulation, exact hierarchical numbering, and
  unqualified variable values. Detailed traces belong to code-execution-
  tracing and must distinguish source inference from runtime observation.
- Narrow previous-fix-attempt analysis to attempts with evidence relevant to the
  same reproducer and demonstrated divergence. Do not preserve a history merely
  because it exists.
- Omit an unconditional wait-for-approval rule. Respect explicit user requests
  and repository policy; otherwise an authorized bug-fix task normally includes
  implementation and verification.
- Do not prescribe running a unit suite merely because an integration failure
  changed source code. Select focused regression coverage from the changed
  module, contract, and repository test topology.

## Conclusion

Preserve the procedure's evidence packet, one-failure focus, contract-first
test-validity check, mock-aware divergence analysis, bounded hypothesis set,
and diagnosis-before-patch gate. Create one runner-neutral test-failure-
diagnosis skill that composes with the proposed code-execution-tracing skill,
then add concise diagnosis and mock-inspection guidance to Jest and Vitest and
extend the QA role. Do not migrate the application-specific Tracer workflow,
fixed paths, forced report mechanics, or unconditional approval and test-order
rules.
