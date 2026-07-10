---
name: tool-runtime-implementation
description: Use when coding, reviewing, or testing product code that implements tool registries, tool calls, action parsing, protected file rules, tool logs, or runtime tool execution.
metadata:
  category: stack-and-domain
---

# Tool Runtime Implementation

Use this application-domain pack for product internals that expose, parse, route, execute, or audit tools.

## Boundary

- This pack helps development agents work on product tool runtimes.
- It does not turn product tools into development methodology tools.
- Load a prompt or contract reviewer only when an independent review context is needed.

## Guidance

- Keep tool schemas, parser behavior, execution authority, and logs aligned.
- Validate arguments before side effects.
- Make protected paths, denied actions, and recovery behavior explicit.
- Preserve enough execution trace for users and reviewers to understand what happened.

## Verification

- Run parser, registry, protected-file, and execution log tests.
- Run prompt-surface tests when tool invocation instructions change.
- Check failure cases for denied, malformed, partial, and retried tool calls.
