# Harden Event Contract Claim-Helper Scope Identity And Reporting

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/harden-event-contract-claim-helper-scope-identity-and-reporting.md

Completion: direct-main

## Summary

Correct five verified claim-helper defects so an Event Contract claim has one stable normalized repository-relative path identity, cannot cross from a resource-only claim into the primary backlog, cannot be acquired without scope, requires a reason for broad backlog ownership, and appears as a successful exact-file adoption in reporting.

## Context

The command helper implements claim scope parsing, acquisition, extension, conflict checks, and journal reporting in skills/agent-claim-command/scripts/claim.py. The published event-driven exact-file policy at commit 6e59985b8cd0280e729f56eb8d2d362adf3f4ab6 is current main policy. The superseded feature record preserves review evidence that its correction candidate f412674259b246bb0e3bb11edd569982e60c4c89 was unaccepted; this defect is the separate active repair package and does not adopt that candidate.

## Source Evidence

- Parent-authorized reconciliation direction on 2026-07-26 explicitly requests one grouped Ready Defect for five current verified helper defects: case-alias identity overlap; linked resource-only extension into backlog; scope-less acquisition; broad backlog missing reason; and missing successful exact-file report adoption.
- backlog/completed-backlog/features/use-exact-work-item-claims-for-lifecycle-updates.md records the historical case-alias and linked resource-only findings, the preserved root identity, and the supersession boundary.
- skills/agent-claim-command/scripts/claim.py contains the current scope, extension, and report behavior; scripts/test_agent_claim.py contains existing exact-file, resource-only, broad-backlog, and report test coverage that must be hardened.

## Requirements

- Treat a claim identity as its stable normalized repository-relative path, with case normalization when required by the repository filesystem; the recorded active scope remains unchanged after acquisition.
- Do not promise or test detection of mutable symlink, hard-link, inode, mount, or post-acquisition alias changes.
- Reject an extension from a resource-only claim into any backlog scope, including an exact backlog file, without mutating the existing claim.
- Reject acquisition with no file, tree, broad-domain, or named-resource scope.
- Require a non-empty documented scope reason for a broad backlog claim and retain that reason in durable claim and journal evidence.
- Extend report data and rendering so a successful exact-file claim can be identified as adopted successfully rather than disappearing into only generic primary acquisition totals.
- Add focused regressions for each defect and preserve valid non-overlapping stable-path exact-file concurrency.

## Acceptance Criteria

- In a disposable case-insensitive checkout, acquiring a case-varied alias of an already claimed exact file returns the configured conflict outcome and leaves one owner.
- A resource-only claim extended with an exact path under backlog returns a structured rejection, preserves its resource-only scope, and creates no backlog ownership.
- An acquire command with required identity arguments but no scope returns a structured invalid-scope outcome and writes no live claim.
- A broad --backlog acquire without --scope-reason returns a structured invalid-scope outcome; with a reason, the reason is present in the claim and journal event.
- A report covering a successful exact-file acquire and release exposes that successful exact-file adoption in machine-readable output and any matching text rendering.
- Focused tests pass without weakening the stable-path Event Contract assertions.

## Dependencies

None.

## Verification

- Run the focused scripts/test_agent_claim.py cases for the five reproductions and the non-overlapping exact-file control.
- Add and run focused unit tests for stable path normalization, resource-only extension, empty scope acquisition, broad backlog reason validation, and report adoption output; exclude mutable filesystem-alias detection from the verification boundary.
- Run git diff --check and an independent review of the changed helper and tests.

## Open Questions

None.

## Current Starting Reservation

- Parent Coordination Thread: /root.
- Reservation: One parent-owned Ready -> Starting launch reservation.
- Normalized Objective: Harden Event Contract claim-helper scope identity and reporting.
- Intended Root Role: Dev Orchestrator.
- Persistence And Completion: file provider; direct-main completion.
- Dispatched At: 2026-07-26T14:49:01Z.
- Launch Evidence: Parent Coordinator authorized this exact-item reservation. Runtime task creation and acceptance remain pending.
- Backlog Claim: reserve-starting-harden-event-contract-019f9ea6.
- Backlog Claim Event: 177de9e2-aade-4273-9025-67083bab0cde.
- Canonical Execution Identity: Thread and task 019f9ea6-6328-7580-9213-6e60b3a9de76; parent coordination thread /root; worktree /Users/martinbechard/.codex/worktrees/8b79/dev-methodology; intended candidate branch codex/harden-event-contract-claim-helper-019f9ea6.
- Next Lifecycle Owner: the same root Dev Orchestrator must record a distinct Starting -> Running acceptance before artifact mutation.

