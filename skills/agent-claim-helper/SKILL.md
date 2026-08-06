---
name: agent-claim-helper
description: Use the common claim-helper operation, input, result, and uncertain-outcome contract through one configured provider.
metadata:
  category: development-practice
---

# Agent Claim Helper

Agent Claim Helper is the provider-neutral interface for claim operations. Agent Claim decides when a claim is required, which scope to request, how to handle conflicts and deadlines, and when to release it. One configured agent-claim-helper-* Provider Skill maps this interface to command-line invocation or MCP tool calls.

This interface does not select a provider, define claim policy, or make an unavailable provider selectable.

## Operation Contract

Provider Skills preserve these semantic input names through the naming convention of their invocation mechanism. `repository` is the absolute project root. A scope is exactly one work-item, path-domain, or resource shape; Agent Claim selects the shape.

| Operation | Required inputs | Optional inputs |
|---|---|---|
| Read Claim Status | repository | none |
| Acquire Claim | repository, claim_id, agent, task, root_task_id, and exactly one scope | parent_claim_id; branch, base, and worktree_path for isolated-checkout creation |
| Extend Claim | repository, claim_id, and net-new path-domain or resource scope | scope_reason when the path-domain requires it; complete resource timing fields for resource scope |
| Extend Claim Deadline | repository, claim_id, requested_hard_stop_duration_seconds, extension_evidence | none |
| Heartbeat Claim | repository, claim_id | none |
| Release Claim | repository, claim_id | disposition and blocker_reference only as required by Agent Claim for a work-item release |
| Reset Claim Registry | repository | none |
| Maintain Claim Journal | repository | hot_days, default 2 |
| Report Claim Contention | repository | since, default 2d |

An Acquire Claim scope is exactly one of: `work_item_id` with `activity`; one or more `files` or `trees`; `project_files`; `backlog`; `all_files`; or one `resource`. Tree, project-files, backlog, and all-files scopes include `scope_reason`. Resource scope includes `resource_class`, `resource_id`, `expected_duration_seconds`, and `requested_hard_stop_duration_seconds`. Extend Claim accepts the same path-domain and resource shapes but never a work-item scope and applies only their net-new portion.

The configured provider performs exactly the requested operation. It does not switch to a sibling provider after a rejection or failure.

## Structured Outcomes

Except for the explicit human-readable report mode described by a Provider Skill, every completed invocation returns one structured result with `schema_version: 2` and `outcome`. The following canonical outcomes and minimum result fields are exact.

| Operation | Canonical outcomes | Required result fields beyond schema_version and outcome |
|---|---|---|
| Read Claim Status | STATUS | registry, claims |
| Acquire Claim | SHARED_CHECKOUT_ACQUIRED, ISOLATED_CHECKOUT_ACQUIRED, CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, CLAIM_ID_EXISTS, INVALID_SCOPE, INVALID_WORK_ITEM_SCOPE, INVALID_DEADLINE_POLICY, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, WORKTREE_CREATE_FAILED | every result has journal; acquisition success has claim, registry, target; CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED has conflicting_claim_ids, overlaps; SHARED_CHECKOUT_REQUIRED has reason, message, requested_scopes; CLAIM_ID_EXISTS has claim_id; INVALID_SCOPE has message, offending_scope, replacement, rejection; INVALID_WORK_ITEM_SCOPE and INVALID_DEADLINE_POLICY have message, field, rejection; INVALID_IDENTIFIER has field, message; INVALID_WORKTREE_PATH has expected_worktree, provided_worktree, message; WORKTREE_ROOT_NOT_IGNORED has worktree_root, required_ignore_pattern, message; WORKTREE_CREATE_FAILED has message |
| Extend Claim | EXTENDED, CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, CLAIM_NOT_FOUND, INVALID_SCOPE, INVALID_WORK_ITEM_SCOPE, INVALID_DEADLINE_POLICY | every result has journal; EXTENDED has claim, added_scope, already_owned_scope; CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED has conflicting_claim_ids, overlaps, added_scope, already_owned_scope; SHARED_CHECKOUT_REQUIRED has reason, message, requested_scopes; CLAIM_NOT_FOUND has claim_id; INVALID_SCOPE has message, offending_scope, replacement, rejection; INVALID_WORK_ITEM_SCOPE and INVALID_DEADLINE_POLICY have message, field, rejection |
| Extend Claim Deadline | DEADLINE_EXTENDED, CLAIM_NOT_FOUND, INVALID_DEADLINE_EXTENSION | journal; DEADLINE_EXTENDED has claim, deadline_extension; CLAIM_NOT_FOUND has claim_id; INVALID_DEADLINE_EXTENSION has field, rejection, message |
| Heartbeat Claim | HEARTBEAT, CLAIM_NOT_FOUND | journal; HEARTBEAT has claim; CLAIM_NOT_FOUND has claim_id |
| Release Claim | RELEASED, CLAIM_NOT_FOUND, INVALID_WORK_ITEM_RELEASE, RELEASE_ERROR | journal; RELEASED has claim and work-item disposition fields when applicable; CLAIM_NOT_FOUND has claim_id; INVALID_WORK_ITEM_RELEASE has field, rejection, message; RELEASE_ERROR has reason, message, claim_id |
| Reset Claim Registry | RESET | journal, registry, claims |
| Maintain Claim Journal | JOURNAL_MAINTAINED, INVALID_HOT_DAYS, JOURNAL_MAINTENANCE_FAILED | hot_days and archived for JOURNAL_MAINTAINED; hot_days for INVALID_HOT_DAYS; message and archived for JOURNAL_MAINTENANCE_FAILED |
| Report Claim Contention | REPORT, INVALID_SINCE | REPORT has window, event_count, metrics, work_items, coverage_gaps; INVALID_SINCE has message |

