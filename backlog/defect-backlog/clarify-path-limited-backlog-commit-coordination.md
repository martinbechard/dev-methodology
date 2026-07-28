# Clarify path-limited backlog commit coordination

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md

Completion: direct-main

## Summary

Clarify and enforce claim-scoped, path-limited file-provider Git mutations so unrelated primary-worktree use does not serialize a one-file backlog update, while true overlaps and transient Git contention are handled truthfully and boundedly.

## Context

The user reported that an agent waited for Coordinator serialization even though the live integrate-project-wiki-role-routing-019faa18 project_files claim covered unrelated non-backlog paths. The agent explained this by shared primary worktree, index, HEAD, and commit. The user said this blocks many tasks and requested a second work item clarifying single-file backlog commits.

The user additionally requires every lifecycle mutation assignment or baton to Dev Backlog Steward to list exact canonical repository-relative provider path or paths. An in-place mutation names one current path; a move or archive names both source and destination; a multi-record operation names every path and its atomic rationale. Conversation title is display-only and never provider identity or mutation scope.

The user further requires command-level path binding: every mutating Git command names its exact authorized repository-relative provider pathspec after --. Staging, commits, moves, and archive operations cannot use broad, wildcard, directory, inferred, or implicit-index scope. The instruction manifest, claim paths when a claim applies, staged and committed paths, immutable changed-path set, and provider references must agree exactly.

## Source Evidence

Direct user authorization in the canonical parent conversation on 2026-07-28. The user reported the unrelated integrate-project-wiki-role-routing-019faa18 project_files claim, stated that this blocks many tasks, and requested a second item clarifying single-file backlog commits. The same user supplied the exact-path lifecycle-baton and command-level path-binding amendments before creation.

## Requirements

- Define that claim overlap, not mere shared primary-worktree use, determines methodology ownership conflicts. A project_files claim excludes backlog and alone does not block a nonoverlapping exact backlog mutation.
- Define a safe path-limited Git commit for an existing backlog file, an exclusive-create new file, and an archive or move pair. Each immutable commit must contain exactly the intended provider paths and bytes, preserve unrelated staged and dirty state, and remain valid if main advances.
- Prohibit broad staging and ordinary index-wide commits for exact provider mutations. Use a supported path-limited Git mechanism and verify the immutable changed-path set and bytes.
- Distinguish a short Git or index lock from methodology serialization. A transient lock or moving HEAD requires bounded, evidence-based reconciliation, not indefinite Waiting for Coordinator or a fabricated claim conflict.
- Permit nonoverlap when scopes, main authority, path snapshots, and commit preconditions are satisfied. Serialize true overlap or broad scope.
- Require accurate conversation titles: never Waiting for Claim when no overlap exists, and use bounded coordination or reconciliation only when another owner controls the next event.
- Put the normative claim rule in skills/agent-claim/SKILL.md. Put file-provider mechanics in skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md. Align skills/codex-workitem-coordination/SKILL.md only if its current central procedure conflicts. Keep skills independent and do not copy cross-skill policy.
- Require every lifecycle mutation assignment or baton to Dev Backlog Steward to carry an exact canonical repository-relative provider-path manifest. Refuse vague, title-only, conversational, directory, wildcard, partial, mismatched, inferred, or missing scope. Never derive mutation scope from conversation title.
- For an in-place mutation, require its one current path. For move or archive, require both source and destination. For multi-record mutation, require every path and a stated atomic rationale. Preserve durable exact-path manifest evidence.
- Require every mutating Git argv to name exact authorized repository-relative pathspecs after --. Staging must not use git add ., unbounded git add -A, directory staging, wildcard staging, or implicit index reuse. Commit must use a supported path-limited form with exact authorized pathspecs after --, not whatever is staged.
- Before each mutation, compare the Git argv pathspec manifest with the instruction manifest and applicable claim scope. After each mutation, compare the immutable commit changed-path set and bytes. Any mismatch is BLOCKED or failed, never successful.
- Treat the anticipated governed manifest as discovery only, not approval. Obtain exact scope-specific user approval before mutating a governed skill definition.

## Acceptance Criteria

- The MySQL example is not blocked solely by an unrelated non-backlog project_files claim.
- One-file and archive or move commits preserve unrelated staged and dirty state, while a true overlap stops safely.
- Nonoverlap, moving-main, and transient-lock handling are deterministic and bounded rather than indefinitely serialized.
- Conversation titles accurately describe the actual coordination state.
- Exact-path manifests reject missing, partial, inferred, wildcard, directory, mismatched, and move-source-or-destination omissions.
- Focused executable tests or a testable wrapper prove exact Git argv path binding and no unbounded fallback, including changed-path proof.

## Dependencies

None

## Verification

- Add focused coverage for project_files plus backlog, staged-state preservation, moving main, overlap, archive pair, and immutable changed-path proof.
- Add negative coverage for missing, partial, inferred, wildcard, directory, and mismatched manifests, plus move omission of either source or destination.
- Add focused executable coverage or a testable wrapper proving exact Git argv pathspecs and the absence of broad staging or commit fallback.
- Run focused contract tests, parser or backlog report validation, applicable generator freshness checks, and git diff --check.
- Obtain independent review of claim scope, provider mechanics, title accuracy, and command-level path binding.

## Open Questions

- What exact Git primitive and bounded lock or HEAD reconciliation procedure should be supported?
- Does current claim-helper behavior or existing guidance contradict the intended contract?

## Notes

Collision reconciliation before creation searched ordinary active typed folders, backlog/user-action-required, and backlog/holding only. It found no matching canonical path, slug, source reference, or overlapping outcome. Future Ideas were not inspected.

Exact-path manifest for this creation: backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md. The exclusive-create operation, explicit staging pathspec, path-limited commit pathspec, immutable changed-path set, and Provider Reference must all name exactly this one path.

This Ready item authorizes backlog capture only. It does not approve any governed definition mutation, reserve capacity, dispatch execution, or change a lifecycle state.
