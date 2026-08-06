# Extract Future Idea Management

Status: Ready

Type: Feature

Provider: file

Work Item ID: extract-future-idea-management

Completion: direct-main

## Summary

Move Future Idea capture, inventory, validation, and promotion out of the file work-item creation and lifecycle providers into a dedicated `manage-future-ideas` skill, with one shared file-provider transaction skill for atomic writes and commits.

## Context

`create-file-work-item` currently creates ordinary work items, captures Future Ideas, promotes them, classifies work, and owns the exact Git transaction for both ordinary creation and promotion. `manage-file-work-items` separately owns Future Ideas inventory and validation. Future Ideas are explicitly not work items or lifecycle states, so those responsibilities do not belong inside either provider interface.

The split should leave the provider implementations focused on their public contracts:

- `create-work-item-file` creates ordinary file-backed work items.
- `manage-work-items-file` manages ordinary work-item lifecycle.
- `manage-future-ideas` owns the file-backed Future Ideas model, capture, explicit inventory, validation, and promotion workflow.
- `commit-file-provider-transaction` owns the exact-path, no-overwrite, resource-coordination, path-limited Git commit, immutable-proof, and unrelated-state preservation procedure shared by ordinary creation and promotion.

## Source Evidence

On 2026-08-05, the user requested a complete audit for additional naming and responsibility changes. The Backlog Management group currently lists Future Ideas Capture, Future Idea Promotion, and Exact Backlog Creation Transaction inside `create-file-work-item`, while `skills/manage-file-work-items/SKILL.md` also contains a Future Ideas Workflow. Source headings and instructions confirm that Future Ideas are not ordinary work items and are excluded from normal lifecycle inventory and dispatch.

## Requirements

- Add `skills/manage-future-ideas/SKILL.md` with the Future Ideas definition, file authority, capture, explicit inventory, validation, promotion, result, and non-dispatch boundaries.
- Add `skills/commit-file-provider-transaction/SKILL.md` with one operation covering the supported ordinary one-path creation and atomic two-path Future Idea promotion shapes.
- Remove Future Ideas procedures and definitions from `create-work-item-file` except for a concise boundary that routes an explicit Future Ideas request to `manage-future-ideas`.
- Remove Future Ideas procedures and definitions from `manage-work-items-file` except for a concise exclusion from ordinary lifecycle inventory and dispatch.
- Make ordinary file-provider creation and Future Idea promotion use the shared transaction procedure without duplicating its claim, Git, rollback, or immutable-proof rules.
- Keep Future Ideas file-provider-only, lightweight, non-dispatchable, outside lifecycle counts, and excluded from ordinary duplicate scans unless promotion is requested.
- Keep promotion explicitly authorized and require a complete reciprocal source/destination record in one atomic transaction.
- Route `manage-future-ideas` only when a request or an explicitly authorized workflow calls for Future Ideas; do not make it an unconditional backlog-management dependency.
- Update the Backlog Management group, affected Agent routing, templates, evaluations, and generated documentation to show the non-overlapping peer skills.

## Acceptance Criteria

- `create-work-item-file` implements ordinary creation without owning Future Ideas capture or promotion.
- `manage-work-items-file` implements ordinary lifecycle management without listing or validating Future Ideas.
- `manage-future-ideas` is the sole source for Future Idea behavior and retains every current safety and authority boundary.
- `commit-file-provider-transaction` is the sole source for ordinary creation and promotion transaction mechanics.
- An explicit Future Idea capture, explicit inventory, and promotion all pass focused behavioral tests; ordinary backlog inventory continues to ignore Future Ideas.
- Atomic promotion, no-overwrite behavior, exact path-limited commits, rollback, immutable proof, and unrelated dirty/staged state preservation remain covered.
- The skill-group model shows these as non-overlapping members and does not present Future Ideas as a work-item provider lifecycle.

## Dependencies

- align-work-item-creation-provider-names
- align-work-item-management-provider-names

## Blocked Evidence

