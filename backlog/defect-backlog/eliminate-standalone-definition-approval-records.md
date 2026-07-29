# Eliminate Standalone Definition Approval Records

Status: Blocked

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/eliminate-standalone-definition-approval-records.md

Completion: direct-main

## Summary

Remove the manually invoked definition-change approval checker and its duplicate standalone YAML inputs. Keep exact-scope user authorization durably in the canonical work item, and remove approval-record files from the repository root and the ignored `.codex/approval-records` directory.

## Context

The repository currently tracks 113 root files matching `approval-record-*.yaml`. Seven additional local records exist under the ignored `.codex/approval-records` directory. These files duplicate authorization evidence that the work-item contract already requires.

The command implemented by `scripts/render-agents-technology-skills.py` accepts `--check-definition-change`, `--approval-record`, and `--regenerated-from`. It validates a separately supplied YAML mapping but does not create approval, enforce filesystem mutation, authenticate provenance, own retention, archive records, or delete them. No repository contract defines a durable location or cleanup lifecycle for the standalone files. The README example passes a root-relative `approval-record.yaml`, and completed implementation commits have accumulated the inputs in the repository root.

The durable authority boundary remains necessary: changes to governed agent and skill definitions require explicit user direction for exact canonical paths, and additional governed paths require additional approval. The defect is the duplicate standalone-file and manually invoked checker mechanism, not the exact-scope authorization rule.

## Source Evidence

Direct user direction in Codex task `019faec9-c3ea-7d92-b350-6b21f091cb60` on 2026-07-29:

> "ok let's get rid of this garbage and delete the files in the root in the corresponding .codex subfolder. create a workitem to get rid of this and Record it in the workitem."

The direction followed a discussion in the same canonical task establishing that the checker is manually invoked by an implementation agent, is not a Git hook or CI enforcement mechanism, and duplicates approval evidence that belongs in the work item.

## Requirements

- Remove the standalone definition-change checker interface from `scripts/render-agents-technology-skills.py`, including `--check-definition-change`, `--approval-record`, and `--regenerated-from`, together with implementation that exists only to support those command paths.
- Remove instructions that require agents to create or pass standalone approval-record YAML files.
- Make the canonical work item's `Governed Definition Approval` section the durable record of exact approved governed paths, exact user wording, date, and user-message provenance.
- Preserve the rule that authorization is exact-path and explicit, and that any additional governed definition outside the work item's approved manifest requires additional user approval recorded in that work item before mutation.
- Preserve generated-mirror ownership rules and the prohibition against direct generated-definition edits.
- Delete every tracked root file matching `approval-record-*.yaml`.
- Delete every local file under `.codex/approval-records` and remove the empty directory when deletion is safe.
- Do not migrate the standalone YAML files elsewhere. Retain historical evidence through Git history and completed work-item records.
- Update `PROJECT.yaml`, generated `AGENTS.md` guidance, README documentation, templates, design output, and focused tests so they describe and enforce the work-item-native authority contract without referring to a standalone approval record or pre-mutation checker command.
- Add regression coverage that fails when a root `approval-record-*.yaml` file is tracked or when maintained guidance instructs agents to create standalone approval-record YAML.
- Keep approval evidence out of design principles and generated mirrors except where those outputs reproduce the approved steady-state work-item contract.

## Acceptance Criteria

- `git ls-files 'approval-record-*.yaml'` returns no paths.
- `.codex/approval-records` contains no files and is removed when empty.
- The renderer exposes none of `--check-definition-change`, `--approval-record`, or `--regenerated-from`.
- Maintained repository guidance contains no command or instruction requiring a standalone approval-record YAML file.
- A canonical work item can record exact governed-definition approval without creating a second approval artifact.
- The work-item contract still requires exact canonical governed paths, exact user direction, date, and provenance, and still blocks scope expansion without additional recorded user approval.
- Direct editing of generated definition mirrors remains prohibited and supported regeneration remains source-owned.
- Focused tests cover removal of the command interface, root-file hygiene, work-item-native approval evidence, additional-scope handling, and generated-mirror ownership.
- Relevant generated outputs are fresh and consistent with the two approved skill-definition sources.
- Independent review confirms that removal of the checker does not weaken the explicit exact-scope user-authorization boundary.

