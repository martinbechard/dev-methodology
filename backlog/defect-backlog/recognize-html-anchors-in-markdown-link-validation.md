# Recognize HTML Anchors In Markdown Link Validation

Status: Starting

Type: Defect

Provider: file

Owner: Unowned

Work Item ID: recognize-html-anchors-in-markdown-link-validation

Completion: main-branch

Canonical Conversation: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Root Agent Task: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Parent Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/recognize-html-anchors-in-markdown-link-validation

Worktree: /Users/martinbechard/.codex/worktrees/b07b/dev-methodology

Phase: External delivery accepted; canonical verification resumption

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

Starting Recorded At: 2026-08-08T17:26:18Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: Resume the preserved Root Dev Orchestrator task for this exact work item.

Normalized Objective: Accept the authorized external delivery evidence, verify the maintained dev-methodology README link through the delivered validator, and perform terminal file-provider closure when the focused completion checks pass.

Dispatch Time: 2026-08-08T17:26:18Z

Intended Root Role: Dev Orchestrator

Launch Result: Started

Canonical Execution: 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Last Contact: 2026-08-08T17:26:18Z

Next Reconciliation At: 2026-08-08T17:40:00Z

## Prior Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fda3c-1c2a-7061-9b3b-3deb3db114cd

Evidence: The canonical root execution accepted the Starting handoff, established the clean work-item branch and worktree, and is determining the owning validator before bounded implementation.

Observed At: 2026-08-07T03:21:54Z

Started At: 2026-08-07T03:21:54Z

Deadline or Expires At: 2026-08-07T07:21:54Z

Next Action: Locate the structured Markdown-link validator owner, then assign exactly the owning implementation and focused tests.

Next Reconciliation At: 2026-08-07T03:36:54Z

## User Action Required

Recorded At: 2026-08-07T03:29:36Z

### Question for the User

Do you approve re-homing implementation of recognize-html-anchors-in-markdown-link-validation to /Users/martinbechard/dev/mcp-agent-ops, with source mutation and direct-main delivery authority limited to src/mcp_agent_ops/verification/markdown_links.py and tests/unit/verification/test_markdown_links.py, followed by verification against dev-methodology README.md and terminal closure of the original dev-methodology file-provider work item?

### Why User Input Is Required

The owning validator is outside dev-methodology. Source mutation and direct-main delivery in the external repository require the user's authority.

### Explicit Exclusions

No other mcp-agent-ops files, package release/version/tag/publication, broad suite, framework, dev-methodology source mutation, or unrelated cleanup is authorized.

### Reproduced Evidence

The structured verify_markdown_links check against dev-methodology README.md returns missing_anchor for design/agent-and-skill-definitions.html#hierarchy-title. The target HTML contains the explicit id hierarchy-title.

### External Repository Evidence

The external primary /Users/martinbechard/dev/mcp-agent-ops was clean at 89f2df0d80fc91f3944849b5387e4ac82ba79e40. Zero external source or test mutation occurred. The temporary external branch and worktree were removed.

### Work Claim and Blocker Evidence

Work claim recognize-html-anchors-work-019fda3c was released with disposition blocked, blocker reference external-repository-authority-required:mcp-agent-ops, and release event 7fff15f1-f0aa-423e-bd63-a87eb1f99586. The original zero-mutation discovery history remains preserved above.

### Resolution

Answered and approved on 2026-08-08. In external canonical task `019fe259-29e9-7be2-8edd-036ff256b631`, the user supplied the exact bounded execution prompt authorizing implementation and direct-main delivery in `/Users/martinbechard/dev/mcp-agent-ops`, limited to `src/mcp_agent_ops/verification/markdown_links.py` and `tests/unit/verification/test_markdown_links.py`, with all recorded exclusions preserved. This direct user instruction resolves the recorded authority question; it is not inferred from technical access or delivery success.

### Unattended Work Boundary

The user-authority boundary is satisfied. Resume only through Ready -> Starting -> Running in the preserved canonical task before dev-methodology verification or terminal provider closure. No additional external source mutation, release, publication, installation, dev-methodology source change, or unrelated cleanup is authorized.

## External Delivery Evidence

External Task: `019fe259-29e9-7be2-8edd-036ff256b631`

External Repository: `/Users/martinbechard/dev/mcp-agent-ops`

Accepted Candidate and Main Commit: `a06549b3b57472814a87c1cd9c03e6a2e4420861`

Baseline: `89f2df0d80fc91f3944849b5387e4ac82ba79e40`

Changed Paths: `src/mcp_agent_ops/verification/markdown_links.py`; `tests/unit/verification/test_markdown_links.py`

Review: Independent review GOOD with no findings on the accepted commit.

Verification: Nine focused tests passed; targeted Ruff, mypy, and `git diff --check` passed; a clean checkout at the exact main commit remained clean.

Delivery: External local `main` fast-forwarded to the accepted candidate. The candidate is ancestral to external `main`; no push, release, tag, publication, packaging, deployment, installation, or version change occurred.

Operational Limitation: The external primary checkout contains only untracked `.codex/agent-claim/` operational state created by its configured claim helper. A clean verification checkout at the exact main commit is clean. No out-of-scope ignore or metadata change was made.

Recovery Evidence: Accidental local commit `7c00444e9c713ebba6f56895b7176b3dfb36c164` was restored exactly to the baseline before accepted delivery, never pushed or published, and is not on final external `main`.

Next Action: Preserve this evidence, record Ready -> Starting for canonical task `019fda3c-1c2a-7061-9b3b-3deb3db114cd`, then have that same root execution record Starting -> Running, verify the maintained README link with the delivered validator, and perform terminal closure only if the configured completion checks pass.
