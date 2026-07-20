# Build The Agent And Skill Mind Map

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7e8f-f751-7ef2-83d3-31d17323de48.
- Branch: codex/build-agent-skill-mind-map-resume-019f7e8f.
- Worktree: /Users/martinbechard/.codex/worktrees/c1cd/dev-methodology.
- Dependencies: replace-router-with-setup-detector and verify-codex-skill-activation are completed.
- Preserved evidence: archived integration task 019f7d30-de3a-7e61-a838-a3e127383b27 and accepted cumulative candidate 67ee16ef002d297e755a6284fe20afde4457d4f2; reconcile and semantically extract the mind-map portion rather than rebuild or discard it.
- Phase: completed and integrated on main.

## Completion Evidence

- Preserved source provenance: archived task 019f7d30-de3a-7e61-a838-a3e127383b27, accepted source commit 0cd05b35f7e793c4b9191b5b5c3fce52955c7ef1, and cumulative candidate 67ee16ef002d297e755a6284fe20afde4457d4f2.
- Final corrected candidate: 0e5a286f407efc12ad75a67325ef9183a2b95002 on codex/build-agent-skill-mind-map-resume-019f7e8f.
- Fresh independent final review: PASS with no required correction or open question.
- Fresh focused verifier: PASS on 23 focused tests, support-checklist, hierarchy, technology-detection, skill-documentation and adapter-manifest freshness, JavaScript syntax, exact detector-source paths, link resolution, and diff hygiene.
- Main integration commits: b97bb48, 35790ec, 76c0e49, fa0425e, and 026f100. The final integrated main commit is 026f100deab77685dccc8cf7a0cd46aaec35dc60.
- Post-integration verification: 23 focused tests passed; build-support-checklist, build-agent-skill-hierarchy, build-technology-detection, and build-skill-docs freshness checks passed; both explorer JavaScript files passed syntax checks; main was clean.
- Integration ownership: exact nine-path and merge:integration:main claim 019f7e8f-mind-map-integration acquired at event 2a56c5ff-cce5-469d-a6f4-5215bde08367 and released at event facfffde-c33e-4432-aacb-feaf61c1fd84.
- Browser environment warning: the resource-only browser:in-app claim was released at event a3173fee-7b31-4ac0-9691-0cd37249b3ff after the in-app browser rejected the local file URL under host policy. Parent disposition classified this as an environment warning; no prohibited workaround was attempted.
- Terminal backlog ownership: exact source/destination claim 019f7e8f-mind-map-completion acquired at event b0d55304-b4ca-4d9a-825c-292f14d9265b.
- Cleanup eligibility: the task worktree is clean and the source branch is patch-equivalent to main. No topology-only merge was created; the parent owns rebase-and-skip cleanup followed by non-forcing branch deletion.

## Summary

Build an interactive mind map for exploring agents, definition-owned skills, detected technology skills, loading mechanisms, model profiles, harness adapters, activation evidence, and verification status.

## Context

The repository already generates conceptual agent definition, skill, detection, hierarchy, and evaluation data, but the current views do not provide one explorable relationship model. The visualization must consume the stable detector and evidence schemas rather than encode relationships manually.

See the series [index](index.md).

## Requirements

- Generate one joined explorer data contract from conceptual agent definitions, skill catalog, technology detection registry, model profiles, adapters, evaluation cases, and verified receipts.
- Show definition-owned edges separately from detected-folder edges.
- Show Claude preload, Claude dynamic Skill-tool loading, Codex instruction-driven loading, optional availability overrides, and any verified app-server injection evidence.
- Provide filters for agent, skill category, technology, capability, folder scope, harness, model profile, loading mode, declaration status, and verified behavior.
- Link agent nodes to conceptual agent definition sources and generated adapters.
- Link skill nodes to SKILL.md and detection metadata.
- Link evidence status to evaluation cases and receipts.
- Make missing, unsupported, blocked, manual, declared, and verified states visually distinct.
- Keep the view usable with the current catalog size and keyboard accessible.
- Generate data; do not duplicate the catalog in hand-authored page code.

## Acceptance Criteria

- A user can start from an agent and identify every definition-owned and potentially detected skill.
- A user can start from a skill and identify agents, technologies, loading modes, and verification evidence.
- TypeScript, Spring Boot, Python, and FastAPI paths are distinguishable.
- Manual observations cannot appear as verified behavior.
- Filtering to one harness shows its actual preload or dynamic-loading semantics.
- All links resolve and all generated data freshness checks pass.
- The visualization works without network access.

## Dependencies

- replace-router-with-setup-detector
- verify-codex-skill-activation

## Verification

- Run generated-data freshness tests.
- Validate every displayed node and edge against source data.
- Test keyboard navigation and representative filters.
- Inspect the page at desktop and narrow viewport widths.
- Perform an independent comparison against the support checklist and hierarchy.

## Notes

- Do not begin implementation against the obsolete routing registry.
- Wireframes and interaction sketches may be prepared before dependencies complete, but final data binding must use the detector and verified evidence schemas.
