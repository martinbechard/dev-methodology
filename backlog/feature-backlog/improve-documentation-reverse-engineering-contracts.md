# Improve Documentation Reverse-Engineering Contracts

Status: Proposed

Type: Feature

## Summary

Clarify the documentation reverse-engineering methodology, project configuration contract, artifact templates, wiki handoffs, and synchronized distributed representations so that bottom-up creation remains authoritative, pass acceptance reflects the evidence available at each layer, documentation mode is persisted, and a final top-down semantic reconciliation checks the completed hierarchy.

## Context

Feedback from a reverse-engineering run identified ambiguity in pass gating, documentation readiness, hybrid wiki and specification processing, and final cross-layer reconciliation. The current documentation-reverse-engineer skill already establishes the intended bottom-up sequence, but the complete affected contract needs to make clear that an intentionally absent later or parent layer is not a current-pass defect.

The methodology must distinguish whether an artifact accurately documents the implemented system from whether that system is ready for implementation or change. Known product defects and unresolved design decisions can be accurately documented. They block artifact acceptance only when they create insufficient evidence, leave a current-pass requirement unresolved, or otherwise meet an explicit blocking condition.

Likely affected sources include:

- skills/documentation-reverse-engineer/SKILL.md
- skills/documentation-bootstrap/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/development-methodology/assets/templates/project-template.yaml
- Structured artifact creation and review skills, templates, and checklists used by the reverse-engineering passes
- skills/project-wiki-create/SKILL.md
- skills/project-wiki-topic-write/SKILL.md
- skills/project-wiki-review/SKILL.md
- skills/project-wiki-topic-verify/SKILL.md
- README.md, relevant design pages, generated adapters, metadata, and regression tests that describe or encode the same contracts

Confirm the complete affected surface from repository evidence before implementation. Keep ownership boundaries clear: orchestration belongs in the reverse-engineering methodology, artifact semantics belong in the applicable create and review skills, wiki behavior belongs in project-wiki skills, and harness or repository mutation behavior must not be duplicated.

## Requirements

### Preserve Bottom-Up Creation

- Preserve this creation sequence without reversal:
  1. Project configuration.
  2. Repository inventory.
  3. Module designs.
  4. High-level designs.
  5. Architecture.
  6. Functional specifications.
  7. Wiki and README integration.
- Keep prerequisite-layer completion and per-pass review as gates before dependent artifact creation.
- Do not redesign the methodology beyond the requirements in this item.

### Clarify Pass Acceptance

- Review each artifact against source evidence, completed prerequisite layers, and the requirements of the current pass.
- Do not treat the intentional absence of a later or parent layer as a blocker, defect, or missing input during an earlier pass.
- Reserve BLOCKED for missing prerequisites, insufficient evidence, unresolved findings within the current pass, or unavailable mandatory dependencies.
- Distinguish documentation acceptance from implementation readiness.
- Allow an accurate reverse-engineered artifact to pass while explicitly documenting product defects, unimplemented behavior, open design decisions, and implementation-readiness limitations that do not prevent accurate current-pass documentation.
- Keep those defects, decisions, and limitations visible for downstream reconciliation and planning rather than silently resolving or omitting them.

### Add Final Top-Down Semantic Reconciliation

- Add a final reconciliation after every bottom-up layer and the wiki integration exist.
- Reconcile in this direction:
  1. Wiki and functional specifications.
  2. Architecture.
  3. High-level designs.
  4. Module designs.
  5. Source.
- Verify that higher-level language, workflows, boundaries, terminology, decisions, known defects, and links remain semantically consistent with the authoritative lower-level artifacts and source evidence.
- Treat this reconciliation as supplemental verification. It must not replace bottom-up creation, prerequisite gates, or per-pass artifact review.
- Define correction and re-review behavior when reconciliation finds a mismatch, including which authoritative layer owns each correction.

### Persist Documentation Mode

- Add an explicit documentation mode to the project configuration contract and its template or schema representation.
- Support at least the hybrid wiki and specification mode selected during documentation bootstrap.
- Persist the selected mode in PROJECT.yaml so downstream agents do not depend on conversational context.
- Define validation, defaults or migration behavior, and handling of unsupported or missing values.
- Ensure bootstrap, project configuration, reverse engineering, and downstream wiki processing consume the persisted selection consistently.

