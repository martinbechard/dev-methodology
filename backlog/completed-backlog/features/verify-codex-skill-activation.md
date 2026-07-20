# Verify Codex CLI Skill Activation

Status: Completed

Type: Feature

## Completion Evidence

- Delivery: the accepted activation runtime identity contribution is integrated on main at f5d58ca8bc8143f333bb09266583b5247b35e2fb. It pins mcp-agent-ops 0.3.0 and runtime digest 314a780796740e8e31c375af7e5a3b1f8446d7566b2732846f266fe1cca13aeb in the executable evaluation contract.
- Reporting dependency: the accepted strict reporting integration is present on main at 90c937a488f1f82d3573621a83d0bfbd9f55033d and supplies the complete required handoff response shape that removed the activation-run blocker.
- Documentation correction: 353273d2806b7109033ec3954e7a7394126d4db5 keeps the operator-facing base-case version aligned with the activation contract and adds a regression against future documentation drift.
- Review: independent review accepted the activation contribution for correctness, narrow scope, runtime provenance, deterministic coverage, and compatibility with reporting after the bounded documentation correction. A fresh independent review of the correction returned PASS with no findings.
- Verification: the installed runtime independently reported mcp-agent-ops 0.3.0, 26 files, and the required digest. Python 3.11 focused verification passed, the evaluator suite passed all 118 tests, the reporting suites passed 82 and 29 tests, the combined offline suite validator passed, and the digest-bound invocation dry run passed. The previously confirmed unrelated project-organiser catalog mismatch remained baseline-only.
- Integration integrity: main was clean at 290ca87194be9b6829d992b7fb70aa76dbd5b468, with f5d58ca and 353273d both confirmed as ancestors. No implementation, live scenario, generator, browser, deployment, or broad regression was rerun for this identical reviewed integration.
- Terminal lifecycle: Dev Backlog Steward acquired PRIMARY ownership of only the active and completed archive paths at event bdc9a245-8478-4fa7-b234-c51df850e9cf under terminal authority from parent task 019f77f4-c4bd-7c91-b197-c987a7beb838. The archive commit and clean release are reported in the terminal handoff.

## Summary

Build and run a Codex CLI evaluation suite that proves definition-owned and detected-folder skills were actually activated and used by agents launched from generated native agent definitions.

## Context

Current tests prove definitions, installation, detector behavior, fixtures, and manual outcomes. They do not yet provide complete captured evidence that Codex invoked an agent, loaded each required skill, and applied its observable requirements. The suite must run after the detector and generated native agent definition contract stabilizes.

See the series [index](index.md).

## Requirements

- Run the installed Codex CLI version and record its version with every evaluation.
- Invoke generated Codex agents rather than reproducing their prompts manually.
- Capture agent identity, concrete model, invocation, detected AGENTS.md guidance, skill catalog visibility, skill-load events, commands, outputs, and timestamps.
- Prove definition-owned skill activation for representative coding, review, setup, QA, security, documentation, and coordination agents.
- Prove detected-folder activation for TypeScript, Java and Spring Boot, Python, and FastAPI scopes.
- Include a read-only review case with before and after project hashes.
- Test Codex skills.config by name only as an explicit enable or disable feature, not as preloading.
- Test whether agent-local skills.config is honored by the installed Codex version before relying on it for isolation.
- Use stable behavioral assertion identifiers and seeded defects.
- Require trusted capture provenance and an independent verifier.
- Update the generated support checklist only from receipts that pass the evidence validator.
- Preserve raw harness output or a content-addressed reference to it.

## Acceptance Criteria

- At least one Coding Agent run proves each required definition-owned generic skill was loaded.
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