## Dependencies

None.

## Verification

- Run focused renderer tests proving that the removed command-line options are unavailable and ordinary rendering still works.
- Run focused work-item creation and coordination tests for exact-path approval recorded in the canonical item and additional-scope rejection.
- Run a repository-tree assertion that no tracked root path matches `approval-record-*.yaml`.
- Inspect `.codex/approval-records` and require zero remaining files after cleanup.
- Search maintained sources for `--approval-record`, `--check-definition-change`, standalone approval-record creation instructions, and obsolete checker outcomes.
- Regenerate only the supported outputs owned by the approved skill-definition sources and run their freshness checks.
- Run the directly affected bundle-content and technology-renderer tests.
- Run `git diff --check`.
- Obtain fresh independent code and methodology review of the exact-scope authorization boundary.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- `skills/codex-workitem-coordination/SKILL.md`
- `skills/create-file-work-item/SKILL.md`

### Allowed Dependent Artifacts

- `PROJECT.yaml`
- `AGENTS.md`
- `README.md`
- `skills/development-methodology/assets/templates/file-work-item-template.md`
- `scripts/render-agents-technology-skills.py`
- `scripts/test_technology_detection.py`
- `scripts/test_codex_workitem_coordination.py`
- `scripts/test_bundle_content.py`
- `design/generated/skill-definitions.js`
- `generated/adapters/agent-generation-manifest.json`
- Generator-owned runtime adapter files whose conceptual agent definitions consume `codex-workitem-coordination` or `create-file-work-item`, but only when supported regeneration from either approved canonical skill source changes their generated bytes.
- Deletion of tracked root files matching `approval-record-*.yaml`.
- Deletion of local ignored files under `.codex/approval-records` and removal of that directory when empty.

### Approval Resolution

Approved at creation on 2026-07-29 by the direct user request in Codex task `019faec9-c3ea-7d92-b350-6b21f091cb60`: "ok let's get rid of this garbage and delete the files in the root in the corresponding .codex subfolder. create a workitem to get rid of this and Record it in the workitem."

This approval is limited to the two governed canonical skill-definition paths listed above and the dependent cleanup artifacts listed separately. It does not authorize changes to conceptual agent definitions, schemas, model profiles, skill metadata, adapter-owned skill definitions, or any additional distributed skill definition. Discovery of another governed canonical path requires new explicit user approval recorded in this work item before that path is mutated.

## Notes

## Missed-Settlement Reconciliation

Transition: Starting -> Ready.
Reconciled At: 2026-07-29T17:38:47Z.
Settlement Deadline: 2026-07-29T17:36:38Z.
Canonical Conversation and Root Agent Task: 019faeef-ff87-74b0-b834-79a811be1656.
Owner: Unowned.
Canonical Acceptance: None observed.
Source Mutation Evidence: None observed.
Required Resumption: Reuse the same canonical task through a new Ready -> Starting -> Running sequence.
Reconciliation: Ready.

## Historical Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: 019faeef-ff87-74b0-b834-79a811be1656.
Launch Reservation: One synchronized bounded launch reservation in the adaptive-capacity batch.
Normalized Objective: Eliminate standalone definition approval records.
Dispatch Time: 2026-07-29T17:35:38Z.
Intended Root Role: Root Dev Orchestrator.
Canonical Conversation and Root Agent Task: 019faeef-ff87-74b0-b834-79a811be1656.
Direct Conversation-Title Handoff: Eliminate Standalone Definition Approval Records.
Branch: codex/eliminate-standalone-definition-approval-records.
Worktree: /Users/martinbechard/.codex/worktrees/00b6/dev-methodology.
Owner: Unowned pending accepted root.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T17:35:38Z to 2026-07-29T17:36:38Z (exactly 60 seconds; shared adaptive-capacity batch window).
Runtime Launch Result: Direct conversation-title handoff accepted for the synchronized batch.
Canonical Conversation: 019faeef-ff87-74b0-b834-79a811be1656.
Owner Acceptance: Pending.
Reconciliation: Pending.