### Define Hybrid Processing

- Keep module designs, high-level designs, architecture, and functional specifications as structured authoritative artifacts.
- Use wiki processing to create standard main pages, domain hubs, indexes, and appropriately granular leaf topics.
- Make wiki pages synthesize accepted specifications and link to authoritative artifacts instead of duplicating them verbatim.
- Include navigation, glossary, open decisions, known defects, and maintenance history where applicable.
- Define how hybrid processing avoids orphaned authoritative artifacts, duplicate ownership, conflicting claims, and oversized wiki pages.

### Invoke Project-Wiki Capabilities

- Make the wiki pass invoke the appropriate project-wiki creation, topic-writing, review, and verification capabilities.
- Define the inputs, outputs, ownership, and completion evidence for each wiki capability used by the pass.
- Preserve the project-wiki source-priority, page-granularity, navigation, review, correction-loop, and verification contracts rather than copying their procedures into the reverse-engineering skill.

### Synchronize Distributed Contracts

- Inspect the complete affected skill packages, templates, references, configuration contracts, generated adapters, documentation, metadata, and regression tests before editing.
- Update every distributed representation that must remain synchronized.
- Regenerate derived artifacts from their canonical sources rather than editing generated output directly.
- Keep skill ownership boundaries explicit and avoid duplicating harness behavior, generic claim behavior, or project-local instructions.
- Update regression coverage so the bottom-up order, pass acceptance rules, persisted documentation mode, hybrid behavior, wiki capability handoffs, and final top-down reconciliation cannot silently regress.

## Acceptance Criteria

- The documented creation sequence remains project configuration through wiki and README in the required bottom-up order.
- Every pass states that it is reviewed against source evidence, accepted prerequisites, and current-pass requirements.
- Earlier passes do not require artifacts that are intentionally created only by later passes.
- BLOCKED semantics are consistent across the orchestration skill, affected artifact review contracts, templates, and examples.
- Documentation acceptance and implementation readiness are separately represented and can produce different outcomes without ambiguity.
- The methodology includes one final top-down semantic reconciliation after the full hierarchy exists and explicitly states that it supplements rather than replaces bottom-up work.
- PROJECT.yaml has a validated, persisted documentation-mode selection that supports hybrid wiki and specification processing.
- A bootstrap-selected hybrid mode survives handoff to later agents without relying on chat history.
- Hybrid mode preserves structured artifacts as authoritative and produces useful wiki navigation and synthesis without verbatim duplication.
- The wiki pass explicitly routes creation, topic writing, review, and verification to the corresponding project-wiki capabilities.
- Navigation, glossary, open decisions, known defects, and maintenance history have defined ownership and placement rules where applicable.
- Canonical sources, generated adapters, public documentation, metadata, templates, checklists, and regression expectations agree.
- Repository sweeps find no contradictory workflow order, obsolete gating language, or conversational-only documentation-mode selection.
- The implementation report lists files changed, exact behavioral clarifications, configuration or schema changes, validation results, and compatibility or migration considerations.

## Dependencies

None.

## Verification

- Review the completed change against the original feedback captured in this item and map every required outcome to repository evidence.
- Run the repository skill and bundle validation suite:

```bash
python3 scripts/validate-agent-skills.py skills
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
git diff --check
```

- Run any narrower tests added for documentation-mode parsing, template validation, generated representations, pass gating, and wiki orchestration before the full suite.
- Sweep canonical and generated content for conflicting pass order, BLOCKED semantics, documentation readiness language, documentation-mode fields, hybrid behavior, wiki capability names, and reconciliation direction.
- Independently review the changed methodology, configuration contract, templates, and wiki handoffs with the applicable structured artifact and skill review capabilities.

## Notes

- The final top-down pass is semantic reconciliation, not a reversed authoring workflow.
- Product defects and open design decisions remain visible evidence. Their existence alone does not make an accurate document unacceptable.
- Compatibility work must state how existing PROJECT.yaml files without a documentation-mode field are interpreted or migrated.
- Do not copy project-wiki implementation details into the reverse-engineering skill; invoke the owning capabilities and retain their contracts by reference.
