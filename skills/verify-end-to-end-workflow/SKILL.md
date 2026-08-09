---
name: verify-end-to-end-workflow
description: Verify complete user or system workflows across real boundaries without assuming a particular automation framework. Use for end-to-end tests, acceptance workflows, authenticated or stateful journeys, runtime coordination, visible failure states, or reproducible system-level evidence.
metadata:
  category: development-practice
---

# Verify End To End Workflow

Prove the complete workflow with explicit environment ownership and observable assertions.

## Workflow

1. Identify the authoritative workflow, actors, starting state, dependencies, and expected result.
2. Route specialized automation guidance when the project provides it.
3. Make service, process, session, identity, data, and cleanup ownership explicit.
4. Exercise success and material failure paths through real public boundaries.
5. Prefer stable user-visible or contract-level observations over timing assumptions.
6. Capture reproducible steps, assertions, runtime errors, and diagnostic artifacts.
7. Distinguish product failures from environment, identity, data, or runtime setup blockers.

## Resource Coordination

Applicable project instructions own resource-coordination selection. They load the selected
procedure, if any. Apply the loaded resource-coordination procedure when its event contract
requires protection during verification. Preserve the complete behavior and evidence that the
loaded procedure requires. When applicable project instructions select none and load no
resource-coordination procedure, perform no claim procedure and no claim-specific evidence
handling. In that none-selected case, do not discover, acquire, heartbeat, or release claims.

## Evidence Handoff And Commit Authority

Verify End To End Workflow owns evidence capture and the verifier handoff. It does not own delivery integration, publication, or provider lifecycle mutation.

Include coordination evidence only when the loaded procedure requires it. In the none-selected
case, omit claim-specific fields, placeholders, and not-applicable results.

- Only the delivery owner applies the effective Commit-selected skill.
- For main-branch, the delivery owner applies deliver-work-item-main-branch.
- For feature-branch, the delivery owner applies deliver-work-item-feature-branch.
- Evidence-only or no mutation authority is terminal: return the evidence handoff without applying a Commit skill or creating a commit.
- When repository delivery is required and Commit is UNSET, ask for the Commit selection and stop before delivery.
- Do not create a commit outside the effective Commit-selected skill.

## Evidence Delivery Decision Table

Apply the evidence-only or no-mutation row before evaluating Commit. A terminal evidence handoff does not become a delivery request merely because Commit is UNSET or selected.

| Request authority | Commit selection | Result |
| --- | --- | --- |
| Evidence-only or no mutation authority | UNSET | Return the terminal evidence handoff; apply no Commit workflow and create no commit. |
| Evidence-only or no mutation authority | main-branch or feature-branch | Return the terminal evidence handoff; apply no Commit workflow and create no commit. |
| Repository delivery required | UNSET | Ask for Commit selection and stop before delivery; create no commit. |
| Repository delivery required | main-branch | Return evidence to the delivery owner for deliver-work-item-main-branch. |
| Repository delivery required | feature-branch | Return evidence to the delivery owner for deliver-work-item-feature-branch. |

Return the commands, results, diagnostic artifacts, blockers, cleanup state, and applicable worktree status as reproducible evidence.

## Review Evidence

Read references/review-checklist-verify-end-to-end-workflow.md during verification or review.
