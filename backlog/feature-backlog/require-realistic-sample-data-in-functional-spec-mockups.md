# Require Realistic Sample Data In Functional Specification Mockups

Status: Ready

Type: Feature

Provider: file

Work Item ID: require-realistic-sample-data-in-functional-spec-mockups

Completion: main-branch

## Summary

Add a dedicated mockups section to the functional specification template that requires realistic-looking sample data for every distinct mockup.

## Context

The functional specification template currently has an Interface Examples section with criteria for when a UI mockup is required. It does not state the data-fidelity contract for a mockup.

The motivating case has three heatmap mockup tables: Wall time, Tokens, and Models. The current specification supplied only one concrete sample. The missing samples make the other modes less observable and can hide mode-specific rows, units, empty states, and unavailable-value behavior.

Realistic-looking means fictional, internally coherent, representative of the documented domain, and detailed enough to exercise the visible contract. It does not mean production data, personal information, or company-internal information.

This outcome is a distinct extension of the completed Work Item `define-functional-specification-ux-mockup-criteria`. That item determines when proportionate interface examples are required. This item defines the sample-data fidelity required inside each mockup.

## Source Evidence

The user requested this enhancement on 2026-08-13: add a mockups section to the functional specification template that requires realistic-looking sample data. The user identified three heatmap mockup tables, Wall time, Tokens, and Models, for which the current specification supplied only one concrete sample.

Current repository evidence:

- `skills/route-documentation-work/assets/templates/functional-spec-template.md` contains Interface Examples guidance for proportionate UI mockups but no sample-data fidelity requirement.
- `skills/create-functional-spec/SKILL.md` defines when a UI mockup, wireframe, or interaction diagram is required but does not require realistic sample data for each distinct mockup.
- `skills/review-functional-spec/references/review-checklist-functional-spec.md` checks whether required mockups exist but does not check the fidelity or coverage of their sample data.

## Requirements

- Add a clearly identified Mockups section to `skills/route-documentation-work/assets/templates/functional-spec-template.md` without weakening the existing Interface Examples criteria.
- Require every distinct mockup, view state, mode, or materially different table to contain its own representative sample data when its visible contract differs.
- Require fictional sample values that look realistic for the documented domain and remain internally coherent across labels, identifiers, units, totals, timestamps, states, and related views.
- Require samples to expose mode-specific structure and behavior instead of relying on one concrete sample for several materially different mockups.
- Require the specification to distinguish zero, empty, partial, unavailable, error, loading, selected, or comparison states when those states affect the documented interface.
- Prohibit personal information, secrets, production data, and company-internal information in sample data.
- Label sample data as illustrative when a reader could mistake it for authoritative production evidence.
- Use the Wall time, Tokens, and Models heatmap tables as a focused regression case: each table must have realistic sample rows and values that demonstrate its distinct contract.
- Align the functional specification review checklist and focused regression coverage with the template requirement when needed to make the requirement observable.
- Preserve the existing rule that a UI mockup is required only when the documented layout, state, or interaction criteria apply.

## Acceptance Criteria

- The functional specification template contains a dedicated Mockups section with an explicit realistic-sample-data requirement.
- A specification with three materially different heatmap tables cannot satisfy the template by supplying concrete data for only one table.
- Wall time, Tokens, and Models examples each show representative rows, values, units, and applicable state semantics for that mode.
- Example values are fictional, plausible, internally consistent, and free of personal or company-internal information.
- The guidance explains when one shared data set is sufficient and when each mockup needs distinct data.
- Review guidance makes missing, generic, contradictory, or unsafe mockup sample data an observable finding.
- Focused tests fail when multiple materially distinct mockups rely on only one concrete sample and pass when each required mockup has coherent representative data.
- Existing proportionate-example and permitted no-example behavior remains intact.

## Dependencies

None.

## Verification

- Inspect the template, functional-specification creation guidance, and review checklist together for compatible terminology and normative force.
- Add focused regression coverage for one-sample versus three-sample heatmap specifications.
- Run the applicable bundle-content and generated-document freshness checks.
- Run `git diff --check` and obtain fresh independent review of the exact candidate.

## Open Questions

- Should the Mockups section be a child of Interface Examples or a peer section? Resolve this from template structure while preserving the required heading and data-fidelity contract.
- Which sample-data consistency checks are best expressed as template prose, review questions, or deterministic regression fixtures?

## Notes

- Do not require separate data when several mockups intentionally show the same entities across a state transition. In that case, preserve stable identifiers and explain the changed values or state.
- Do not turn realistic-looking sample data into fabricated source evidence or measured production results.
