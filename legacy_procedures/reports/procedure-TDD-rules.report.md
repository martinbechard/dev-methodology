# Migration Report: Unit and Integration Testing Rules

## Source

- [Legacy procedure](../procedure-TDD-rules.md)

## Purpose and Scope

The procedure mandates a strict red-green-refactor loop for feature, bug-fix, and refactoring work. It also defines test planning, focused and broader test execution, test structure, failure diagnosis, project logging, review, and dependency follow-up. Much of its detail assumes one former TypeScript project, its documentation registry, tracer, commands, and status files.

## Worthwhile Durable Guidance

- Establish the intended behavior and success criteria before implementation; use the applicable design, contract, and existing project guidance as evidence.
- For a behavior change, add a small, specific regression test before implementation when the change can be tested. Confirm that it fails for the expected reason, then make the smallest change that makes it pass.
- Work one behavior at a time. Start with a focused test, then run the relevant broader suite and proportionate build or type checks after the change and after any refactor.
- Test observable behavior and contracts. Keep mocks at external boundaries, introduce them only when the current scenario needs them, and keep fixtures and setup readable.
- Treat an unexplained failing test as active work. Reproduce it, inspect the failure and available logs before changing code, distinguish product defects from environment failures, and escalate unresolved requirements rather than silently changing business behavior.
- Keep test suites intelligible by splitting genuinely unwieldy suites along behavioral boundaries. Integration scenarios deserve isolated setup and independent review when their complexity requires it.
- Reassess callers and dependents when a public contract changes, and preserve code-review and verification evidence in the task handoff.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Coverage | Recommendation |
| --- | --- | --- | --- |
| Design and plan alignment before coding; clarify changed business rules | Careful Coding; Coding Agent; Development Methodology and module-design skills when artifacts exist | Partial | Add an explicit pre-implementation rule: inspect the applicable requirement, design, contract, and repository guidance; ask when they conflict or do not establish the intended behavior. Do not require a specific documentation topology. |
| Red-green-refactor, one behavior at a time, and minimal implementation | New Test-Driven Development skill; Careful Coding; Coding Agent | Missing | Create a framework-neutral skill that defines the testable-change loop and delegates runner syntax to Jest, Vitest, or project-local guidance. |
| Focused test first, then module/broader tests and build | Jest; Vitest; QA And Verification Agent | Partial | Preserve the focused-to-broader sequence, but make breadth risk-based and report skipped or environment-blocked checks. |
| Contract-focused assertions, boundary mocks, readable fixtures, failure modes | Jest; Vitest; Coding Agent | Complete | Keep the current guidance; no migration change is required. |
| Test plans tied to intended behavior | New Test-Driven Development skill; QA And Verification Agent; Development Methodology templates | Partial | Require a lightweight list of scenarios or acceptance checks for non-trivial changes. Keep its storage project-defined. |
| Test naming, file-size limit, and integration-test file layout | Jest; Vitest; project-local guidance | Partial | Keep only the outcome: focused, understandable suites and isolated complex integration scenarios. Do not impose global identifiers, a 250-line threshold, or directory names. |
| Setup and teardown for test isolation | Jest; Vitest | Partial | Add one runner-neutral line: reset shared state and restore mocks/resources in the framework's appropriate setup and teardown hooks. Do not name Tracer or Jest-only APIs. |
| Failure diagnosis, logs, root-cause evidence, and environment escalation | Runtime Diagnostician; QA And Verification Agent; Careful Coding | Partial | Add a compact triage path: reproduce, inspect failure output and relevant logs, verify the affected boundary, then escalate an ambiguous requirement or environment issue with evidence. |
| Code review of production and integration-test changes | Code Review Agent; QA And Verification Agent | Partial | State that test changes are production-quality changes and should be within the changed-scope review. A separate checklist artifact is not universally needed. |
| Check dependent callers after interface changes | Coding Agent; Code Review Agent; Ast Grep | Partial | Add a post-contract-change check for callers, imports, fixtures, and tests, using repository-appropriate search tools. |
| Append-only logs, status files, attempts, and three-strikes blocking | Development Orchestrator; Manage Backlog | Partial | Retain only optional, project-level progress and blocker tracking. Do not make timestamps, glyphs, attempt counters, or an automatic three-failure cutoff a portable testing rule. |

