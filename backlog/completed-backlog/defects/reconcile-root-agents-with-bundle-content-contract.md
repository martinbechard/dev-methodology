# Reconcile Root AGENTS With Bundle-Content Contract

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/reconcile-root-agents-with-bundle-content-contract.md

Completion: direct-main

## Summary

Reconcile the committed root AGENTS.md maintenance guidance with the bundle-content contract so the authoritative repository-maintenance, source-boundary, and verification policy is expressed consistently.

## Context

An independently archived baseline candidate dce1fc7f12dd20f6e2292f4c85f16425745c80ff reproduces nine failures from two focused bundle-content tests. The root cause is one policy-contract mismatch: committed root AGENTS.md is out of sync with assertions that define required repository-maintenance and source-boundary guidance. The active durable-defect role task cannot expand into root AGENTS.md because that path is outside its approved scope.

## Source Evidence

The user’s standing direction authorizes durable Ready logging of confirmed defects. Reproduction command: /opt/homebrew/bin/python3.11 -m unittest scripts.test_bundle_content.BundleContentTests.test_agents_guidance_keeps_repo_maintenance_local scripts.test_bundle_content.BundleContentTests.test_roles_keep_mutation_independent_from_resource_coordination. The command reports two tests and nine failures against independently archived immutable candidate dce1fc7f12dd20f6e2292f4c85f16425745c80ff.

## Requirements

- Determine whether the current root AGENTS.md policy or the bundle-content assertions are authoritative, using current repository evidence.
- Reconcile the non-authoritative side without weakening the repository-maintenance, source-boundary, or verification contract.
- Preserve all nine subfailures as one root-cause grouping:
  - repo-local operating contract.
  - Do not create separate skill files for repo-local maintenance procedures.
  - Update README.md when the public skill inventory.
  - Update the design HTML files that describe skills, conceptual agent definitions.
  - Keep Codex openai.yaml metadata beside each source SKILL.md.
  - Run scripts/openai_metadata.py skills after skill name or description changes so derived Codex interface fields stay aligned while policy and dependencies remain hand-authored.
  - Select tests from the changed behavior and its actual dependency paths.
  - A tier identifies the affected surface; it never triggers a full repository regression.
  - .worktrees contains ignored linked agent checkouts rooted at the primary worktree.
- Keep this work separate from the active durable-defect role task.

## Acceptance Criteria

- One evidence-backed authority decision identifies whether root AGENTS.md or the assertions must change.
- The accepted contract preserves every listed maintenance, source-boundary, metadata, and verification requirement.
- Both focused failing tests pass.
- The full scripts.test_bundle_content suite passes.
- An independent review accepts the authority decision and correction.

## Dependencies

None.

## Verification

- Run /opt/homebrew/bin/python3.11 -m unittest scripts.test_bundle_content.BundleContentTests.test_agents_guidance_keeps_repo_maintenance_local scripts.test_bundle_content.BundleContentTests.test_roles_keep_mutation_independent_from_resource_coordination.
- Run /opt/homebrew/bin/python3.11 -m unittest scripts.test_bundle_content.
- Obtain independent review.

## Open Questions

Determine from current repository evidence whether root AGENTS.md guidance or bundle-content assertions are authoritative; this is an agent-resolvable technical authority question, not a user-action gate.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Reconcile root AGENTS.md with the bundle-content contract without weakening the repository-maintenance, source-boundary, metadata, or verification requirements.
- Dispatched At: 2026-07-26T19:10:06Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Current Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-item Thread: 019f9fd6-d7c1-7902-bf33-e10883383b7e.
- Canonical Root Agent Task: 019f9fd6-d7c1-7902-bf33-e10883383b7e.
- Root Dev Orchestrator: /root.
- Delivery Branch: codex/reconcile-root-agents-bundle-contract.
- Private Worktree: /Users/martinbechard/.codex/worktrees/9188/dev-methodology.
- Phase: authority discovery.
- Started At: 2026-07-26T19:14:17Z.
- Acceptance Evidence: The canonical root Dev Orchestrator accepted ownership after the parent-owned Starting reservation.
- Claim Evidence: accept-running-019f9fd6-d7c1-7902-bf33-e10883383b7e; SHARED_CHECKOUT_ACQUIRED; claim event 5d2b6720-e3c3-4e4c-97be-8586fe802c7a.

## Blocked Handoff

Blocker: The live project-files claim integrate-reconcile-root-agents-019f9fd6 cannot be released after the accepted non-ancestral primary-main integration. The helper validates the claimant linked-worktree HEAD at 71387a2968d3f879e12d599887bc2981e1bb7144 instead of the primary-main integration 1dded7f556cf4270e2a0bff12178382eac17c3c4, and rejected normal release as missing_commit_or_no_change in event 0abe6b25-19f3-4635-bb38-15769a7861ec.

Blocker Owner: Parent Coordinator 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a, with the delivery and recovery owner for backlog/defect-backlog/bind-project-files-claims-to-primary-worktree.md.

Coordinator Next Action: Preserve the canonical task, accepted delivery, live claim, and claim history while the new helper defect is delivered and independently reviewed.

Unblock Condition: A supported helper release becomes available and safely releases this exact claim, integrate-reconcile-root-agents-019f9fd6, while preserving its ordered claim evidence.

Preserved Canonical Identity: Work-item Thread and Root Agent Task 019f9fd6-d7c1-7902-bf33-e10883383b7e; branch codex/reconcile-root-agents-bundle-contract; linked worktree /Users/martinbechard/.codex/worktrees/9188/dev-methodology.

Preserved Delivery Evidence: Accepted candidate 71387a2968d3f879e12d599887bc2981e1bb7144; accepted non-ancestral primary-main integration 1dded7f556cf4270e2a0bff12178382eac17c3c4; independent review PASS; focused verification 2/2 PASS; full bundle verification 126/126 PASS; renderer byte-equal; post-main checks PASS; primary and integration worktrees clean when observed.

Live Claim Evidence: integrate-reconcile-root-agents-019f9fd6 is a project-files claim with baseline 71387a2968d3f879e12d599887bc2981e1bb7144, linked checkout topology, and worktree /Users/martinbechard/.codex/worktrees/9188/dev-methodology. Its current task-worktree HEAD remains 71387a2968d3f879e12d599887bc2981e1bb7144.

Prohibited Actions: Do not use no-change release, out-of-domain reconciliation, claim-registry editing, duplicate integration, provider completion, or cleanup. Do not release, extend, edit, or take over the live project-files claim.

Safe Resumption: Only after the unblock condition, transition Blocked -> Ready -> Starting -> Running in the same canonical task before any terminal completion. The Parent Coordinator owns Ready -> Starting; the same root Dev Orchestrator owns Starting -> Running.

## Notes

The root-AGENTS delivery is complete. The prior claim-recovery blocker is satisfied.

## Completion Evidence

- Accepted source commit: 71387a2968d3f879e12d599887bc2981e1bb7144.
- Direct-main integration commit: 1dded7f556cf4270e2a0bff12178382eac17c3c4.
- The integration commit is an ancestor of current main.
- README.md and scripts/test_bundle_content.py blobs match exactly between the accepted source and integration commits.
- Preserved review: PASS.
- Preserved verification: focused 2/2 PASS and full bundle 126/126 PASS.
- Current focused observation: the two original failing tests pass on current main.
- The former blocking claim integrate-reconcile-root-agents-019f9fd6 is absent from the live registry.
- Git diff check passed and the primary worktree was clean before this terminal archive transaction.
