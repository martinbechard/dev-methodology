# Separate Claim Policy From Claim Helper Family

Status: Running

Type: Defect

Provider: file

Work Item ID: separate-claim-policy-from-claim-helper-family

Completion: direct-main

## Summary

Keep `agent-claim` as the resource-coordination policy, introduce an exact `agent-claim-helper` Interface Skill, and rename its command-line and MCP providers so policy, interface, and implementation identities are no longer conflated.

## Context

`agent-claim` owns claim events, scope, conflict, deadline, uncertainty, and cleanup policy. `agent-claim-command` and `agent-claim-mcp` do not provide alternative policies; they explain two ways to execute the same helper operations. The current `agent-claim-*` family label therefore overlaps the policy skill's name and makes it easy to mistake `agent-claim` for a provider or the helper implementations for policy owners.

The corrected structure is:

- Policy skill: `agent-claim`
- Interface Skill: `agent-claim-helper`
- Family notation: `agent-claim-helper-*`
- Providers: `agent-claim-helper-command` and `agent-claim-helper-mcp`

Source inspection also found `agent-claim` telling callers to read status through the same configured "transport." The command-line helper is not a transport, and MCP is a protocol. Current test and design names repeat the same inaccurate shorthand.

## Source Evidence

On 2026-08-05, the user requested further naming and responsibility changes to be logged as work items, required Provider Skills to match their interface stem, and reiterated that "transport" must be reserved for an actual transport layer. The current policy/helper boundaries are in `skills/agent-claim/SKILL.md`, `skills/agent-claim-command/SKILL.md`, `skills/agent-claim-mcp/SKILL.md`, and the Resource Coordination scenario in `design/skill-groups/concurrent-tasking.md`.

## Requirements

- Keep `agent-claim` responsible only for resource-coordination and claim policy.
- Add `skills/agent-claim-helper/SKILL.md` as the exact Interface Skill publishing the common helper operations, inputs, structured outcomes, and uncertain-outcome reconciliation contract.
- Rename the two provider packages and frontmatter identities to `agent-claim-helper-command` and `agent-claim-helper-mcp`.
- Keep the command provider responsible for local command invocation and the MCP provider responsible for MCP tool calls and protocol-specific result handling.
- Preserve the MCP provider's current unavailable-until-parity boundary; interface conformance does not imply runtime availability.
- Make Project Configurator and generated AGENTS.md routing select exactly one verified helper provider only when resource coordination selects `agent-claim`.
- Replace inaccurate non-network `transport` wording with `claim helper`, `command-line invocation`, `MCP protocol`, `tool call`, or an actual named transport such as stdio or WebSockets when one is evidenced.
- Rename helper-focused tests and documentation whose `transport` label groups command invocation with MCP rather than testing an actual communication transport.
- Update interface, policy, provider, setup, routing, migration, and unavailable-provider evaluations and stale-name checks.

## Acceptance Criteria

- `agent-claim`, `agent-claim-helper`, `agent-claim-helper-command`, and `agent-claim-helper-mcp` have distinct, non-overlapping documented responsibilities.
- The helper providers share the complete `agent-claim-helper-` stem and realize the same helper contract.
- Project guidance loads policy plus one verified helper provider when selected and loads neither when resource coordination is none.
- No maintained source or generated output uses the retired helper identities.
- Maintained resource-coordination documentation does not call command invocation or MCP itself a transport.
- Command and MCP parity tests retain every existing operation and structured outcome, including the truthful unavailable MCP boundary.
- Focused setup, helper, policy, bundle, migration, and stale-name checks pass.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate the policy, interface, both renamed providers, and Project Configurator package.
- Run claim-policy tests, renamed helper parity tests, project-configuration tests, bundle tests, and evaluation coverage checks.
- Regenerate skill metadata, Agent guidance, native adapters, hierarchy views, and documentation, then run freshness checks.
- Search maintained sources for the retired helper identities and inaccurate `command transport` or `MCP transport` wording.
- Run `git diff --check` and obtain fresh independent methodology review and verification.

## Open Questions

None. An implementation may name an evidenced stdio or WebSocket transport separately, but the provider identities remain command-line and MCP helper implementations.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-claim/SKILL.md
- skills/agent-claim-command/SKILL.md
- skills/agent-claim-mcp/SKILL.md
- skills/agent-claim-helper/SKILL.md
- skills/agent-claim-helper-command/SKILL.md
- skills/agent-claim-helper-mcp/SKILL.md
- skills/create-project-configuration/SKILL.md
- agents/roles/project-setup/project-configurator.role.yaml

### Allowed Dependent Artifacts

