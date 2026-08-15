# Require Explicit User Approval for New Infrastructure

Owner: /root/require_explicit_user_approval_for_new_infrastructure

Status: Running

Type: Defect

Priority: High

Provider: file

Work Item ID: require-explicit-user-approval-for-new-infrastructure

Completion: main-branch

## Summary

Require explicit user approval before Dev Architect or `create-architecture` authorizes a new harness, runner, simulator, service, or other material infrastructure.

## Context

During Specialization Examples verification, technical architecture work expanded into a durable browser verifier even though the user's actual requirement was local `file://` page verification. Architecture justification and reviewer acceptance were incorrectly treated as sufficient authority for new infrastructure.

The current sources also need a precise distinction: an original user request can authorize infrastructure when it explicitly names or requires that infrastructure, but an agent must not infer approval from general scope, technical need, implementation convenience, or architecture acceptance.

## Source Evidence

The user explicitly requested this Defect on 2026-08-14 and authorized changes to `skills/create-architecture/SKILL.md` and `agents/roles/dev-activities/dev-architect.role.yaml` with focused tests and required generated projections.

The user directed that approval is satisfied only when the original request explicitly includes the infrastructure or when a later User Action Required answer approves it. Technical justification, architecture acceptance, scope language, or implementation need alone is insufficient.

The current conflict is visible in `skills/create-architecture/SKILL.md` near line 33 and the Dev Architect role decisions: the sources prohibit inferred approval but do not clearly preserve explicit infrastructure authorization contained in the original request.

## Requirements

- Update `skills/create-architecture/SKILL.md` so architecture may authorize new material infrastructure only from explicit user approval.
- Update `agents/roles/dev-activities/dev-architect.role.yaml` with the same authority boundary.
- Define material infrastructure to include a new harness, runner, simulator, service, or an equivalent durable execution facility.
- Treat approval as present when the original user request explicitly includes the exact infrastructure outcome or when a later User Action Required answer explicitly approves it.
- Reject approval inferred only from technical justification, reviewer or architecture acceptance, broad scope language, implementation need, convenience, test coverage goals, or an agent's recommendation.
- When approval is absent, preserve the proposed architecture and route one exact User Action Required question with options and tradeoffs before authorizing infrastructure implementation.
- Preserve ordinary authority for fixtures, helpers, and focused tests that do not introduce material infrastructure.
- Regenerate only mechanically owned role and skill projections through their owning generator.
- Update directly affected design documentation only when the owning generator or a focused freshness check proves it is required.

## Governed Scope Authorization

The user's explicit approval covers these canonical governed definitions:

- `skills/create-architecture/SKILL.md`
- `agents/roles/dev-activities/dev-architect.role.yaml`

It also covers these direct dependent artifacts:

- focused assertions in `scripts/test_bundle_content.py`
- mechanically generated Dev Architect role adapters and skill projections through the owning generator
- directly affected generated or maintained design documentation only when freshness requires it

No other skill definition, agent definition, ordinary fixture, helper, runtime implementation, or infrastructure implementation is approved by this Work Item.

## Acceptance Criteria

- The architecture skill and Dev Architect role use the same explicit-approval rule.
- A test proves that an original request explicitly naming the new infrastructure supplies approval.
- A test proves that a later recorded User Action Required answer supplies approval.
- Negative tests reject technical justification, reviewer acceptance, architecture acceptance, broad scope language, and implementation need when explicit user approval is absent.
- A test proves that ordinary fixtures, helpers, and focused tests remain within normal implementation authority when they do not create material infrastructure.
- Missing approval produces one exact User Action Required route and no infrastructure authorization.
- Canonical sources, generated projections, and directly affected documentation remain fresh and consistent.
- Independent governed-definition and prompt-contract review passes.

## Verification

- Run the focused bundle assertions for architecture and Dev Architect authority.
- Run positive and negative explicit-approval scenarios.
- Run role and skill validation.
- Run owning-generator freshness checks and verify the exact generated manifest.
- Run `git diff --check` for the exact changed paths.
- Obtain independent review of the authority boundary and model-facing approval language.

## Dependencies

None.