## Prior Running Acceptance Evidence (Superseded)

- Canonical Thread: 019f9ea6-6328-7580-9213-6e60b3a9de76.
- Canonical Root Agent Task: 019f9ea6-6328-7580-9213-6e60b3a9de76.
- Root Role: Dev Orchestrator.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Worktree: /Users/martinbechard/.codex/worktrees/8b79/dev-methodology.
- Intended Candidate Branch: codex/harden-event-contract-claim-helper-019f9ea6.
- Phase: superseded by the later Ready state and retained as recovery history.
- Started At: 2026-07-26T13:45:21Z; root Orchestrator accepted the reserved work item before implementation mutation.
- Backlog Claim Acquisition: claim start-running-harden-event-contract-019f9ea6; event e5a63bff-dc75-462b-8104-5b17da793a4c; acquired from primary main at f1c8c04c4a24be8e48579fc997d1a6f09daacf88.
- Backlog Claim Release: due immediately after this short provider commit; release evidence is retained in the claim journal.

## Current Running Acceptance

- Canonical Thread And Root Agent Task: 019f9ea6-6328-7580-9213-6e60b3a9de76.
- Root Role: Dev Orchestrator.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Worktree: /Users/martinbechard/.codex/worktrees/8b79/dev-methodology.
- Intended Candidate Branch: codex/harden-event-contract-claim-helper-019f9ea6.
- Phase: user-corrected stable-path implementation.
- Started At: 2026-07-26T14:50:37Z; the root Orchestrator accepted the durable Starting reservation before artifact mutation.
- Backlog Claim Acquisition: claim accept-stable-path-harden-event-contract-019f9ea6; event 5460f6f6-76e9-412a-95a0-1a54d7aa9090; acquired on primary main at 28839ee0484e236de15aed3268506097ee37b8ab.

## Material Phase Evidence

- Candidate: 9ae3dd286490e3f3e8dd14066d1c72676d86c3d4.
- Candidate Paths: scripts/test_agent_claim.py and skills/agent-claim-command/scripts/claim.py only.
- Dev Coder Red/Green Evidence: the candidate adds focused reproductions for each of the five assigned Event Contract defects and the valid non-overlapping exact-file control; the red reproductions were used to drive the correction and the focused suite was green for the submitted candidate.
- Fresh Review Disposition: REJECTED.
- Review Finding: HIGH — future nonexistent case aliases and unexpected samefile OSError paths fail open, so a conflicting exact-file claim can be admitted.
- Correction Attempt: 1, assigned to the original Dev Coder against the same candidate scope.
- Integration And Verification: no integration or final verification has been accepted; correction and fresh review remain required.

## Stable-Path Candidate Review

- Candidate: 437ad55782223b2f9c7f443c44254c3028ede6ce.
- Candidate Paths: scripts/test_agent_claim.py and skills/agent-claim-command/scripts/claim.py only.
- Evidence: 24 focused and edge tests passed, together with compilation and git diff --check.
- Fresh Review Disposition: REJECTED.
- Review Finding: HIGH — new requests are normalized and casefolded, but pre-upgrade live claim files and trees are compared verbatim; on an insensitive filesystem, a legacy README.md claim and a new readme.md request can coexist.
- Correction Attempt: 1, assigned to the original Dev Coder. Normalize stored file and tree identities for comparison only using the same lexical and case rules; do not resolve targets or inodes and do not mutate the registry.
- Required Regression: add a public regression that seeds a legacy stored claim and then submits the new request.
- Verifier And Integration: no verifier or integration has been accepted.

## Replacement Candidate Review

- Replacement Candidate: b803c1ba70db747915218e08ecd64de8c059555e, atop rejected candidate 9ae3dd286490e3f3e8dd14066d1c72676d86c3d4.
- Fresh Review Disposition: REJECTED.
- Review Finding 1: HIGH — a dangling symlink to a nonexistent target can be claimed concurrently with that target.
- Review Finding 2: HIGH — the fail-closed boolean identity result silently deduplicates or drops requested ownership during multi-file acquisition.
- Rejection History: two candidate attempts have now been rejected.
- Current Disposition: artifact mutation is paused for parent investigation and a revised plan.
- Verifier And Integration: no verifier result or integration has been accepted.

