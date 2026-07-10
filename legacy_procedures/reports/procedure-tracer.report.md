# Tracer Utility Procedure Migration Report

## Source

Source procedure: [procedure-tracer.md](../procedure-tracer.md)

## Durable Purpose

The procedure describes temporary, opt-in runtime instrumentation for diagnosing a complex code path. Its enduring value is not the CIBC Driver tracer implementation or Chrome storage; it is a disciplined way to record nested execution, inspect inputs and outputs safely, bound diagnostic data, and clean up state between test runs.

The future catalog should distinguish two related jobs:

- explaining an execution path from source or test evidence;
- adding temporary runtime instrumentation when that evidence is insufficient.

The first belongs to the proposed code-execution-tracing skill identified by the code-tracing procedure. This procedure contributes the second job and should not be merged into a source-only trace workflow.

## Durable Guidance Worth Keeping

- Make instrumentation opt-in and disabled by default outside a focused diagnostic session.
- Record function entry, exit, relevant inputs, return values, errors, and nesting only when they help answer a bounded question.
- Prefer a wrapper or helper around a narrow boundary over repetitive, hand-written logging throughout the implementation.
- Make trace output readable as a hierarchy and filterable by a stable, meaningful label.
- Handle non-serializable and circular values safely; redact or summarize rather than failing the diagnostic path.
- Bound trace depth, output volume, retention, and destination so an accidental loop or noisy path cannot exhaust storage or expose excessive data.
- Clear or isolate a diagnostic session before it begins, and reset tracer state between tests to avoid cross-test contamination.
- Treat trace output as evidence, not as a substitute for a focused reproduction and verification result.

## Mapping To The Current Catalog

| Procedure point | Current destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Keep a debugging change scoped, explicit, and verified | [careful-coding](../../skills/careful-coding/SKILL.md) | Partial: it requires surgical, goal-driven changes, but does not describe instrumentation lifecycle or data limits. | Add a short routing rule that temporary diagnostics must be opt-in, bounded, and removed or disabled after use. |
| Reproduce a runtime failure, gather logs, and report a verified path | [Runtime Diagnostician](../../agents/roles/development-use/runtime-diagnostician.role.yaml) | Partial: its reproduction and log-evidence contract fits incidents, but it has no skill for adding safe trace instrumentation. | Add the proposed instrumentation skill to this role; retain the role's high-effort incident boundary. |
| Diagnose test behavior and reset state between runs | [jest](../../skills/jest/SKILL.md) and [vitest](../../skills/vitest/SKILL.md) | Partial: both require focused execution and diagnose failures, but neither covers isolation of trace state, output caps, or value-safe serialization. | Add a brief cross-reference to the proposed skill for temporary instrumentation in tests; do not duplicate its workflow in both framework skills. |
| Debug Electron background behavior and inspect logs or user-data locations | [electron-main](../../skills/electron-main/SKILL.md) | Partial and platform-specific: it points to logs and user-data paths, but it does not define portable trace controls. | Keep Electron routing as a companion only when the traced boundary is in the main process. |
| Capture browser traces, console evidence, and screenshots | [playwright](../../skills/playwright/SKILL.md) | Adjacent: it covers browser-test artifacts, not application-level execution logging. | Do not broaden Playwright into a general tracer skill; route browser-bound cases to it after instrumentation is considered. |
| Explain evidence, uncertainties, and diagnosis | [structured-explanation](../../skills/structured-explanation/SKILL.md) | Partial: its FACT, HYPOTHESIS, UNKNOWN, and ANSWER model prevents overclaiming, but it does not prescribe collection of runtime events. | Use it for the resulting diagnosis, not as the instrumentation workflow. |
| Preserve execution evidence in a product tool runtime | [tool-runtime-implementation](../../skills/tool-runtime-implementation/SKILL.md) | Partial and domain-specific: it calls for enough execution trace for auditability, but not developer diagnostic instrumentation. | Keep its audit-log boundary separate; do not make all product tracing temporary debugging telemetry. |
| Use a trace to explain a named test, route, command, or function | Proposed code-execution-tracing skill | Partial complement: that proposal governs evidence-labelled trace narratives, including when a run is needed. | Cross-link the two skills. Escalate to instrumentation only when static and existing runtime evidence cannot answer the question. |

## Coverage Assessment

