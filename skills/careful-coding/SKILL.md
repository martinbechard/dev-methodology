---
name: careful-coding
description: Use when the agent is about to implement, modify, refactor, or debug code and should bias toward explicit assumptions, simple designs, surgical diffs, and verified success criteria.
metadata:
  category: development-practice
---

# Careful Coding

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Think Before Coding

Do not assume, hide confusion, or skip tradeoffs.

Before implementing:
- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them instead of picking silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop, name what is confusing, and ask.
- Read the project intent, local guidance, callers, tests, and established patterns before deciding what the code should do.

## Simplicity First

Write the minimum code that solves the problem. Avoid speculative work.

- Add no features beyond what was asked.
- Add no abstractions for single-use code.
- Add no flexibility or configurability that was not requested.
- Add no error handling for impossible scenarios.
- If a 200-line solution could be 50 lines, rewrite it.

Ask whether a senior engineer would call the solution overcomplicated. If yes, simplify.

Prefer a named parameter object when several same-shaped arguments, optional arguments, or evolving call sites would otherwise make calls ambiguous. Prefer simple conditionals while the cases remain stable; use an explicit strategy or dispatch structure when independently changing cases would make one conditional brittle.

## Surgical Changes

Touch only what is necessary. Clean up only changes created by the current work.

When editing existing code:
- Do not improve adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style, even if another style seems preferable.
- If unrelated dead code appears, mention it instead of deleting it.

When changes create orphans:
- Remove imports, variables, functions, and files made unused by the current changes.
- Do not remove pre-existing dead code unless explicitly asked.

Every changed line must trace directly to the user's request.

Handle errors at the boundary that owns recovery, translation, retry, or user communication. Preserve useful causes and do not swallow failures to make a test or command appear successful.

## Goal-Driven Execution

Define success criteria and loop until verified.

Transform tasks into verifiable goals:
- Add validation -> write tests for invalid inputs, then make them pass.
- Fix a bug -> write a test that reproduces it, then make it pass.
- Refactor a module -> ensure relevant tests pass before and after.

For multi-step tasks, state a brief plan:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria support independent execution. Weak criteria, such as make it work, require clarification.

## Success Signal

These guidelines are working when diffs contain fewer unnecessary changes, implementations need fewer rewrites due to overcomplication, and clarifying questions happen before implementation mistakes.
