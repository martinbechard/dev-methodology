# Clarify path-limited backlog commit coordination

Status: Running

Type: Defect

Owner: Root Dev Orchestrator for canonical task 019fab2d-d9ac-7a82-8107-04260716d4d0

Provider: file

Provider Reference: backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md

Completion: direct-main

## Resumption Evidence

Controlling Dated User Answer: 2026-07-28 — “ok I approve”

Canonical-Task Provenance: The answer was received in the canonical parent conversation for canonical work-item Thread and root task 019fab2d-d9ac-7a82-8107-04260716d4d0.

Approved Governed Scope Only:

- skills/create-file-work-item/SKILL.md
- skills/manage-file-work-items/SKILL.md

Explicitly Excluded: skills/agent-claim/SKILL.md, skills/codex-workitem-coordination/SKILL.md, and arbitrary non-backlog files.

Preflight Gate: No source mutation occurs until an approval record exists and both exact supported preflights for the two approved definition paths return ALLOWED.

## Superseded User Action Required Clarification

The earlier broader question that named skills/agent-claim/SKILL.md, skills/create-file-work-item/SKILL.md, and skills/manage-file-work-items/SKILL.md is retained as superseded clarification evidence. The controlling answer above approves only the two paths listed in Approved Governed Scope Only and does not approve excluded paths.

## Dispatch Reservation

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Canonical Work-Item Thread: 019fab2d-d9ac-7a82-8107-04260716d4d0

Canonical Root Agent Task: 019fab2d-d9ac-7a82-8107-04260716d4d0

Launch Reservation: One bounded live handshake for the canonical work-item Thread.

Dispatch Time: 2026-07-29T01:17:14.465238Z

Normalized Objective: Clarify and enforce claim-scoped, path-limited file-provider Git mutations for the exact provider record while preserving unrelated primary-worktree state.

Intended Root Role: Dev Orchestrator

Branch: codex/clarify-path-limited-backlog-commit-019fab2d

Worktree: /Users/martinbechard/.codex/worktrees/95f4/dev-methodology

Observed Launch Evidence: Parent Dev Backlog Coordinator authorized one bounded resumption reservation for the preserved canonical Thread and root task identity.

Required Next Lifecycle Transition: The same canonical task's root Dev Orchestrator must record Starting to Running before any implementation or approval work.

Conversation-Title Handoff: Synchronized with the Parent Coordinator; the title is display-only and does not alter the canonical provider identity or mutation scope.

Resumption Ready Commit: e3ca0888553d908420bf2df3718a06b757629885

Resumption Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim ready-starting-clarify-path-limited-019fab2d; journal event 1a61bfbc-a14a-4b9a-a6d3-347718f313d5; exact path backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md.

Approved Scope and Preflight Gate: The controlling answer approves only skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md. No source mutation occurs until an approval record exists and both exact supported preflights return ALLOWED.

## Running Evidence

Root Dev Orchestrator: Root Dev Orchestrator for canonical task 019fab2d-d9ac-7a82-8107-04260716d4d0

Canonical Work-Item Thread: 019fab2d-d9ac-7a82-8107-04260716d4d0

Canonical Root Agent Task: 019fab2d-d9ac-7a82-8107-04260716d4d0

Branch: codex/clarify-path-limited-backlog-commit-019fab2d

Worktree: /Users/martinbechard/.codex/worktrees/95f4/dev-methodology

Started At: 2026-07-29T01:18:03.065326Z

Phase: Lifecycle acceptance recorded after resumption; no definition, test, documentation, mirror, candidate, review, integration, delivery, or other source mutation has started.

Starting Reservation Commit: 8ae2360cbe52e799d4653fe99a1aad49b36bec9c

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim starting-running-clarify-path-limited-019fab2d; journal event bc2405de-c2f8-4584-85e6-d6555e74b906; exact path backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md.

Controlling Approval and Gate: The dated controlling answer “ok I approve” applies only to skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md. Do not mutate either source path until an approval record exists and both exact supported preflights return ALLOWED.

## Summary

