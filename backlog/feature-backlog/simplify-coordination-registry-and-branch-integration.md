# Simplify Coordination Registry And Branch Integration

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/simplify-coordination-registry-and-branch-integration.md

Completion: direct-main

## Current Execution

- Owner: Dev Orchestrator
- Canonical task: 019f8510-331a-75e1-9dee-ba1b966e595f
- Worktree: /Users/martinbechard/.codex/worktrees/a85a/dev-methodology
- Branch: codex/simplify-coordination-registry-and-branch-integration
- Starting main: 22b9c30697433fa1160a65168cf861328ac9fae4
- Phase: Implementing the approved coordination-registry reset and fresh-current-main integration guidance.
- Started: 2026-07-21
- Running-record claim: start-coordination-registry-guidance-019f8510, acquired as event 03d64dc7-0ac8-4c8b-89a2-9067a458965a.
- Open issues: None.
- Accepted candidate: Pending.

## Summary

Clarify that the repository coordination registry is temporary conflict-avoidance state rather than delivery authority, document safe administrative reset of inactive entries, and make current-main reconciliation branches the default for integrating accepted file content without importing unrelated branch history.

## Context

The completed Wiki Ingester interruption-recovery item integrated a verified fifteen-path semantic union on main. Its final tree was correct and clean, but registry release rejected unrelated backlog commits made newly reachable through the candidate branch ancestry. The release failure did not represent a concurrent writer, dirty worktree, lost product change, or invalid integration. The sole inactive registry entry was safely removed after confirming no matching process, no other entry, clean main, and preserved task and journal evidence.

The coordination process treated the registry entry as stronger authority than its actual purpose and overvalued two-parent ancestry as provenance. A fresh branch from current main carrying only the accepted file content would have avoided the ancestry collision. Commit messages and the work item can preserve source provenance without importing unrelated history.

## Source Evidence

The user directed the parent coordinator on 2026-07-20: “make sure that we don't lose these lessons. I suggest you create an enhancement to the appropriate skills files.” The user also clarified that the registry is a scratchpad used to avoid conflicts between agents and explicitly authorized resetting it after the sole inactive entry was confirmed.

## Proposed Governed Definition Scope

- skills/agent-claim/SKILL.md
- skills/agent-work-merge/SKILL.md
- skills/codex-workitem-coordination/SKILL.md

Supported generated skill mirrors and directly related focused tests or design documentation may be regenerated or updated from those approved canonical sources. No conceptual agent definition, skill metadata, registry implementation, or unrelated distributed skill is included.

## Requirements

- Use the user-facing term coordination registry when explaining temporary ownership state. Keep existing command and identifier names stable unless a separately approved compatibility change is required.
- State that the coordination registry prevents concurrent conflicting work but does not determine whether reviewed, verified, committed product delivery exists.
- Define an administrative reset procedure for inactive registry entries. Before reset, inspect task state, running processes, claimed worktrees, Git cleanliness, preserved commits, shared resources, other registry entries, and journal evidence.
- Permit removal only when the target entry is inactive, its work is preserved or completed, no claimed resource remains in use, and reset cannot erase another active owner's protection.
- Preserve a readable snapshot or journal reference for every administrative reset. Reset only registry state; do not rewrite Git, mutate project files, or invent release evidence.
- Treat release-validation failures as coordination diagnostics. Do not automatically invalidate correct integrated bytes, review, verification, or completion evidence when the failure concerns inactive or ancestry-only scratch state.
- For direct integration, start from a fresh branch based on current main and apply only the accepted file content or explicitly selected commits required by the work item.
- Do not merge cumulative feature-branch history merely to preserve provenance when it contains out-of-scope commits. Record source commit identifiers in the integration commit and work item instead.
- Use a full-history merge only when the complete imported history is intentional, reviewed, and within the integration ownership scope.
- When semantic reconciliation is required, preserve both accepted contracts on the fresh current-main branch, regenerate supported outputs, review the reconciled diff, and integrate that bounded result.
- Keep registry cleanup, Git integration, and terminal backlog completion as distinct operations whose evidence is reported separately.

## Acceptance Criteria

- The three approved skill definitions consistently describe the registry as temporary coordination state rather than delivery authority.
- The documented reset procedure cannot remove an active writer, dirty unpreserved worktree, or live shared resource.
- Integration guidance prefers a fresh current-main reconciliation branch and exact accepted files over cumulative ancestry merges.
- Provenance remains auditable through commit messages and work-item evidence without requiring unrelated source ancestry on main.
- A focused regression covers the Wiki Ingester pattern: correct clean final tree, ancestry-only out-of-domain history, sole inactive registry entry, preserved evidence, administrative reset, and separate terminal backlog completion.
- Existing normal acquisition, conflict prevention, heartbeat, safe release, recovery, and active-owner protections remain intact.
- Applicable skill validation, supported generated-mirror freshness, focused bundle tests, and Git diff validation pass.
- Fresh independent methodology review accepts the exact definition and test changes.

## Dependencies

None.

## Verification

- Run the exact governed-definition approval check for each approved skill before mutation.
- Validate the changed skill definitions and supported mirrors.
- Run focused coordination, merge, registry-reset, and bundle regressions.
- Prove an active writer or dirty unpreserved worktree blocks administrative reset.
- Prove a current-main reconciliation branch integrates only its accepted paths while retaining source commit provenance in durable evidence.
- Run Git diff validation and fresh independent methodology review.
- Do not run the full agent catalog solely for this bounded guidance change.

## User Action Required

Exact governed-definition approval is required before changing the proposed distributed skill definitions.

## Question For The User

Do you approve changing exactly skills/agent-claim/SKILL.md, skills/agent-work-merge/SKILL.md, and skills/codex-workitem-coordination/SKILL.md, together with their supported generated skill mirrors and directly related focused tests or design documentation, to implement the coordination-registry reset and fresh-current-main integration guidance in this item?

## Why User Input Is Required

Repository policy requires explicit scope-specific user approval before mutating any distributed skill definition. The request to update the appropriate skills authorizes creation of this enhancement but does not name the exact governed paths.

## Options And Tradeoffs

- Approve the proposed three-skill scope: implement the complete coordination, integration, and parent-scheduling guidance together.
- Narrow the scope: name the skill paths that may change and leave the remaining lessons documented only in this work item.
- Defer: move the item to Holding while retaining the incident evidence and proposed procedure.

## Resolution

Approved on 2026-07-21. In parent task 019f77f4-c4bd-7c91-b197-c987a7beb838, after the exact three-skill scope and tradeoffs were presented, the user answered: "ok I approve". This authorizes exactly skills/agent-claim/SKILL.md, skills/agent-work-merge/SKILL.md, and skills/codex-workitem-coordination/SKILL.md, together with their supported generated skill mirrors and directly related focused tests or design documentation, for the requirements recorded in this item.

## Unattended Work Boundary

The exact approval is recorded. The assigned Dev Orchestrator must run each supported governed-definition pre-mutation check with this approval provenance before changing the three approved skill definitions. No other governed definition is authorized.

## Notes

- The Wiki Ingester product integration remains valid and completed; this enhancement addresses the reusable coordination process only.
- Manual deletion of arbitrary registry entries is not the desired steady state. The enhancement must distinguish evidence-backed inactive-entry reset from removal that could expose active work to collision.
