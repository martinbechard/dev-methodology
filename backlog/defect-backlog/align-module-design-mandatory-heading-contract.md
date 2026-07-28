# Align module-design optional-section instructions with the mandatory heading contract

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/align-module-design-mandatory-heading-contract.md

Completion: direct-main

## Summary

Align module-design optional-section instructions with the mandatory heading contract.

## Context

The primary affected skill is skills/create-module-design/SKILL.md. The creation and review gates require every level-two heading, while the template directs authors to remove Configuration, External Interfaces, and UI And Notification Behavior when inapplicable. Following the template creates an artifact the required gates reject.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 20,85; skills/development-methodology/assets/templates/module-design-template.md:285,295,303; skills/review-module-design/SKILL.md:28; skills/development-methodology/SKILL.md:123. Independent reviewer /root/confirm_create_module_design accepted it as CONFIRMED_CRITICAL.

## Requirements

- Preserve the three mandatory headings and record why each is not applicable; make artifact-specific heading contracts override the generic section-removal rule.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Modules with no applicable content retain Configuration, External Interfaces, and UI And Notification Behavior with explicit not-applicable text.
- Creation and review gates accept the retained headings.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover all three headings with a module that has no applicable content.
- Require creation and review gates to accept retained not-applicable sections.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/create-module-design/SKILL.md. It does not authorize a skill-definition mutation. Each governed SKILL.md changed later requires its own exact scope-specific user approval, provenance record, and accepted pre-mutation check. The template is a separate supporting path and must remain aligned with approved skill changes.