## Scheduling Boundary

Provider creation does not authorize execution. While crisis epoch `blocked-crisis-20260813T223935Z` remains active, this Ready Defect must wait until the Dev Backlog Coordinator selects it as the one sole local work-item execution.

User Priority Override: High. This was the next eligible local crisis Work Item after Specialization Examples reached terminal cleanup. It takes precedence over other queued work to prevent further architecture-authority drift. The Starting handoff below records its separate reservation.

## Starting Handoff Evidence

- Transition: `Ready -> Starting`.
- Reserved At: `2026-08-14T21:37:25Z`.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Priority: High, by explicit user override.
- Baseline: `5c2cf1a832500beab322ca6f7d63c9b55a107d03` on configured primary branch `main`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Normalized Objective: Require explicit user approval before architecture authorizes a new harness, runner, simulator, service, or equivalent material infrastructure, while preserving ordinary authority for non-infrastructure fixtures, helpers, and focused tests.
- Intended Root Owner: One Dev Orchestrator execution launched by one canonical visible Codex Work Item task.
- Capacity: Sole local dev-methodology crisis execution. Map Evaluation Contracts remains Ready and unexecuted.
- Coordination Boundary: Claim-free crisis reservation. No claim operation occurred; SOLO supplies local exclusivity.
- Preserved State: Retain the dirty terminology provider bytes, Map draft and post-reset claim evidence, historical Specialization verifier worktree and branch, other preserved candidates, and untracked plans and temporary artifacts.
- Approved Scope: The governed definitions and direct dependent artifacts listed in Governed Scope Authorization. No unrelated skill definition, agent definition, ordinary fixture, helper, runtime implementation, or infrastructure implementation is authorized.
- Required Dispatch: Create one visible Codex task with the exact reference-plus-delta prompt, then launch exactly one nested Dev Orchestrator. Creation does not imply Running.
- Required Acceptance: The nested Dev Orchestrator records `Starting -> Running` claim-free before source mutation.
- Required Runtime Title: `Starting — Require Explicit User Approval For New Infrastructure`.

## Canonical Runtime Assignment

- Assigned At: `2026-08-14T21:39:09Z`.
- Codex Task ID: `01a00236-ec5c-7811-ad56-6877828d2287`.
- Conversation ID: `01a00236-ec5c-7811-ad56-6877828d2287`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Runtime Project: Saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Requested Title: `Starting — Require Explicit User Approval For New Infrastructure`.
- Creation Outcome: Unique direct `threadId` success with no client or pending identity and no retry. The read response truncates display text only.
- Lifecycle Boundary: Provider remains `Starting` until exactly one nested Dev Orchestrator accepts and durably records `Starting -> Running` claim-free.
- Execution Boundary: The visible root launches exactly one nested Dev Orchestrator for this authoritative Work Item and owns its own title and required subagent messaging.

## Evaluation-Contract Scope Decision

### Question for the User

May this Work Item expand its approved scope to include `evals/agent-tests/dev-architect/fixtures/cases.yaml` and `evals/agent-tests/dev-architect/scenarios.yaml`, then run the existing live-model Dev Architect evaluation suite?

### Why User Input Is Required

The accepted candidate needs executable positive and negative evaluation coverage before its evaluation gate can pass. The existing Dev Architect evaluation catalogs are the technically appropriate owners, but the durable Governed Scope Authorization names only focused assertions in `scripts/test_bundle_content.py` and explicitly excludes other ordinary fixtures from this Work Item. The Coordinator cannot silently widen that exact boundary.

### Options and Tradeoffs

- **Expand this Work Item (recommended):** Authorize only the two named evaluation-contract files and the existing live-model Dev Architect suite. This keeps the contract and its executable coverage together, then requires fresh architecture, governed-definition, prompt-contract, and independent verification gates.
- **Create a separate provider-owned Work Item:** Preserve this candidate and create a separate focused evaluation-contract item. This Work Item remains unable to pass its evaluation gate until that dependency is delivered.

### Preserved Evidence And Unattended Boundary

