# Stop test-strategy from rerunning technology-skill routing

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/stop-test-strategy-from-rerunning-technology-routing.md

Completion: direct-main

Owner: Dev Orchestrator /root

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-defects-019fa9bb

Normalized Objective: Keep test-strategy work within the setup-selected technology-skill routing rather than rerunning detection during ordinary work.

Dispatch Time: 2026-07-28T19:19:58Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa2d-300b-7012-9a14-03dc3039a7ac

Root Agent Task: 019faa2d-300b-7012-9a14-03dc3039a7ac

Next Lifecycle Owner: Root Dev Orchestrator

Canonical Branch: codex/stop-test-strategy-routing-019faa2d

Canonical Worktree: /Users/martinbechard/.codex/worktrees/8c28/dev-methodology

Current Phase: Approved definition change pending pre-mutation check

Started At: 2026-07-28T19:27:05Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED; claim starting-to-running-019faa2d-300b-7012-9a14-03dc3039a7ac; event bd656c33-2dea-46b3-b122-9599156ecf50; primary main baseline f0f5c17a6af52fdcf332fc7cf48e7c0b49ee98ef.

## Summary

Keep test-strategy work within the setup-selected technology-skill routing rather than rerunning detection during ordinary work.

## Context

The primary affected skill is skills/test-strategy/SKILL.md. It directs work to rerun technology-skill routing even though the project configuration assigns that detection responsibility to Project Configurator. This can create inconsistent routing and exceeds ordinary-work authority.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the routing conflict for skills/test-strategy/SKILL.md. Independent reviewer /root/confirm_critical_e accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use the setup-selected technology skillset during ordinary test-strategy work.
- Remove ordinary-work directions to rerun technology detection.
- Preserve a defined escalation route for genuine configuration changes.

## Acceptance Criteria

- Test-strategy does not rerun detector routing during ordinary work.
- It follows the project-configured skillset.
- A configuration-change route remains explicit and owned by Project Configurator.

## Dependencies

None

## Verification

- Exercise ordinary test-strategy work with configured routing.
- Confirm no detector rerun occurs.
- Verify the configuration-change escalation route remains available.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

Do you approve changing only skills/test-strategy/SKILL.md so ordinary test-strategy work consumes the project-configured active-scope technology skillset, does not rerun or infer technology routing from repository evidence, and refers missing or stale routing caused by genuine configuration changes to Project Configurator?

## User Action Required

Question: Do you approve changing only skills/test-strategy/SKILL.md so ordinary test-strategy work consumes the project-configured active-scope technology skillset, does not rerun or infer technology routing from repository evidence, and refers missing or stale routing caused by genuine configuration changes to Project Configurator?

Why Input Is Required: Only the user can grant exact governed skill-definition mutation approval and provenance.

Unattended Work Boundary: All implementation and delivery activities stop. Only provider coordination and read-only preservation may continue.

Resolution: Approved on 2026-07-28. Exact user direction: Just get rid of step 3, don't add that stuff. The skills might be testing skills not necessarily tech skills. Also line 10 is idiotic because the routing is already done implicitly for the testing agent.

## Approval Boundary

Disposition: BLOCKED_APPROVAL_REQUIRED.

Governed Scope Requiring Approval: skills/test-strategy/SKILL.md only.

Supported Generated Effects After an Approved Canonical Edit: generated/adapters/** and design/generated/skill-definitions.js, regenerated through the supported source-owned generator; never hand-edit a generated mirror.

Excluded Before Approval: No governed definition mutation, invented-provenance approval record, test mutation, generator or regeneration, generated-mirror mutation, candidate production, delivery, or completion.

Evidence: skills/test-strategy/SKILL.md line 10 consumes routed guidance, while workflow step 3 routes specialized skills from repository evidence. Accepted lint evidence is evals/results/2026-07-28-methodology-skill-lint.md lines 371-381. AGENTS.md and PROJECT.yaml require explicit scope-specific user approval before a governed definition mutation.

Same-Thread Resumption: Record the exact answer and provenance once. An approved answer moves this item to Ready in the typed defect path, then the Coordinator records Ready to Starting for this same canonical Thread; the same root Dev Orchestrator accepts it and its sole Steward records Starting to Running. Run the supported pre-mutation check with the exact approval record before any definition edit.

## Resumption Evidence

Transition: User Action Required to Ready recorded on 2026-07-28.

Answer Provenance: User message in preserved canonical Runtime Thread 019faa2d-300b-7012-9a14-03dc3039a7ac, routed to Parent Coordination Thread 019fa9bb-1423-7e80-bcde-3caa765e3758.

Approved Scope and Semantics: skills/test-strategy/SKILL.md only. Delete current line 10 and Workflow step 3, add no replacement routing language, and mechanically renumber. No other governed definition scope is approved.

Preserved Execution Identity: Runtime Thread and Root Agent Task 019faa2d-300b-7012-9a14-03dc3039a7ac; canonical branch codex/stop-test-strategy-routing-019faa2d; canonical worktree /Users/martinbechard/.codex/worktrees/8c28/dev-methodology; prior lifecycle history remains intact.

Pre-Mutation Requirement: Before any governed definition mutation, create the exact approval record from this user direction and pass the supported definition-change preflight for skills/test-strategy/SKILL.md.

## Starting Reservation Evidence

Transition: Ready to Starting recorded by Parent Dev Backlog Coordinator on 2026-07-28.

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Launch Reservation: resume-stop-test-strategy-019faa2d-300b-7012-9a14-03dc3039a7ac.

Reservation Time: 2026-07-28T21:49:12Z.

Canonical Execution Identity: Runtime Thread and Root Agent Task 019faa2d-300b-7012-9a14-03dc3039a7ac; canonical branch codex/stop-test-strategy-routing-019faa2d; canonical worktree /Users/martinbechard/.codex/worktrees/8c28/dev-methodology.

Required Next Acceptance: The existing sole Root Dev Orchestrator must separately accept Starting to Running through its Dev Backlog Steward before any governed-definition mutation. No replacement Thread is authorized.

## Running Acceptance Evidence

Transition: Starting to Running recorded on 2026-07-28.

Root Dev Orchestrator: Dev Orchestrator /root.

Accepted At: 2026-07-28T21:52:24Z.

Canonical Execution Identity: Runtime Thread and Root Agent Task 019faa2d-300b-7012-9a14-03dc3039a7ac; canonical branch codex/stop-test-strategy-routing-019faa2d; canonical worktree /Users/martinbechard/.codex/worktrees/8c28/dev-methodology.

Current Phase: Approved definition change pending pre-mutation check.

Claim Evidence: SHARED_CHECKOUT_ACQUIRED; claim resumed-starting-to-running-019faa2d-300b-7012-9a14-03dc3039a7ac; event ec946a55-efa3-4c37-9985-f2891400e92b; primary main baseline 78f21b8f763ebc319ac274585131e2cb17fb02ac.

Exact Approval Provenance: User direction in the preserved canonical Runtime Thread authorizes skills/test-strategy/SKILL.md only: delete current line 10 and Workflow step 3, add no replacement routing language, mechanically renumber remaining workflow steps, and do not broaden policy.

Pre-Mutation Boundary: No governed definition mutation occurs in this lifecycle transaction. Before any approved definition edit, create the exact approval record and pass the supported pre-mutation check for skills/test-strategy/SKILL.md.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/test-strategy/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
