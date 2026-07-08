---
type: Skill
name: langgraph
description: Use when coding, reviewing, or testing LangGraph workflows, graph state, nodes, edges, tools, checkpoints, retries, streaming, or AI analysis pipelines.
---

# LangGraph

Use this pack for graph-based AI workflows and analysis pipelines.

## Routing

- Load with Coding Agent for graph definitions, state schemas, nodes, edges, tool use, checkpoints, and streaming.
- Load with Code Review Agent when workflow state, retry behavior, data safety, or external model calls change.
- Combine with TypeScript Strict, prompt skills, persistence packs, and test packs.

## Guidance

- Keep graph state typed and small enough to inspect.
- Make each node responsible for one transformation or decision.
- Preserve traceability from inputs to generated outputs and review verdicts.
- Keep data-safety constraints close to model calls and prompt assembly.

## Verification

- Run focused workflow tests with deterministic fixtures.
- Test retry, partial failure, and resumed execution paths.
- Check prompt and output contracts when graph shape or state changes.
