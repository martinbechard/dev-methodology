# Migration Review: Creating Requirements Documents

## Source

[Legacy procedure](../procedure-create-requirements.md) defines a building-block specification: prepare from source material, use a template, describe responsibility and observable interfaces, retain only material constraints, and review the result. This review compares it with the live skill catalog, templates, canonical roles, and repository maintenance contract.

## Durable Guidance

- Inspect authoritative repository evidence before choosing or drafting an artifact; record unknown facts as open questions rather than filling them with assumptions.
- Choose the smallest document shape that matches the decision: functional specification for actor-visible behavior, architecture for system-wide concerns, high-level design for a coherent subsystem, and module design for one implementation unit.
- State scope, responsibilities, boundaries, contracts, dependencies, non-goals, constraints, and verification at the level owned by the selected artifact. Keep functional specifications user-facing and implementation designs technical without duplicating lower-level detail.
- Use diagrams only when they make a real relationship clearer; keep Mermaid or another editable representation authoritative and align every diagram with its surrounding text.
- Keep documentation concise, direct, source-backed, and reviewable. Defer discussed but non-essential capabilities through a named backlog item, open question, or future design rather than presenting them as current requirements.

## Mapping And Coverage

| Legacy point | Live destination | Coverage | Action |
| --- | --- | --- | --- |
| Identify the building block and gather requirements, discussions, and source material before drafting | [development-methodology](../../skills/development-methodology/SKILL.md) workflow and document-type selection; each create skill's repository-inspection workflow | Covered | Keep the live source-first routing. It makes the legacy building-block label precise instead of treating it as a sixth artifact type. |
| Begin with a standard template and replace placeholders completely | [create-functional-spec](../../skills/create-functional-spec/SKILL.md), [create-high-level-design](../../skills/create-high-level-design/SKILL.md), and [create-module-design](../../skills/create-module-design/SKILL.md), with their template assets | Covered | Retain the focused templates; select one after classifying the work. |
| Keep scope and responsibilities focused; use action statements; avoid scope creep | [create-module-design](../../skills/create-module-design/SKILL.md) responsibilities and invariants; [create-high-level-design](../../skills/create-high-level-design/SKILL.md) scope and non-goals; [structured-design](../../skills/structured-design/SKILL.md) plain, concrete, actionable prose | Covered | No catalog change. The live templates provide stronger source and verification expectations than the fixed three-to-seven-item rule. |
| Record inputs, outputs, dependencies, key behaviors, and component-specific constraints | Module-design public contracts, dependencies, processing rules, configuration, external interfaces, and error handling; high-level-design contracts and interaction model | Covered | Route one implementation unit to module design and multi-module collaboration to high-level design. |
| Keep functional requirements separate from interfaces, classes, and implementation choices | [development-methodology](../../skills/development-methodology/SKILL.md) document-type selection; [create-functional-spec](../../skills/create-functional-spec/SKILL.md) actor-viewpoint scope; [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md) steady-state checks | Covered | Keep this separation. Technical contracts belong in module or high-level design when needed. |
| Use clear language, respect requested limits, and use only useful examples | [structured-design](../../skills/structured-design/SKILL.md) required discipline and [review-structured](../../skills/review-structured/SKILL.md) concision check | Covered | Preserve outcome-oriented concision, not the arbitrary five-to-seven bullet cap or a compulsory examples section. |
| Include four C4 diagrams and customize template examples | [create-architecture](../../skills/create-architecture/SKILL.md), high-level-design template, and documentation-page-verifier diagram checks | Partly covered by design | Keep the live relationship-driven diagram policy; do not mandate C4 views for every artifact. Use a system-context or component diagram when it clarifies an actual boundary or collaboration. |
| Separate discussed non-essential features from undiscovered suggestions | Functional-spec open questions and related backlog items; high-level-design non-goals; [create-backlog](../../skills/create-backlog/SKILL.md) when work needs tracking | Covered | Treat only authorized, source-backed deferred work as backlog candidates. Record unvalidated ideas as open questions, not requirements. |
| Review clarity, completeness, textual/diagram consistency, and stakeholder feedback | Artifact-specific review skills, [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md), and [artifact-review-agent](../../agents/roles/development-use/artifact-review-agent.role.yaml) | Covered | Use the matching checklist and verifier; retain stakeholder feedback as an authoritative source when supplied. |

## Recommendations

No new skill or canonical agent is recommended. The legacy procedure combines three existing artifact levels, and splitting that combination into functional specifications, high-level designs, and module designs is the current catalog's deliberate improvement.

No live-skill change is required. The only reusable principle that might look missing—avoid implementation detail in requirements—is already explicit in the functional-specification review path and document-type router. Adding a generic building-block-specification template would reintroduce an overlapping sixth document shape.

## Omits

Do not retain the fixed filename pattern, mandatory section names, three-to-seven responsibility count, three-to-five behavior count, five-item suggestion cap, or mandatory examples. The selected template and project taxonomy should determine structure and placement.

Do not retain the requirement that every specification has all four C4 diagrams. A module or functional specification commonly needs no diagram, while architecture and high-level design use only diagrams that clarify an actual boundary, dependency, lifecycle, flow, ownership, or verification relationship.

Do not retain the legacy invitation to add undiscussed suggestions directly to a requirements document. An unvalidated suggestion is either an open question or separate future work; it must not silently acquire requirement status.

## Conclusion

Keep the legacy procedure as historical input only. Its source-first drafting, bounded scope, responsibility and contract clarity, constraint ownership, diagram consistency, and review principles are all covered by the existing methodology. Preserve its useful intent through the current artifact router and review skills; make no new skill, agent, or template.
