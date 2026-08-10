# Make the Python Skill and Project Scripts Windows Portable

Owner: Dev Orchestrator

Status: Running

Type: Feature

Provider: file

Work Item ID: make-python-skill-and-project-scripts-windows-portable

Completion: main-branch

## Starting Handoff Evidence

Parent Coordination Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Dispatch Reservation: First normal multitask wave after terminology completion.

Normalized Objective: Make the Python skill and project Python scripts portable to native Windows and verify the complete tracked inventory.

Dispatch Requested At: 2026-08-10T00:44:00Z

Intended Root Role: Dev Orchestrator

Launch Result: Reserved; canonical root launch follows this committed transition.

Last Contact: 2026-08-10T00:44:00Z

Next Reconciliation At: 2026-08-10T00:59:00Z

## Active Execution Evidence

Condition Type: fresh-independent-review

Owner: Fresh independent code and methodology-artifact reviewers under visible Root Dev Orchestrator 019fe928-e2d8-7f91-91b2-bd27990a7414

Evidence: Both entirely fresh reviewers reached clean read-only checkpoints on exact candidate cbab82b1f65f9096aa8c6b7ae9d7794f690715ff and confirmed the clean 13-path range and diff hygiene. The methodology-artifact reviewer reports a provisional terminal NEEDS CORRECTION for one low-priority repository-maintenance rule breach: new README.md lines 781 and 783 use inline code formatting for unittest, excluded_cases, and killpg, while scripts/test_bundle_content.py line 1270 hard-codes one affected span; all substantive cleanup-evidence, README-strength, generated-freshness, provenance, skill, and negative-inventory checks are otherwise green. The code reviewer reports 28/28 focused contracts green and is validating whether the Windows wrappers prove bounded job-wide descendant reaping after TerminateJobObject rather than waiting only for the root. Its attempted local python3 command-smoke phase used an unsupported interpreter without tomllib and is not candidate evidence; no supported Python 3.11 rerun has started. Neither reviewer has mutated any state. Source remains frozen, and no native Windows pass is claimed.

Observed At: 2026-08-10T05:56:23Z

Started At: 2026-08-10T05:45:49Z

Deadline or Expires At: 2026-08-10T06:45:49Z

Next Action: Complete this provider transaction, reacquire the visible root's exact activity=work claim, release both fresh reviewers to finish terminal synthesis and any remaining supported read-only check, then record their exact terminal verdicts. Because this is the final authorized correction cycle, any confirmed finding or scope gap returns to the Parent Coordinator without source mutation or another correction attempt.

Next Reconciliation At: 2026-08-10T06:11:23Z

## Exceptional Recovery Manifest

Authorized By: Parent Coordinator 019fb057-1767-7ef2-b5fa-41f4417b20b3 on 2026-08-10T04:30:57Z

Preserved Candidate: 7cb7e0312f0ce7e077c903886f8235a69f84971e

Preserved Baseline: 16 authorized owners and 118 exact inherited identities, with resolutions remaining observable and no widening into those unrelated contracts.

Recovery Scope:

- Add Windows-selected root-plus-child process-tree cleanup tests for both changed cleanup paths.
- Make taskkill failure and descendant ownership fail closed.
- Capture ordinary unittest skips and reject every unclassified skip, including symlink-capability skips.
- Compare stable sanitized diagnostic signatures for authorized test baselines so a new Windows-specific cause under an existing test ID fails.
- Keep README evidence statements no stronger than behavior actually verified by the gate.

Recovery Constraints: Use only the Work Item's already-approved Windows-portability implementation, directly traceable tests, verifier, workflow, and documentation scope. Preserve non-destructive history, the canonical task identity, candidate 7cb7e031, and the inherited baseline. Do not mutate unrelated baseline contracts.

Cycle Limit: This is the final authorized correction cycle. After fresh independent review and verification, any unresolved finding or scope gap returns to the Parent Coordinator without another source correction attempt.

## Execution Identity

Canonical Conversation: Codex task 019fe928-e2d8-7f91-91b2-bd27990a7414; the runtime exposes one visible task/thread identifier for this execution

Root Agent Task: 019fe928-e2d8-7f91-91b2-bd27990a7414

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/make-python-skill-and-project-scripts-windows-portable

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/make-python-windows-portability-work-019fb057

Current Phase: Reviewing

Work-Item Claim: Visible claim python-windows-portability-visible-work-34-019fe928 was released with handoff at the fresh-review checkpoint; source remains frozen until the visible root reacquires the exact activity=work claim.

## Execution Handoff Reconciliation

Previous Root Agent Task: /root/python_windows_portability

Previous Disposition: Stopped at a clean handoff with no source mutation and released its exact claims.

Canonical Visible Task: 019fe928-e2d8-7f91-91b2-bd27990a7414

Reconciled At: 2026-08-10T00:58:46Z

Lifecycle Preservation: Status remains Running; Ready -> Starting and Starting -> Running were not repeated.

## Summary

Update the portable Python skill to require standard-library, cross-platform temporary-file handling and verify every tracked Python file in this repository against an explicit Windows compatibility contract. Correct project-owned portability defects and add native Windows verification so supported scripts do not depend on macOS or POSIX-only paths, commands, permissions, locking, or process behavior.

## Context

The current Python skill requires predictable resource handling but does not state how Python code should create temporary files and directories across operating systems. Runtime guidance separately recommends the Unix command mktemp, while native Windows does not provide that command. Python already supplies portable temporary-file APIs and operating-system-specific temporary-root selection through the tempfile module.