## Parent Investigation And Final Correction Contract

- Parent ACK: 2026-07-26 acknowledgement from parent coordination thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a authorizes one final correction attempt under this contract.
- Identity Contract: every identity comparison must return explicit SAME, DIFFERENT, or ERROR.
- Identity Error Handling: an ERROR during normalization rejects the whole acquire as INVALID_SCOPE, preserves registry and journal bytes unchanged, and drops no requested path.
- Conflict Error Handling: an ERROR during conflict comparison is treated as overlap.
- Dangling Symlink Handling: reject a dangling symlink until its target exists, including when the target is a sibling requested in the same acquire.
- Mandatory Public Command Regressions: prove atomicity, no live claim, unchanged bytes, dangling-symlink target behavior, existing aliases, hard-link aliases, and injected samefile OSError behavior.
- Permitted Checks: cumulative targeted tests, compilation, and git diff --check only.
- Required Gates: a brand-new review and verifier must both pass before any integration.
- Retry Boundary: any fresh material finding prohibits further Dev Coder retry and requires Running -> Blocked with Owner: Unowned.

## User-Authorized Blocked Resolution

- User Answer: on 2026-07-26, in canonical task 019f9ea6-6328-7580-9213-6e60b3a9de76, the user explicitly corrected the contract after the filesystem-alias explanation and said, "ok carry on."
- Provenance: user direction relayed through the parent coordination thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Revised Authority: symlinks may be rewritten after acquisition. Mutable symlink, hard-link, inode, mount, and post-acquisition alias guarantees and tests are logically unhelpful and disproportionate; changing filesystem aliases does not alter recorded active scope.
- Superseded Recovery Evidence: the prior candidate and review history, including the alias-specific findings and final-correction contract, remains preserved as superseded recovery evidence only.
- Resumption Authority: the item is Ready and awaits a separate same-task parent-owned Ready -> Starting reservation, followed by root-owned Starting -> Running acceptance. This transaction does not reserve or dispatch it.

## Blocked Final Review Handoff

- Canonical Execution Identity Preserved: Thread and task 019f9ea6-6328-7580-9213-6e60b3a9de76; parent thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a; worktree /Users/martinbechard/.codex/worktrees/8b79/dev-methodology; branch codex/harden-event-contract-claim-helper-019f9ea6.
- Rejected Candidate Chain: 9ae3dd286490e3f3e8dd14066d1c72676d86c3d4 -> b803c1ba70db747915218e08ecd64de8c059555e -> 0c8eb0af7b1286e63d1a4607c16d49f41a4dddac.
- Final Fresh Review: REJECTED, HIGH — _normalize_repository_path checks only the final requested-path symlink. A dangling parent component (dangling-dir -> missing-dir) permits concurrent exact claims for dangling-dir/child.py and missing-dir/child.py, which become aliases when the target directory exists.
- Evidence: material checks passed, including targeted review tests, py_compile, git diff --check, and clean candidate branch observation.
- Delivery State: no verifier, no integration or main artifact claim, no accepted candidate, and no completion or archive.
- Claims: None after this provider transaction's truthful release.
- Exact Unblock: explicit authorization plus a fresh bounded design and implementation plan that inspects every requested path component and rejects unresolved symlink components; adds a public-command regression for the nested dangling alias and target; and re-runs a new independent review and verifier.
- Resumption: only Blocked -> Ready -> Starting -> Running in this same canonical task. No correction attempt 3 is authorized under this lifecycle.

## Notes

- Reproduction 1: on a case-insensitive disposable primary checkout, acquire one exact file and then acquire the same file through a case-varied alias; the second claim must conflict.
- Reproduction 2: acquire one named resource only, then extend that claim with an exact backlog file; current coverage permits a resource-only claim to enter a non-overlapping file scope, so backlog-domain crossing needs an explicit regression.
- Reproduction 3: invoke acquire with claim identity arguments but no scope selector; the helper must not create a scope-less claim.
- Reproduction 4: invoke acquire with --backlog but no --scope-reason; broad backlog ownership needs the documented justification required by the Event Contract.
- Reproduction 5: acquire and release one exact file successfully, then run report --format json; report output must retain a distinguishable successful exact-file adoption signal.
- Creation authority is the parent-authorized grouped-defect request. This direct-main Ready record is unowned until normal Coordinator dispatch. Claim evidence for creation: None; Event Contract creation is claim-free.
