---
name: create-github-work-item
description: Create one authoritative GitHub issue after provider-backed duplicate detection. Use when the effective work-item provider is github or an explicit one-item request selects GitHub issue creation.
metadata:
  category: development-practice
---

# Create GitHub Work Item

Create one independently actionable GitHub issue. The GitHub provider record is the sole durable work-item authority.

## Inputs And Authority

- Resolve the repository owner and name, item type, title, summary and context, requirements, acceptance criteria, dependencies, verification expectations, source evidence, requested labels, relationships, and initial ownership evidence.
- Use this skill when applicable project guidance selects provider github or an explicit one-item request selects GitHub. A task override does not silently change the project default.
- Require an authenticated GitHub provider interface with repository read and issue mutation capability. Return BLOCKED when authentication, repository authority, a required capability, or mutation permission is unavailable.
- Keep private, proprietary, sensitive, credential, PII, or company-internal evidence out of a provider record whose visibility is unsuitable.

## Duplicate Detection

1. Read the target repository through the provider and confirm its observed identity before searching or mutating.
2. Search open and recently closed issues using the durable outcome, distinctive title terms, source reference, and known relationship references.
3. Read plausible matches rather than relying on search snippets. Compare their requirements, acceptance criteria, dependencies, and source evidence.
4. When one issue represents the same durable work, do not create another. Return the observed existing issue and state, and identify any authorized management update that remains.
5. When several plausible matches cannot be distinguished safely, return BLOCKED with their issue references instead of guessing or creating a duplicate.

## Creation

1. Normalize one complete issue body with the work type, summary and context, requirements, acceptance criteria, dependencies, verification expectations, source evidence, and initial lifecycle status READY.
2. Use provider-native issue links or task-list relationships when repository convention supports them. Preserve GitHub issue terminology.
3. Apply only repository-supported labels, assignees, milestone or project fields, and relationships that the request or configured convention authorizes. Do not invent a new taxonomy as a side effect.
4. Create the issue through the GitHub provider interface.
5. Re-read the created issue through the provider. Verify the observed repository, issue number, URL, native open or closed state, title, body, labels, assignees, milestone or project fields, and relationships against the requested content.

## Partial Mutation And Recovery

- Treat a timeout, disconnect, or ambiguous create response as a possibly completed mutation. Search and read the provider state before retrying; never retry creation blindly.
- If the issue exists but a follow-up label, assignment, relationship, or body update failed, preserve its identity, record the observed partial state, and retry only the missing authorized mutation.
- Return BLOCKED when required content cannot be verified or corrected. Include the issue reference and exact mismatch so management can reconcile it without creating a second issue.

## Boundaries

- Do not create repository backlog files, cached issue mirrors, or fallback local queues on success, provider failure, authentication failure, permission denial, or partial mutation.
- Do not create a pull request or treat a pull request as the work-item identifier.
- Do not close, reopen, claim, resume, block, fail, abandon, or complete an existing issue; those operations belong to manage-github-work-items.
- Do not infer provider github from a remote, installed tool, existing issue, template, or hosting account.

## Result

Return CREATED or EXISTING, the observed repository, canonical work-item identifier, issue number and URL, native state, lifecycle status, type, labels, assignees, relationships, source evidence, and next action. Return BLOCKED with the failed provider boundary and observed remote state when creation cannot finish safely.
