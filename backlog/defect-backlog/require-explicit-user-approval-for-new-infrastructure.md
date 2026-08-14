# Require Explicit User Approval for New Infrastructure

Owner: Unowned

Status: Starting

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
