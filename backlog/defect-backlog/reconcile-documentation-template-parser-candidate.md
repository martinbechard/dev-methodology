# Reconcile Documentation Template Parser Candidate

Status: Running

Type: Defect

Provider: file

Work Item ID: reconcile-documentation-template-parser-candidate

Completion: main-branch

## Summary

Reassess the abandoned documentation-template parser hardening against current main and port only behavior that remains missing.

## Context

The branch codex/enforce-documentation-template-conformance-b948-correction3 at 6fd28466768643c05d1332a101df994089e2b3cb contains four parser and fixture commits. It covers context grammar, container boundaries, readiness parsing, command inventory, path resolution, contradiction checks, and deterministic regression cases.

The branch was previously judged mergeable, but a fresh non-mutating merge against current main now conflicts in validate_fixture.py and test_fixtures.py. Current main changed those same maintained surfaces after the review baseline. The branch must not be merged through automatic conflict selection.

## Source Evidence

On 2026-08-12, the user approved preserving the branch's useful outcome before deleting legacy worktrees. Fresh integration reconciliation found content conflicts against current main, requiring a replacement work item rather than direct integration.

## Requirements

- Compare all four branch commits with the current documentation-writer template-conformance fixture and tests.
- Classify each parser rule and regression case as already covered, obsolete, or a current defect.
- Port only confirmed current-main gaps using the present parser structure.
- Preserve current template, context, readiness, command, path, and contradiction semantics.
- Do not restore stale fixture structure or resolve conflicts by selecting an entire branch version.

## Acceptance Criteria

- Every distinct candidate behavior has a recorded disposition.
- Confirmed gaps have focused current-main regression tests.
- Existing accepted documentation-template behavior remains intact.
- The legacy branch is unnecessary for future implementation after this record is committed.

## Dependencies

None.

## Verification

- Inspect commits f016c8619d68d535e274b4bba8d6b9c0284a3c07, 0483c6d117503370d4371ba5d8f8ca909538d0b2, b9483a3997c720352edcfa2e98e87f894ae34bcc, and 6fd28466768643c05d1332a101df994089e2b3cb.
- Run the focused Dev Documentation Writer template-conformance fixture tests.
- Run git diff --check.
- Obtain independent review of every retained or rejected behavior.

## Open Questions

None.

## Notes

