---
name: create-work-item
description: Create one authoritative work item through the effective Persistence provider while preserving provider-owned identity, duplicate detection, verification, and failure evidence.
metadata:
  category: development-practice
---

# Create Work Item

Create Work Item is the provider-neutral contract for creating one durable work item. The effective Persistence selection supplies one exact provider implementation without changing this shared input, identity, procedure, or result vocabulary.

## Work Item Identity

- Treat Work Item ID as one opaque provider-owned identifier.
- Let the selected provider create, resolve, collision-check, and verify the identifier.
- Pass Work Item ID unchanged across generic callers. Do not parse it or replace it with a path, URL, branch, commit, pull request, or merge request.
- Keep a provider path or URL as diagnostic location evidence when the selected provider supplies one.

## Inputs

Resolve the effective Persistence provider and one complete work-item description. The description includes the type, title, summary and context, requirements, acceptance criteria, dependencies, verification expectations, source evidence, requested lifecycle state, ownership evidence, and authorized provider-native fields or relationships that apply.

Preserve private, proprietary, sensitive, credential, PII, and company-internal information at a visibility appropriate for the selected provider. Do not infer provider selection from repository files, remotes, templates, installed tools, authenticated sessions, existing work items, or hosting metadata.

## Create Work Item

1. Resolve the effective Persistence selection from applicable project guidance or an explicit one-item provider request.
2. When Persistence is UNSET, ask for the provider decision before durable mutation. When it is none, return BLOCKED because no durable provider exists.
3. Normalize one complete, independently actionable work-item description without replacing provider-native terminology or identifiers.
4. Apply the exact selected create-work-item provider implementation. Do not call a different provider as a fallback.
5. Let the provider own duplicate detection, creation authority, mutation, partial-mutation recovery, and read-after-write verification.
6. Return the provider's observed result without manufacturing success, an identifier, a location, or lifecycle evidence.

## Result

Return CREATED, EXISTING, or BLOCKED with the selected provider, Work Item ID or none, diagnostic location when one exists, observed provider state, lifecycle status, type, ownership and relationship evidence, source evidence, duplicate decision, mutation evidence, and next action or blocker.

CREATED and EXISTING require provider-observed identity and state. BLOCKED names the failed authority, capability, ambiguity, or verification boundary and preserves any observed partial mutation so a later provider operation can reconcile it without creating a duplicate.

## Provider Boundary

Provider implementations retain their native authority, identifiers, duplicate searches, supported lifecycle values, atomicity, partial-mutation recovery, verification, unsupported-operation results, and no-fallback rules. The interface does not make one provider depend on another provider and does not make an unsupported provider appear implemented.
