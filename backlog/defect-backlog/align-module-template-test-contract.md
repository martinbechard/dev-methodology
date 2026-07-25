# Align Module Design Template And Bundle Test Contract

Status: Ready

Type: Defect

## Summary

Align the create-module-design bundle-content test with the maintained module-design template contract for the Implementation Readiness section.

## Context

`python3 -m unittest scripts.test_bundle_content` fails in `test_planned_hld_and_module_creation_contracts`. The test expects the exact phrase `Begin this section with **READY.** or **BLOCKED.**`, while `skills/development-methodology/assets/templates/module-design-template.md` currently begins the instruction with `TODO: Immediately after the retained blockquote note, begin the authored section content with **READY.** or **BLOCKED.**`. The mismatch reproduces on baseline commit 4fe3c217 and current main.

Source Evidence: The user directed durable logging of confirmed defects in Codex thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a. The failing assertion is in scripts/test_bundle_content.py; the affected canonical template is skills/development-methodology/assets/templates/module-design-template.md.

## Requirements

- Determine whether the executable assertion or the intended template wording is authoritative.
- Make the test and canonical template contract agree without weakening the requirement that Implementation Readiness begins with READY or BLOCKED.
- Preserve the parallel Documentation Acceptance distinction and the required heading structure.
- Obtain exact canonical-path approval before changing any governed distributed skill definition.

## Acceptance Criteria

- `test_planned_hld_and_module_creation_contracts` passes using the project-supported Python interpreter.
- The module template still instructs authors to put READY or BLOCKED first in the Implementation Readiness content.
- The test verifies the intended semantic contract rather than an obsolete formatting fragment.

## Dependencies

None.

## Verification

- Run `python3 -m unittest scripts.test_bundle_content` and retain the result.
- Run the narrow affected test before the full module.
- Run the governed-definition approval check if the canonical template or a distributed skill is changed.
- Obtain fresh independent review.

## Notes

This is a baseline-reproduced regression, not a current-main-only failure. Do not implement a template or skill-definition change without the required approval manifest.
