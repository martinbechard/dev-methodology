# Separate Claim Policy From Claim Helper Family

Status: Completed

Type: Defect

Provider: file

Work Item ID: separate-claim-policy-from-claim-helper-family

Completion: direct-main

Owner: Unowned

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

Phase: Final Fresh Re-review After Correction Attempt 2.

Owner: Unowned.

Started At: 2026-08-06T06:19:50Z.

Accepted Execution Evidence: Root Dev Orchestrator accepted this exact Work Item ID for the Starting -> Running transition in canonical task 019fd5b5-aca7-7cb1-9ae0-012fb84e13db and supplied the canonical branch, isolated worktree, and baseline commit.

Provider Operation Evidence: Work Item ID update claim separate-claim-policy-from-claim-helper-family-update-correction and exact provider path claim separate-claim-policy-from-claim-helper-family-path-correction both returned SHARED_CHECKOUT_ACQUIRED before this mutation.

Verified Title Handoff: Reviewing — Separate Claim Policy From Claim Helper Family.

Next Action: Reacquire the exact activity=work claim and resume the bounded Dev Coder lane from its preserved isolated diff.

Next Reconciliation At: 2026-08-06T06:37:19Z.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Accepted Candidate Commit: ac8270d2570436738fd1b0b6bb2dbbedb690049a.

Accepted Candidate Commit: 9501f48c6b0f6f52c8fad8eab3df92d524e26a38.

Accepted Candidate Commit: 5fa7620a6471574d2bf84a12e541805780d4bac6.

Evidence: Root released work claim separate-claim-policy-work-019fd5b5-12 with disposition handoff. Final attempt 2 commit 5fa7620a6471574d2bf84a12e541805780d4bac6 is clean on top of 9501f48c. Findings are resolved: current outcomes are separated from legacy normalization with reachability tests; concurrent-tasking uses the exact Operation Contract and full members; and the bundle unavailability assertion is definitive. GREEN helper26/provider-family6/bundle2 plus metadata, skill, evaluation, support, hierarchy, and diff freshness checks are recorded. The worktree is clean. A same-criteria material failure requires blocker handoff, not a third correction. Intended title: Reviewing — Separate Claim Policy From Claim Helper Family.

Coordinator Scope Disposition: The seven paths scripts/agent_skill_evals/validation.py, scripts/test_role_mutation_policy.py, scripts/test_technology_detection.py, evals/agent-tests/dev-orchestrator/test_fixtures.py, evals/agent-tests/wiki-ingester/executable_harness.py, evals/projects/project-configuration-routing/TASK.md, and evals/projects/project-configuration-routing/available-skills.txt are ordinary non-governed support consumers already authorized by requirements and acceptance. Only minimal identity/path replacements are permitted. No User Action Required or lifecycle change, new approval, or broad suite is authorized.

Observed At: 2026-08-06T07:45:27Z.

Started At: 2026-08-06T06:17:04Z.

Deadline or Expires At: 2026-08-06T09:45:27Z.

Next Action: Reacquire exact activity=work and dispatch entirely new fresh-context Dev Code Reviewer and Methodology Artifact Reviewer against final head 5fa7620a; if either finds the same material criteria failing, perform blocker handoff, no third correction. Verification waits for both acceptance gates.

Next Reconciliation At: 2026-08-06T07:57:27Z.

## Blocked Evidence

Transition: Running -> Blocked.

Blocked At: 2026-08-06T07:53:48Z.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Intended Title: Blocked — Separate Claim Policy From Claim Helper Family.

Preserved Candidates: ac8270d2570436738fd1b0b6bb2dbbedb690049a; 9501f48c6b0f6f52c8fad8eab3df92d524e26a38; 5fa7620a6471574d2bf84a12e541805780d4bac6.

Final Review Evidence: Both final independent reviews returned NEEDS_CORRECTION. Released work claim separate-claim-policy-work-019fd5b5-13 has outcome RELEASED, disposition blocked, blocker reference correction-loop-exhausted-final-review, and event 60585bc8-9252-4900-ba1c-8bfe49397529.

Confirmed Findings: (1) The concurrent-tasking class diagram omits Extend Claim, Extend Claim Deadline, Heartbeat Claim, and Reset Claim Registry. (2) The agent-claim-helper report contract says segment agent and acquisition outcome, but the command/design schema uses owner and omits acquisition outcome. (3) create-project-configuration says the selected helper is loaded “by reference,” while the renderer, README, tests, and AGENTS inline it.

Blocker Owner: Dev Backlog Coordinator.

Observable Unblock Condition: One later evidence-backed Coordinator recovery disposition authorizes a fresh bounded cycle limited to these three findings after re-reading current main, using the same original coder and candidate only. Then transition Blocked -> Ready -> Starting -> Running before mutation.

Requested Next Action Owner: Dev Backlog Coordinator.

