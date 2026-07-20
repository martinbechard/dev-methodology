# Document The Cross-Harness Skill Lifecycle

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7e8f-f75f-71c1-b138-4a1775b15fdf.
- Branch: codex/document-cross-harness-skill-lifecycle.
- Worktree: /Users/martinbechard/.codex/worktrees/ac58/dev-methodology.
- Dependencies: replace-router-with-setup-detector and verify-codex-skill-activation are completed.
- Preserved evidence: source commit 3e26250447dd5bc095c4ceef22de3beb093e1fd4 within accepted cumulative candidate 67ee16ef002d297e755a6284fe20afde4457d4f2; semantically reconcile its four cross-harness paths against current main rather than replaying the combined candidate.
- Phase: completed on main; terminal archive and cleanup handoff recorded.

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

## Completion Evidence

- Preserved source provenance: cross-harness source commit 3e26250447dd5bc095c4ceef22de3beb093e1fd4 was semantically reconciled from accepted cumulative candidate 67ee16ef002d297e755a6284fe20afde4457d4f2 instead of being rebuilt or discarded.
- Accepted candidate: f7d202bfd95e5b28e49b8d4ed9e1ced6b722eb85 on codex/document-cross-harness-skill-lifecycle. The earlier incorrectly expanded f7d202b hash was rejected and is not delivery evidence.
- Fresh independent documentation review: ACCEPT with no findings. It confirmed the single authoritative lifecycle owner, cross-harness mechanism accuracy, sibling-page consistency, five resolving primary-source URLs, and 42 changed-page local paths and fragments with zero failures.
- Focused verification: four lifecycle documentation tests and five selected bundle, generator, and documentation-owner tests passed; scripts/build-skill-docs.py --check reported current output; git diff checks passed; no governed definition or generated-definition mirror changed. The complete agent catalog was intentionally not run for this bounded documentation item.
- Main integration: cbd37825c7ca7328f4b3538087974cdb2beb0a60. The same nine focused tests, documentation freshness check, and diff hygiene passed on main.
- Cleanup eligibility: the private branch and worktree are clean and patch-equivalent to main after cherry-pick integration. Per the parent cleanup rule, no zero-byte topology merge is created; the parent rebases the clean branch onto current main so Git skips the applied patch, then removes the worktree and deletes the ancestor branch non-forcing.
- Integration claim: integrate-cross-harness-lifecycle-019f7e8f acquired event c98f904e-e57d-4318-9a16-ec565023ac98 and released cleanly at event 3dbcc11d-586e-45e2-9b9c-841f1b0cb0f0. The initial primary-worktree contention attempt was preserved at event 9d9c1fe4-a210-41c1-a7c0-249ec3d12961 and resolved by direct release notification rather than isolated integration.
- Terminal backlog claim: complete-cross-harness-lifecycle-019f7e8f acquired exact active and completed paths at event 8185b759-dcb0-41f5-ada0-e88e7bcb814e; its clean release follows this archive commit and is reported in the terminal handoff.

## Notes

- A source-backed outline may be prepared while dependencies run, but final status must remain blocked until implementation and Codex evidence are stable.
