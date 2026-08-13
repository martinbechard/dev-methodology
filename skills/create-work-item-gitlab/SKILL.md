---
name: create-work-item-gitlab
description: Create one authoritative GitLab issue with duplicate prevention, typed requirements, provider-native relationships, and verified observed identity. Use when the effective work-item provider is GitLab or the user explicitly requests one GitLab issue without changing the project default.
metadata:
  category: development-practice
---

# Create Work Item GitLab

The Work-item content is the Work-item authority and is stored according to the Persistence provider's specific format. Create one independently actionable GitLab issue without creating a shadow queue.

## Work Item ID

- Represent Work Item ID as the observed GitLab instance, namespace, project, and issue IID. Resolve and collision-check it only through GitLab provider operations; generic lifecycle callers pass it unchanged.
- Keep the issue URL as diagnostic location evidence. Native state changes and terminal organization preserve the same Work Item ID.

## Authority And Inputs

- Use the configured GitLab instance, namespace, and project when GitLab is the effective provider. A one-item explicit request may select GitLab for that item but does not rewrite the project default.
- Resolve the title, type, summary, requirements, acceptance criteria, dependencies, verification expectations, source evidence, labels, milestone or project fields, relationships, and initial ownership evidence.
- Require an authenticated GitLab issue interface with project authority and every capability needed by the requested operation. Return BLOCKED before mutation when authentication, project authority, permission, or a required capability is unavailable.
- Use GitLab provider reads and mutations as the sole issue authority. Do not create repository backlog files, cached issue mirrors, GitHub issues, or generic external records as a fallback.
- Keep sensitive, private, proprietary, credential, or company-internal evidence out of an issue whose visibility is unsuitable. An explicitly requested export is non-authoritative and must identify itself as an export.

## Create Work Item

1. Search open and recently closed issues in the observed target project for the same durable outcome. Read plausible matches and compare their title, content, labels, milestone, relationships, and state.
2. When one durable duplicate exists, do not create another issue. Return the observed GitLab instance, namespace, project, issue internal identifier, URL, state, and ownership evidence for the existing item. When several plausible matches exist, return BLOCKED with the candidates rather than guessing.
3. Create exactly one issue for one independently actionable outcome. Preserve the normalized type, summary, requirements, acceptance criteria, dependencies, verification expectations, and source evidence in the issue content or configured project fields.
4. Apply only configured labels, milestone or project fields, assignees, and provider-native relationships. Do not alter unrelated project configuration or records.
5. Read the issue back from GitLab after creation and after each related mutation. Verify the observed namespace, project, issue internal identifier, URL, state, labels, assignees, relationships, milestone or project fields, and updated content.
6. If creation succeeds but a later mutation or verification fails, preserve the observed issue identity and return BLOCKED with the partial-mutation evidence and exact reconciliation action. Never retry by creating a second issue or writing a fallback record.

## Delivery Boundary

- The GitLab issue stores the Work-item content. A branch, commit, or merge request is delivery evidence, not the Work-item identifier.
- Issue creation does not prove delivery completion. Use merge request, approval, pipeline, and merge terminology accurately when later evidence is recorded.
- When delivery is hosted somewhere other than GitLab, record that host and its provider-accurate delivery reference without changing the GitLab work-item provider.

## Result

Return the selected provider, Work Item ID, observed GitLab instance, namespace, project, issue IID, diagnostic URL, native state, canonical lifecycle status, type, labels, assignees, milestone or project fields, relationships, ownership evidence, duplicate decision, and next runnable action or blocker.
