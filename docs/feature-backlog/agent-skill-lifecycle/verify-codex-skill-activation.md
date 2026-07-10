# Verify Codex CLI Skill Activation

Status: Proposed

Type: Feature

## Summary

Build and run a Codex CLI evaluation suite that proves fixed-role and detected-folder skills were actually activated and used by generated canonical agents.

## Context

Current tests prove definitions, installation, detector behavior, fixtures, and manual outcomes. They do not yet provide complete captured evidence that Codex invoked a canonical agent, loaded each required skill, and applied its observable requirements. The suite must run after the detector and generated agent contract stabilizes.

See the series [index](index.md).

## Requirements

- Run the installed Codex CLI version and record its version with every evaluation.
- Invoke generated canonical Codex agents rather than reproducing their prompts manually.
- Capture agent identity, concrete model, invocation, detected AGENTS.md guidance, skill catalog visibility, skill-load events, commands, outputs, and timestamps.
- Prove fixed-role skill activation for representative coding, review, setup, QA, security, documentation, and coordination agents.
- Prove detected-folder activation for TypeScript, Java and Spring Boot, Python, and FastAPI scopes.
- Include a read-only review case with before and after project hashes.
- Test Codex skills.config by name only as an explicit enable or disable feature, not as preloading.
- Test whether agent-local skills.config is honored by the installed Codex version before relying on it for isolation.
- Use stable behavioral assertion identifiers and seeded defects.
- Require trusted capture provenance and an independent verifier.
- Update the generated support checklist only from receipts that pass the evidence validator.
- Preserve raw harness output or a content-addressed reference to it.

## Acceptance Criteria

- At least one fixed-role Coding Agent run proves each required generic skill was loaded.
- At least one folder-guided run proves the relevant technology skills were loaded from AGENTS.md instructions.
- A negative control fails when a required skill is disabled or unavailable.
- A restrictive or misleading prompt cannot make the evaluator count an unobserved skill as loaded.
- The installed Codex behavior for agent-local skills.config is recorded as supported, unsupported, or version-limited with evidence.
- Verified checklist counts increase only for agents and skills proven by valid receipts.
- Fixture passes remain visibly distinct from behavior-verified passes.

## Dependencies

- replace-router-with-setup-detector

## Verification

- Run the evidence validator against valid and deliberately invalid receipts.
- Rerun all existing TypeScript and Spring Boot fixtures.
- Add and run Python and FastAPI fixtures.
- Confirm read-only evaluations do not mutate their project copy.
- Independently inspect captured Codex events and checklist updates.

## Notes

- Preparation may define trace parsers and disposable fixture orchestration before the dependency completes, but final executions and receipts must use the stable detector-generated artifacts.
- Do not treat developer instructions, skills.config, or a result section named Skills Used as activation evidence.
