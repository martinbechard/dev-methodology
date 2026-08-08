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

Load both available scopes in one multi-scope artifact call before mutation when the runtime supports that operation. Update only the selected scope. Do not copy all shared entries into the project artifact.

## Update Workflow

1. Identify the concept, preferred term, definition, intended scope, and source of authority.
2. Check both standards for an existing entry, overlap, or semantic conflict.
3. Create or revise one positive preferred-term entry with a precise definition.
4. Add Use for or Examples only when they clarify a real boundary.
5. Omit Avoid for the initial entry unless retained evidence already proves persistent biased substitution.
6. Add or extend Avoid only when a review, correction history, or supplied artifact shows repeated use of the nonpreferred term after the preferred concept was available, or shows a persistent misleading metaphor that the definition alone did not correct.
7. State the observed evidence and why reinforcement is necessary.
8. Validate the selected terminology.md structure and review the triggering text against the updated standard when that text is available.

Update an existing entry instead of creating a duplicate. Do not weaken or silently replace a shared preference through a project entry without explaining the narrower project distinction.

## Result

Return the selected scope, changed preferred entry, whether Avoid was omitted or added, the evidence supporting any reinforcement, semantic conflicts checked, and validation result.
