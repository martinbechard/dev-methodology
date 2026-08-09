# Correct the Skill Group Registry Section Test

Status: Ready

Type: Defect

Provider: file

Work Item ID: correct-skill-group-registry-section-test

Completion: main-branch

## Summary

Correct the resource-helper regression test so it reads the maintained Skill Group Registry section at its current heading and continues to verify the registry totals and inventory prose.

## Context

The focused command `python3 -m unittest -v scripts.test_resource_claim_helper` fails in `test_skill_group_inventory_prose_matches_the_registry_total`. The test asks `_markdown_section` for the exact heading `3. Skill Group Registry`, while `design/object-oriented-skill-group-models.md` currently contains the registry under `3.2 Skill Group Registry`. The resulting `ValueError: substring not found` prevents the intended count assertions from running. The maintained registry exists; the defect is the stale section lookup, not a missing registry.

## Source Evidence

During evaluation-protocol maintenance on 2026-08-09, the focused resource-helper suite reproduced the failure. The user then asked whether a defect work item had been created for the reported unrelated failure. Repository maintenance guidance requires an unrelated focused failure to be recorded as a distinct defect rather than absorbed into the active change.

## Requirements

- Update the focused test to locate the current Skill Group Registry section without weakening its ownership or count assertions.
- Preserve the intended checks that the registry totals forty-seven skills, the maintained prose uses the matching total, and stale forty-four wording is absent.
- Determine whether the section lookup should use the exact current numbered heading or a stable bounded heading-selection helper.
- Do not rename or restructure the maintained design merely to satisfy a stale test unless independent document evidence requires that change.

## Acceptance Criteria

- `test_skill_group_inventory_prose_matches_the_registry_total` reaches and evaluates all intended assertions.
- The focused resource-helper test module passes except for independently recorded unrelated failures, if any.
- A negative regression proves that a missing or ambiguous Skill Group Registry section still fails clearly.
- The change is limited to the owning test/helper unless source-backed discovery proves a maintained-document defect.

## Dependencies

None.

## Verification

- Run the corrected focused test directly.
- Run `python3 -m unittest -v scripts.test_resource_claim_helper`.
- Run Python compilation and Ruff for every changed Python path.
- Run `git diff --check`.

## Open Questions

- Should `_markdown_section` accept a stable section title independently of numeric prefixes, or should this test bind intentionally to `3.2 Skill Group Registry`?