Clarify the guidance and contract in exactly skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md for canonical file-provider records under backlog/** only.

## Context

The user requested a narrow clarification after earlier candidate work overreached into a production-style Git transaction helper and broad concurrency behavior. This item is guidance and contract clarification for file-provider backlog records, not a runtime transaction implementation.

The user additionally requires every lifecycle mutation assignment or baton to Dev Backlog Steward to list exact canonical repository-relative provider path or paths. An in-place mutation names one current path; a move or archive names both source and destination; a multi-record operation names every path and its atomic rationale. Conversation title is display-only and never provider identity or mutation scope.

The required contract remains narrow: a complete exact canonical provider-path manifest for creation, update, move, archive, and justified atomic multi-record operations; explicit exact repository-relative pathspecs after -- in mutating Git commands; a path-limited commit; immutable commit changed-path, committed-byte, and Provider Reference proof; preservation of unrelated staged and dirty state; and refusal of missing, partial, inferred, wildcard, directory, or mismatched manifests.

## Source Evidence

Direct user authorization in the canonical parent conversation on 2026-07-28. The user reported the unrelated integrate-project-wiki-role-routing-019faa18 project_files claim, stated that this blocks many tasks, and requested a second item clarifying single-file backlog commits. The same user supplied the exact-path lifecycle-baton and command-level path-binding amendments before creation.

## Requirements

- Apply the required contract only to canonical file-provider records under backlog/** in skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md.
- Require complete exact canonical provider-path manifests for creation, update, move, archive, and justified atomic multi-record operations. Refuse missing, partial, inferred, wildcard, directory, and mismatched manifests.
- Require explicit exact repository-relative pathspecs after -- in mutating Git commands, a path-limited commit, and immutable changed-path, committed-byte, and Provider Reference proof while preserving unrelated staged and dirty state.
- Exclude a production or runtime Git transaction helper or engine. Do not define or simulate Agent Claim internals, Git or index lock settlement, concurrent or moving HEAD races, commit-attribution protocols, or arbitrary non-backlog file behavior.
- Preserve exact scope-specific approval and preflight gates before any governed definition mutation.

## Acceptance Criteria

- The two approved skills state the narrow backlog/** guidance and contract without introducing a reusable runtime transaction helper or engine.
- Exact-path manifests reject missing, partial, inferred, wildcard, directory, mismatched, and move-source-or-destination omissions.
- Guidance requires path-limited commits, immutable changed-path and committed-byte proof, Provider Reference agreement, and unrelated staged and dirty preservation.
- Tests remain test-only contract evidence and do not implement or claim coverage for claim engines, lock or race coordination, concurrent HEAD, commit attribution, or a general transaction engine.

## Dependencies

None

## Verification

- Run exact approval preflights and structural validation of both approved skills.
- Add focused deterministic contract assertions, supported skill-mirror freshness checks, and relevant existing file-provider fixtures.
- Use only a few minimal temporary-Git examples for ordinary one-file create or update and source-destination move with path preservation.
- Do not implement or claim test coverage for claim engines, lock or race coordination, concurrent HEAD, commit attribution, or a general transaction engine.

## Scope Correction / Delivery Clarification

On 2026-07-28, the user asked why the work overreached, accepted the explanation, and directed: “ok fix the workitem wording so this doesn't happen again.” The clarification limits the outcome to guidance and contract wording in skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md for canonical file-provider records under backlog/** only.

Rejected candidates dd36a8485c783f70dad5afbdcabe3a1cab4327c9 and d76e67c7a2eb277e5a4e742202f3c7723fdf8046 were not integrated and motivated this clarification. They do not authorize production helpers, claim-engine behavior, Git or index lock settlement, concurrent or moving HEAD behavior, commit attribution protocols, or arbitrary non-backlog behavior.

## Notes

Collision reconciliation before creation searched ordinary active typed folders, backlog/user-action-required, and backlog/holding only. It found no matching canonical path, slug, source reference, or overlapping outcome. Future Ideas were not inspected.

Exact-path manifest for this creation: backlog/defect-backlog/clarify-path-limited-backlog-commit-coordination.md. The exclusive-create operation, explicit staging pathspec, path-limited commit pathspec, immutable changed-path set, and Provider Reference must all name exactly this one path.

This Ready item authorizes backlog capture only. It does not approve any governed definition mutation, reserve capacity, dispatch execution, or change a lifecycle state.