## Obsolete or Project-Specific Guidance to Omit

- References to header links, definitions.md, design/modules, refactoring-plan-status.md, code-review-checklist.md, and procedure files from the former repository.
- The stated monetary penalty and mandatory user permission for a specific document-creation path.
- Fixed pnpm command syntax, required test ID format, fixed 250-line threshold, prescribed filenames, and a project-specific test folder layout.
- Tracer.reset, Tracer.enter, Tracer.exit, trace.log, maxWrites, and the backtracing/indentation conventions. These belong only in a project that supplies that tracing system.
- The required append-only project-log filename, timestamp/glyph grammar, attempt counters, and status-file timing.
- Commands and tools tied to a prior runtime, including search_files, list_files, write_to_file, and ask_followup_question.
- The reset procedure that deletes implementation files and renames test files to .old. It is high-risk recovery guidance, not a portable default.
- A blanket ban on runner cache clearing or configuration changes. Those actions require repository-specific ownership and approval rules, not a universal test rule.

## Precise Suggested Additions

### New Test-Driven Development Skill

Create a small, framework-neutral Test-Driven Development skill for behavior-changing code work. Its routing should pair it with Coding Agent and QA And Verification Agent, then with Jest, Vitest, Playwright, or a project-specific test skill as applicable. Its core workflow should be:

1. Read the applicable requirements, design, contracts, and repository instructions; state any unresolved behavior before coding.
2. For each testable behavior, define the smallest scenario and expected outcome.
3. Add or adjust one focused test and run it to establish the relevant failure when practical. If the existing system cannot express this safely, record why and select equivalent verification.
4. Implement the smallest scoped change, rerun the focused check, then run proportionate broader checks.
5. Refactor only while checks remain green; recheck callers and dependents after public-contract changes.
6. On failure, preserve the output, diagnose before changing code, and escalate requirement ambiguity or environment uncertainty with evidence.

### Jest and Vitest

Add the following shared guidance to both skills:

- When a behavior change has automated coverage, run the narrowest affected test first and then choose the broader suite from the changed boundary and blast radius.
- Keep each test focused on a named behavior or contract; split suites when their setup or scenario mix obscures failures.
- Reset shared state and restore mocks, timers, files, or connections in the runner-appropriate lifecycle hooks.
- Use the repository's documented scripts and runner syntax rather than assuming a package manager or argument convention.

### Agent Roles

- Coding Agent: add that, for testable behavior changes, it follows the Test-Driven Development skill and returns the focused and broader verification evidence.
- QA And Verification Agent: add a failure-triage handoff requirement that records reproduction command, observed result, suspected boundary, and whether the issue is code, requirement ambiguity, or environment.
- Code Review Agent: add an explicit changed-scope check that regression coverage exercises the intended contract and that mocks do not replace the behavior under test.
- Do not create a dedicated TDD agent. TDD is a workflow shared by implementation and verification roles, not an independent ownership boundary.

## Conclusion

The legacy procedure contains a strong portable core: behavior-first tests, focused red-green-refactor work, minimal implementation, layered verification, disciplined mocks, evidence-led diagnosis, and contract-impact follow-up. The live bundle already covers parts of this through Careful Coding, Jest, Vitest, and the Coding and QA roles, but it lacks the cross-framework workflow that connects them. Add one concise Test-Driven Development skill and the targeted role/runner additions above. Keep the former project's tracing, document registry, command syntax, logging regime, file thresholds, and destructive reset playbook out of distributed skills.
