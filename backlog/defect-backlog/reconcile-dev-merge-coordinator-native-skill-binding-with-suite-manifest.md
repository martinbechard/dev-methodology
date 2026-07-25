# Reconcile Dev Merge Coordinator Native Skill Binding With Suite Manifest

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/reconcile-dev-merge-coordinator-native-skill-binding-with-suite-manifest.md

Completion: direct-main

## Summary

Reconcile the Dev Merge Coordinator suite required-skill contract with its generated Codex native agent so the current-main validate-only catalog check succeeds without weakening resource-coordination or governed-definition authority.

## Context

At current main commit 1ac1ebf7ca7dcea4b0f1fbd8a9720a2070cd6e5a, the exact validate-only command below exits 1 while loading the suite catalog. The runner raises ValueError: dev-merge-coordinator native agent does not include required skill agent-claim.

The Dev Merge Coordinator suite manifest requires agent-claim. The conceptual role and generated Codex native adapter list definition-owned skills agent-work-merge, review-structured-artifact, and fix-explanation, but not agent-claim. The native adapter instead directs the agent to load codex-harness-directives before acting. The runner validates every manifest-required skill against the native agent's declared instructions.

The fixed-versus-conditional authority must be reconciled before any delivery choice: the role says resource coordination is project-selected and conditional, while the suite currently fixes agent-claim as a required skill. The delivery must determine the correct contract source and preserve the governed-definition approval boundary.

## Source Evidence

- Explicit delegated user direction on 2026-07-25: create exactly one separate Ready file-backed defect for the freshly reproduced current-main failure: dev-merge-coordinator native agent does not include required skill agent-claim.
- Current-main reproduction at 1ac1ebf7ca7dcea4b0f1fbd8a9720a2070cd6e5a:

  ```text
  /Users/martinbechard/.pyenv/versions/3.11.10/bin/python3 evals/agent-tests/runner.py --harness codex --suite dev-merge-coordinator --validate-only
  ```

- Observed result: exit 1 with ValueError: dev-merge-coordinator native agent does not include required skill agent-claim.
- Record-time inspection confirmed the fixed manifest requirement in evals/agent-tests/dev-merge-coordinator/suite.yaml, the omission from agents/roles/dev-activities/dev-merge-coordinator.role.yaml and generated/adapters/codex/agents/dev-merge-coordinator.toml, and the runner validation boundary in evals/agent-tests/runner.py.
- The integration owner confirmed the related inputs were unchanged, while Project Bootstrapper selective validation passes.

## Requirements

- Reconcile the effective Dev Merge Coordinator suite required-skill contract and generated/native Codex agent binding so they agree on whether agent-claim is required.
- Determine and document whether agent-claim is a fixed definition-owned requirement for this role or a conditional project-selected procedure, using the authoritative sources rather than a validation-only shortcut.
- Preserve Dev Merge Coordinator repository-mutation, integration-resource, and resource-coordination semantics.
- Treat conceptual role definitions, distributed skill definitions, metadata, and generated adapter mirrors as governed surfaces where applicable.
- Before mutating a governed canonical source, obtain explicit, scope-specific user approval and pass the required definition-change pre-mutation check.
- Regenerate native output only from an approved canonical source; do not edit generated adapter output by hand.

## Acceptance Criteria

- The Dev Merge Coordinator suite manifest and generated Codex native agent express the same required-skill contract.
- The exact current-main validate-only command succeeds for the Dev Merge Coordinator suite without the missing agent-claim error.
- Focused regression coverage detects a future mismatch between this suite-required skill contract and the generated native agent instructions.
- The fixed-versus-conditional authority decision is traceable to authoritative project, role, suite, and generator sources.
- Any governed canonical mutation has recorded, exact user approval and a successful pre-mutation check; supported generated mirrors are refreshed only through the approved generator path.
- The active Dev Coder binding defect and the Running lifecycle-handoff defect remain separate and unchanged unless independently authorized.

## Dependencies

None.

## Verification

- Run the exact baseline command using the repository-supported Python 3.11 interpreter.
- Run focused Dev Merge Coordinator suite-manifest, native-agent, runner validation, and authority-contract regression tests.
- Run relevant generated-definition and skill-document freshness checks when an approved canonical source requires regeneration.
- Run git diff --check and obtain fresh independent review.

## Open Questions

- Does the suite intentionally require agent-claim as a fixed evaluated native skill, or must it model the role's conditional project-selected coordination procedure without a fixed native binding?

## Notes

This transaction records the defect only. It does not authorize implementation, governed-definition mutation, generated-output edits, or changes to the separate Dev Coder binding or lifecycle-handoff work items. Resolve the fixed-versus-conditional authority before choosing a repair surface.