This item authorizes cleanup delivery but does not perform it during work-item creation. Preserve unrelated working-tree and backlog state.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.
Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
Launch Reservation: One root Dev Orchestrator launch requested for the preserved canonical work-item task.
Normalized Objective: Eliminate standalone definition approval records.
Dispatch Time: 2026-07-29T18:19:03Z.
Intended Root Role: Root Dev Orchestrator.
Launch Result: Requested.
Canonical Conversation and Root Agent Task: 019faeef-ff87-74b0-b834-79a811be1656.
Direct Conversation-Title Handoff: Eliminate Standalone Definition Approval Records.
Branch: codex/eliminate-standalone-definition-approval-records.
Worktree: /Users/martinbechard/.codex/worktrees/00b6/dev-methodology.
Owner: Unowned pending accepted root.
Last Contact: 2026-07-29T18:19:03Z; launch request recorded by Dev Backlog Steward.
Next Reconciliation: No later than 2026-07-29T18:34:03Z.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

This current handoff uses the no-short-settlement contract. The historical settlement evidence above remains preserved as prior attempt evidence.

## Active Execution Evidence

Transition: Starting -> Running.

Parent Coordinator Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Canonical Thread: 019faeef-ff87-74b0-b834-79a811be1656.

Root Agent Task: 019faeef-ff87-74b0-b834-79a811be1656.

Root Role: Dev Orchestrator.

Owner: Root Dev Orchestrator.

Branch: codex/eliminate-standalone-definition-approval-records.

Worktree: /Users/martinbechard/.codex/worktrees/00b6/dev-methodology.

Started At: 2026-07-29T18:21:38Z.

Provider Claim: provider-running-eliminate-standalone-definition-approval-records-019faeef; acquired 2026-07-29T18:21:30.006119Z.

Current Phase: Running with implementation pending.

Owner Acceptance: Accepted by Root Dev Orchestrator through canonical task 019faeef-ff87-74b0-b834-79a811be1656 at 2026-07-29T18:21:38Z.

Reconciliation: Starting -> Running recorded by Dev Backlog Steward on primary main.

## Blocked Evidence

Transition: Running -> Blocked.

Blocked At: 2026-07-29T19:10:33Z.

Canonical Thread: 019faeef-ff87-74b0-b834-79a811be1656.

Root Agent Task: 019faeef-ff87-74b0-b834-79a811be1656.

Owner: Unowned.

Preserved Execution Owner and Coordination State: Root Dev Orchestrator accepted the canonical task; Running execution is suspended pending the configured-root validation route.

Exact Blocker: Configured mcp-agent-ops skill_validate rejects candidate, source, and primary-checkout paths as outside configured skill roots without inspecting either approved skill; no dynamic configured-root mutation tool is exposed, and the structured rejection forbids fallback.

Blocker Owner: Project Configurator / configured validator infrastructure.

Unblock Condition: An authorized configured-root route can validate exactly skills/codex-workitem-coordination and skills/create-file-work-item from candidate 7cca88fee05db053e452729fcc094cc8309623ed.

Requested Coordinator Recovery Action: Establish the authorized configured-root validation route, then resume this same canonical task through Blocked -> Ready -> Starting -> Running and perform one genuine read-only skill_validate attempt.

Preserved Candidate: 7cca88fee05db053e452729fcc094cc8309623ed.

Integration Branch: codex/eliminate-standalone-definition-approval-records-integration-019faeef.

Integration Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/eliminate-standalone-definition-approval-records-integration-019faeef.

Source Mapping: 13997b4db187cac289920d530752c3d74b69ef60 + c817df1735d035a1d7b2ae3bda162400a86d6e2e -> 7cca88fee05db053e452729fcc094cc8309623ed.

Code Review: Fresh independent code review GOOD.

Focused Verification: PASS.

Methodology Review: Blocked solely by the configured-root skill_validate rejection.

Resource Disposition: No source or integration mutation performed; candidate, branch, worktree, review, and verification evidence are preserved.

Safe-to-Resume Assessment: Safe only after the stated unblock condition is satisfied and the normal Blocked -> Ready -> Starting -> Running lifecycle sequence is recorded for this same canonical task.
