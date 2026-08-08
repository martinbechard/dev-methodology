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

Invoke terminology-standard's Refresh Terminology Standards operation once before the initial load so the decision does not use a stale process snapshot. Then invoke Load Terminology Standards once and require its catalog revision to equal the refresh revision. A loaded aggregate or its no-content ABSENT form is available for the decision relative to that revision and its source labels. If refresh or load is unavailable, fails, or returns mismatched revisions, return TERMINOLOGY STANDARD UPDATE: BLOCKED with the failed capability and required owner remediation, and make no mutation. Shared user updates therefore require supported shared-scope access as well as the user's explicit scope selection.

The loaded result does not prove that an unlisted physical root exists or was eligible. When the requested mutation depends on examining a named physical scope that is not covered by explicit provider evidence, return TERMINOLOGY STANDARD UPDATE: BLOCKED instead of inferring completeness.

Update only the selected scope. Do not copy all shared entries into the project artifact.

## Update Workflow

1. Identify the concept, preferred term, definition, intended scope, and source of authority.
2. Consume the pre-mutation refresh and Load Terminology Standards results already obtained for the scope decision and stop without mutation when either is unavailable or their revisions differ.
3. Check every standard returned in the configured snapshot for an existing entry, overlap, or semantic conflict.
4. Create or revise one positive preferred-term entry with a precise definition.
5. Add Use for or Examples only when they clarify a real boundary.
6. Omit Avoid for the initial entry unless retained evidence already proves persistent biased substitution.
7. Add or extend Avoid only when a review, correction history, or supplied artifact shows repeated use of the nonpreferred term after the preferred concept was available, or shows a persistent misleading metaphor that the definition alone did not correct.
8. State the observed evidence and why reinforcement is necessary.
9. Validate the selected terminology.md structure and retain the selected target file's SHA-256 digest.
10. Invoke Refresh Terminology Standards a second time. If it does not return TERMINOLOGY REFERENCE SNAPSHOT REFRESHED with terminology.md among the available names, preserve the valid file mutation and return TERMINOLOGY STANDARD UPDATE: PUBLICATION INCOMPLETE with the refresh evidence and remediation.
11. Invoke Load Terminology Standards once against the refreshed snapshot. Require the returned catalog revision to equal the refresh revision and a returned source digest to equal the selected target digest. On mismatch or load failure, preserve the valid file mutation and return TERMINOLOGY STANDARD UPDATE: PUBLICATION INCOMPLETE.
12. Review the triggering text against the refreshed standard when that text is available.

Update an existing entry instead of creating a duplicate. Do not weaken or silently replace a shared preference through a project entry without explaining the narrower project distinction.

## Result

Return TERMINOLOGY STANDARD UPDATE: COMPLETE only after the refreshed snapshot is verified. Include the selected scope, authorized target, pre-mutation and published revisions, returned source labels, configured-snapshot coverage limit, selected target digest, changed preferred entry, whether Avoid was omitted or added, the evidence supporting any reinforcement, semantic conflicts checked within the pre-mutation snapshot, and validation result. COMPLETE describes the authorized mutation and verified snapshot publication; it does not assert coverage of an unlisted physical root.

When the provider or refresh capability is unavailable before mutation, required physical-scope coverage evidence is absent, or shared-target authority is incomplete, return TERMINOLOGY STANDARD UPDATE: BLOCKED with zero mutation and the named remediation. When file mutation and validation succeeded but refresh or publication verification failed, return TERMINOLOGY STANDARD UPDATE: PUBLICATION INCOMPLETE with the preserved target, target digest, refresh or reload evidence, and named remediation. Do not report zero mutation or revert a valid file after a post-mutation publication failure.