- The legacy branch and worktree can be deleted after this work item is committed and verified.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T11:43:11Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e8923f2cb1fe967806a0542359d15af01d94ac19` on primary `main`.
- Capacity: Slot 5 of 5. Independent Dev Documentation Writer parser-fixture scope; exclude private Backlog Dispatcher, provenance, evaluation terminology, and Dev Orchestrator routing paths.
- Transition Claims: `start-reconcile-documentation-template-parser-candidate-work-item`; event `15cd995b-42fc-4349-b444-1e6285b3566d`. `start-reconcile-documentation-template-parser-candidate-provider`; event `2a464966-4444-480a-ad81-fc595bbe1e79`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T11:46:27Z.
- Codex Task ID: `019ffaf1-8f30-7470-b274-de3293c49bec`.
- Conversation ID: `019ffaf1-8f30-7470-b274-de3293c49bec`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Documentation Template Parser Candidate`.
- Initial Action: Launch one Dev Orchestrator subagent for this authoritative provider record.
- Creation Outcome: Unique success decoded from a complete JSON-string envelope, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-reconcile-documentation-template-parser-candidate-visible-task`; event `e19fe050-5824-40ea-8e61-7bcc73f3889a`. `adopt-reconcile-documentation-template-parser-candidate-provider`; event `c2558b55-6929-4697-ab70-1ba6646d4e99`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T11:47:54Z.
- Transition: `Starting -> Running`.
- Owner: Dev Orchestrator.
- Canonical Conversation ID: `019ffaf1-8f30-7470-b274-de3293c49bec`.
- Canonical Codex Task ID: `019ffaf1-8f30-7470-b274-de3293c49bec`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: implementation planning and current-main reconciliation.
- Accepted Execution Evidence: The canonical Dev Orchestrator acquired work-item update ownership and accepted the normalized assignment on the reserved primary-main execution.
- Next Action: Compare the four candidate commits with current main, review a bounded implementation and TDD plan, then port only confirmed gaps.

## Candidate Behavior Dispositions

The current-main comparison classified all 31 distinct candidate behaviors as `Already covered`. No candidate behavior is obsolete, and no current defect remains.

1. `Already covered` — Require the contract-owned `docs/inventory-normalization-module-design.md` artifact and read evidence only from that path.
2. `Already covered` — Resolve required source and test paths relative to the artifact, and reject absolute, escaping, nonexistent, or missing references.
3. `Already covered` — Run artifact tests through a copied fixture so relative resolution is exercised without changing the source fixture.
4. `Already covered` — Parse backtick and tilde fences, HTML comments, visible prose, and structural prose separately, and reject unclosed containers.
5. `Already covered` — Count only top-level level-two headings while retaining nested blockquote headings as visible prose.
6. `Already covered` — Read readiness from the first visible line and accept only plain or balanced-bold `READY.` and `BLOCKED.` leads.
7. `Already covered` — Require exactly one command-only `bash`, `sh`, or `shell` fence and inventory its complete non-comment lines.
8. `Already covered` — Detect runnable commands outside that fence in directives, inline code, non-shell fences, quoted prose, and list items.
9. `Already covered` — Recognize assignments, shell operators, runner names, and `command`, `exec`, `nohup`, `env`, `sudo`, and `timeout` wrappers.
10. `Already covered` — Exclude explanatory Node prose from runnable-command detection.
11. `Already covered` — Inventory local inline, full-reference, and shortcut-reference links with normalized labels, angle-bracket destinations, and titles.
12. `Already covered` — Prevent external reference destinations from replacing required local evidence while allowing unrelated external references.
13. `Already covered` — Evaluate coverage claims from visible prose while retaining negative disclaimers and bounded source-only or success-path context.
14. `Already covered` — Reject the six original source-coverage contradiction forms.
15. `Already covered` — Ignore hidden required disclaimers, commands, and contradiction prose according to visible-evidence semantics.
16. `Already covered` — Treat HTML comment markers inside a fence as literal fenced content.
17. `Already covered` — Treat nested blockquote disclaimers and contradictions as visible evidence-bearing prose.
18. `Already covered` — Verify that routed-authoring deterministic check identifiers exist in the Judge catalog.
19. `Already covered` — Derive the source-test count from the subprocess result while disabling bytecode writes.
20. `Already covered` — Exclude inline-image and reference-image destinations from source and test evidence.
21. `Already covered` — Track blockquote depth for fences so quoted fences cannot supply headings, commands, paths, or coverage evidence.
22. `Already covered` — Treat HTML comment markers inside quoted fences as literal content.
23. `Already covered` — Reject a fence closed from a different blockquote container.
24. `Already covered` — Recognize `To verify, run`, `env -u`, `timeout -s`, and adjacent shell-segment command forms.
25. `Already covered` — Extend contradiction grammar to checks and suites, including the three added contradiction cases.
26. `Already covered` — Detect an imperative command after an introductory clause such as `After editing, run`.
27. `Already covered` — Avoid treating bare connective `that` as source-branch anaphora.
28. `Already covered` — Recognize comma, colon, and whitespace separators after `After editing`.
29. `Already covered` — Do not extend an HTML comment across a blockquote-depth change; expose the intervening command and mark the container invalid.
30. `Already covered` — Reject fence content crossing from quoted to unquoted containers.
31. `Already covered` — Reject fence content crossing from unquoted to quoted containers.

The legacy whole-file context is rejected because it points at the retired `skills/development-methodology` template path and outdated scenario skill names. Current main uses `skills/route-documentation-work` and adds stricter bold-command and `command --` detection. Restoring either legacy file wholesale would regress accepted current behavior.

## Independent Review And Verification Evidence

- Dev Architect: `ACCEPT`; the no-source-change plan is the smallest sound approach.
- Dev Code Reviewer: `PASS`; all 31 dispositions are accepted with no material findings.
- Dev Verifier: `VERIFIED — PASS`; all four commit objects exist, both candidate paths are clean, and the bounded legacy-tip comparison found no removed behavior.
- Focused Check: `PYTHONDONTWRITEBYTECODE=1 python3 evals/agent-tests/dev-documentation-writer/test_fixtures.py` passed 38 tests.
- Whitespace Check: scoped `git diff --check` passed for `validate_fixture.py` and `test_fixtures.py`.
- Source Candidate: No source change and no empty commit are justified. The legacy branch is unnecessary for future implementation after this record is delivered.
