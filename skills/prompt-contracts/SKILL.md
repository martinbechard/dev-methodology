---
name: prompt-contracts
description: Review model-facing instructions, inputs, state, outputs, tool authority, retry behavior, evaluation coverage, and data boundaries without assuming a particular orchestration framework or model provider. Use for prompt review, tool-contract review, planning-contract review, or model-runtime boundary assessment.
metadata:
  category: development-practice
---

# Prompt Contracts

Trace promises across instructions, state, tools, outputs, retries, and verification.

## Workflow

1. Identify instruction sources, input schemas, state transitions, tool contracts, output consumers, and terminal outcomes.
2. Route specialized runtime guidance when repository evidence identifies an implementation variant.
3. Compare each stated promise with parser, schema, execution, recovery, and evaluation behavior.
4. Check authority, protected data, repeated side effects, cancellation, retry, and fallback ownership.
5. Report verified contracts, contradictions, missing evidence, corrections, and residual risk.

## Review Evidence

Read references/review-checklist-prompt-contracts.md during prompt or runtime contract review.
