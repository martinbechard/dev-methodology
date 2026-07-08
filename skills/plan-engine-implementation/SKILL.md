---
type: Skill
name: plan-engine-implementation
description: Use when coding, reviewing, or testing product code that implements planning engines, YAML plans, semantic review loops, evidence tracking, retry policy, or plan verification prompts.
---

# Plan Engine Implementation

Use this application-domain pack for product internals that create, validate, execute, or verify plans.

## Boundary

- This pack is for coding the plan engine inside a project.
- It is separate from the development agent's own planning behavior.
- Use Code Review Agent for fresh-context review when plan semantics or verification contracts change.

## Guidance

- Keep plan schema, execution state, evidence, and verdicts distinct.
- Make retry and resume behavior deterministic.
- Preserve traceability from plan items to source evidence and verification output.
- Avoid silent fallback plans that hide parser or semantic failures.

## Verification

- Run focused schema, parser, semantic review, retry, and verification prompt tests.
- Check malformed, incomplete, contradictory, and partially executed plans.
- Run build or typecheck after changing plan data structures.
