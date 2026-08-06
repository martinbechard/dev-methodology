# Extract Future Idea Management

Status: Running

Owner: Root Dev Orchestrator 019fd5b5-aca7-7cb1-9ae0-010ac945c985

## User Action Required

Do you approve adding exactly evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md to this work item’s governed manifest so the Dev Backlog Steward evaluation suite can be made executable and consistent?

Why user input is required: This is the only newly required governed skill definition outside the existing manifest. The other four support paths—evals/agent-tests/dev-backlog-steward/agents/supervisor.toml, agents/judge.toml, fixtures/cases.yaml, and test_contract.py—are ordinary non-governed evaluation/test dependents covered by the executable-suite acceptance requirement and need no separate approval.

Options and tradeoffs: Approve permits exactly that suite-contract SKILL.md addition plus corrections to those four already-authorized ordinary support files, then the same canonical task resumes through User Action Required -> Ready -> Starting -> Running and focused rereview/verification. Defer preserves candidates and evidence without implementation. Decline leaves acceptance unmet for later disposition.

Unattended boundary: Stop all implementation, correction, verification, integration, and delivery until the user answers and lifecycle resumption occurs. Exclude every other skill, role, definition, and broad suite/framework.

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

## Starting Reservation — 2026-08-06T06:12:33Z

- Transition: Ready -> Starting.
- Coordinator reservation: Dev Backlog Coordinator reserved this Work Item ID on current main at 2026-08-06T06:12:33Z.
- Owner handoff: Dev Backlog Coordinator retains reservation ownership and will hand off to one root Dev Orchestrator after launch acceptance.
- Root Agent Task: Not assigned; no child task was created by this reservation transaction.
- Launch result: Pending; this provider transaction does not start a task or create execution ownership.
- Next action: Launch one root Dev Orchestrator and record Starting -> Running only after accepted execution evidence.

## Current Execution

Transition: Starting -> Running.

Canonical Conversation: 019fd5b5-aca7-7cb1-9ae0-010ac945c985.

Root Agent Task: /root.

Owner: Root Dev Orchestrator 019fd5b5-aca7-7cb1-9ae0-010ac945c985.

Branch: codex/extract-future-idea-management.

Worktree: /Users/martinbechard/.codex/worktrees/e9e9/dev-methodology.

Baseline / current main at launch: cc5574b798c0fab87fb5c9c6b3c6acd935030feb.

Coordinator reservation commit: cd5878a187a4771e4f16ffdfca0bae890960e254.

Phase: Provider lifecycle transition.

Accepted Execution Evidence: The canonical root task accepted this exact Work Item ID, established the isolated execution branch and worktree, and acquired the exact update and provider-path claims required for this atomic transition.

Provider Operation Evidence: Work Item ID update claim extract-future-idea-management-update and exact path claim extract-future-idea-management-file returned SHARED_CHECKOUT_ACQUIRED.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator 019fd5b5-aca7-7cb1-9ae0-010ac945c985.

Evidence: Direct unblock repair 46b92c842693bb96b5e756632a8df35b241511bc was reviewed and verified. The canonical root is actively accepting the exact approved resumption. User approval and manifest expansion are durable in Ready commit d9e76dfb and Starting commit e37e082a. Final candidate 211f11e17e1a52e8ed8f43dce52e39ad95e50ba5 is clean with no implementation defect, blocker, or User Action Required. Decisive code and methodology reviews are APPROVED. The independent focused verifier reports all executable checks PASS but overall FAIL only because the required Agent Skill validator rejects linked-worktree paths; the gate will rerun on authoritative current main after integration. Work heartbeat event: 2299d87f-0040-4020-8fb6-357f59ebcbcf. Handoff event: 43f6d6da-6534-476b-8a66-5e961bf416fe. Required title: Integrating — Extract Future Idea Management.

Observed At: 2026-08-06T14:03:56Z.

Started At: 2026-08-06T12:32:17Z.

Deadline or Expires At: 2026-08-06T14:32:17Z.

Next Action: Perform final current-main integration with exact project-files and main-integration claims, then rerun skill validation and complete post-integration verification and review. Exclude all other definitions, broad suites, and frameworks.

Next Reconciliation At: 2026-08-06T14:18:56Z.

## User Action Required Transition — 2026-08-06T07:27:07Z

- Transition: Running -> User Action Required.
- Recovery authority: Dev Backlog Coordinator authorized this exact provider transaction.
- Owner: Unowned.
- Canonical task: 019fd5b5-aca7-7cb1-9ae0-010ac945c985.
- Source path: backlog/feature-backlog/extract-future-idea-management.md.
- Destination path: backlog/user-action-required/extract-future-idea-management.md.
- Review candidate: 20129c822f0ce78fe46a0aeaaa6e7b719d841dc6.
- Corrected candidate: c94dc4fd674405f9c96c10c51c99ed24fcd767f3.
- Released work-claim blocked-disposition event: b6665918-a435-4e73-a29f-0e31bfa4b8af.
- Question recorded first in the User Action Required section above.
- Next action: Wait for the user answer before any implementation, correction, verification, integration, or delivery resumes.

## User Answer and Ready Resumption — 2026-08-06

- Transition: User Action Required -> Ready.
- Exact answer: `I approve`.
- Provenance: Direct user message in canonical work-item conversation `019fd5b5-aca7-7cb1-9ae0-010ac945c985` on 2026-08-06, immediately after the exact recorded question above.
- Approved governed addition: Exactly `evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md`.
- Ordinary dependent clarification: `evals/agent-tests/dev-backlog-steward/agents/supervisor.toml`, `evals/agent-tests/dev-backlog-steward/agents/judge.toml`, `evals/agent-tests/dev-backlog-steward/fixtures/cases.yaml`, and `evals/agent-tests/dev-backlog-steward/test_contract.py` are non-governed support paths already covered by the executable-suite acceptance requirement.
- Exclusions: No other skill, role, governed definition, broad suite, or framework is approved.
- Preserved candidates: `20129c822f0ce78fe46a0aeaaa6e7b719d841dc6` and `c94dc4fd674405f9c96c10c51c99ed24fcd767f3`.
- Next action: The parent Dev Backlog Coordinator may record Ready -> Starting for the same canonical task; implementation remains stopped until that task separately records Starting -> Running and reacquires the exact activity=work claim.

## Starting Handoff Evidence — 2026-08-06T12:17:44Z

Starting Recorded At: 2026-08-06T12:17:44Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Resume the preserved Future Idea management candidate with exactly the newly approved Dev Backlog Steward suite-contract skill and the four already-authorized ordinary support paths, then complete focused rereview, verification, and direct-main delivery.

Launch Result: Started

Canonical Conversation: `019fd5b5-aca7-7cb1-9ae0-010ac945c985`

Last Contact At: 2026-08-06T12:14:03Z

Next Reconciliation At: 2026-08-06T12:32:44Z

Preserved Candidate Evidence: `20129c822f0ce78fe46a0aeaaa6e7b719d841dc6` and `c94dc4fd674405f9c96c10c51c99ed24fcd767f3` remain the canonical source and corrected candidates.

Next Action: The existing canonical root Dev Orchestrator records Starting -> Running, reacquires the exact Work Item ID activity=work claim, and resumes the preserved correction; no replacement task is created.

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
- evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md

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
- evals/agent-tests/dev-backlog-steward/agents/supervisor.toml
- evals/agent-tests/dev-backlog-steward/agents/judge.toml
- evals/agent-tests/dev-backlog-steward/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-steward/test_contract.py
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