- Transition: `Running -> User Action Required`.
- Recorded At: `2026-08-14T22:30:56Z`.
- Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Preserved Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate: `e658f6d00a779e731098cbd1ea6e698b0104c2af` on branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236` in its clean isolated worktree.
- Preserved Plan: `require-explicit-user-approval-for-new-infrastructure-plan-01a00236.json` with synchronized HTML sibling.
- Delivery State: Nothing integrated or delivered.
- Scope Finding: Candidate R1 coverage uses the two named evaluation-contract files, which remain outside the durable approved scope until the user answers.
- Coordination Boundary: Claim-free crisis transition. No claim operation occurred.
- Required Runtime Title: `Waiting for User — Require Explicit User Approval For New Infrastructure`.
- Unattended Work Boundary: Do not modify, review, run the live-model suite, integrate, deliver, replace the execution, or infer approval until the user answers in the canonical task. Preserve the clean candidate, branch, worktree, plan, and all prior evidence.

## User Answer And Resumption Evidence

- Exact User Clarification: `these files don't need my approval, they are internal test details`.
- Exact Standing-Policy Clarification: `This is an existing policy - I always said you can update the test fixtures, but require approval for the skills agents templates etc that are deployed for use in projects`.
- Policy Classification: Apply approval by deployment role, not by path name alone. Internal test-harness fixtures and evaluation contracts do not require separate approval. Skills, agent definitions, templates, and comparable artifacts deployed for use in projects require approval.
- Classified Internal Test Details: `evals/agent-tests/dev-architect/agents/judge.toml` and `evals/agent-tests/dev-architect/skills/dev-architect-suite-contract/SKILL.md`.
- Transition Sequence: `User Action Required -> Ready -> Starting -> Running`.
- Resumed At: `2026-08-14T22:55:58Z`.
- Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Resumed Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate: `e658f6d00a779e731098cbd1ea6e698b0104c2af` on branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236` in its clean isolated worktree.
- Preserved Plan: `require-explicit-user-approval-for-new-infrastructure-plan-01a00236.json` with synchronized HTML sibling.
- Coordination: Claim-free crisis resumption. Private-worktree correction does not trigger a Resource Claim event.
- Required Runtime Title: `Running — Require Explicit User Approval For New Infrastructure`.
- Next Action: Correct the internal evaluation contract, run the existing live-model Dev Architect suite, repeat fresh review, then run independent verification.

## Crisis Capacity Safe-Stop Reconciliation

- Transition: `Running -> Ready`.
- Recorded At: `2026-08-14T23:08:31Z`.
- Reason: This Work Item self-resumed from the user's valid deployment-role policy clarification while Map Evaluation Contracts already occupied the sole local crisis slot. The Coordinator stopped it at its next safe boundary without treating the capacity violation as candidate failure.
- Preserved Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Preserved Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate: `e658f6d00a779e731098cbd1ea6e698b0104c2af` on branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236`.
- Preserved Dirty Private Worktree: `.worktrees/require-explicit-user-approval-infrastructure-candidate-01a00236` contains exactly three modified tracked files and one untracked evaluation summary: `evals/agent-tests/dev-architect/agents/judge.toml` (5 insertions/1 deletion), `evals/agent-tests/dev-architect/skills/dev-architect-suite-contract/SKILL.md` (5 insertions/1 deletion), `scripts/test_bundle_content.py` (52 insertions), and `evals/agent-tests/run-evidence/summary.json`.
- Preserved User Clarification: Internal test-harness fixtures and evaluation contracts do not require separate approval; deployed skills, agent definitions, templates, and comparable project-consumed artifacts do.
- Evaluation State: No model call and no live-evaluation claim occurred before the stop.
- Preserved Lifecycle Evidence: User-answer/resumption commits `81be0151` and `c916dafe` remain historical evidence.
- Coordination Boundary: Claim-free crisis reconciliation. No claim query or release occurred.
- Required Runtime Title: `Ready — Require Explicit User Approval For New Infrastructure`.
- Unattended Work Boundary: Preserve the dirty private worktree byte-for-byte. Do not correct, stage, commit, clean, review, run the live evaluation, verify, integrate, deliver, replace, or resume until the Coordinator reserves this same canonical execution after the current sole crisis item becomes terminal or truthfully non-active.

