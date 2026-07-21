# Configure Agent Claim Transport Adapters

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/configure-agent-claim-transport-adapters.md

Completion: direct-main

## Discovery Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f85c8-626e-77b2-8b7e-09a893d60c1b
- Worktree: /Users/martinbechard/.codex/worktrees/4e3b/dev-methodology
- Branch: codex/configure-agent-claim-transport-adapters
- Starting main: 2624b5b25ba6e5548051d7b9953933b1e57b3f87
- Phase: Bounded transport inventory and exact governed-scope discovery completed; implementation is paused for path-specific approval.
- Started: 2026-07-21
- Running-record claim: start-agent-claim-transport-adapters-019f85c8, acquired event 8a69729f-031d-465d-8ff1-2e0c3951e62c.
- Open issues: The exact eight-path governed-definition scope requires the user answer below.
- Accepted candidate: Pending.

## User Action Required

### Question For The User

Do you approve changes to exactly the eight governed-definition paths listed below for this work item, with standalone agent-claim-mcp and agent-claim-command adapters selected and verified by Project Configurator, and with no other governed definition changed unless separately approved?

1. skills/agent-claim/SKILL.md
2. skills/agent-claim/agents/openai.yaml
3. skills/agent-claim-mcp/SKILL.md
4. skills/agent-claim-mcp/agents/openai.yaml
5. skills/agent-claim-command/SKILL.md
6. skills/agent-claim-command/agents/openai.yaml
7. skills/create-project-configuration/SKILL.md
8. agents/roles/project-setup/project-configurator.role.yaml

### Why User Input Is Required

The evidence-backed design requires eight governed definition paths. Repository policy requires exact path-specific approval before mutation.

### Options And Tradeoffs

- Approve the exact eight-path scope: implement standalone transport skills selected by Project Configurator.
- Narrow the scope by naming allowed paths: preserve the remaining behavior as blocked follow-up work.
- Defer: retain the discovery result without implementation.

### Resolution

Pending.

### Unattended Work Boundary

No governed or project mutation is authorized while this question is pending. Preserve the decision to use standalone adapter skills rather than generator-owned materializations.

### Discovery Evidence

- Canonical task: 019f85c8-626e-77b2-8b7e-09a893d60c1b.
- Clean branch/worktree: codex/configure-agent-claim-transport-adapters at /Users/martinbechard/.codex/worktrees/4e3b/dev-methodology, based on 2624b5b25ba6e5548051d7b9953933b1e57b3f87.
- Composition evidence: mutating roles keep transport-neutral agent-claim semantics; PROJECT.yaml and generated AGENTS.md select exactly one standalone MCP or command adapter; the command implementation moves with the independently distributable command adapter.
- UAR routing claim: route-agent-claim-adapters-approval, acquired event 779b72b1-c565-44b9-9f93-c45b5586fcc0.

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
