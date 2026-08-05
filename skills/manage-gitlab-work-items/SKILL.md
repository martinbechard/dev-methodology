---
name: manage-gitlab-work-items
description: Manage authoritative GitLab issues through lookup, ownership, lifecycle, dependency, recovery, and terminal updates with verified provider evidence. Use when the effective work-item provider is GitLab or the user explicitly requests management of identified GitLab issues without changing the project default.
metadata:
  category: development-practice
---

# Manage GitLab Work Items

Manage GitLab issue state while keeping provider lifecycle and delivery completion distinct.

## Work Item ID

- Accept the GitLab Work Item ID as one opaque input. This provider resolves it to the observed instance, namespace, project, and issue IID, checks collisions through GitLab, and reports the URL only as diagnostic location evidence.
- Preserve the same Work Item ID across native state changes and terminal organization. Generic callers must not parse its provider-specific components.

Acquire the exact opaque Work Item ID before any work or provider mutation. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. Use blocked only with its bounded blocker reference. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The provider remains the lifecycle authority.

## Authority And Lookup

- Use the configured GitLab instance, namespace, and project when GitLab is the effective provider. A one-item explicit request may select GitLab for that item but does not rewrite the project default.
- Require an authenticated GitLab issue interface with project authority and every capability needed by the requested operation. Return BLOCKED without mutation when authentication, project authority, permission, or a required capability is unavailable.
- Use GitLab provider reads and mutations as the sole issue authority. Do not read from or write repository backlog files, cached issue mirrors, GitHub issues, or generic external records as a fallback.
- Resolve each item from its Work Item ID to the observed GitLab instance, namespace, project, and issue IID. Treat the issue URL as diagnostic location evidence; a branch, commit, or merge request never replaces that identity.
- Keep sensitive, private, proprietary, credential, or company-internal evidence out of an issue whose visibility is unsuitable. An explicitly requested export is non-authoritative and must identify itself as an export.

## Inventory Work Items

- Inventory or retrieve issues using provider-native filters and return observed state rather than inferred task state.

Report ambiguous matches and their observed identities instead of guessing which issue the caller intended.

## Transition Work Item

- Assign or unassign ownership, record the canonical task identifier and material phase, and update only configured labels, milestone or project fields, notes, and relationships.
- Map GitLab native state to READY, RUNNING, BLOCKED, USER_ACTION_REQUIRED, HOLDING, AWAITING_REVIEW, COMPLETED, FAILED, or ABANDONED without treating a native open or closed state as sufficient lifecycle evidence.
- Record dependencies and blocking relationships with GitLab-native links, related issues, notes, or configured project fields. Preserve the exact blocker, next-action owner, recovery evidence, and bounded retry state.
- Record branch, commit, merge-request, approval, pipeline, merge, review, check, main-observation, and enabled resource-coordination release evidence using GitLab terminology and provider-supported history.
- When delivery is hosted somewhere other than GitLab, record that host and its provider-accurate delivery reference without changing the GitLab work-item provider.
- Read the issue back after every mutation. Verify the observed namespace, project, issue internal identifier, URL, state, labels, assignees, relationships, milestone or project fields, and updated content.

## Reconcile Work Item Completion

1. Keep issue completion independent from delivery completion. Merge-request publication, approval, a successful pipeline, a closed merge request, or a merge action is intermediate evidence unless the configured completion contract is fully satisfied.
2. Close an issue only after completion disposition READY and the configured review, check, merge when applicable, main-observation, and any enabled resource-coordination release evidence are all present.
3. Apply the provider-native terminal state, labels, assignees, relationships, milestone or project fields, notes, and lifecycle evidence required by the authorized transition.
4. Read the terminal issue back. Verify the observed namespace, project, issue internal identifier, URL, state, labels, assignees, relationships, milestone or project fields, and updated content.
5. Only after the terminal update is observed may the result return terminal evidence and lifecycle COMPLETED.
6. If the provider terminal update fails after completion disposition READY, preserve the READY disposition and accepted delivery evidence, apply the delivery-mode recovery lifecycle, and reconcile only the pending GitLab update without rerunning valid delivery work.

## Recover Work Item

- When a mutation partially succeeds or observed state contradicts the requested transition, preserve the observed issue and delivery evidence and choose the recovery lifecycle from the effective completion mode. For feature-branch delivery, preserve lifecycle AWAITING_REVIEW for the same delivery identity. For direct-main delivery, preserve lifecycle RUNNING. Record lifecycle BLOCKED when safe reconciliation cannot continue. Never unconditionally reset lifecycle to RUNNING. Return the exact reconciliation action. Do not repeat an ambiguous mutation or create a fallback record.
- Reopen only when authorized recovery or correction requires a nonterminal lifecycle state. Preserve prior terminal and delivery evidence in GitLab history.
- Reopen, unblock, or resume from the provider record and accepted delivery evidence rather than inferring success from a task title, stopped task, branch, or merge-request state alone.

## Report Work Items

Return the selected provider, Work Item ID, observed GitLab instance, namespace, project, issue IID, diagnostic URL, native state, canonical lifecycle status, labels, assignees, relationships, milestone or project fields, delivery and recovery evidence, mutations verified from GitLab, next runnable action, and any blocker or reconciliation requirement.