## Reconciled Evaluation Crisis Reservation

- Transition: `Ready -> Starting`.
- Reserved At: `2026-08-14T23:23:36Z`.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Baseline: `480cff0ef16e586afa9ca3c6ce1a7ad71088f229` on configured primary branch `main`.
- Capacity Trigger: Map Evaluation Contracts completed and archived, releasing the sole local crisis slot.
- Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Preserved Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate And Worktree: `e658f6d00a779e731098cbd1ea6e698b0104c2af`, branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236`, and the exact dirty private-worktree manifest recorded above.
- Preserved User Policy: Internal test-harness fixtures and evaluation contracts do not require separate approval; deployed skills, agent definitions, templates, and comparable project-consumed artifacts do.
- Authorized Scope: Continue only the preserved internal evaluation-contract correction, existing live-model Dev Architect suite, fresh governed-definition and prompt review, independent verification, integration, and terminal delivery for this Work Item.
- Hard Boundary: Preserve dirty bytes; do not reset or reimplement them. Do not expand into new deployed skill, agent, template, infrastructure, or unrelated evaluation scope.
- Coordination Boundary: Claim-free sole local crisis reservation. No claim operation occurred.
- Required Runtime Title: `Starting — Require Explicit User Approval For New Infrastructure`.
- Required Acceptance: The same Dev Orchestrator records a new claim-free `Starting -> Running` acceptance before dirty-worktree mutation or evaluation resumes.

## Reconciled Running Acceptance

- Transition: `Starting -> Running`.
- Accepted At: `2026-08-14T23:24:39Z`.
- Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Root Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate And Worktree: `e658f6d00a779e731098cbd1ea6e698b0104c2af`, branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236`, and the exact dirty private-worktree manifest recorded above.
- Exact Latest User Answer: `Not just for this run - all runs`.
- User Disclosure Authorization: The user explicitly authorized sending the exact provenance identifier `Martin.Bechard@DevConsult.ca` to live evaluation models for all runs. This standing authorization does not permit unrelated disclosure, logging, or scope expansion.
- Coordination: Claim-free acceptance under the sole local crisis reservation. No Resource Claim event was triggered by lifecycle acceptance or private-worktree mutation.
- Required Runtime Title: `Implementing — Require Explicit User Approval For New Infrastructure`.
- Next Action: Preserve and complete the existing internal evaluation-contract correction, run the authorized existing live-model suite, then repeat fresh review and independent verification.

## Live Evaluation Response-Schema Blocker

- Transition: `Running -> Blocked`.
- Recorded At: `2026-08-14T23:32:57Z`.
- Exact Blocker: The existing live Dev Architect suite fails before every scenario because Codex rejects the coordinator response schema. Keyword `uniqueItems` is unsupported at `claimRelease.eventIds`.
- Evaluation Outcome: `INFRASTRUCTURE_FAILED`; zero scenarios executed and zero Judge results were produced. This is not candidate-failure evidence.
- Recovery Owner: Existing `evals/agent-tests` runner and coordinator response-schema owner through one bounded supporting recovery under this canonical Work Item.
- Unblock Condition: Correct the existing runner/schema compatibility boundary so the coordinator response schema is accepted without weakening uniqueness validation, obtain independent source review and focused regression verification, and prove the live suite reaches scenario execution before retrying this Work Item's evaluation.
- Preserved Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Preserved Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved Candidate And Worktree: `e658f6d00a779e731098cbd1ea6e698b0104c2af`, branch `work-item/require-explicit-user-approval-for-new-infrastructure-01a00236`, three modified tracked files, and untracked `evals/agent-tests/run-evidence/` plus `evals/agent-tests/run-reports/` evidence.
- User-Data Authority: Standing authorization at provider commits `edb15f37` and `83c699bc` remains valid for existing evaluation-suite runs and is unchanged by this blocker.
- Resource State: The live-evaluation claim was released; no claim remains. Crisis recovery continues claim-free.
- Required Runtime Title: `Blocked — Require Explicit User Approval For New Infrastructure`.
- Supporting Recovery Boundary: Diagnose and correct only the existing runner/coordinator response-schema compatibility needed for `claimRelease.eventIds`. Do not create a new harness, runner, simulator, service, response contract, or unrelated infrastructure; do not weaken the semantic uniqueness requirement.
- Safe Resume: Preserve all dirty correction and run evidence. Resume the Work Item only through `Blocked -> Ready -> Starting -> Running` after the supporting recovery passes independent review and focused verification.