Blocker: The two naming items have not yet delivered the exact `create-work-item-file` and `manage-work-items-file` canonical sources from which this responsibility split must proceed.

Blocker Owner: Dev Backlog Coordinator.

Exact Unblock Condition: Both dependency Work Item IDs reach terminal successful dispositions on current main; `skills/create-work-item-file/SKILL.md` and `skills/manage-work-items-file/SKILL.md` exist as the canonical provider definitions; and their source and integration claims are released.

Permitted Resumption Transition: Blocked -> Ready after the Coordinator verifies that exact condition.

## Ready Recovery — 2026-08-06

- Transition: Blocked -> Ready.
- Recovery authority: Dev Backlog Coordinator authorized this single provider transaction after reconciling both declared dependencies on current main.
- Dependency reconciliation: align-work-item-creation-provider-names is terminal successful with archive commit 793d4303a7440803ad79f5440a77ffee7882081d; align-work-item-management-provider-names is terminal successful with archive commit 4182c62110e1a87c6687b68e40bdb1f8b3fbc155.
- Current main: 4182c62110e1a87c6687b68e40bdb1f8b3fbc155; both dependency commits are ancestors of current main.
- Canonical sources: skills/create-work-item-file/SKILL.md and skills/manage-work-items-file/SKILL.md exist on current main.
- Claim reconciliation: The dependency source and integration claims are released; the current claim registry has no live claim for either dependency.
- Exact unblock condition: Satisfied. Both dependency Work Item IDs have terminal successful dispositions on current main, both canonical provider definitions exist, and their source and integration claims are released.
- Owner: Unowned.
- Next action: Parent Dev Backlog Coordinator may reserve Ready -> Starting; this recovery does not create execution ownership.

## Verification

- Resolve both dependency Work Item IDs from provider state before lifecycle transition.
- Run the governed-definition pre-mutation check for every canonical source listed below.
- Validate all four affected or new skill packages.
- Run file-provider creation, lifecycle, Future Ideas, promotion atomicity, claim, Git path-limiting, rollback, and unrelated-state preservation tests.
- Run affected Agent suites, bundle tests, evaluation coverage checks, and backlog-report regressions proving ordinary inventory excludes Future Ideas.
- Regenerate supported metadata, adapters, group documentation, and evaluation documentation and run freshness checks.
- Run `git diff --check` and obtain fresh independent methodology review and verification.

## Open Questions

- Determine whether the shared transaction skill should expose one discriminated transaction procedure or two named procedures backed by the same invariants; either design must keep one authoritative rule set.

## Governed Definition Approval

### Governed Canonical Sources

- skills/create-work-item-file/SKILL.md
- skills/manage-work-items-file/SKILL.md
- skills/manage-future-ideas/SKILL.md
- skills/commit-file-provider-transaction/SKILL.md
- agents/roles/dev-activities/dev-backlog-steward.role.yaml

### Allowed Dependent Artifacts

- AGENTS.md
- PROJECT.yaml
- README.md
- skills/route-documentation-work/assets/templates/file-work-item-template.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/skill-groups/backlog-management.md
- design/skill-groups/concurrent-tasking.md
- design/work-item-provider-and-completion-contracts.md
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- evals/agent-tests/dev-backlog-steward/suite.yaml
- evals/projects/file-work-item-template-contract/requests.md
- evals/projects/file-work-item-template-contract/verify.py
- scripts/test_bundle_content.py
- scripts/test_generate_backlog_report.py
- New package `agents/openai.yaml` metadata produced from only the approved new skill sources.
- Supported generated Agent, skill, hierarchy, catalog, evaluation, and native-adapter outputs produced from the approved canonical sources.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's request to identify and log further responsibility changes. The exact split follows the audited source boundaries: Future Ideas are not work items, and the current creation and management providers both contain Future Ideas responsibilities. Approval is limited to the exact governed canonical paths above after the two named dependencies establish the renamed provider sources.

## Notes

The dependency is about canonical source identity, not shared-file convenience. The item must remain Blocked until the two renamed provider definitions exist; it must not be dispatched as Ready against the retired paths.
