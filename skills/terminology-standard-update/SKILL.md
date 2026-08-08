---
name: terminology-standard-update
description: Create or update terminology.md with positive-first preferred terms and add avoided-term reinforcement only when observed usage provides evidence for it.
metadata:
  category: documentation-methodology
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 47ac232b-bf33-45ac-992e-3a5d993200e9
Created-UTC: 2026-08-08T19:24:44Z
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: git-derived
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->

# Terminology Standard Update

Create or update a Terminology Standard without turning it into an exhaustive synonym blacklist. Apply terminology-standard for artifact discovery, precedence, entry format, and application boundaries.

## Scope Decision

Use the project terminology.md by default for a concept specific to one project. Update the shared user standard only when the user explicitly selects shared scope and the preference is intended to apply across projects.

A shared user update also requires a caller-supplied authorized target path or provider-owned mutation capability for one configured shared reference root. Do not derive that target from the path-free reference_load result.

Invoke terminology-standard's Load Terminology Standards operation once before mutation. A loaded aggregate or its no-content ABSENT form is available for the decision relative to the returned catalog revision and source labels. If the operation returns UNAVAILABLE, return TERMINOLOGY STANDARD UPDATE: BLOCKED with the failed capability and required owner remediation, and make no mutation. Shared user updates therefore require supported shared-scope access as well as the user's explicit scope selection.

The loaded result does not prove that an unlisted physical root exists or was eligible. When the requested mutation depends on examining a named physical scope that is not covered by explicit provider evidence, return TERMINOLOGY STANDARD UPDATE: BLOCKED instead of inferring completeness.

Update only the selected scope. Do not copy all shared entries into the project artifact.

## Update Workflow

1. Identify the concept, preferred term, definition, intended scope, and source of authority.
2. Consume the one Load Terminology Standards result already obtained for the scope decision and stop without mutation when it is UNAVAILABLE.
3. Check every standard returned in the configured snapshot for an existing entry, overlap, or semantic conflict.
4. Create or revise one positive preferred-term entry with a precise definition.
5. Add Use for or Examples only when they clarify a real boundary.
6. Omit Avoid for the initial entry unless retained evidence already proves persistent biased substitution.
7. Add or extend Avoid only when a review, correction history, or supplied artifact shows repeated use of the nonpreferred term after the preferred concept was available, or shows a persistent misleading metaphor that the definition alone did not correct.
8. State the observed evidence and why reinforcement is necessary.
9. Validate the selected terminology.md structure and review the triggering text against the updated standard when that text is available.

Update an existing entry instead of creating a duplicate. Do not weaken or silently replace a shared preference through a project entry without explaining the narrower project distinction.

## Result

Return TERMINOLOGY STANDARD UPDATE: COMPLETE with the selected scope, authorized target, returned catalog revision and source labels, configured-snapshot coverage limit, changed preferred entry, whether Avoid was omitted or added, the evidence supporting any reinforcement, semantic conflicts checked within that snapshot, and validation result. COMPLETE describes the authorized mutation; it does not assert coverage of an unlisted physical root. When the provider is unavailable, required physical-scope coverage evidence is absent, or shared-target authority is incomplete, return TERMINOLOGY STANDARD UPDATE: BLOCKED with zero mutation and the named remediation.
