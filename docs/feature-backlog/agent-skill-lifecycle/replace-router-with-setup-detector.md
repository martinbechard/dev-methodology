# Replace Task-Time Routing With Setup-Time Technology Detection

Status: Completed

Type: Feature

## Summary

Replace the per-task technology router with a focused setup-time detector that produces source-backed folder skill loadouts for AGENTS-PLAN.yaml and unconditional technology-loading guidance for AGENTS.md. Add Python and FastAPI skills and align fixed-role generation with Claude and Codex semantics.

## Context

The current implementation asks ordinary coding, review, verification, and diagnostic agents to rerun a router. Generic skills also appear in the routing registry even though canonical role definitions already own them. The detector refactor was started but interrupted; the working tree contains uncommitted path renames that belong to this item and must be reconciled rather than assumed complete.

Claude skills properties preload full fixed-role skill content. Codex normally discovers enabled skills and follows developer instructions to load them. Codex skills.config controls availability and selection but does not preload skill bodies. Folder-specific technology skills should be established during project setup and loaded dynamically from the nearest project guidance.

See the series [index](index.md) and design/technology-skill-detection-spec.md.

## Requirements

- Keep generic fixed-role skills only in canonical role definitions, not technology detection metadata.
- Generate Claude skills properties for fixed-role skills and state in agent instructions that those skills govern the work.
- Generate Codex developer instructions that require fixed-role skills to be loaded before acting.
- Omit Codex skills.config by default; support explicit name-based or path-based availability overrides only when the canonical definition requests them.
- Validate that a restrictive Claude tools allowlist includes Skill whenever dynamic folder technology skills are required.
- Rename and rewrite the router as a setup-time technology detector with no agent-role, task-time binding, prompt-keyword, read-confirmation, or optional-command-tool behavior.
- Keep the canonical detector implementation under scripts and generate any runtime mirror needed by standalone installed skills.
- Detect specialized technology and domain skills for setup-agent-selected folder scopes.
- Preserve scope-safe monorepo detection, nearest owning manifests, companion skills, missing required skills, and exclusive conflict handling.
- Generate AGENTS-PLAN.yaml loadouts with source evidence.
- Generate AGENTS.md instructions that tell every agent working under a matching folder to load the detected technology skills before acting without rerunning detection.
- Add a generic python-coding skill.
- Add a FastAPI-specific skill that composes with python-coding.
- Add deterministic Python and FastAPI detection metadata and fixtures.
- Remove obsolete route-technology-skills identifiers, routing terminology, generated files, role outputs, and documentation claims.

## Acceptance Criteria

- Canonical non-setup roles no longer include or invoke a technology router.
- Project Agent Setup is the owner of technology detection and generated folder bindings.
- Generic skills are absent from the technology detection registry.
- TypeScript, Spring Boot, Python, and FastAPI scopes produce exact expected loadouts.
- Mixed repositories produce separate scope loadouts without sibling or root-workspace contamination.
- Generated AGENTS.md contains unconditional folder skill-loading instructions.
- Generated Claude agents preload fixed-role skills.
- Generated Codex agents contain deterministic fixed-role loading instructions and no redundant skills.config entries.
- A restrictive Claude tools fixture without Skill fails validation when dynamic folder loading is expected.
- Installed detector artifacts match the canonical source.

## Dependencies

None.

## Verification

- Run every detector and generated-output freshness check.
- Run repository unit tests and project-wiki tests.
- Run Agent Skill validation.
- Refresh shared Codex, Agents, and Claude installs.
- Execute installed detection against TypeScript, Spring Boot, Python, FastAPI, mixed, missing-skill, and conflict fixtures.
- Run git diff checks and an independent read-only audit.

## Completion Evidence

- Agent Skill validation passed.
- Technology detection, generated documentation, hierarchy, and support-checklist freshness checks passed.
- Repository unit tests passed with 78 tests.
- Project-wiki unit tests passed with 16 tests.
- Shared Agents, Codex, and Claude installs were refreshed.
- The installed detector produced the expected TypeScript, Spring Boot, Python, and FastAPI loadouts.
- Git diff validation passed.

## Notes

- Treat design/technology-skill-detection-spec.md as the initial focused contract and adjust it only when implementation evidence requires clarification.
- Do not claim Codex activation behavior from detector tests; that belongs to verify-codex-skill-activation.