No existing skill owns the full portable practice of adding temporary runtime tracing safely. The gap is material: current skills say to inspect logs, run focused tests, and keep changes narrow, but none require a bounded session, redaction or safe serialization, depth and write limits, a controlled sink, reset semantics, or removal or disablement after diagnosis.

This is one reusable development-practice skill, not a collection of additions to Electron, Jest, Vitest, Playwright, or tool-runtime-implementation. Those skills should route to it only in their applicable contexts.

## Exact Additions Recommended

Create one development-practice skill named runtime-trace-instrumentation. Its description should state:

> Use when debugging requires temporary runtime instrumentation of a code path. Add an opt-in, bounded trace session with safe value handling, scoped filtering, test isolation, and a clear cleanup or disablement plan.

Its body should contain the following durable rules:

1. State the diagnostic question, target boundary, expected evidence, permitted data, and stop condition before adding instrumentation.
2. Reuse the project's established logger or tracer when it meets the contract. Otherwise add the smallest local helper or wrapper around the relevant boundary; do not spread ad-hoc logs through unrelated code.
3. Keep tracing disabled by default. Enable it through explicit test or diagnostic configuration, never through a permanent production default.
4. Emit an ordered, nested event model only for entry, exit, return, error, awaited continuation, and material state transition. Include stable event labels that can be filtered.
5. Serialize values defensively. Detect cycles and non-serializable values; summarize large values; redact secrets, tokens, personal data, credentials, raw customer content, and other sensitive fields before any sink receives them.
6. Bound maximum nesting, event count, payload size, retention, and sink. On a limit, record one truncation event and stop tracing rather than continuing unbounded.
7. Define the sink and access boundary. Use test output, a local file, or an approved project diagnostic sink; do not introduce a browser-storage, cloud, or shared-log dependency without project authorization.
8. Clear or isolate the session at the start, reset all tracer state in test setup or teardown, and verify that concurrent or repeated tests cannot inherit configuration or events.
9. Run the smallest reproduction or focused test, preserve the command and relevant trace excerpt as evidence, then report the observed result separately from hypotheses.
10. Remove temporary instrumentation after the issue is resolved, or leave a reusable helper only when it is opt-in, documented, tested, and does not retain sensitive or unbounded data.

Add the following routing statement to Runtime Diagnostician after the skill exists:

> Load runtime-trace-instrumentation when existing logs and reproduction evidence do not expose the relevant runtime boundary. Use it only for a bounded diagnostic session and include the trace limits and cleanup result in the output.

Add the proposed skill to Coding Agent and QA And Verification Agent, with role comments that make it conditional: Coding Agent when a scoped diagnostic code change is required, and QA And Verification Agent when test isolation or focused runtime evidence is required. Do not create a dedicated tracing agent; the capability is a bounded technique used by existing implementation, verification, and incident roles.

## Guidance To Omit Or Narrow

- Omit the CIBC Driver, file path, Chrome storage, and fixed API names. They describe one implementation, not portable methodology.
- Omit logging arbitrary user data. The procedure's examples include user data without a confidentiality boundary; the replacement must default to redaction and data minimization.
- Do not prescribe a static singleton tracer, a deep-copy implementation, or one serialization algorithm. Projects may have a structured logger, debugger, OpenTelemetry-compatible mechanism, or test reporter that better fits their runtime.
- Narrow unlimited tracing. Unlimited depth and disabled write caps are unsafe defaults; any exceptional override must remain local, explicit, and bounded by payload size and retention.
- Do not make Chrome storage or any persistent shared sink the default trace destination. Storage choice is architecture, privacy, and authorization dependent.
- Do not require function-entry or function-exit logging for every function. Instrument only boundaries that answer the diagnostic question, otherwise traces become noisy and costly.
- Correct the malformed numbering and code comment in the legacy best-practices section rather than carrying them forward.
- Do not equate a trace with correctness. A trace can show one observed path; assertions, acceptance checks, and focused tests remain the verification surface.

## Conclusion

Keep the procedure's strongest operational controls: opt-in tracing, hierarchical evidence, filtering, safe value handling, bounded output, session clearing, and test-state reset. Create one focused runtime-trace-instrumentation skill and route to it from existing coding, verification, and runtime-diagnosis work. Pair it with the proposed code-execution-tracing skill, but preserve their boundary: one collects safe runtime evidence; the other explains an execution path without overstating what was observed.
