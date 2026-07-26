# Reconcile Root AGENTS With Bundle-Content Contract

Status: Running

Type: Defect

Owner: /root (Dev Orchestrator)

Provider: file

Provider Reference: backlog/defect-backlog/reconcile-root-agents-with-bundle-content-contract.md

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

## Notes

Runnable next action: inspect the committed guidance, its source boundaries, and the assertions; reconcile the non-authoritative surface; then run both focused tests and the full bundle-content suite. Do not change project files as part of this record-creation task.
