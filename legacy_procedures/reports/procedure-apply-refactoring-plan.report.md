# Assessment: Apply Refactoring Plan

## Source and scope

Source: [procedure-apply-refactoring-plan.md](../procedure-apply-refactoring-plan.md).

This procedure is a legacy, repository-specific execution playbook for applying
an already approved refactoring plan. It combines generally useful delivery
discipline with assumptions about a TypeScript codebase, a definitions index,
a status file, a Tracer utility, local design-file naming, and linked legacy
procedures. This assessment identifies guidance that should be retained in the
portable skill and canonical-agent model; it does not preserve the procedure as
a portable workflow.

## Worthwhile durable guidance

- Make the smallest logical change at a time and verify it before starting the
  next change.
- Define a concrete verification path for refactoring: relevant tests pass
  before and after the change, then run the proportionate broader checks.
- Diagnose a failure before changing code. Treat unexplained test or type
  failures as active work rather than masking them.
- Prefer type-safe, simple implementations and avoid assertion-based shortcuts
  unless the surrounding project explicitly justifies them.
- Read the applicable project instructions, design, requirements, contracts,
  and repository patterns before resolving a contradiction. Escalate genuine
  ambiguity instead of silently choosing an authority.
- Keep mocks at external boundaries and prefer real parsing, validation, and
  state transitions where they are practical.
- Record completion, verification, and blocked state in the repository's
  actual backlog or tracking system so another agent can recover the work.
- Make design review evidence-based and actionable; limit approved design
  updates to supported corrections or clarified intent.
- When recurring failures expose a reusable gap, propose a narrowly scoped
  preventative rule or test. The proposal must be reviewed rather than
  automatically incorporated into global guidance.

## Mapping to live skills and canonical agents

| Procedure point | Live destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Correctness, type safety, explicit assumptions, small diffs | careful-coding; coding-agent | Partial | Add a short type-safety rule to careful-coding: avoid unsafe assertions and escape hatches unless justified by a verified boundary or project convention. Keep the existing simplicity and surgical-diff rules. |
| Root-cause analysis before a fix; explain the result | runtime-diagnostician; structured-explanation; fix-explanation | Partial | Add a general failure-triage sequence to careful-coding or a dedicated diagnosis skill: reproduce, gather evidence, form and test hypotheses, then change code. Do not require hidden reasoning blocks. |
| One logical issue per step; verify after each | careful-coding; coding-agent | Covered | Keep as-is. Careful-coding already requires scoped work, a short verifiable plan, and focused checks. |
| Review existing design documentation with concrete, actionable findings | review-structured; review-module-design; review-high-level-design; artifact-review-agent | Covered | Keep current artifact-specific review routing and completed-checklist evidence. Do not retain the legacy filename convention. |
| Maintain task sequence and immediately record completion evidence | create-backlog; manage-backlog; backlog-steward; development-orchestrator | Partial | Add an explicit implementation handoff rule to coding-agent: update the repository's chosen work item with verification and blocked evidence when the task is backlog-managed. Avoid prescribing one status-file format. |
| Test-driven refactoring and focused-to-broad verification | careful-coding; coding-agent; jest; vitest; qa-and-verification-agent | Partial | Preserve regression-test-before-and-after intent in careful-coding and coding-agent. Do not impose TDD as an unconditional cycle: choose test-first when a behavior contract can be expressed, and use investigation first for unclear failures. |
| Mocking only at suitable boundaries | jest; vitest; qa-and-verification-agent | Partial | Add a shared mock-boundary principle to Jest and Vitest: do not mock the unit's own logic merely to observe it; justify integration-boundary mocks. Keep stack-specific exceptions local. |
| Resolve code, test, requirement, and design discrepancies from authoritative inputs | project-wiki-query; fix-explanation; coding-agent | Partial | Add an authority-resolution rule to coding-agent: inspect the project-defined source of truth, report conflicts, and obtain clarification when authority is ambiguous. Do not hard-code design documents above all other evidence. |
| Prevent duplicate or divergent definitions | coding-agent; ast-grep; TypeScript-specific skills when applicable | Missing portable guidance | Create a language-agnostic contract-discovery addition to coding-agent, not a definitions-index rule: locate existing public types, schemas, interfaces, and contracts before introducing a parallel representation. |
| Debug with logs, backtracing, and a troubleshooting hierarchy | runtime-diagnostician; qa-and-verification-agent | Partial | Add evidence guidance to runtime-diagnostician for focused logs, process state, reproduction, and call-path tracing. Keep observability tool names and log-file locations project-local. |
| Stop repeated unsuccessful attempts | runtime-diagnostician; development-orchestrator | Missing safe policy | Add an escalation threshold to runtime-diagnostician: after repeated failed hypotheses, pause implementation, summarize evidence, broaden diagnosis or seek review. Never mandate deletion and rewrite solely by attempt count. |
| Feed recurring generic failures back into methodology | methodology-maintainer; methodology-artifact-reviewer | Partial | Add a maintenance intake rule: propose a reusable skill or agent change only with cross-project evidence, a concrete failure mode, scope, and regression check. |

