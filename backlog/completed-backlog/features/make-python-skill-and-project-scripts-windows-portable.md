# Make the Python Skill and Project Scripts Windows Portable

Owner: Dev Backlog Coordinator in user-authorized SOLO crisis recovery

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/make-python-skill-and-project-scripts-windows-portable.md

Work Item ID: make-python-skill-and-project-scripts-windows-portable

Completion: main-branch

Accepted Candidate Commit: 9eb990c01b45689a2de9d2699c93748bc9eaa28e

Delivery Commit: a2430012b0e95dce40f9d7fab814138c2ac24f59

Observed Main Commit: bf2744161e83b57e62627d671544f8e2c0e89429

Completed At: 2026-08-10T15:25:31Z

## Terminal Delivery Evidence

Completion Disposition: READY under the user's narrowed acceptance and explicit instruction to finish the item.

Integration: Main merge commit a2430012b0e95dce40f9d7fab814138c2ac24f59 contains accepted candidate 9eb990c01b45689a2de9d2699c93748bc9eaa28e. Current-main generated documentation was retained during the one conflict and then regenerated through its owning script in commit bf2744161e83b57e62627d671544f8e2c0e89429.

Integrated Verification: `/opt/homebrew/bin/python3.11 scripts/test_python_windows_portability.py` returned `PORTABLE_PREFLIGHT_PASSED` on `platform: darwin`, Python 3.11.13, with 63 supported test files and no Windows-specific failure or native-Windows claim. Focused portability contracts, process-cleanup tests, the Project Bootstrapper cleanup test, the bundle contract, Python compilation, Ruff, and Git diff validation had already passed for the accepted candidate.

Accepted Omissions: The user replaced the native-Windows execution requirement with documented portable APIs plus successful macOS behavior. Native Windows execution and another independent review cycle were therefore not required for terminal acceptance and are not claimed.

Main Observation: Main is clean at bf2744161e83b57e62627d671544f8e2c0e89429; the delivery merge is an ancestor of the observed tip and no integration residue remains.

Next Action: None for this Work Item. Continue the active SOLO crisis with the remaining crisis-set items.

## Active Crisis Epoch

Epoch ID: backlog-crisis-2026-08-10T06-32-31Z

Declared At: 2026-08-10T06:32:31Z

Coordinator: Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Trigger: The user explicitly retained crisis mode until all blocked work is completed, and current inventory contains six Blocked items.

Current Crisis Set:

- make-python-skill-and-project-scripts-windows-portable — native-Windows execution is no longer required; candidate reconciliation remains before terminal delivery.
- create-html-document-outlines-from-raw-information
- render-structured-explanations-as-html
- use-mcp-hierarchy-plans-for-complex-development
- align-orchestrated-development-lifecycle-with-documentation-design-system
- align-skills-modularization-with-documentation-design-system
- align-wiki-skills-and-project-context-with-documentation-design-system

Other Mutator Preservation: Canonical task 019fe9f2-a42b-77f2-9c2a-96c29e5f4e38 stopped at a safe boundary. Its source HEAD 1ac2a92e retains an unstaged ten-line scripts/test_bundle_content.py correction; primary main retains its staged provider-only phase update. No lifecycle, review, verification, integration, or cleanup continued after the pause.

Entry Reset: The configured live claim registry was reset exactly once after preservation. Reset outcome RESET; event d92acd9e-8839-43b6-aea0-116b74ab4751; live claims empty; audit journal retained.

Claim Boundary: No claim status, acquire, extend, heartbeat, release, report, maintenance, or additional reset operation is permitted after the entry reset until this crisis epoch exits.

Exit Condition: Every crisis-set item is Completed, Abandoned, or Superseded; no active item remains Blocked; no crisis or unrelated item is being changed; every crisis change is committed; and every combined regression has a concrete disposition.

## Starting Handoff Evidence

Parent Coordination Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Dispatch Reservation: First normal multitask wave after terminology completion.

Normalized Objective: Make the Python skill and project Python scripts portable to native Windows and verify the complete tracked inventory.

Dispatch Requested At: 2026-08-10T00:44:00Z

Intended Root Role: Dev Orchestrator

Launch Result: Reserved; canonical root launch follows this committed transition.

Last Contact: 2026-08-10T00:44:00Z

Next Reconciliation At: 2026-08-10T00:59:00Z

## Recovery Evidence

Corrected Candidate: 9eb990c01b45689a2de9d2699c93748bc9eaa28e

Corrected Findings: Both Windows CreateProcessW wrappers now pass inherited standard handles to the real child through STARTF_USESTDHANDLES. Every TerminateJobObject path polls JobObjectBasicAccountingInformation until ActiveProcesses is zero or the bounded cleanup deadline fails closed. The README and focused bundle assertion no longer use prohibited inline-code spans.

Local Verification: 28 portability contracts, two agent-skill cleanup tests, one Project Bootstrapper root-and-child cleanup test, the native-Windows README/workflow bundle assertion, Python 3.11 compilation, focused Ruff, and Git diff validation pass. The broader bundle file retains two unrelated existing unused-variable Ruff findings. No native Windows pass is claimed.

Remaining Gate: Reconcile the preserved 13-path candidate with current main without importing its long stale ancestry or replacing newer generated documentation. Then rerun the recorded macOS portability contracts and focused consumers before delivery.

Preserved Review Evidence: The terminal review findings are fully represented by the corrected source and focused contracts. Native Windows execution is explicitly waived. Candidate-to-current-main reconciliation, focused macOS verification, delivery, and provider closure remain outstanding.

## User Resolution

User Answer: "we're down to 5% of tokens - let's leave it at ensuring you only use documented portable APIs and that they work on mac"

Resolved At: 2026-08-10

Acceptance Disposition: Require documented portable APIs, deterministic portability contracts, and successful macOS execution. Do not require or claim native Windows execution, the Windows Server workflow, or a three-version Windows matrix.

External Attempt Evidence: Candidate branch 9eb990c0 was published after approval. Manual workflow dispatch returned HTTP 404 because python-windows.yml is absent from the remote default branch. Draft pull request 10 produced no checks for the same reason and was closed without merge. The candidate branch remains published.

## Current Blocker

Exact Blocker: A direct merge of the stale candidate ancestry into current main produced one generated-HTML conflict. Managed review rejected resolving and committing that broad merge because it would import Windows-specific changes beyond the newly narrowed acceptance without reviewed reconciliation. The merge was aborted cleanly; current main remains unchanged by the candidate.

Blocker Owner: Dev Backlog Coordinator under active SOLO crisis recovery.

Unblock Condition: Reconcile only the approved documented-portable-API and macOS-tested behavior from candidate 9eb990c0 onto current main, preserve newer generated documentation, run focused macOS checks, and complete delivery without claiming native Windows evidence.

Next Action: Continue this exact item as the current sequential crisis recovery when sufficient execution context is available. Do not repeat the rejected broad merge or reintroduce the external Windows gate.

Claim Disposition: Crisis-mode SOLO recovery uses no claim mechanism. No native Windows pass or integration is claimed.

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

Current Phase: Reviewing — Needs Correction

Work-Item Claim: Visible claim python-windows-portability-visible-work-36-019fe928 was released with handoff after terminal fresh review. No work claim will be reacquired without a new explicit Parent Coordinator disposition.

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
