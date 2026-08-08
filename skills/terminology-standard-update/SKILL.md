---
name: terminology-standard-update
description: Create or update terminology.md with positive-first preferred terms and add avoided-term reinforcement only when observed usage provides evidence for it.
metadata:
  category: documentation-methodology
---

# Terminology Standard Update

Create or update a Terminology Standard without turning it into an exhaustive synonym blacklist. Apply terminology-standard for artifact discovery, precedence, entry format, and application boundaries.

## Scope Decision

Use the project terminology.md by default for a concept specific to one project. Update the shared user standard only when the user explicitly selects shared scope and the preference is intended to apply across projects.

Invoke terminology-standard's Load Terminology Standards operation for both scopes before mutation. A PRESENT or conclusively ABSENT scope is available for the decision. If either requested scope is UNAVAILABLE, return TERMINOLOGY STANDARD UPDATE: BLOCKED with the unavailable scope and required capability or owner remediation, and make no mutation. Shared user updates therefore require supported shared-scope access as well as the user's explicit scope selection.

Update only the selected scope. Do not copy all shared entries into the project artifact.

## Update Workflow

1. Identify the concept, preferred term, definition, intended scope, and source of authority.
2. Load both scopes and stop without mutation when either scope is UNAVAILABLE.
3. Check both standards for an existing entry, overlap, or semantic conflict.
4. Create or revise one positive preferred-term entry with a precise definition.
5. Add Use for or Examples only when they clarify a real boundary.
6. Omit Avoid for the initial entry unless retained evidence already proves persistent biased substitution.
7. Add or extend Avoid only when a review, correction history, or supplied artifact shows repeated use of the nonpreferred term after the preferred concept was available, or shows a persistent misleading metaphor that the definition alone did not correct.
8. State the observed evidence and why reinforcement is necessary.
9. Validate the selected terminology.md structure and review the triggering text against the updated standard when that text is available.

Update an existing entry instead of creating a duplicate. Do not weaken or silently replace a shared preference through a project entry without explaining the narrower project distinction.

## Result

Return TERMINOLOGY STANDARD UPDATE: COMPLETE with the selected scope, changed preferred entry, whether Avoid was omitted or added, the evidence supporting any reinforcement, semantic conflicts checked, and validation result. When scope access is incomplete, return TERMINOLOGY STANDARD UPDATE: BLOCKED with zero mutation and the named remediation.
