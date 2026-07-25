# Reconcile Project Bootstrapper native skill binding with the suite manifest

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/reconcile-project-bootstrapper-native-skill-binding-with-suite-manifest.md

Completion: direct-main

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