This repository currently contains 159 tracked Python files across scripts, distributed skill packages, evaluation harnesses, tests, and fixtures. No repository-native Windows CI workflow was found during creation. A macOS-only green test result therefore does not establish that project Python entry points work on Windows.

The audit must distinguish executable project tooling from deliberately platform-specific test fixtures without silently excluding either. Every tracked Python file remains in the inventory, and every exclusion or conditional test requires a documented reason and an observable Windows disposition.

## Source Evidence

On 2026-08-09 in canonical parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3, the user directed: “we should just use portable python - add a work item to adjust the python skill and verify all of the python scripts in this project so we can run them on windows.”

Creation-time discovery confirmed that skills/python/SKILL.md contains no temporary-file portability rule, that the repository contains 159 tracked Python files, and that no .github Windows workflow is currently present.

## Requirements

- Update skills/python/SKILL.md to require Python-owned temporary files and directories to use the standard-library tempfile APIs rather than shelling out to mktemp, PowerShell, or another operating-system command.
- Explain in the Python skill that tempfile selects the operating-system temporary root, can honor TMPDIR, TEMP, or TMP where supported, and should normally be used through context managers for deterministic cleanup.
- Require portable path and process handling through pathlib, shell-free subprocess argument vectors, supported executable discovery, and explicit operating-system branches only when behavior genuinely differs.
- Inventory every tracked Python file in the repository, including scripts, distributed skill helpers, evaluation harnesses, tests, and fixtures. Give every file an explicit Windows disposition: portable and exercised, corrected by this item, deliberately platform-specific with a bounded reason, or non-entry-point fixture data exercised by an owning test.
- Correct project-owned Windows portability defects found by the inventory. Cover path separators, drive and UNC paths, temporary roots, executable suffixes and discovery, environment variables, file locking, deletion of open files, symlink availability, permissions and modes, signals, subprocess behavior, and atomic file replacement when applicable.
- Ensure every supported Python command and test can run on native Windows without WSL, Git Bash, or Unix command emulation.
- Add a repository-owned native Windows verification route. It must compile or import every tracked Python file and run all supported project Python tests and command smoke checks, while reporting explicit classified exclusions rather than silently omitting files.
- Preserve intentional security and failure-boundary semantics. Do not weaken containment, path validation, atomicity, locking, or cleanup requirements merely to make a test pass on Windows.
- Document the supported Windows and Python versions and the local command that reproduces the same portability checks.

## Acceptance Criteria

- The Python skill explicitly directs Python implementations to use tempfile for portable temporary files and directories and does not require mktemp for Python-owned work.
- A committed inventory accounts for every tracked Python file, and an automated test fails when a new Python file lacks a Windows disposition.
- Every project Python entry point intended for users or repository maintenance runs on native Windows using documented commands.
- Every tracked Python file compiles or imports in its intended context on Windows, or has an explicit, tested platform-specific disposition with a concrete reason.
- Native Windows verification covers path, environment, temporary-file, subprocess, locking, cleanup, and file-replacement behaviors that differ from macOS or Linux.
- Windows checks do not require WSL, Git Bash, mktemp, Unix path roots, or POSIX-only shell commands.
- The native Windows verification route passes on the final main commit, along with the focused Linux or macOS regression checks for changed behavior.
- The Python skill, its generated or maintained documentation, the portability inventory, and the verification commands remain current under their owning freshness checks.

## Dependencies

- Ready defect `remediate-inherited-supported-test-baseline-failures` at `backlog/defect-backlog/remediate-inherited-supported-test-baseline-failures.md`, created in commit `8b7e883fa9217a96072801500155394b612c920f`; this records the authorized inherited baseline only and has no inferred dispatch or capacity reservation.

## Verification

- Validate skills/python/SKILL.md with the repository skill validator.
- Run the focused Python-skill contract test that proves tempfile guidance and rejects operating-system-command requirements for Python-owned temporary storage.
- Run the automated complete Python-file inventory check and prove an unclassified file fails it.
- Run Python compilation or import checks for every tracked Python file in a clean native Windows checkout.
- Run every supported project Python test and command smoke check on native Windows.
- Run focused cross-platform regressions for temporary paths, Windows drive and UNC paths, executable discovery, open-file cleanup, locking, symlink capability handling, subprocess invocation, and atomic replacement.
- Run affected generated-output freshness checks and git diff checks.

## Open Questions

- Which repository-native CI provider or local Windows execution environment should own the native Windows job when implementation begins?
- Which tracked Python files are intentionally platform-specific fixtures, and what equivalent Windows evidence is required for each owning behavior?

## Governed Definition Approval

### Governed Canonical Sources

- skills/python/SKILL.md

### Allowed Dependent Artifacts

- scripts/test_bundle_content.py
- scripts/test_python_windows_portability.py
- .github/workflows/python-windows.yml
- README.md

### Approval Resolution

Approved at creation. The user explicitly requested adjustment of the Python skill on 2026-08-09 in canonical parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3. This approval covers only skills/python/SKILL.md as the governed definition. Project Python implementation files may be changed only when the complete inventory identifies a concrete Windows portability defect within this work item; any additional governed skill or Agent definition requires separate exact-path authority.

## Notes

Python tempfile portability does not require exposing the resolved macOS /private path in user-facing output. Retained evaluation Evidence is not temporary data and should use an explicit caller-selected Artifact location rather than relying on a temporary directory that is expected to be cleaned automatically.
