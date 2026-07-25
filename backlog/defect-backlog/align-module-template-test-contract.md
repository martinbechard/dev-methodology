# Align Module Design Template And Bundle Test Contract

Status: Running

Type: Defect

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Align module design template and bundle test Implementation Readiness contract.
- Dispatched At: 2026-07-25T01:04:12Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

## Execution Ownership

- Work-Item Thread: 019f96ce-dd33-7bf2-bbe1-73e2af07da52
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Agent Task Id: 019f96ce-dd33-7bf2-bbe1-73e2af07da52
- Owner: Dev Orchestrator
- Branch: codex/align-module-template-test-contract
- Worktree: /Users/martinbechard/.codex/worktrees/1e75/dev-methodology
- Phase: diagnosis-and-implementation
- Started At: 2026-07-25T01:08:24Z
- Coordination: Enabled; agent-claim short backlog transaction completed before this provider mutation.
- Claim Evidence: backlog-starting-running-019f96ce-dd33-7bf2-bbe1-73e2af07da52; agent-claim event a731c430-1b5e-4da7-b30d-5999f2942bea; resource backlog:mutation:align-module-template-test-contract.

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
