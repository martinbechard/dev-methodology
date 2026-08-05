# Scope Skill-Under-Test Protection To Agent Tests

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/scope-skill-under-test-protection-to-agent-tests.md

Completion: direct-main

Owner: Root Dev Orchestrator

## Summary

Return `scripts/render-agents-technology-skills.py` to its single technology-detection and rendering responsibility. Move the special no-mutation rule for a skill or agent under test into the existing `evals/agent-tests/AGENTS.md` protocol, where test agents inherit it together with the root `AGENTS.md` instructions and must log findings instead of changing the target to make a test pass.

## Context

The current repository-wide agent-and-skill definition approval/precheck policy was placed in `PROJECT.yaml`, generated root `AGENTS.md` guidance, and `scripts/render-agents-technology-skills.py`. That makes the technology detection/rendering script responsible for unrelated approval checking.

The special restriction was intended for agent evaluation workflows only: a test agent must not change the agent definition, skill, generated target behavior, or other target under test merely to make a suite pass. The existing common test protocol at `evals/agent-tests/AGENTS.md` already directs a supervisor to preserve evidence and route a finding to Dev Backlog Steward rather than make an unreviewed target fix. It is the smallest existing nested instruction file to make this scope explicit. Agents working there inherit both the root and nested `AGENTS.md` files.

`backlog/defect-backlog/eliminate-standalone-definition-approval-records.md` is Blocked. It correctly identifies the checker options and standalone approval records as removable, but incorrectly preserves the repository-wide special policy. This item corrects that policy scope without editing or unblocking the existing item during creation.

## Source Evidence

Direct user direction in Codex task `019fd25f-7adb-7490-bdb8-b73aadc8e79b` on 2026-08-05:

> “OK the policy is wrong. the technology detection should remain a single-purpose script. The special approval requirement was for test agents to avoid changing skills under test - they should log issues instead. So what we should have done is create an AGENTS.md in the test folder adding that restriction only to agents defined for testing. It would automatically use both AGENTS.md. log that item”

Discovery at creation confirmed that `evals/agent-tests/AGENTS.md` already exists. The smallest correction is to amend that common nested protocol, not create another `AGENTS.md`.

## Scope and Authority

This request authorizes logging this work item only. It does not authorize a governed distributed `SKILL.md`, conceptual role definition, agent schema, model profile, adapter-owned definition, skill metadata, or generated definition mirror change. Implementation must discover and record any separately required authorization before mutating a governed canonical source.

The implementation scope is limited to removing the misplaced policy/checker from the technology-rendering and generated-guidance path, adding the test-only restriction to the existing `evals/agent-tests/AGENTS.md`, and changing focused support tests or documentation only where they exist solely for that misplaced policy. Preserve independently justified root instructions, generated-mirror source ownership, and ordinary authorization boundaries.

## Requirements

- Keep `scripts/render-agents-technology-skills.py` single-purpose: technology detection and rendering only. Remove repository-wide agent/skill-definition approval and precheck behavior from that script.
- Remove the misplaced policy/checker from `PROJECT.yaml`, generated root `AGENTS.md` guidance, and focused tests or documentation that exist only to support it.
- Remove the obsolete `--check-definition-change`, `--approval-record`, and `--regenerated-from` interface and approval-record files through coordinated reconciliation with `backlog/defect-backlog/eliminate-standalone-definition-approval-records.md`.
- Amend the existing `evals/agent-tests/AGENTS.md` protocol. For agents operating in that subtree, explicitly prohibit changing a skill under test, agent definition/behavior under test, generated target behavior under test, or product target merely to make a test pass.
- Require those test agents to preserve governed evidence and log the issue or defect through the configured backlog path instead of making an unreviewed target fix.
- Rely on normal nested-`AGENTS.md` inheritance; do not duplicate root instructions in the nested file.
- Preserve root instructions unrelated to this misplaced special policy, generated-mirror source ownership, and ordinary authorization boundaries that have an independent legitimate basis.
- Do not broaden delivery into changes to distributed skill definitions, conceptual role definitions, schemas, model profiles, or skill metadata.

## Acceptance Criteria

