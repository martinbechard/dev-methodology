---
name: terminology-standard
description: Apply preferred project and shared user terminology from terminology.md when writing or revising durable technical prose or user-visible language.
metadata:
  category: documentation-methodology
---

# Terminology Standard

A Terminology Standard defines the preferred words for concepts used in project-authored prose and user-visible language. It starts with what writers should say. It adds avoided terms only when observed usage shows that a preferred definition needs reinforcement.

## Artifact Contract

Use the exact filename terminology.md at either supported scope:

- The shared user standard applies across projects.
- The project standard narrows or extends the shared standard for one project.

Load both scopes before covered writing or review. When the runtime provides one multi-scope artifact operation, request the project and shared user copies in one call. Do not search arbitrary user-home paths or expose their physical locations. When only direct project-file access is available, use the project-root terminology.md and report that the shared user scope was unavailable.

An absent standard is valid. Continue the requested work without creating terminology.md unless the user asks to create or update it.

Apply the shared user entries first. A project entry governs within its project when the two standards overlap. Report an unresolved semantic conflict when the narrower entry does not make the intended distinction clear.

## Entry Format

Use one preferred term as each heading under Preferred Terms. Every entry requires a definition. Add Use for or Examples only when they clarify the concept boundary.

Add Avoid only after evidence shows repeated substitution, a misleading domain metaphor, or another persistent bias toward a nonpreferred term. Do not populate Avoid as a speculative synonym list.

```markdown
# Terminology Standard

## Preferred Terms

### Test suite

Definition: A named collection of related tests that are selected and evaluated together.

Use for:

- The stable collection of tests, independent of any one execution.

Avoid:

- Campaign: This metaphor obscures that the item is a test collection.
```

The Avoid section is optional. The example shows its shape, not a requirement to add it with the initial definition.

## Apply Preferred Terminology

1. Load the available shared user and project standards.
2. Identify the concept expressed by each material term in the covered text.
3. Use the preferred term whose definition matches that concept.
4. Apply an avoided-term rule only within the concept and scope stated by its entry.
5. Preserve the artifact's technical meaning, normative force, and established structure.
6. Report conflicts or uncovered concepts instead of inventing a new standard entry.

Do not perform blind substring replacement. Preserve exact identifiers, code, schemas, commands, quoted text, external product names, and source-native wording retained as evidence unless the requested work explicitly changes them.

## Result

Return the standards and scopes applied, any project-over-shared precedence decision, unresolved terminology conflict, and the covered writing result.
