---
name: codex-harness-directives
description: Apply Codex-specific safeguard and routing directives. Use when a generated Codex agent may create or modify repository files, launch subagents, or route work through Codex model profiles.
---

# Codex Harness Directives

This skill owns directives that apply to Codex-generated agents but do not belong in portable conceptual roles or cross-harness skills.

## Skill Instruction Loading

- When the configured mcp-agent-ops skill_load operation is available, load the complete selected set of skills that is not already in context in one bounded skill_load call.
- Do not list the catalog before loading known skill names. Do not load known skills individually, construct terminal commands for their retrieval, or reread skills already returned in the current context.
- Use the supplied filesystem-backed SKILL.md paths when skill_load is unavailable or the configured server cannot initialize or connect. Read each fallback file completely, using bounded reads that do not require repeating truncated bulk output.
- Apply the same rule when later routing selects request-specific skills. Load supporting resources only after their owning skill instructions identify those resources as required.

## Collaboration Subagent Launch Contract

A collaboration subagent is a bounded internal Codex dispatch owned by the launching Agent. It is not a separate user-visible Codex work-item task.

## Context Inheritance

- Set fork_turns to none for every collaboration subagent launch by default.
- Use a small positive recent-turn count only for a stated conversation-only dependency. The dependency must be unavailable in durable references and cannot be expressed adequately in the assignment prompt. Record the dependency and selected count in the launch announcement.
- Set fork_turns to all only when full parent-conversation inheritance is essential. Record an explicit task-specific justification in the launch announcement.
- Fresh context means fork_turns none. A bounded positive-turn exception is fresh only for the stated conversation-only dependency.

## Self-Contained Assignment

Every assignment states its objective, exact scope, durable references, required checks, expected result, and prohibitions. An assignment that omits any field is invalid and must not launch.

## Single-Turn Subagent Iterations

- The existing fork_turns none default gives each collaboration subagent fresh launch context. This section prevents that context from growing through later reuse.
- Give each collaboration subagent a semantic assignment name, such as page-coder or verifier-procedure-coder. A sequence number is not required.
- Give each collaboration subagent exactly one execution turn. After it returns, treat that subagent identity as finished.
- Never call followup_task or otherwise reuse a finished collaboration subagent, even for the same assignment, a correction, retry, rereview, or continuation. Do not request or enable allow_reuse when a runtime exposes that option.
- Launch a new fresh-context collaboration subagent for every later turn. This does not replace, archive, or recreate the separate canonical user-visible Work Item task.

## Compact Durable Handoff

Build each later assignment from the authoritative Work Item and durable evidence, not the prior subagent conversation. Include the provider locator, semantic assignment, current candidate commit when one exists, relevant plan, review, test, or receipt locators when they exist, the exact delta, and preservation or prohibition boundaries. Reference stable facts already stored in those sources instead of copying the full conversational or lifecycle history.

## SOLO Measurement Trial

When the user enables this protocol during SOLO operation, use Agent Report after each terminal Work Item to record collaboration subagent identities and execution-turn counts, cache-inclusive tokens, uncached input plus output tokens, and estimated API-equivalent cost with its pricing assumption. The protocol succeeds only when no collaboration subagent identity has more than one execution turn. Measurement is not a delivery gate: do not rerun work, create synthetic Work Items, or add evaluation cases solely to collect it.

## Launch Announcement

Send exactly one concise user-visible launch announcement immediately before the dispatch. State the subagent name, assignment, and context inheritance. State the role and model only when either value is overridden. Add no plan, progress, lifecycle history, evidence summary, or surrounding explanation, and do not repeat the announcement.

## Subagent Return

A collaboration subagent returns only a final outcome or one specific decision the owning Agent cannot make. Routine progress receipts, heartbeat messages, lifecycle-history summaries, or repeated evidence messages are prohibited. The owner observes runtime state through collaboration tools and reads durable evidence only when a decision requires it.

## Separate Codex Task Boundary

Separate user-visible Codex work-item tasks remain governed by coordinate-codex-tasks. They use explicit provider and canonical-task handoffs, receive a self-contained dispatch prompt, and receive no implicit parent-conversation inheritance.

## Safeguard Routing

- Do not generate, delegate, retry, or split a prompt that asks a Sol-, Terra-, or Luna-backed Codex agent to perform cybersecurity work.
- If the current task or a planned delegation crosses that boundary, preserve completed work and return the routing requirement to the parent agent or user so a supported route can be selected.
- Treat an additional automated-safeguard check as a stop signal for that dispatch. Do not try to bypass it by rephrasing, fragmenting, or moving the same request to another affected agent.
- Do not infer or state that the safeguard notice itself means the user violated a policy. Report only the observed stop and the required routing change.

## Scope

- Apply these directives only in the Codex harness.
- Keep project instructions, role authority, skill procedures, and verification requirements unchanged.
- Do not copy these directives into provider-neutral role definitions or generated agents for other harnesses.
