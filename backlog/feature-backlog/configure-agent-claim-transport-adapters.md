# Configure Agent Claim Transport Adapters

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/configure-agent-claim-transport-adapters.md

Completion: direct-main

## Current Execution

- Owner: Dev Orchestrator
- Claim: None; the exact Running-record transaction is released after this committed transition, and artifact ownership must be acquired separately before integration.
- Canonical task: 019f870e-5de9-7730-a8ca-658250ba8b24
- Worktree: /Users/martinbechard/.codex/worktrees/87f4/dev-methodology
- Branch: codex/configure-agent-claim-transport-adapters-reconcile-019f870e
- Starting main: 71771f33507ab1e4aa529c07cb2f581f5384874d
- Phase: Reconcile the preserved independently accepted candidate 1b276dc63b1901b98c1731b695348f8c11b9be1f onto fresh current main, preserve current-main contracts, integrate only the accepted transport-adapter scope, run focused post-integration verification, and complete the backlog item separately.
- Started: 2026-07-21
- Running-record claim: start-claim-transport-adapters-019f86a0, acquired event cc4e4dbb-24bb-4750-b99d-bc61968ff342.
- Open issues: None. Do not replay or import the rejected simplify-project-configuration candidate.
- Accepted candidate: 1b276dc63b1901b98c1731b695348f8c11b9be1f, independently ACCEPTED and VERIFIED-WARN with only two unrelated pre-existing Wiki Ingester warnings.
- Integration wait started: 2026-07-21T22:52:00Z.
- Claim attempts: 7 total at initial, 5, 10, 15, 20, 25, and 30 minutes.
- Final outcome: CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED at event ecd65be9-8ab5-4f69-ac94-ada954a3ba1f.
- Prior wait events: 501d508e-87d1-4d6d-b397-30c319551863, 8facc903-da42-4f81-b4a8-541a7fe2657f, 8e1f6ca6-6fbc-44c2-9c47-442728ab1b4b, 1168cf58-89d6-4b67-b649-46c89dce7d06, 1d6b91c6-c6ca-47ca-b7f0-6e851c34ed40, and 26a0b96f-b697-4f6e-99f1-8495754b5f2c.
- Unblock condition: simplify-project-config-impl-019f86b1 releases normally after its correction is committed or safely handed off, and fresh-main reconciliation confirms the accepted transport contract can be integrated without discarding either contribution.
- Resumption: Preserve these exact Blocked bytes until the unblock condition is satisfied; then transition through Ready, acquire new exclusive ownership, record the new owner, and only then set Running.
- Blocked-handoff claim: block-claim-transport-integration-019f86a0, acquired event 0580f671-8d86-4c5b-9fc7-89f48b0f4231.

## Resumption Evidence

- Pre-attempt Blocked state: commit c9b29931f3b4c316f63ecff93264b5b412361ea0, blob 429e9a534ab8c230737e48373bb81e98a1072a07, Status Blocked, Owner Unowned, Claim None.
- Unblock evidence: simplify-project-config-impl-019f86b1 released cleanly at event a9a6193b-3784-4fc3-a59b-5dfe0adcbe6a, and its separate Blocked lifecycle transaction committed as 71771f33507ab1e4aa529c07cb2f581f5384874d and released at event f7b82231-19ae-41e7-833c-c36fd10ee41d.
- Failed resumption attempt: event 49c4b151-363c-4859-a33f-22c39497fa3b returned SHARED_CHECKOUT_RELEASE_REQUIRED while the simplify lifecycle transaction held the shared checkout; the exact Blocked bytes were preserved and no owner was inferred.
- Eligibility transition: the released blocker satisfied the recorded unblock condition, making this item Ready for a fresh owner before the successful acquisition below.
- Successful new ownership: resume-claim-transport-019f870e acquired the exact backlog file at event 7c834eac-ec6f-4efc-8af2-7da1a098f7ac; only after that acquisition were the new Dev Orchestrator owner and Status Running recorded.
- Preserved delivery evidence: accepted candidate 1b276dc63b1901b98c1731b695348f8c11b9be1f remains durable on codex/configure-agent-claim-transport-adapters and must be reconciled rather than reimplemented.

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

- Answer: Approved.
- User wording: "yes".
- Date: 2026-07-21.
- Provenance: direct user response in parent backlog-coordination task 019f77f4-c4bd-7c91-b197-c987a7beb838 to the exact eight-path question recorded above.
- Approved governed scope: the eight definition paths listed in the question above.
- Approved dependent scope: their supported generated mirrors and directly related non-governed project configuration, renderer, validation, documentation, and focused test surfaces required by this work item.
- Exclusions: no other governed definition unless separately approved.
- Disposition: Ready for a fresh canonical Dev Orchestrator task.

### Unattended Work Boundary

Implementation is authorized only within the exact resolved scope above. Preserve the decision to use standalone adapter skills rather than generator-owned materializations.

### Discovery Evidence

- Canonical task: 019f85c8-626e-77b2-8b7e-09a893d60c1b.
- Discovery branch/worktree were clean and removed after routing the question; fresh delivery must start from current main.
- Composition evidence: mutating roles keep transport-neutral agent-claim semantics; PROJECT.yaml and generated AGENTS.md select exactly one standalone MCP or command adapter; the command implementation moves with the independently distributable command adapter.
- UAR routing claim: route-agent-claim-adapters-approval, acquired event 779b72b1-c565-44b9-9f93-c45b5586fcc0.
- Approval transaction claim: approve-claim-transport-adapters-20260721, acquired event dfb1ec1a-ead3-4888-815d-0985f490f50a.

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
