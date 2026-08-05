# Apply the Object-Oriented Skill Group Design

## Goal

Apply the approved skill names and public procedure headings from the object-oriented skill-group proposal while keeping Agent references, provider routing, generated mirrors, and individual evaluations coherent.

## Design Authority

- design/object-oriented-agent-and-skill-model.md defines the reusable relationship and diagram standards.
- design/object-oriented-skill-group-models.md owns the canonical proposal-name registry and links the seven applied group designs.
- Commit c426c970153948f9d5d2d92f1b7b718613a8d4f7 is the reviewed applied-design baseline.
- The active user request on 2026-08-04 explicitly directs creation of separate work items to update skills and their individual evaluations according to this design.

## Scope Rules

- Each child owns one coherent skill family or integration boundary.
- Each changed skill receives a focused behavioral probe or equivalent individual evaluation update.
- Renames update exact governed Agent references and skill metadata in the same child that owns the rename, unless a listed dependency deliberately sequences a cross-family reference update.
- Generated mirrors are refreshed only from approved canonical sources.
- Historical result records remain historical and are not rewritten merely to replace old skill names.
- Every governed path must pass the supported definition-change precheck using the approval evidence recorded in its child item.

## Work Items

1. [Align Baseline Development Skills](align-baseline-development-skills.md)
2. [Align Project Setup Skills](align-project-setup-skills.md) — Blocked: evaluator catalog-validation recovery required.
3. [Align Documentation Methodology Skills](align-documentation-methodology-skills.md)
4. [Align Work-Item Creation Provider Skills](align-work-item-creation-provider-skills.md)
5. [Align Work-Item Management Provider Skills](align-work-item-management-provider-skills.md) — Starting; reserved for its preserved canonical Thread.
6. [Split Backlog Blockage And Dispatch-Mode Skills](split-backlog-blockage-and-dispatch-mode-skills.md)
7. [Align Resource Coordination Skills](align-resource-coordination-skills.md) — Ready; preserved canonical delivery evidence awaits parent dispatch.
8. [Align Codex Work-Item Coordination Skill](align-codex-work-item-coordination-skill.md)
9. [Align Integration And Delivery Skills](align-integration-and-delivery-skills.md)
10. [Align Review And Verification Skills](align-review-and-verification-skills.md)

## Dependency Order

- Baseline Development precedes Documentation Methodology because the documentation rename must update the review-structured-artifact reference after its baseline procedure changes settle.
- Work-Item Management Providers and Resource Coordination precede Codex Work-Item Coordination because the coordinating skill consumes both procedure families.
- Resource Coordination and Codex Work-Item Coordination precede Integration And Delivery because delivery uses the selected claim and delivery vocabulary.
- Review And Verification follows Integration And Delivery because end-to-end-verification currently names both delivery providers.
- All other children may proceed independently when exact path claims and shared evaluation-file capacity allow.

## Definition Of Good

- All forty-one current skills and two approved extractions are represented by the canonical proposed package names and procedure headings assigned to their primary groups.
- Cross-group references use the same names as the proposal registry.
- Agent definitions, skill metadata, generated adapters, catalogs, and maintained documentation contain no stale live reference to a removed skill name.
- Every changed or created skill has an individual evaluation that exercises its public procedure vocabulary and important boundaries.
- Focused tests, generated-output freshness checks, full evaluation catalog validation, independent review, and final integrated regression pass.
