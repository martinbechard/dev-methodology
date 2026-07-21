# Configure Agent Claim Transport Adapters

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/configure-agent-claim-transport-adapters.md

Completion: direct-main

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Separate agent-claim policy from its MCP and command execution procedures, and configure one verified transport during project setup so runtime agents neither probe nor fall back dynamically.

## Context

The user-reviewed dialogue on 2026-07-21 rejected runtime MCP probing and fallback as wasteful and delay-inducing. The current agent-claim skill combines claim semantics, MCP routing, command fallback, capability checks, and ambiguous-dispatch recovery in one procedure.

The desired boundary is one shared claim-semantics contract plus two mutually exclusive transport adapters. Candidate skill identifiers are agent-claim-mcp and agent-claim-command; final names remain subject to source discovery and definition approval.

## Source Evidence

- On 2026-07-21, the user rejected dynamic MCP probing and fallback because it adds avoidable delay.
- The user then proposed splitting the steps required to obtain a claim through MCP from those required to obtain it through a script, and accepted continued design discussion on that basis.
- On 2026-07-21, the user explicitly requested creation of work items based on the completed conversations.

## Requirements

- Keep claim scope, conflicts, acquisition states, recovery, heartbeat expectations, release safety, and completion meaning in one shared agent-claim semantics contract.
- Put exact MCP tool calls, structured results, and MCP-specific error handling in one adapter procedure.
- Put command discovery, arguments, exit codes, JSON results, and command-specific error handling in another adapter procedure.
- Make Project Configurator select and verify exactly one transport during setup.
- Render the chosen transport into AGENTS.md so runtime agents invoke it directly.
- Remove runtime probing and dynamic fallback between transports.
- Fail explicitly and request reconfiguration when the configured transport is unavailable.
- Preserve ambiguous-dispatch reconciliation without switching transports.
- Obtain exact, scope-specific approval before changing any governed skill definition.

## Acceptance Criteria

- A configured MCP project loads only the shared semantics and MCP adapter instructions.
- A configured command project loads only the shared semantics and command adapter instructions.
- Runtime claim operations do not probe the unused transport or switch transports after failure.
- Both adapters produce behaviorally equivalent coordination results for supported operations.
- Transport unavailability produces a deterministic configuration error rather than fallback latency.
- Tests cover setup verification, generated guidance, success, structured rejection, unavailable transport, and ambiguous dispatch.

## Dependencies

None.

## Verification

- Inventory current MCP and command branches in agent-claim and their callers.
- Determine whether supported runtimes can compose the shared contract and one adapter directly; otherwise specify generator materialization.
- Run exact governed-definition checks after user approval.
- Run focused adapter parity, configuration, generation, and failure-path tests.
- Run Git diff validation and independent methodology review.

## Open Questions

- Should the adapters be standalone skills composed at generation time, or generated materializations owned by agent-claim for runtimes that cannot compose skills?

## Notes

- Direct registry-file editing is not a supported transport because it bypasses atomic validation.
- This item does not change claim outcome names; that is tracked separately.
