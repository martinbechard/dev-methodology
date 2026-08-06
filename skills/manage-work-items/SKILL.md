---
name: manage-work-items
description: Define the provider-neutral contract for work-item inventory, lifecycle transitions, completion reconciliation, recovery, and reporting. Use when a lifecycle consumer or management provider needs the shared work-item identity, lifecycle, result, and procedure vocabulary.
metadata:
  category: development-practice
---

# Manage Work Items

Manage Work Items is the Interface Skill for durable work-item management. Lifecycle
consumers use this contract without naming a provider implementation. Each
Persistence-selected Provider Skill preserves this vocabulary while it applies its native
authority, storage, mutation, recovery, and reporting rules.

This skill defines no provider selection or provider operation. Applicable project guidance
selects exactly one management provider. The selected Provider Skill owns every provider read
and mutation and must not fall back to a sibling provider or a shadow record.

## Work Item Identity

- Treat Work Item ID as one opaque, stable identifier owned and resolved by the selected
  provider.
- Pass Work Item ID unchanged through inventory, transition, reconciliation, recovery, and
  reporting. Generic consumers must not parse provider paths, repository identities, issue
  numbers, keys, or URLs from it.
- Treat a provider path or URL as diagnostic location evidence. Moving, closing, reopening, or
  archiving the provider record does not create a new logical Work Item ID.
- Keep provider lifecycle authoritative. Runtime task state, conversation titles, branches,
  commits, pull requests, merge requests, and claim records are supporting evidence only.

## Lifecycle Definitions

Use one canonical lifecycle vocabulary across providers:

- READY: The item is authorized, complete enough to dispatch, and has no unmet prerequisite.
- STARTING: The item has a durable dispatch reservation and awaits accepted execution ownership.
- RUNNING: The provider records accepted execution ownership and current execution evidence.
- STALLED: Progress has stopped, but the exact cause or unblock condition remains unknown.
- BLOCKED: A known preventing cause has an owner, evidence, and an observable unblock condition.
- USER_ACTION_REQUIRED: One genuine user decision, authority grant, value judgment, or user-held
  fact is required.
- HOLDING: Authorized direction intentionally defers the item without an immediate user question.
- AWAITING_REVIEW: Verified feature-branch publication exists, but review, checks, merge, or main
  observation remains incomplete.
- COMPLETED: The selected completion contract and provider terminal update are both observed.
- FAILED: Delivery ended without satisfying completion and the provider records terminal failure
  evidence.
- ABANDONED: Authorized direction ends the work without delivery and preserves terminal evidence.

Do not infer a canonical lifecycle solely from a provider-native open or closed value. Do not
infer completion from silence, a stopped task, a clean worktree, a commit, publication, approval,
or merge evidence alone.

## Result Vocabulary

Return results with these meanings:

- READY: The requested management procedure completed and its provider result was read back or
  otherwise verified.
- BLOCKED: The procedure cannot continue safely. Return the provider, Work Item ID when known,
  failed boundary, observed state, preserved evidence, blocker owner, and next authorized action.
- AWAITING_REVIEW: Completion remains nonterminal for the same feature-branch delivery identity.
  Preserve its accepted commit, publication, review, check, merge, and recovery evidence.
- COMPLETED, FAILED, and ABANDONED: These are provider lifecycle outcomes. Return one only after
  the selected provider durably records and verifies that terminal state.

Keep procedure success distinct from lifecycle READY. A successful transition can return result
READY while the provider lifecycle is STARTING, RUNNING, BLOCKED, USER_ACTION_REQUIRED, HOLDING,
or AWAITING_REVIEW.

Every result identifies the selected provider, requested procedure, Work Item ID when known,
observed canonical lifecycle, provider-native state or location evidence when applicable,
authorized mutations, verification evidence, and next action. An unsupported selected provider
returns BLOCKED with truthful zero-mutation evidence and no fallback.

## Inventory Work Items

Read the selected provider's authoritative collection. Resolve requested filters and identities
through that provider, map observed records to the canonical lifecycle and shared result fields,
and report invalid, duplicate, ambiguous, or provider-mismatched records without guessing.

## Transition Work Item

Apply one caller-authorized lifecycle transition to the exact Work Item ID. Verify the current
provider state permits the transition, preserve unrelated provider data, record the required
identity and lifecycle evidence, and read the durable provider result back before returning.
Never combine two lifecycle transitions into one inferred operation.

## Reconcile Work Item Completion

Keep delivery completion separate from provider completion. Apply a terminal provider update only
after the selected completion process returns disposition READY with its required review, check,
delivery, merge when applicable, main-observation, and triggered resource-coordination evidence.
Read the provider result back before returning lifecycle COMPLETED. If the terminal update fails,
preserve accepted delivery evidence and reconcile only the pending provider operation.

## Recover Work Item

Reconcile ambiguous, partial, interrupted, stale, or contradictory provider state from observed
provider and immutable delivery evidence. Do not repeat an ambiguous mutation. Preserve the same
Work Item ID and delivery identity, retry only a missing authorized operation, and return BLOCKED
when safe reconciliation cannot continue.

## Report Work Items

Return the selected provider, opaque Work Item ID, observed canonical lifecycle, provider-native
state and diagnostic location when applicable, ownership, dependencies, delivery and recovery
evidence, verified mutations, next runnable action, and any blocker or reconciliation requirement.

## Provider Realization Contract

Every manage-work-items-* Provider Skill must expose the five public procedure headings in this
Interface Skill and preserve every shared member meaning. A provider may add native fields,
authority rules, supported operations, or stricter evidence requirements. It must not redefine a
shared lifecycle state, parse another provider's identity, select Persistence, or fall back to a
sibling provider.
