# Document The Cross-Harness Skill Lifecycle

Status: Running

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7e8f-f75f-71c1-b138-4a1775b15fdf.
- Branch: codex/document-cross-harness-skill-lifecycle.
- Worktree: /Users/martinbechard/.codex/worktrees/ac58/dev-methodology.
- Dependencies: replace-router-with-setup-detector and verify-codex-skill-activation are completed.
- Preserved evidence: source commit 3e26250447dd5bc095c4ceef22de3beb093e1fd4 within accepted cumulative candidate 67ee16ef002d297e755a6284fe20afde4457d4f2; semantically reconcile its four cross-harness paths against current main rather than replaying the combined candidate.
- Phase: current-main provenance reconciliation, focused documentation review/verification, direct integration, and terminal completion.

## Summary

Create one authoritative explanation of skill discovery, availability, preloading, dynamic loading, project detection, generated guidance, activation evidence, and tool restrictions across supported harnesses.

## Context

The repository currently spreads skill semantics across README.md, agent-definition runtime documentation, specialization strategy pages, conceptual agent definition maps, generated definitions, and evaluation documentation. Several earlier explanations conflated Claude preloading, Codex availability filtering, dynamic discovery, and actual skill activation.

See the series [index](index.md).

## Requirements

- Define generic definition-owned skills, detected-folder specialized skills, optional tool skills, and unsupported technology fallback.
- Explain Claude skills properties as full-content preloading.
- Explain Claude dynamic invocation through the Skill tool and the effect of restrictive tools allowlists.
- Explain Codex catalog discovery and developer-instruction-driven loading.
- Explain Codex skills.config as enable or disable selection by name or absolute path, not preloading.
- Explain Codex app-server skill input items as caller-controlled full instruction injection.
- Distinguish availability, preload, dynamic invocation, content read, behavioral application, and verified evidence.
- Explain the setup-time detector, PROJECT.yaml, generated AGENTS.md, and Claude bridge responsibilities.
- Document adapter generation rules and portability constraints.
- Link claims to primary runtime documentation and local test evidence.
- Remove stale task-time routing and model-stage execution claims.
- Keep README.md and relevant design pages consistent with the authoritative explanation.

## Acceptance Criteria

- A reader can determine whether each runtime mechanism makes a skill available, preloads it, requests it, or proves its use.
- Tool allowlist risks are explicit.
- The documented detector workflow matches generated project guidance.
- Codex claims distinguish schema support from behavior proven by the installed CLI suite.
- Claude claims distinguish preloaded definition-owned skills from dynamic folder skills.
- No design page describes normal agents as rerunning technology detection.
- Documentation freshness and repository content tests cover the core distinctions.

## Dependencies

- replace-router-with-setup-detector
- verify-codex-skill-activation

## Verification

- Run repository documentation and generated-output checks.
- Sweep for obsolete router terminology and contradictory preload claims.
- Verify every external mechanism claim against a primary source.
- Perform an independent documentation review using the applicable review checklist.

## Notes

- A source-backed outline may be prepared while dependencies run, but final status must remain blocked until implementation and Codex evidence are stable.
