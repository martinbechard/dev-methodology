# Procedure Analysis: Creating Usage Scenarios

## Source

- Procedure: [procedure-create-usage-scenarios.md](../procedure-create-usage-scenarios.md)
- Scope reviewed: the complete legacy procedure against the live distributed skills, templates, and canonical development-use roles.

## Durable Guidance

The procedure’s durable contribution is a scenario-coverage discipline for functional documentation: inventory the authoritative behaviors first, choose a small coherent set of actor-centred scenarios, make each scenario traceable to its source requirements, and make the interaction and step narrative agree. Concrete inputs, outputs, processing explanations, edge cases, and approval status make a proposed workflow inspectable before implementation.

This is not a separate documentation type. A usage scenario is a focused functional workflow or verification scenario. The live functional specification route already owns actors, entry points, workflows, states, edge cases, acceptance behavior, verification blocks, and an editable Mermaid workflow diagram. The portable gap is an explicit way to record scenario-to-requirement coverage and to distinguish a proposed scenario from an approved source of truth.

## Mapping

| Procedure point | Live destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Inventory responsibilities and key behaviors before choosing scenarios | create-functional-spec; documentation-reverse-engineering; Documentation Architect | Partial | Add an optional scenario coverage inventory before writing a scenario-heavy functional specification. It should identify the authoritative behavior, source, and the scenario or verification block that covers it. |
| Plan a small coherent scenario set; group naturally related behavior | create-functional-spec; development-methodology | Partial | Add selection guidance: use the smallest scenario set that covers the material actor paths, state changes, and important negative behavior. Do not prescribe two or three responsibilities per scenario. |
| Write each scenario using a consistent structure | functional-spec-template; create-functional-spec | Covered | Retain the functional specification template and its workflow and verification sections. Do not restore a separate usage-scenario template unless repeated target-project use demonstrates a distinct artifact need. |
| Use a descriptive building-block and focus filename | Target project documentation convention | Not portable | Omit from distributed skills. The selected artifact, documentation root, and project naming rules determine the file name. |
| Show interaction flow in a numbered Mermaid sequence diagram | create-functional-spec; functional-spec-template; documentation-page-verifier | Partial | Preserve editable Mermaid diagrams when ordered handoffs clarify the workflow, but do not require a sequence diagram or numbered steps for every scenario. When a diagram and prose both use numbered steps, require that they correspond. |
| Mark diagram steps with responsibilities and behaviors | create-functional-spec; documentation-page-verifier | Missing, minor | Add concise traceability guidance: annotate or accompany a diagram with the source-backed responsibility, rule, state, or acceptance behavior it illustrates when that mapping is not otherwise clear. |
| Supply a matching step-by-step breakdown | create-functional-spec; review-functional-spec | Partial | Add a consistency check to review-functional-spec: diagrammed paths, prose steps, states, and verification assertions must not contradict one another. |
| Create a standalone rendered artifact for every Mermaid diagram | functional-spec-template; documentation-page-verifier | Covered with safer policy | Keep Mermaid as the maintained source. Produce and link an SVG or other rendered companion only when the project’s review or publishing surface cannot render Mermaid. |
| Provide JSON input and output data for every step | functional-spec-template; create-module-design; create-high-level-design | Partial | Include representative concrete inputs, outputs, and data shapes only where contracts, transformations, or implementation ambiguity benefit from them. Use the project’s actual serialization format; do not impose JSON on UI-only, command-line, or non-serializable steps. |
| Explain processing at every step | create-functional-spec; create-module-design; create-high-level-design | Partial | Keep functional specifications actor-observable. Move internal algorithms and component processing rules to module or high-level designs unless the detail changes the user-visible contract. |
| Use only terms and behavior supported by the specification | create-functional-spec; documentation-page-verifier; documentation-reverse-engineering | Covered | No addition. The source-authority and source-backed-content rules already prohibit invented behavior. |
| Link from scenario to specification and add the reverse link after approval | functional-spec-template; project-wiki; target-project AGENTS.md | Partial | Add a project-aware approval and traceability rule to create-functional-spec. Record the proposal as pending when approval is required; after approval, update the owning authoritative document or index using the target project’s link convention. |
| Obtain user approval before treating the scenario as accepted | Target project AGENTS.md; backlog or approval workflow | Partial | Preserve the approval gate only when the project requires one. A portable skill should make approval status explicit and avoid claiming acceptance without evidence, not require a particular approver or workflow. |

## Precise Additions

Amend create-functional-spec with a short optional Scenario Coverage subsection in its workflow:

1. When a functional specification is intended to validate or illustrate requirements through scenarios, inventory the authoritative responsibilities, rules, and key behaviors first.
2. Select the smallest coherent scenario set that covers the material actor paths, states, external handoffs, and negative behavior. Keep each scenario focused enough to review without hiding unrelated behavior.
3. For every material behavior, record its authoritative source and the workflow, diagram, or verification block that covers it. Record uncovered behavior as an open question or planned coverage rather than inventing a scenario.
4. When a workflow diagram and prose both enumerate steps, keep their identifiers and outcomes aligned. Add responsibility or rule annotations only where the mapping would otherwise be ambiguous.
5. Use representative concrete data in the format native to the contract when it clarifies a transformation, boundary, or assertion. Keep internal processing detail in a technical design unless it affects observable behavior.
6. When the target project requires approval, mark the scenario proposed until approval evidence exists. After approval, create the reciprocal link from the owning requirement, functional index, or project wiki page according to the project’s documentation convention.

Amend review-functional-spec with two checklist checks:

1. For scenario-driven specifications, does an authoritative coverage inventory account for material responsibilities, rules, actor paths, state changes, and important negative behavior?
2. Do workflow prose, diagrams, source links, and verification assertions agree, with no unsupported behavior introduced by a scenario example?

No new canonical agent is needed. Documentation Architect should select the functional-spec route, and Artifact Review Agent should apply the strengthened functional-spec checklist. QA And Verification Agent may use the resulting verification blocks, but does not own scenario authoring.

## Omit List

- The separate usage-scenario-template.md dependency, legacy file path, and building-block filename pattern.
- A universal requirement for exactly two or three responsibilities and exactly two or three behaviors per scenario.
- Mandatory sequence diagrams, numbered diagram steps, diagram note blocks, and separate rendered artifacts for every scenario.
- JSON input and output data for every step, regardless of whether the workflow has a serialized contract.
- Detailed internal processing prose in an actor-centred functional specification.
- The exact wiki-link syntax and a mandatory specification-directory layout.
- A universal user-approval workflow, named approver, or automatic backlink timing. These remain project-owned governance rules.
- The legacy copyright, personal contact details, generator attribution, historic file-path statement, and quotation.

## Conclusion

Do not recreate Creating Usage Scenarios as a distributed skill or specialized agent. Incorporate its portable value into create-functional-spec and review-functional-spec as optional scenario coverage, cross-representation consistency, and project-aware approval traceability. The existing functional specification template already supplies the primary artifact shape, workflow diagram support, source authority, open questions, and verification blocks; the proposed additions make scenario-heavy specifications more complete without forcing a second competing documentation format.
