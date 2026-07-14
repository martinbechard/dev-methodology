---
name: agent-harness
description: Use when coding, reviewing, or testing product code that implements a custom agent harness, execution loop, mode system, tool orchestration, or long-running local development harness.
metadata:
  category: stack-and-domain
---

# Agent Harness

Use this application-domain pack when the project being edited implements an agentic harness as product code.

## Boundary

- This is not a conceptual agent definition.
- Load it when a development agent is editing product internals that behave like an agent harness.
- Create a separate development agent only when a distinct context, authority model, or output contract is needed.

## Guidance

- Separate harness state, prompt state, tool state, and user-visible state.
- Keep retries, cancellation, and resume behavior explicit.
- Treat tool execution as a contract with auditability and failure reporting.
- Keep development-time safety rules separate from runtime product behavior.

## Verification

- Run focused harness tests for execution state, cancellation, retry, and tool routing.
- Run prompt or fixture tests when prompt-facing behavior changes.
- Inspect logs when behavior depends on long-running local processes.