Scope Boundary: No correction attempt 3, no other changes, broad suites, or new framework.

## Recovery Ready Evidence

Transition: Blocked -> Ready.

Transitioned At: 2026-08-06T08:00:41Z.

Coordinator Recovery Authorization: Parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3 supplied an evidence-backed recovery disposition that satisfies the recorded unblock condition and authorizes one fresh bounded cycle.

Satisfied Unblock Evidence: Recovery is limited to the three preserved findings on candidate 5fa7620a6471574d2bf84a12e541805780d4bac6, with the same canonical task/conversation 019fd5b5-aca7-7cb1-9ae0-012fb84e13db, branch codex/separate-claim-policy-from-claim-helper-family, worktree /Users/martinbechard/.codex/worktrees/1bee/dev-methodology, and original coder.

Ready Scope: Reconcile only the class-diagram operation members, the report segment-field contract, and the helper-routing inline-versus-reference mismatch. Preserve all blocker, candidate, final-verdict, canonical-identity, attempt-history, and scope evidence.

Next Action: Ready -> Starting through the authorized Coordinator and then Starting -> Running before mutation.

## Starting Handoff Evidence

Transition: Ready -> Starting.

Reservation At: 2026-08-06T08:01:52Z.

Coordinator Reservation and Dispatch Authority: Parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3 authorized this reservation and dispatch.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db; the existing canonical work-item task is adopted without replacement.

Owner: Dev Backlog Coordinator retains reservation ownership pending launch acceptance.

Owner: Root Dev Orchestrator.

Objective: One fresh bounded recovery limited to the three preserved findings on candidate 5fa7620a6471574d2bf84a12e541805780d4bac6, using the same original coder.

Launch Result: Started.

Next Reconciliation At: 2026-08-06T08:11:52Z.

Required Next Acceptance: The existing canonical Root Dev Orchestrator must accept Starting -> Running before mutation.

## Active Execution Evidence (Fresh Recovery)

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Branch: codex/separate-claim-policy-from-claim-helper-family.

Worktree: /Users/martinbechard/.codex/worktrees/1bee/dev-methodology.

Candidate Chain: ac8270d2570436738fd1b0b6bb2dbbedb690049a -> 9501f48c6b0f6f52c8fad8eab3df92d524e26a38 -> 5fa7620a6471574d2bf84a12e541805780d4bac6.

Phase: Direct-Main Integration.

Observed At: 2026-08-06T08:02:56Z.

Started At: 2026-08-06T08:02:56Z.

Deadline or Expires At: 2026-08-06T09:02:56Z.

Evidence: The same canonical Root Dev Orchestrator is active with the original coder implement_claim_helper_family. It will acquire the exact activity=work claim, then dispatch only the three authorized findings preserved by Coordinator recovery. No other source, candidate, provider, broad suite, or framework mutation is authorized.

Next Action: Acquire the exact activity=work claim and dispatch only the three authorized findings to the same original coder.

Next Reconciliation At: 2026-08-06T08:14:56Z.

## Active Execution Evidence (Review Checkpoint)

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Accepted Recovery Candidate: b953b9fe31fe3cb256a68defcc634f66b3233532.

Observed At: 2026-08-06T08:10:06Z.

Started At: 2026-08-06T08:10:06Z.

Deadline or Expires At: 2026-08-06T09:10:06Z.

Evidence: The candidate branch is clean. Its exact seven paths and four focused tests plus freshness checks are GREEN. Work claim separate-claim-policy-recovery-work-019fd5b5 was released with outcome RELEASED and disposition handoff at event 87409873-12c4-41f5-abb4-af3d8e5f366b. The canonical root will dispatch exactly one fresh Dev Code Reviewer and one fresh Methodology Artifact Reviewer, then a verifier only if both accept.

Next Action: Reacquire exact activity=work and dispatch exactly one fresh Dev Code Reviewer plus one fresh Methodology Artifact Reviewer; run a verifier only if both accept.

Next Reconciliation At: 2026-08-06T08:22:06Z.

## Active Execution Evidence (Verification Checkpoint)

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Branch: codex/separate-claim-policy-from-claim-helper-family.

Worktree: /Users/martinbechard/.codex/worktrees/1bee/dev-methodology.

Accepted Candidate: b953b9fe31fe3cb256a68defcc634f66b3233532 (clean).

Observed At: 2026-08-06T08:15:41Z.

Started At: 2026-08-06T08:15:41Z.

Deadline or Expires At: 2026-08-06T09:15:41Z.

Review Evidence: Fresh Dev Code Reviewer recovery_code_review returned ACCEPTED with no findings. Fresh Methodology Artifact Reviewer recovery_methodology_review returned ACCEPTED with no findings. Both confirmed the three exact corrections, seven-path scope, focused tests, generated alignment, and no current-main overlap. Review work claim separate-claim-policy-recovery-review-work-019fd5b5 was released RELEASED/handoff at event a2254dde-b3e8-411f-b42d-73897d8013a2.