`REPORT` uses report `schema_version: 2`. Its `work_items` value has `schema_version: 1`, `items`, and `diagnostics`; diagnostics contains `missing_release_event_ids`, `release_without_acquisition_event_ids`, `contradictory_event_ids`, and `historical_non_work_item_event_ids`.

## Legacy Event Normalization

The current result table lists only outcomes reachable from a current provider invocation. Historical journals may contain these legacy event outcomes; report and maintenance operations normalize them without presenting the legacy vocabulary as current operation results.

| Legacy event outcome | Canonical normalized outcome |
|---|---|
| PRIMARY | SHARED_CHECKOUT_ACQUIRED |
| ISOLATE | ISOLATED_CHECKOUT_ACQUIRED |
| RECOVER | DIRTY_CHECKOUT_RECOVERY_ACQUIRED |
| WAIT | CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED |
| PRIMARY_REQUIRED | SHARED_CHECKOUT_REQUIRED |
| ISOLATE_REQUIRED | ISOLATED_CHECKOUT_SETUP_REQUIRED |
| RECOVERY_REQUIRED | DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED |

A historical `PRIMARY_REQUIRED` event with explicit `shared_checkout_claimed: true` normalizes to `SHARED_CHECKOUT_RELEASE_REQUIRED`. When that evidence is absent, reporting preserves `PRIMARY_REQUIRED` and records a coverage gap instead of inventing an ownership state.

Work-item claim objects preserve `work_item_id`, `activity`, `claim_id`, `incarnation_id`, `agent`, `root_task_id`, `claimed_at`, `heartbeat`, and `acquisition_outcome`. Each `work_items.items` entry preserves `work_item_id` and `segments`. Every report segment contains exactly `claim_id`, `incarnation_id`, `owner`, `root_task_id`, `activity`, `acquired_at`, `released_at`, `disposition`, `blocker_reference`, `duration_seconds`, `open`, `live`, `acquisition_event_id`, and `release_event_id`. Validation failures preserve the live registry.

Read the complete structured result before applying Agent Claim policy. Do not decide from a process exit code, tool-call status, or provider connection state alone.

## Reconcile an Uncertain Outcome

When a mutating invocation stops after dispatch and its result is unknown, do not repeat it. Use the same configured Provider Skill to run Read Claim Status for the same repository. Reconcile the reported claim state, then continue from that state.

If the configured provider cannot return status, ask Project Configurator to restore or replace the configured helper. Do not use a sibling provider to guess whether the mutation completed.

## Provider Realization Contract

Every agent-claim-helper-* Provider Skill realizes all operations, preserves every common input and structured result meaning, and states its provider-specific availability boundary. A Provider Skill may define command flags, MCP tool fields, result envelopes, or startup checks. It must not redefine Agent Claim policy or imply that interface conformance proves runtime availability.