- The renderer, project configuration, generated root guidance, and focused support material no longer define or invoke the misplaced repository-wide approval/precheck process.
- `scripts/render-agents-technology-skills.py` exposes none of `--check-definition-change`, `--approval-record`, or `--regenerated-from`, while its ordinary technology detection and rendering behavior remains intact.
- The existing `evals/agent-tests/AGENTS.md` explicitly applies the no-mutation/log-defect rule to test agents in that subtree, including skills and agent definitions or behavior under test.
- The nested instruction supplements rather than duplicates inherited root instructions.
- A focused evaluation scenario demonstrates that a target finding is preserved and logged rather than repaired by changing the target under test.
- The existing standalone-record defect is reconciled or superseded at dispatch/integration so the two items do not deliver conflicting policy.
- No change to a governed definition occurs unless separately authorized and recorded at implementation time.

## Dependencies

No hard dependency.

Coordinate overlapping removal of the checker interface and approval-record files with `backlog/defect-backlog/eliminate-standalone-definition-approval-records.md`. That item is Blocked and must be reconciled or superseded at dispatch/integration because its requirement to preserve the global policy conflicts with this corrected outcome.

## Verification

- Run focused assertions that the renderer, `PROJECT.yaml`, and generated root guidance no longer contain the misplaced policy/checker and that ordinary renderer behavior still works.
- Run focused static checks that the existing nested `evals/agent-tests/AGENTS.md` contains the test-only no-mutation/log-defect rule without copied root guidance.
- Run the focused evaluation-suite behavior check proving findings are preserved and routed instead of modifying a skill, agent definition, behavior, or other target under test.
- Run `git diff --check`.
- Obtain fresh independent review of the corrected scope and the exact integration reconciliation with the existing blocked defect.
- Do not run a broad suite or live-model evaluation unless later implementation evidence makes either necessary.

## Open Questions

None. The existing `evals/agent-tests/AGENTS.md` is the confirmed common nested protocol for agent-evaluation work.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One root Dev Orchestrator launch reservation for the highest-priority corrected-scope item.

Normalized Objective: Scope skill-under-test protection to agent tests.

Dispatch Time: 2026-08-05T16:12:59Z.

Intended Root Role: Root Dev Orchestrator.

Launch Result: Not attempted.

Canonical Conversation: None.

Owner: Unowned pending accepted root.

Last Contact: 2026-08-05T16:12:59Z; parent Coordinator reservation recorded by Dev Backlog Steward.

Next Reconciliation: No later than 2026-08-05T16:27:59Z.

Required Next Lifecycle Transition: A root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

## Current Running Acceptance Evidence

Transition: Starting -> Running.

Canonical Work-Item Thread: 019fd2b6-8e14-7f60-bac1-ef3566d83492.

Canonical Root Agent Task: /root.

Parent Coordinator Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Accepted Owner: Root Dev Orchestrator.

Branch: main delivery context; implementation worktree initially detached at f82c2c8d597143694a1c42383797b764c5aac806.

Execution Worktree: /Users/martinbechard/.codex/worktrees/6c5c/dev-methodology.

Accepted At: 2026-08-05T16:17:28Z.

Active Execution Evidence: Root Dev Orchestrator accepted ownership and began active discovery/provider startup.

Provider-Mutation Claim: scope-skill-under-test-protection-to-agent-tests-starting-running-019fd2b6; exact file claim acquired by Dev Backlog Steward at 2026-08-05T16:18:39.269433Z, outcome SHARED_CHECKOUT_ACQUIRED, journal event 95dcf87e-f74a-48cd-ba8e-7de2ee2463aa.

## Completion Evidence

Completion Disposition: READY through direct-main delivery.

Implementation Commit: 828574f159d6cfbdd367642b8689cc9e57743511.

Independent Review: GOOD.

Independent Verification: READY.

Focused Tests: Four focused tests PASS.

Renderer Reproduction: Exact renderer reproduction PASS.

Diff Check: PASS.

Governed Definitions: Unchanged.

Excluded Candidate: 7cca88fe excluded and not an ancestor of post-integration main.

Integration Claim: f98463a6-4f32-486c-bfe5-22f50fc8c778 released by journal event 2064d606-b1c3-4085-a341-4e141c511cee.

Main Observation: 828574f159d6cfbdd367642b8689cc9e57743511 observed on main after integration.

Terminal Provider Claim: scope-skill-under-test-protection-to-agent-tests-complete-019fd2b6; exact active and completed paths claimed by Dev Backlog Steward at 2026-08-05T16:48:36.840655Z, outcome SHARED_CHECKOUT_ACQUIRED, journal event 4d034ed5-99f2-4381-a6d9-44a123be94e2.

Completed At: 2026-08-05T16:48:36Z.
