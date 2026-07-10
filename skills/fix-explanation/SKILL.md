---
name: fix-explanation
description: Explain a code fix or patch in a structured way, using the structured-explanation skill and classifying the nature of the fix. Use when the agent needs to explain what changed, why it was needed, and whether the fix is new functionality, a functional improvement, an optimization, backwards-compatibility work, or a migration.
metadata:
  category: development-practice
---

# Fix Explanation

Use structured-explanation to explain the fix.

Do not explain fixes in loose prose by default. Structure the explanation so
the reader can inspect:

- what failed or needed change
- what was changed
- why that change solves the problem
- whether the problem was a non-conformity with upstream requirements, design,
  or prior artifacts
- what kind of fix it is
- how the explanation items relate to each other

## Workflow

1. Use structured-explanation.
2. State the top-level question as the fix being explained.
3. Ground the explanation in concrete evidence:
   - changed files
   - relevant APIs, types, or commands
   - observed failures, errors, or incorrect behavior
4. Explicitly assess conformance against previous steps when applicable:
   - requirements vs design
   - design vs code
   - prior artifact contract vs current artifact behavior
5. State clearly whether the fix addresses a non-conformity.
6. If the artifact is conformant but still undesired, state that the upstream
   specification or design is what must change.
7. End with a direct classification of the fix type.
8. If there is uncertainty about the category, state it as UNKNOWN or
   HYPOTHESIS, then still give the best supported final classification.
9. If the explanation is being used to guide ongoing implementation or the
   user asks to preserve it, save it to a tracked file in the repository.

## Required Output

The explanation should end with a clear final answer that includes:

- the main reason for the fix
- the key mechanism of the fix
- whether there are non-conformities and where they occur
- exactly one fix-type classification from the taxonomy below

Prefer naming the classification in a dedicated final ANSWER.

When the explanation is also being used as a working artifact, prefer saving it
as a plan or other tracked document in the repository rather than leaving it
only in chat.

## Non-Conformity Rule

Always distinguish between these two cases:

### Non-Conformity

Use this when some downstream artifact does not conform to an upstream source
that already required different behavior.

Examples:
- a design that does not respect requirements
- code that does not implement the design
- a phase artifact that violates the phase contract or prior-phase inputs

### Conformant But Undesired

Use this when the artifact behaves consistently with its upstream source, but
the upstream source itself is undesirable.

Examples:
- code matches the design, but the design is wrong
- a design matches the requirements, but the requirements are wrong

In that case, say explicitly that there is no downstream non-conformity at the
fix point, and that the upstream specification needs to change.

## Fix-Type Taxonomy

Choose exactly one of these unless the user explicitly asks for multiple
angles.

### New Functionality

Use this when the change adds a new capability or new supported behavior that
did not exist before.

Tests:
- A previously unsupported user case is now supported.
- The main point of the change is addition, not repair.

### Functional Improvement

Use this when existing behavior still has the same broad purpose, but the
change materially improves correctness, completeness, safety, or usability.

Tests:
- The system already did this job before.
- The change improves how well it performs that job in functional terms.
- The main benefit is better behavior, not merely faster or cleaner execution.

### Optimization

Use this when the intended functionality stays the same and the main change is
improved operation such as performance, efficiency, resource usage, or reduced
overhead.

Tests:
- The supported behavior is intentionally unchanged.
- The value comes from operating better, not behaving differently.

### Backwards-Compatibility

Use this when the change adds support for a new case while still keeping older
cases working.

Tests:
- The code now accepts or supports an additional case.
- The old case is still intentionally supported.
- The change preserves compatibility across multiple supported forms, paths, or
  interfaces.

### Migration

Use this when the change is required to complete or support a refactoring,
rename, interface shift, or modification of existing functionality.

Tests:
- The old form is no longer meant to remain supported.
- The change aligns callers and callees after an internal change.
- The purpose is convergence on the new shape, not simultaneous support for
  both old and new shapes.

## Decision Rule

When deciding between backwards-compatibility and migration:

- choose backwards-compatibility if the code is meant to support both the old
  and new cases
- choose migration if the code is being updated to the new case and the old
  case is not intended to remain a supported path

## Writing Rules

- Use the item types from structured-explanation.
- Keep FACT items concrete and tied to files, logs, commands, or observed
  behavior.
- When one item is a true child of another, nest it under that parent item
  rather than flattening it.
- When two items are siblings or an item has multiple non-tree relationships,
  keep them as peers and use explicit references such as ADDRESSES,
  RELATES-TO, SUPPORTS, or another short relation label.
- Do not use a reference label as a substitute for a real parent-child
  relationship.
- Include a dedicated ANSWER that states whether there are non-conformities.
- If there are non-conformities, identify:
  - the upstream source
  - the non-conforming artifact
  - the nature of the mismatch
- If there are no non-conformities, say that explicitly and state that the
  upstream specification/design is what requires change.
- Do not call something backwards-compatible unless the code really supports
  both paths.
- Do not call something an optimization if the behavior materially changed.
- Do not call something new functionality when it is really repair or
  migration work.
- If the fix is small, keep the explanation short rather than expanding the
  structure unnecessarily.

## Relationship Rules

Use these structure rules consistently:

- Parent-child relationship:
  - nest the child item under the parent item
- Sibling relationship:
  - keep both items at the same structural level
- Multiple relations or cross-links:
  - keep the item at the correct structural level and add one or more explicit
    reference fields such as ADDRESSES, RELATES-TO, or DEPENDS-ON

Examples:

- A TEST that exists only to verify one FIX should be nested under that
  FIX.
- A FIX that addresses two separate PROBLEM items should remain one item
  and reference both problems explicitly.
- A BENEFIT that follows directly from one FIX should be nested under that
  FIX.

## Persistence Rule

When the fix explanation will guide an active implementation, recovery after a
crash, or progress tracking:

- save the explanation to a tracked repository file
- choose the file path using the repository's placement rules
- keep the saved file updated as progress changes

If the user only wants a one-off explanation, saving is optional unless they
ask for it explicitly.
