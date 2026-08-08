---
name: terminology-standard-review
description: Review durable technical prose or user-visible language against project and shared user terminology.md standards without editing the target or the standards.
metadata:
  category: documentation-methodology
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 0f952e38-003d-47bf-8f1a-c7facaaabf97
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

# Terminology Standard Review

Review whether covered language expresses each defined concept with its preferred term. Apply terminology-standard for artifact discovery, scope precedence, entry meaning, and exclusions.

## Inputs

- The exact review target.
- The project identity when project terminology can apply.
- The one structured aggregate result returned by terminology-standard's Load Terminology Standards operation.

## Review Workflow

1. Load terminology-standard and invoke Load Terminology Standards for the active configured terminology.md snapshot.
2. When the result is TERMINOLOGY STANDARD SCOPE UNAVAILABLE, stop with TERMINOLOGY REVIEW: BLOCKED, name the failed capability and its remediation, and make no mutation. Do not return PASS after a provider error.
3. Treat TERMINOLOGY STANDARDS LOADED as conclusive for the configured provider snapshot, including its no-content ABSENT form, and continue with its aggregate.
4. Identify material concept expressions in the target before comparing individual words.
5. Match each expression to the governing preferred-term definition.
6. Record a finding when a different term expresses a governed concept, even when that term is not yet listed under Avoid.
7. Record a stronger finding when the target uses a term already listed under Avoid for that concept.
8. Distinguish a one-off wording error from a repeated pattern that may justify reinforcement through terminology-standard-update.
9. Return the review without editing the target or either standard.

Do not flag exact identifiers, code, schemas, commands, quotations, external product names, or source-native evidence wording. Do not infer that two similar words express the same concept when the surrounding meaning is unclear.

## Review Result

Return TERMINOLOGY REVIEW: PASS only when the active configured snapshot returned TERMINOLOGY STANDARDS LOADED and every governed concept uses its preferred term. Bind PASS to the returned catalog revision and source labels; it is not proof that an unlisted host root exists or was eligible. Return TERMINOLOGY REVIEW: BLOCKED when Load Terminology Standards returned UNAVAILABLE. Otherwise return TERMINOLOGY REVIEW: NEEDS CORRECTION with:

- the target location;
- the expressed concept;
- the observed term;
- the governing preferred term and scope;
- the smallest correction; and
- any repeated-use evidence that may justify an Avoid reinforcement.

Keep reinforcement recommendations separate from current target corrections. A review never adds a preferred or avoided term.