- AGENTS.md
- PROJECT.yaml
- README.md
- skills/agent-claim-command/scripts/claim.py moved with the renamed command provider.
- scripts/render-agents-technology-skills.py
- scripts/test_agent_claim.py
- scripts/test_agent_claim_transport.py renamed to a claim-helper test identity.
- scripts/test_bundle_content.py
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/skill-groups/concurrent-tasking.md
- design/agentic-configuration.html
- design/orchestrated-development-lifecycle.html
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- Provider package `agents/openai.yaml` metadata moved or generated for only the approved old and new package identities.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify naming and responsibility changes and log them as additional work items, including the directions that providers match their interface stem and engineering terms name the actual mechanism. Approval is limited to the exact governed canonical paths above and the stated rename destinations.

## Notes

The Running `store-agent-claim-state-in-gitignored-project-directory` item changes the same policy and helper sources. That is a current exact-path and integration overlap to coordinate; it is not a hard prerequisite because this item can complete independent discovery and reconcile from whichever accepted claim-state version reaches main first.

## Starting Reservation — 2026-08-06T06:13:26Z

- Transition: Ready -> Starting.
- Coordinator reservation: Dev Backlog Coordinator reserved this Work Item ID on current main at 2026-08-06T06:13:26Z.
- Owner handoff: Dev Backlog Coordinator retains reservation ownership and will hand off to one root Dev Orchestrator after launch acceptance.
- Root Agent Task: Not assigned; no child task was created by this reservation transaction.
- Claim-state dependency note: store-agent-claim-state-in-gitignored-project-directory remains paused in User Action Required with no live work claim in the current registry; this reservation does not mutate that provider record.
- Launch result: Pending; this provider transaction does not start a task or create execution ownership.
- Next action: Launch one root Dev Orchestrator and record Starting -> Running only after accepted execution evidence.

## Current Execution

Transition: Starting -> Running.

Owner: Root Dev Orchestrator.

Root Agent Task: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Canonical Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Branch: codex/separate-claim-policy-from-claim-helper-family.

Worktree: /Users/martinbechard/.codex/worktrees/1bee/dev-methodology.

Baseline/Main Coordinator Commit: cc5574b798c0fab87fb5c9c6b3c6acd935030feb.

Delegated Source Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Phase: Implementation.

Started At: 2026-08-06T06:19:50Z.

Accepted Execution Evidence: Root Dev Orchestrator accepted this exact Work Item ID for the Starting -> Running transition in canonical task 019fd5b5-aca7-7cb1-9ae0-012fb84e13db and supplied the canonical branch, isolated worktree, and baseline commit.

Provider Operation Evidence: Work Item ID update claim separate-claim-policy-from-claim-helper-family-update-correction and exact provider path claim separate-claim-policy-from-claim-helper-family-path-correction both returned SHARED_CHECKOUT_ACQUIRED before this mutation.

Verified Title Handoff: Implementing — Separate Claim Policy From Claim Helper Family.

Next Action: Reacquire the exact activity=work claim and resume the bounded Dev Coder lane from its preserved isolated diff.

Next Reconciliation At: 2026-08-06T06:37:19Z.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Evidence: Root paused the Dev Coder at a safe checkpoint and released work claim separate-claim-policy-work-019fd5b5-3 with disposition handoff; no command is running. The initial missing-interface boundary was RED, and the focused three-test slice was GREEN. The full helper module result is unclaimed because output was truncated and must be rerun quietly. Generators and the refreshed stale scan are pending; the candidate remains preserved. The exact current candidate diff footprint is 17 paths (11 current/added, 6 retired). The canonical Root Dev Orchestrator remains on branch codex/separate-claim-policy-from-claim-helper-family in worktree /Users/martinbechard/.codex/worktrees/1bee/dev-methodology, with baseline/main coordinator commit cc5574b798c0fab87fb5c9c6b3c6acd935030feb and parent/delegated source task 019fb057-1767-7ef2-b5fa-41f4417b20b3. Title remains verified: Implementing — Separate Claim Policy From Claim Helper Family.

Coordinator Scope Disposition: The seven paths scripts/agent_skill_evals/validation.py, scripts/test_role_mutation_policy.py, scripts/test_technology_detection.py, evals/agent-tests/dev-orchestrator/test_fixtures.py, evals/agent-tests/wiki-ingester/executable_harness.py, evals/projects/project-configuration-routing/TASK.md, and evals/projects/project-configuration-routing/available-skills.txt are ordinary non-governed support consumers already authorized by requirements and acceptance. Only minimal identity/path replacements are permitted. No User Action Required or lifecycle change, new approval, or broad suite is authorized.

Observed At: 2026-08-06T06:44:22Z.

Started At: 2026-08-06T06:17:04Z.

Deadline or Expires At: 2026-08-06T08:44:22Z.

Next Action: Reacquire exact activity=work and resume the same paused Dev Coder for quiet focused tests, stale-name classification, generators/freshness checks, and candidate commit.

Next Reconciliation At: 2026-08-06T06:59:22Z.
