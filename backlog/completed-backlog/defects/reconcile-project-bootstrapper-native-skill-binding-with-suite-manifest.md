# Reconcile Project Bootstrapper native skill binding with the suite manifest

Status: Completed

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/completed-backlog/defects/reconcile-project-bootstrapper-native-skill-binding-with-suite-manifest.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Reconcile Project Bootstrapper native skill binding with suite manifest.
- Dispatched At: 2026-07-25T11:47:34Z
- Intended Root Role: Dev Orchestrator
- Discovered Ordinary Scope: evals/agent-tests/project-bootstrapper/suite.yaml, its suite-local contract SKILL.md, and focused tests and fixtures.
- Authority Boundary: Any governed or generated-definition mutation requires later exact approval and is not authorized by this reservation.
- Runtime Thread And Task Id: 019f991a-c3b1-7b31-ab52-42152a9f5f0c accepted by the root Dev Orchestrator.

## Reservation Coordination Evidence

- Backlog Claim: reserve-project-bootstrapper-suite-binding-20260725 acquired on primary main at 2026-07-25T11:47:34.139556Z; acquisition journal event 9490e5e8-4ac7-45e1-99eb-708257180a2c.
- Reservation Commit And Release: 1faf4fb7727aed05f84a0863af7c08b457281ade; release journal event 70d78b3f-899d-4f09-a6b5-0c3af8993bfb.

## Execution Acceptance

- Canonical Work-item Thread And Root Task Id: 019f991a-c3b1-7b31-ab52-42152a9f5f0c.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Root Owner: Dev Orchestrator.
- Delivery Branch: Detached at reservation commit 1faf4fb7727aed05f84a0863af7c08b457281ade; delivery claim and branch remain separate from this backlog transaction.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/3767/dev-methodology.
- Primary Main Head At Acceptance: 0a27d2119a6acc49f1111c39f5096ae330857645.
- Phase: Discovery.
- Started At: 2026-07-25T11:50:36.672757Z.

## Running Coordination Evidence

- Backlog Claim: start-running-project-bootstrapper-suite-binding-019f991a acquired on primary main at 2026-07-25T11:50:36.672757Z; acquisition journal event 7c04a63b-762a-4adf-8951-69caddfeac83; resource backlog:mutation:project-bootstrapper-suite-binding.
- Release: This short backlog-mutation claim is released immediately after the committed provider transition; its release journal event is retained in the lifecycle handoff.

## Summary

Make the Project Bootstrapper Codex native-agent skill binding consistent with its suite manifest so the suite validation no longer rejects the generated native agent for omitting agent-claim.

## Context

At current main commit f56c979ce66b783aaedad2a597d5cec617f3100b, the Project Bootstrapper suite declares repositoryMutation required and lists agent-claim in target.requiredSkills. The conceptual role is agents/roles/project-setup/project-bootstrapper.role.yaml, and the generated Codex adapter is generated/adapters/codex/agents/project-bootstrapper.toml. The generated adapter lists documentation-bootstrap and development-methodology as definition-owned skills, but it does not list agent-claim.

The baseline command below exits 1 while loading the suite. The runner raises ValueError stating that the project-bootstrapper native agent does not include required skill agent-claim.

## Source Evidence

- Explicit delegated user direction on 2026-07-25: create exactly one separate Ready file-backed defect for the freshly reproduced current-main failure, project-bootstrapper native agent does not include required skill agent-claim.
- Current-main reproduction at f56c979ce66b783aaedad2a597d5cec617f3100b: /Users/martinbechard/.pyenv/versions/3.11.10/bin/python3 evals/agent-tests/runner.py --harness codex --suite project-bootstrapper --validate-only exits 1 with ValueError: project-bootstrapper native agent does not include required skill agent-claim.
- evals/agent-tests/project-bootstrapper/suite.yaml requires agent-claim for the Project Bootstrapper native agent.

## Requirements

- Reconcile the Project Bootstrapper suite manifest, conceptual role, generation contract, and generated Codex adapter so their required-skill semantics agree.
- Determine from authoritative policy whether agent-claim must be a fixed Project Bootstrapper skill or a conditional skill, and make the suite contract reflect that decision.
- Preserve the distinction between repositoryMutation policy and selected project resource-coordination implementation.
- Do not mutate governed canonical definitions or generated artifacts without separate, exact user approval and the required pre-mutation approval check.

## Acceptance Criteria

- The Project Bootstrapper suite and generated Codex adapter agree on the required agent-claim binding.
- The Project Bootstrapper validate-only command completes without the reported missing-skill ValueError.
- Any governed canonical-source change has exact, scope-specific user approval recorded before mutation, and supported generated mirrors are regenerated rather than edited directly.
- Focused generation and suite validation evidence is recorded with the delivery.

## Dependencies

None.

## Verification

- Run /Users/martinbechard/.pyenv/versions/3.11.10/bin/python3 evals/agent-tests/runner.py --harness codex --suite project-bootstrapper --validate-only.
- Run the focused generator freshness or regeneration checks required by the selected approved source change.
- Run git diff --check and obtain independent review of the exact source and generated diff when a governed definition changes.

## Open Questions

- Does the authoritative Project Bootstrapper contract require agent-claim as a fixed definition-owned skill, or should the suite express a conditional binding that tracks selected resource coordination?

## Notes

Recording this defect authorizes neither implementation nor a governed or generated definition mutation. The existing Dev Coder candidate and its separate backlog item are out of scope.

## Completion Evidence

- Completed At: 2026-07-25T12:07:00Z.
- Accepted delivery and main observation: 2e7c1763198f061ec67ca98c55853e4619f8ac07 is the accepted source and integration commit on primary main. It fast-forwarded from the Running transition commit 8449ab0846caf4558d171d9528c73265b5a81c60; graph reachability and primary-main observation passed.
- Delivered scope: the accepted commit changes exactly evals/agent-tests/project-bootstrapper/suite.yaml, evals/agent-tests/project-bootstrapper/skills/project-bootstrapper-suite-contract/SKILL.md, and evals/agent-tests/project-bootstrapper/test_fixtures.py.
- Independent review: Dev Code Reviewer ACCEPTED the accepted integration with no findings and no distinct defect.
- Verification: Dev Verifier ACCEPTED the fixture module (5/5), exact validate-only command, git diff --check, provenance, and final clean primary-main status. The full catalog remains intentionally deferred to the campaign gate.
- Integration coordination: claim integrate-project-bootstrapper-suite-binding-019f991a acquired event d045658a-3736-48a5-8c79-23e7c013aa28 and released event 21fc7295-78d4-40cb-93f3-c393db88ca2d; no residual paths remained and the registry was empty before terminal provider mutation.
- Earlier lifecycle coordination: the Starting-to-Running provider commit is 8449ab0846caf4558d171d9528c73265b5a81c60 and its backlog claim released under event 7abb0832-e032-412f-a959-069d43a775c2.
- Terminal provider coordination: short primary-main backlog claim complete-project-bootstrapper-suite-binding-019f991a acquired event 9bd46889-443e-4495-9e18-be708fb73a3c. This archive transaction records the terminal provider state; the claim is released only after this commit and final immutable-path verification.
