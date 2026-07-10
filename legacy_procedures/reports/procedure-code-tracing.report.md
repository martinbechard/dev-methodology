# Code Tracing Procedure Migration Report

## Source

Source procedure: [procedure-code-tracing.md](../procedure-code-tracing.md)

## Purpose And Scope

The procedure explains how to trace one test through its implementation as a hierarchical, source-located execution narrative. Its durable goal is to make control flow, relevant state changes, branch outcomes, and function boundaries inspectable.

The procedure is narrower than general debugging: it is a request-response format for explaining an identified test path. It should not claim that static reading observed a runtime execution.

## Durable Guidance Worth Keeping

- Start at the named test and follow the relevant call path into implementation code.
- Give each trace step a source location and a clear description.
- Preserve nesting so callers, callees, and returns are easy to scan.
- Explain branch outcomes, function entry and exit, and relevant side effects.
- Track state only when it affects the outcome being explained.
- State variable values, mock behavior, and branch outcomes only when supported by source or observed execution evidence.
- Distinguish a source-derived trace from a trace confirmed by a debugger, log, or test run.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Trace a test through source code | [structured-explanation](../../skills/structured-explanation/SKILL.md) | Partial: it separates facts, hypotheses, unknowns, and answers, but has no execution-trace workflow or test-oriented output contract. | Retain the evidence and uncertainty discipline as a companion; do not treat it as complete coverage. |
| Find test setup, callees, imports, and structural control-flow candidates | [ast-grep](../../skills/ast-grep/SKILL.md) | Partial: it supports syntax-aware discovery and file-line reporting, but does not establish actual runtime order or variable values. | Keep as a discovery companion for a trace skill. |
| Read source, callers, tests, contracts, and behavior before documenting it | [documentation-reverse-engineering](../../skills/documentation-reverse-engineering/SKILL.md) | Partial: its module-design pass and code-discovery guidance are source-backed and broad, not a concise per-test trace. | Reuse its source-authority and direct-reading discipline; do not add a test-trace format to this documentation-set skill. |
| Diagnose Jest or Vitest tests and run focused checks | [jest](../../skills/jest/SKILL.md) and [vitest](../../skills/vitest/SKILL.md) | Partial: both guide focused test execution and failure diagnosis, but neither explains an execution path step by step. | Add routing from the proposed trace skill when the target uses either framework. |
| Keep any debugging instrumentation or diagnostic patch minimal | [careful-coding](../../skills/careful-coding/SKILL.md) | Partial and indirect: it limits changes but does not define tracing evidence. | Use only when tracing requires a scoped code or test change. |
| Carry out bounded test investigation | [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml) | Partial: the role owns test commands and diagnostic results, without an execution-trace output contract. | Add the proposed skill to this role if the catalog adds it. |
| Explain a code path while implementing or debugging | [Coding Agent](../../agents/roles/development-use/coding-agent.role.yaml) | Partial: the role has structural discovery and patch explanation, without a source-backed trace format. | Add the proposed skill to this role if the catalog adds it. |
| Investigate a long-running runtime failure | [Runtime Diagnostician](../../agents/roles/development-use/runtime-diagnostician.role.yaml) | Partial and adjacent: it handles reproduction and runtime boundaries, not routine test-path explanations. | Do not add the skill by default; load it only when a trace becomes a runtime incident investigation. |

## Coverage Assessment

No existing skill provides all of the procedure's durable contract: target-test orientation, a nested execution narrative, verified source locations, state and branch evidence, and an explicit distinction between static inference and observed execution. The gap is material enough for one focused development-practice skill.

## Precise Suggested Additions

Create a development-practice skill named code-execution-tracing with this purpose: trace a named test, command, route, or function through relevant code without presenting inferred behavior as observed runtime fact.

Its workflow should require the following:

1. Identify the trace target, input, test framework, fixtures, mocks, configuration, and intended question.
2. Read the target and its setup before following calls. Use rg for file and literal discovery and ast-grep when caller, nesting, import, async-flow, or test-structure queries need syntax awareness.
3. Build the shortest relevant call path. Include framework or library internals only when they determine the questioned behavior.
4. Emit a hierarchical trace with a verified file path and line or line range for every source-derived step. Include entry, return, await, callback, exception, side effect, and branch steps when relevant.
5. For every stated value or branch outcome, label it as source-derived, observed from a run, or unknown. Never invent a value merely to make a static trace read like a debugger transcript.
6. When observation is necessary, run the focused test or use approved debugger or logging evidence. Report the command or evidence source and any environment-dependent uncertainty.
7. Finish with the outcome, the decisive conditions, and unresolved gaps.

The skill should recommend structured-explanation when the user needs a diagnosis rather than only a trace. It should route to Jest or Vitest for focused execution, and to Playwright only for browser-bound paths. It should be added to Coding Agent and QA And Verification Agent after the source skill exists. A dedicated agent is not recommended: tracing is a bounded capability that belongs in existing coding and verification work.

## Guidance To Omit Or Narrow

- Omit the universal instruction to apply this format to all future code-tracing work. Skill routing should be triggered by the request and context.
- Narrow simulate a debugger to source-derived trace unless a debugger or test run supplied runtime evidence.
- Do not require a line-by-line account of every implementation detail. Trace only steps material to the user question; collapse irrelevant framework and library internals.
- Keep hierarchical numbering as the default output shape for a detailed trace, not as a requirement for every short explanation.
- Do not report exact variable values or condition outcomes without source, fixture, mock, assertion, log, debugger, or execution evidence.
- Omit the logger-specific example, including its fixed line numbers and values. It will drift and is not portable; replace it with a generic evidence-labelled example in the proposed skill.

## Conclusion

Preserve the procedure's explainability goal, nesting, locations, control flow, and relevant state tracking. The present catalog supplies useful companions but not the complete behavior. Create one focused code-execution-tracing skill, add it to Coding Agent and QA And Verification Agent, and avoid creating a separate tracing agent.
