# Recognize HTML Anchors In Markdown Link Validation

Status: Running

Type: Defect

Provider: file

Owner: Dev Orchestrator

Work Item ID: recognize-html-anchors-in-markdown-link-validation

Completion: main-branch

Canonical Conversation: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Root Agent Task: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Parent Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/recognize-html-anchors-in-markdown-link-validation

Worktree: /Users/martinbechard/.codex/worktrees/b07b/dev-methodology

Phase: Validator ownership discovery

## Summary

Make local Markdown link validation recognize explicit `id` anchors in linked HTML documents so valid Markdown-to-HTML fragment links do not fail verification.

## Context

README.md links to `design/agent-and-skill-definitions.html#hierarchy-title`. The target HTML contains an element whose explicit id is `hierarchy-title`, so browsers can resolve the link. The structured Markdown link verifier nevertheless returns `missing_anchor` for that target.

The false failure obscures real broken-link findings, prevents a clean documentation verification result, and has been repeated as a baseline warning in completed work without an active correction owner.

## Source Evidence

On 2026-08-06, while verifying the shared conditional Agent skill documentation, the structured Markdown link check inspected README.md and returned `missing_anchor` for `design/agent-and-skill-definitions.html#hierarchy-title`. Repository history in completed work items records the same result while confirming that the target HTML contains `id="hierarchy-title"`. The user instructed: "don't forget to log defects for corrections."

## Requirements

- Resolve fragment targets according to the linked file type.
- For HTML targets, recognize explicit `id` attributes as valid fragment destinations.
- Preserve existing Markdown heading-anchor validation for Markdown targets.
- Continue reporting a missing fragment when no matching HTML id or supported named anchor exists.
- Keep path traversal, missing-file, malformed-target, and unsupported-scheme checks unchanged.
- Add focused fixtures for valid and invalid Markdown-to-HTML fragment links.

## Acceptance Criteria

- The README link to `design/agent-and-skill-definitions.html#hierarchy-title` passes structured link validation without changing the valid target.
- A Markdown link to a nonexistent HTML fragment still reports `missing_anchor` with the source path and target.
- Markdown-to-Markdown fragment behavior remains unchanged.
- Focused validator tests cover explicit HTML ids, absent ids, duplicate ids if relevant, and encoded fragments if supported.
- Repository documentation link validation reports only genuine unresolved findings.

## Dependencies

None.

## Verification

- Run the focused Markdown-link validator tests for HTML fragment targets.
- Run structured Markdown link validation for README.md.
- Run structured Markdown link validation for the maintained documentation set.
- Run `git diff --check` in the repository that owns the validator correction.

## Open Questions

- Confirm whether the validator implementation is maintained in this repository or in the configured external tool package before assigning the implementation path.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T03:19:18Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Determine the validator ownership and correct Markdown-to-HTML fragment validation to recognize explicit HTML identifiers while preserving existing Markdown fragment and link-safety behavior.

Dispatch Time: 2026-08-07T03:19:18Z

Intended Root Role: Dev Orchestrator

Launch Result: Started

Canonical Execution: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Last Contact: 2026-08-07T03:21:54Z

Next Reconciliation At: 2026-08-07T03:34:18Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Evidence: The canonical root execution accepted the Starting handoff, established the clean work-item branch and worktree, and is determining the owning validator before bounded implementation.

Observed At: 2026-08-07T03:21:54Z

Started At: 2026-08-07T03:21:54Z

Deadline or Expires At: 2026-08-07T07:21:54Z

Next Action: Locate the structured Markdown-link validator owner, then assign exactly the owning implementation and focused tests.

Next Reconciliation At: 2026-08-07T03:36:54Z