## Obsolete or project-specific guidance to omit

- Hidden thinking blocks and mandatory reasoning disclosure. Current skills
  should request concise, inspectable evidence and explanations, not private
  reasoning traces.
- The requirement that every TypeScript file include a design-document header,
  and the linked definitions index. These are valid only where a target
  repository adopts them.
- Specific design files, directives, review checklist names, and the rule that
  review output use a filename-review.md pattern. Current review skills use
  completed review-checklist files plus findings files.
- A universal status file, its read-diff-confirm update ceremony, and a fixed
  task ordering. The live backlog system supports project-specific lifecycle
  evidence and coordination claims.
- Universal strict TDD, fixed test naming/setup rules, and a single mock policy
  for every stack. Retain outcome-based test discipline, then route to Jest,
  Vitest, Playwright, or project-local instructions.
- The precedence claim that design and definitions always outrank code and
  tests. Authority is project-specific and may include product requirements,
  contracts, migrations, runtime behavior, and approved change requests.
- Monetary penalties, the ban on a named Tracer mock, named trace.log usage,
  environment-variable initialization, and automatic deletion/rewrite after
  three attempts. These are coercive or tool-specific, and deletion is unsafe
  without evidence and authority.
- Automatic creation of future-improvements documentation and automatic edits
  to procedures. Capture proposals through the repository's backlog or
  methodology-maintenance process instead.

## Precise suggested additions

### Amend careful-coding

Add a Refactoring And Failure Diagnosis section:

- For a refactor, identify the behavior or contract that must remain stable;
  run a focused relevant check before and after the change when the project can
  support it.
- When a check fails, reproduce it and collect direct evidence before editing.
  Record the hypothesis and the check that will distinguish it from alternatives.
- Avoid unsafe casts, broad suppressions, and loosely typed escape hatches
  unless a verified external boundary requires one and the project convention
  documents the containment.
- After repeated disproven hypotheses, stop making speculative edits. Summarize
  the evidence, broaden the investigation, request review, or escalate.

### Amend coding-agent

Add these instructions:

- Before introducing a public type, schema, interface, data model, or contract,
  search the project for its existing canonical representation and reuse or
  extend it when appropriate.
- When requirements, design, tests, and running behavior conflict, identify the
  project-defined authority. If it is not clear, report the conflict and ask
  for direction before treating a downstream artifact as defective.
- For backlog-managed work, write completion, verification, and blocked
  evidence to the active work item or its documented equivalent.

### Amend Jest and Vitest

Add the same portable mock rule to both skills:

- Keep mocks at external or nondeterministic boundaries. Do not replace the
  unit's own business logic with a mock simply to observe calls. When an
  integration-boundary mock is necessary, state what real dependency it stands
  in for and why the focused test remains meaningful.

### Amend runtime-diagnostician

Add a bounded recovery rule:

- If several evidence-backed hypotheses fail, pause changes. Preserve the
  reproduction, logs, attempted hypotheses, and results; then choose a broader
  diagnostic boundary, independent review, or user escalation. A rewrite
  remains an option only when its cost and risk are justified by the evidence.

### Amend methodology-maintainer

Add an improvement-intake criterion:

- Convert a failure pattern into shared skill or role guidance only when it is
  demonstrably reusable across projects, states a specific preventative action,
  and has a validation or review check that can detect future drift.

## Conclusion

Do not create a new Apply Refactoring Plan skill or a dedicated refactoring
agent from this procedure. Its portable value is distributed across the
existing Coding Agent, Runtime Diagnostician, QA And Verification Agent,
Backlog Steward, and design-review roles. The highest-value gaps are a shared
failure-triage and escalation rule, explicit canonical-contract discovery,
portable mock-boundary guidance, and a controlled path for turning recurring
failures into methodology improvements. All legacy file conventions, penalties,
and forced deletion behavior should remain omitted.
