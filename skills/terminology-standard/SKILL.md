---
name: terminology-standard
description: Apply preferred project and shared user terminology from terminology.md when writing or revising durable technical prose or user-visible language.
metadata:
  category: documentation-methodology
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 7faae0fc-6944-4574-bea6-874c2bfe6376
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

# Terminology Standard

A Terminology Standard defines the preferred words for concepts used in project-authored prose and user-visible language. It starts with what writers should say. It adds avoided terms only when observed usage shows that a preferred definition needs reinforcement.

## Artifact Contract

Use the exact filename terminology.md at either supported scope:

- The shared user standard applies across projects.
- The project standard narrows or extends the shared standard for one project.

Load both scopes before covered writing, review, or update. Do not search arbitrary user-home paths or expose their physical locations.

## Load Terminology Standards

The provider-neutral operation is Load Terminology Standards. Its configured MCP realization is mcp-agent-ops reference_load. Invoke reference_load exactly once with names set to a one-item list containing terminology.md. The server must run with:

- the active project beneath MCP_AGENT_OPS_WORKSPACE_ROOTS;
- the shared user reference directories in MCP_AGENT_OPS_REFERENCE_ROOTS; and
- terminology.md in MCP_AGENT_OPS_REFERENCE_NAMES.

Map its structured result into exactly one consumer outcome:

- When ok is true, return TERMINOLOGY STANDARDS LOADED with catalog_revision, the aggregated content, aggregate digest, source_count, and every ordered source scope, digest, and byte_count. Project content is first and configured user content follows. Within the aggregate, the first matching preferred-term definition governs, so a project definition takes precedence without losing shared entries for other concepts.
- When the only error code is reference_not_found, return TERMINOLOGY STANDARDS LOADED with no content and conclusive ABSENT status across the configured project and user scopes.
- When reference_load is absent, the server or configured project boundary cannot be used, required reference configuration is missing, or any other error is returned, return TERMINOLOGY STANDARD SCOPE UNAVAILABLE with the failed capability and owner remediation. Do not reinterpret UNAVAILABLE as ABSENT.

This base skill owns the provider-neutral operation and entry-format contract. mcp-agent-ops owns scope discovery, aggregation, ordering, and the structured reference_load result. The runtime configuration owns the authorized project and shared user roots. Do not emulate the provider by searching paths.

An ABSENT standard is valid. Continue the requested work without creating terminology.md unless the user asks to create or update it.

When reference_load returns TERMINOLOGY STANDARD SCOPE UNAVAILABLE, an ordinary project-scoped writing task may use direct project-file access to read the project-root terminology.md. Return TERMINOLOGY APPLICATION: PARTIAL, apply only that project standard, and name shared user scope as unavailable. If the project artifact also cannot be read conclusively, return TERMINOLOGY APPLICATION: BLOCKED and do not claim terminology conformance. This fallback cannot support TERMINOLOGY REVIEW: PASS or any terminology.md mutation. Do not use direct user-home searching as a substitute for reference_load.

Apply the project-first provider aggregate so the first matching project entry governs within its project and shared entries remain available for concepts the project does not redefine. Report an unresolved semantic conflict when the narrower entry does not make the intended distinction clear.

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

1. Load the shared user and project standards through Load Terminology Standards.
2. Branch on the load outcome before inspecting the covered text; use the explicit PARTIAL fallback or stop on BLOCKED.
3. Identify the concept expressed by each material term in the covered text.
4. Use the first preferred term in provider order whose definition matches that concept.
5. Apply an avoided-term rule only within the concept and scope stated by its entry.
6. Preserve the artifact's technical meaning, normative force, and established structure.
7. Report conflicts or uncovered concepts instead of inventing a new standard entry.

Do not perform blind substring replacement. Preserve exact identifiers, code, schemas, commands, quoted text, external product names, and source-native wording retained as evidence unless the requested work explicitly changes them.

## Result

Return the load outcome, standards and scopes applied, any project-over-shared precedence decision, unresolved terminology conflict, unavailable scope, and the covered writing result.
