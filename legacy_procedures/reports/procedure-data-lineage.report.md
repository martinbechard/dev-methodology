# Data Lineage Procedure Migration Report

## Source

Source procedure: [procedure-data-lineage.md](../procedure-data-lineage.md)

## Purpose And Scope

The procedure derives a solution-wide Mermaid graph of values as they cross module, function, class, import, export, and caller boundaries. Its durable purpose is to make an important value's producer, transformation, handoff, and consumer inspectable from source evidence.

That purpose remains useful for cross-boundary contracts, persisted records, security-sensitive values, and hard-to-follow derived state. A mandatory graph of every output, input, and intermediate local variable does not: it is expensive, volatile, and obscures the data paths that matter.

## Durable Guidance Worth Keeping

- Treat code and tests as the authority for actual lineage; inspect callers as well as the module being documented.
- Start from a named value, record, event, or contract and trace it through producers, transformations, handoffs, persistence or serialization boundaries, and consumers.
- Name graph nodes by their actual owner and role so identical local names do not create false associations.
- Distinguish authoritative inputs and state from derived, transient, serialized, and user-visible outputs.
- Use a diagram only when the cross-boundary path is harder to understand in prose, and link the diagram to the source-backed design artifact that explains it.
- Record uncertainty or indirect/dynamic flow as an open question rather than guessing.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Read module code, callers, imports, exports, contracts, and tests before documenting behavior | [documentation-reverse-engineering](../../skills/documentation-reverse-engineering/SKILL.md) | Covered for discovery: its module-design pass requires implementation, callers, imports, exported contracts, and tests; it also permits diagrams for real data-movement relationships. | Retain this source-authority and caller-inspection discipline. |
| Discover function, import, export, class, and nested assignment relationships | [ast-grep](../../skills/ast-grep/SKILL.md) | Partial: it supplies syntax-aware discovery, but deliberately does not establish runtime behavior or document lineage. | Use it to seed evidence; read the matched source before adding a lineage claim. |
| Describe module inputs, outputs, internal data/state, and public contracts | [create-module-design](../../skills/create-module-design/SKILL.md) and its [template](../../skills/development-methodology/assets/templates/module-design-template.md) | Covered at module granularity: Public Contracts and Internal Data And State capture the durable information, without forcing local-variable inventory. | Keep this level of detail by default. |
| Map subsystem producers, consumers, shape owners, and serialization/persistence boundaries | [create-high-level-design](../../skills/create-high-level-design/SKILL.md) and its [template](../../skills/development-methodology/assets/templates/high-level-design-template.md) | Covered: Data Shapes And Contracts requires owners, producers, consumers, and material boundaries; its Data Contract Map is the direct visual destination. | Use this for a multi-module lineage map. |
| Describe system-wide data movement, state ownership, persistence, serialization, and UI paths | [create-architecture](../../skills/create-architecture/SKILL.md) and its [template](../../skills/development-methodology/assets/templates/architecture-template.md) | Covered: Data Flow explicitly covers these concerns and calls for a Data Flow Diagram when several components exchange data. | Use architecture only for project-wide or cross-cutting paths. |
| Select and produce a source-backed technical documentation set | [Documentation Architect](../../agents/roles/development-use/documentation-architect.role.yaml) | Covered: the role routes to documentation-reverse-engineering and the appropriate artifact, but does not prescribe a variable-level graph. | No role change is needed. |

## Coverage Assessment

The catalog already has the right artifact homes: module designs for owned state and contracts, high-level designs for shared data contracts, and architecture for broad data movement. It also has the required source-discovery workflow. The remaining gap is a compact decision rule in documentation-reverse-engineering for when a source-backed lineage pass is warranted and what evidence its map must show. This is a small addition to an existing skill, not a separate capability.

## Precise Suggested Addition

Add the following conditional step under Pass 1 of documentation-reverse-engineering, after the instruction to read callers, imports, exported contracts, and tests:

> When a value, record, event, or state field crosses important module, persistence, serialization, external-service, security, or UI boundaries, trace its producer, transformations, handoffs, owner, and consumers from source evidence. Put the result in the module design, high-level design, or architecture artifact that owns the boundary; add a data-flow or data-contract diagram only when it makes that relationship clearer. Record dynamic or unproven relationships as open questions.

This addition preserves the procedure's most valuable cross-caller investigation while letting the existing templates choose the correct documentation level. It also makes omissions reviewable without creating an ever-growing solution-wide flowchart.

## Guidance To Omit Or Narrow

- Omit the fixed design/data-lineage-flowchart.md filename and the requirement that every project maintain one global graph. Documentation location should follow the selected artifact and target repository structure.
- Omit the requirement that the graph begin with graph LR. Mermaid direction is a presentation choice; flowchart direction should serve readability.
- Omit exhaustive nodes and edges for every local input, output, intermediate variable, assignment, and read. These are implementation details that drift quickly and make diagrams unreadable.
- Narrow the scoped-name convention to a readability principle: label a node with enough owner and role context to disambiguate it. Do not impose module_function_variable identifiers, which break on overloads, closures, generated code, dynamic imports, and non-code data sources.
- Omit a guarantee that all return destinations can be found statically. Dynamic dispatch, callbacks, reflection, framework injection, queues, and external consumers may prevent proof; record the limit instead.
- Omit the ban on all type or contract detail. Include a data shape or contract only when it is required to distinguish the lineage or boundary; do not duplicate unrelated design documentation.

## Conclusion

Keep the procedure's source-backed, cross-caller lineage reasoning, but integrate it as a conditional documentation-reverse-engineering step. Existing module, high-level, and architecture artifacts already provide the appropriate destinations and diagram shapes. Do not create a standalone data-lineage skill or a dedicated agent; the legacy all-variable global flowchart should not be revived.