Next Action: Reacquire exact activity=work and dispatch exactly one fresh focused Dev Verifier; integrate only after verifier acceptance.

Next Reconciliation At: 2026-08-06T08:27:41Z.

## Active Execution Evidence (Integration Checkpoint)

Condition Type: root-execution.

Owner: Root Dev Orchestrator.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Accepted Candidate: b953b9fe31fe3cb256a68defcc634f66b3233532 (clean).

Observed At: 2026-08-06T08:21:30Z.

Started At: 2026-08-06T08:21:30Z.

Deadline or Expires At: 2026-08-06T09:21:30Z.

Verification Evidence: Fresh code and methodology reviews ACCEPTED. Fresh focused verifier recovery_focused_verifier returned PASS for four regression methods, five freshness checks, range diff hygiene, clean state, and mapping all three criteria. Broad, live, browser, and simulator suites were excluded as directed. Verification claim separate-claim-policy-recovery-verify-work-019fd5b5 was released RELEASED/handoff at event 29bb794a-48f1-4468-95f9-c1a17f3f838b.

Next Action: Reacquire exact activity=work, obtain the final project-files integration claim, create a fresh integration branch from current main, apply only accepted candidate content/commits, run smallest integration-sensitive checks, and integrate to main.

Next Reconciliation At: 2026-08-06T08:33:30Z.

## Terminal Delivery Evidence

Transition: Running -> Completed.

Completed At: 2026-08-06T08:28:30Z.

Canonical Task and Conversation: 019fd5b5-aca7-7cb1-9ae0-012fb84e13db.

Accepted Source Candidate: b953b9fe31fe3cb256a68defcc634f66b3233532, preserving candidate chain ac8270d2570436738fd1b0b6bb2dbbedb690049a -> 9501f48c6b0f6f52c8fad8eab3df92d524e26a38 -> 5fa7620a6471574d2bf84a12e541805780d4bac6 -> b953b9fe31fe3cb256a68defcc634f66b3233532.

Independent Review: Fresh Dev Code Reviewer recovery_code_review returned ACCEPTED with no findings. Fresh Methodology Artifact Reviewer recovery_methodology_review returned ACCEPTED with no findings.

Source Verification: Fresh focused verifier recovery_focused_verifier returned PASS for the four exact regression methods, five changed-surface freshness checks, range diff hygiene, clean worktree state, and all three recovery criteria. Broad, browser, live MCP, simulator, and framework suites were excluded as directed.

Integration Branch: codex/separate-claim-policy-from-claim-helper-family-integration.

Integration Mapping: Fresh integration branch started from current main 0b9e26d5d0f032f46e5bbab5f3320eefb359d79b. The four accepted candidate commits were replayed without importing candidate ancestry and committed as 3273f153c171e3959838e476c4ab98752344cc14. Candidate b953b9fe31fe3cb256a68defcc634f66b3233532 and integration commit 3273f153c171e3959838e476c4ab98752344cc14 are byte-equivalent for every non-backlog path.

Main Delivery: Configured main fast-forwarded from 0b9e26d5d0f032f46e5bbab5f3320eefb359d79b to 3273f153c171e3959838e476c4ab98752344cc14. Integration commit 3273f153c171e3959838e476c4ab98752344cc14 is reachable from main, and main was clean after delivery.

Post-Integration Verification: On authoritative main, the four exact claim-helper recovery tests passed. OpenAI metadata, skill documentation, evaluation documentation, support checklist, and agent-skill hierarchy freshness checks passed. Git diff hygiene and clean-state checks passed.

Remote Observation: Remote publication was not requested or configured as part of this local direct-main completion.

Integration Claim Closeout: Project-files integration claim separate-claim-policy-main-integration-files released with outcome RELEASED at event 1e98af2f-436a-4bff-ae9f-2a01e07a160c. Work claim separate-claim-policy-integration-work-019fd5b5 released with outcome RELEASED and disposition handoff at event b17125e6-5b18-4163-91c0-1ecf41fcdc53.

Terminal Provider Claims: Update claim separate-claim-policy-terminal-update-root acquired with outcome SHARED_CHECKOUT_ACQUIRED, incarnation 4740f4e7-4feb-47a6-9e45-514c250b4286. Exact source-and-destination path claim separate-claim-policy-terminal-provider-paths acquired with outcome SHARED_CHECKOUT_ACQUIRED, incarnation 0a7ac21e-ded2-4ed6-89ca-57b98871d114.

Archive Path: backlog/completed-backlog/defects/separate-claim-policy-from-claim-helper-family.md.

Integration Residue: None.

Remaining Blockers: None.

Cleanup Eligibility: The delivered integration branch and preserved source branch are clean and eligible for later Coordinator cleanup. The canonical Codex task remains unarchived as directed.
