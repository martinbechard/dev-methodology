---
name: codex-harness-directives
description: Apply Codex-specific safeguard and routing directives. Use when a generated Codex agent may create or modify repository files, launch subagents, or route work through Codex model profiles.
---

# Codex Harness Directives

This skill owns directives that apply to Codex-generated agents but do not belong in portable conceptual roles or cross-harness skills.

## Collaboration Subagent Launch Contract

A collaboration subagent is a bounded internal Codex dispatch owned by the launching Agent. It is not a separate user-visible Codex work-item task.

## Context Inheritance

- Set fork_turns to none for every collaboration subagent launch by default.
- Use a small positive recent-turn count only for a stated conversation-only dependency. The dependency must be unavailable in durable references and cannot be expressed adequately in the assignment prompt. Record the dependency and selected count in the launch announcement.
- Set fork_turns to all only when full parent-conversation inheritance is essential. Record an explicit task-specific justification in the launch announcement.
- Fresh context means fork_turns none. A bounded positive-turn exception is fresh only for the stated conversation-only dependency.

## Self-Contained Assignment

Every assignment states its objective, exact scope, durable references, required checks, expected result, and prohibitions. An assignment that omits any field is invalid and must not launch.

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
