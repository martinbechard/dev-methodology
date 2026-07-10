---
name: code-execution-tracing
description: Use when explaining a source-level execution path, including entry points, callers, branches, state changes, errors, and exits, without requiring runtime instrumentation or a proprietary tracing tool.
metadata:
  category: development-practice
---

# Code Execution Tracing

Trace what the source can establish and label inference honestly.

## Workflow

1. Name the entry point, input, and question being traced.
2. Follow callers, callees, branches, async boundaries, callbacks, state changes, persistence, and exits that affect the question.
3. Record file, symbol, and tight locations for each material step.
4. Track only values and state that influence control flow or the final outcome.
5. Distinguish guaranteed paths, conditional paths, and paths that depend on unavailable runtime state.
6. Link relevant tests or runtime evidence that confirm the path.
7. End with the observed or inferred result, unresolved branches, and evidence gaps.

Use structure-aware tools when already available, but do not make them a dependency. Use Runtime Evidence Collection when source inspection cannot resolve the actual path taken.
