---
name: deliver-work-item
description: Deliver an accepted work item through the effective Commit-selected provider using one provider-neutral input, result, and evidence contract. Use when Dev Orchestrator must deliver an accepted change after independent review and verification.
metadata:
  category: development-practice
---

# Deliver Work Item

Deliver Work Item is the provider-neutral delivery contract between an accepted change and the Commit-selected Provider Skill. The interface keeps the consumer stable while project guidance selects the delivery implementation.

## Accepted Commit Input

The caller supplies one complete accepted input before delivery:

- Opaque Work Item ID and provider selector.
- Already-resolved Commit provider, effective Commit selector, configured target branch, repository, remote or host when required, and delivery authority.
- Accepted source commit, source branch, worktree, exact changed paths, and clean-worktree evidence.
- Fresh independent review result and the source checks accepted for the commit.
- Smallest credible delivery verification and any required local or remote observation.

The accepted input contains provider-neutral facts. Provider-specific integration, publication, review, merge, and observation details remain inside the selected provider.

The caller resolves the Commit provider before invoking this interface. If Commit is UNSET, return BLOCKED without selecting a default.

## Deliver Work Item

1. Receive the already-resolved Commit provider and confirm that it matches the effective Commit selector.
2. Give the provider the complete accepted commit input.
3. Require the provider to consume but never author or amend the accepted source change. The provider must not modify the accepted commit.
4. Require the provider to preserve one delivery identity across pending gates, accepted corrections, retries, and final observation.
5. Return the provider result and the evidence required for that result.

This interface must not select a provider. It also must not mutate Persistence or dispatch a provider manager. The owning orchestrator applies the prepared Persistence handoff only after it evaluates the returned delivery result.

## Delivery Results

Every provider returns exactly one of READY, AWAITING_REVIEW, or BLOCKED, subject to its documented result refinement.

| Result | Shared meaning |
| --- | --- |
| READY | Delivery proof is complete. The result includes the prepared terminal Persistence handoff, or task-local COMPLETED evidence for provider none. |
| AWAITING_REVIEW | A valid delivery identity exists, but a required review, check, dependency, merge, or final observation remains pending. The result includes the prepared nonterminal Persistence handoff when a provider is selected. |
| BLOCKED | A concrete failure, missing authority, ownership conflict, contradictory state, or missing required evidence prevents safe delivery. The result preserves the accepted commit and names one next action. |

A provider may support only the states that its delivery process can truthfully produce. It must preserve the shared meaning of every state that it returns.

## Delivery Evidence

Return state-keyed delivery evidence that includes:

- Work Item ID, provider selector, effective Commit selector, accepted source commit, exact changed paths, review evidence, and accepted source checks.
- Delivery identity and the provider-specific branch, integration, publication, merge, main-observation, or clean-state facts required for the returned state.
- Completed delivery checks, explicit omissions, residual risk, and applicable claim results.
- The exact pending gate or blocker for AWAITING_REVIEW or BLOCKED.
- A prepared Persistence handoff that names the requested lifecycle update and terminal or nonterminal evidence when a provider is selected.
- Task-local AWAITING_REVIEW or COMPLETED evidence when provider none applies.

Delivery evidence never proves that a separate provider lifecycle update succeeded. The owning orchestrator reconciles that update after this procedure returns.

## Provider Contract

Each Provider Skill:

- exposes the Deliver Work Item procedure with the accepted input, result meaning, and evidence fields in this interface;
- documents any narrower result set without changing the meaning of a supported result;
- owns only its provider-specific delivery procedure and observations;
- consumes the accepted source change without modifying it and preserves the delivery identity; and
- returns the prepared Persistence handoff without selecting or mutating Persistence.

Project Commit routing selects one provider independently from this interface. Provider lifecycle closure remains a separate Persistence responsibility.