## Response-Schema Recovery And Resumption

- Supporting Source Commit: `ae5dfe7b8db9a5e95b4d0ab2aa7f9a5acc99d6da` with parent `3d6c2558eeac54c41dbe6b750bcfbece527078f6`.
- Exact Manifest: `evals/agent-tests/runner.py` and `evals/agent-tests/test_runner.py`.
- Source Mapping: Fast-forward integration preserved the reviewed supporting commit identity on configured branch `main`.
- Source Review: Fresh Dev Code Reviewer returned `PASS` with no findings.
- Independent Verification: Focused schema, exact-one semantic validation, mocked schema-submission reachability, strict-object schema validation, and in-memory compilation passed. Main ran all 160 `test_runner.py` tests successfully.
- Preserved Primary State: The unrelated tracked diff, index entry, 34 untracked paths, and aggregate untracked-content hash were identical before and after integration.
- Live Reachability Proof: `dev-architect:accepted-design` completed with process exit 0, four critical deterministic checks passed, independent Judge disposition `passed`, verified identity bindings, clean batch cleanup, and clean workspace cleanup.
- Live Evidence: `/private/tmp/dev-architect-schema-smoke.mN4OLF/summary.json` with run identity `codex-batch-01-a9de026f1d4c8175dd27dc55a5a12c04`.
- Live Resource: `live-model-evaluation:dev-architect:schema-smoke:01a00236` acquired at event `6b5a9c34-4dcf-41ac-8ea3-db0bb05dc4c4` and released at event `f2423f05-a14f-4e5d-89f0-888425f6fc4e`.
- Support Cleanup: Removed only clean worktree `.worktrees/require-explicit-user-approval-schema-compatibility-01a00236` and its merged branch after ancestry and cleanliness proof.
- Technical Trigger: SATISFIED. Codex accepted the repaired coordinator schema and reached completed scenario and Judge execution without weakening exact-one event-ID validation.
- Transition Sequence: `Blocked -> Ready -> Starting -> Running`.
- Resumed At: `2026-08-15T00:23:01Z`.
- Canonical Task and Conversation: `01a00236-ec5c-7811-ad56-6877828d2287` on host `local`.
- Resumed Dev Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Preserved High Candidate: `e658f6d00a779e731098cbd1ea6e698b0104c2af` and its recorded dirty private worktree remain the only authorized implementation continuation.
- Lifecycle Coordination: Claim-free resumption under the sole local crisis reservation. The separate live-model reachability proof used and released its required timed resource claim.
- Required Runtime Title: `Implementing — Require Explicit User Approval For New Infrastructure`.
- Next Action: Complete the preserved internal evaluation-contract correction, rerun the full existing Dev Architect suite, repeat fresh governed-definition and prompt review, run independent verification, then integrate and deliver.

## Running Acceptance Evidence

- Transition: `Starting -> Running`.
- Accepted At: `2026-08-14T21:40:20Z`.
- Root Orchestrator: `/root/require_explicit_user_approval_for_new_infrastructure`.
- Codex Task ID: `01a00236-ec5c-7811-ad56-6877828d2287`.
- Conversation ID: `01a00236-ec5c-7811-ad56-6877828d2287`.
- Execution Mode: Sole local crisis execution under `blocked-crisis-20260813T223935Z`.
- Coordination: Claim-free acceptance, as reserved by the Starting handoff. No Resource Claim event was triggered.
- Accepted Scope: Governed definitions and direct dependent artifacts listed in Governed Scope Authorization.
- Source Boundary: Preserve all unrelated dirty and untracked state recorded by the Starting handoff.
- Next Action: Dispatch bounded implementation planning to Dev Coder, then obtain Dev Architect plan acceptance before source mutation.
