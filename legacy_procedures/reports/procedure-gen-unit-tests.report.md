# Migration Report: Generate Unit Tests

## Source

- [Legacy procedure](../procedure-gen-unit-tests.md)

## Purpose and Scope

The procedure reconciles a project-local inventory of unit-test plans with Jest test suites, then generates missing coverage or fills plan scenarios that existing suites have not implemented. It also imposes former-project conventions for module system, import aliases, source lookup, file length, and editing tools.

## Worthwhile Durable Guidance

- Start test-generation work with an inventory: identify the applicable test plans, their corresponding suites, and the source modules they cover.
- For every missing suite, implement the relevant planned scenarios; for every existing suite, compare it with its plan and add only uncovered scenarios.
- Keep generated tests focused on the requested plan and observable behavior. Do not add speculative scenarios or unrelated production changes.
- Follow the target repository's documented test runner, module, import, alias, naming, and source-location conventions.
- Split suites when their length, setup, or mixed concerns makes failures difficult to understand; split along behavioral boundaries and preserve discoverable naming.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Coverage | Recommendation |
| --- | --- | --- | --- |
| Do not add work beyond what was requested | Careful Coding; Coding Agent | Complete | Keep the current scope discipline; no change required. |
| Use Jest and the repository's module convention | Jest; TypeScript ESM only when applicable | Partial | Jest should direct agents to inspect the repository's runner and module configuration before authoring imports or tests. Do not make CommonJS a portable default. |
| List plan files and find missing matching suites | Jest; QA And Verification Agent | Missing | Add a conditional test-plan reconciliation workflow for repositories that maintain test plans: inventory plans, map each to its suite, and report missing, stale, or unmatched files. |
| Read a source-file registry before writing tests | project-local guidance; Jest | Partial | Preserve only the general rule to locate and read the source under test from repository evidence. Registries such as File-List.md remain project-local. |
| Create tests for missing suites from their plans | Jest; Coding Agent | Partial | Add an explicit instruction to translate each planned scenario into focused assertions at the smallest useful boundary. |
| Audit existing suites against their full plans and add gaps | Jest; QA And Verification Agent; Code Review Agent | Missing | Add a plan-to-suite coverage audit step that records planned scenarios as covered, missing, obsolete, or blocked before adding focused missing tests. |
| Use the configured alias or local relative imports | Jest; TypeScript ESM | Partial | Add guidance to follow tsconfig, package, runner, and repository alias rules; verify resolved runtime import paths when practical. Do not prescribe one alias or extension syntax. |
| Leave TypeScript or import errors for later | Careful Coding; Jest; TypeScript Strict | Contradicted | Do not retain this as a portable rule. Tests should be syntactically valid and validation failures must be reported; fixing unrelated pre-existing errors remains out of scope. |
| Keep a test file below 200 lines, using suffixes when split | Jest | Partial | Retain the outcome, not the threshold: split suites when size or complexity obscures behavior, with names that make the split discoverable. |
| Use only a particular file-editing tool | None | Omit | Tool selection is runtime-specific and should not be bundled in a testing skill. |

## Obsolete or Project-Specific Guidance to Omit

- The test-plan filename convention, tests-folder location, File-List.md registry, and one-to-one suite filename rule. These are useful only where the repository defines them.
- The CommonJS requirement and the exact @/ alias and .js import examples. Module resolution must be derived from the target project's configuration.
- The instruction to ignore TypeScript and import errors. It risks leaving a test change unusable; only unrelated pre-existing failures may be left untouched and must be reported.
- The 200-line limit, sequential suffix prescription, and the replace_in_file/write_to_file restriction. These are former environment mechanics rather than portable test practice.

## Precise Suggested Additions

### Jest

Add the following guidance after the existing testing principles:

> When a repository maintains unit-test plans, reconcile them before adding tests: inventory applicable plans, map each plan to its suite and source module, then classify planned scenarios as covered, missing, obsolete, or blocked. Add focused tests only for the missing applicable scenarios and report unmatched plans or suites.
>
> Read the repository's Jest, TypeScript, module, and path-alias configuration before choosing imports. Use its documented naming and resolution conventions; do not assume CommonJS, ESM, an alias, or extension policy.
>
> Split a suite by behavior when its size, setup, or scenario mix makes failures hard to localize. Keep split suite names discoverable and fixtures scoped to the behavior they exercise.

### Agent Roles

- Coding Agent: when an explicit test plan exists, map it to the suite and source module, implement missing applicable scenarios, and identify any plan items it could not safely translate into an automated test.
- QA And Verification Agent: independently review plan-to-suite coverage for non-trivial planned test work and include unmatched, obsolete, and blocked scenarios in the verification handoff.
- Code Review Agent: for planned test changes, confirm that new tests exercise the planned behavior rather than merely mocks or implementation detail.

No new dedicated skill or agent is warranted. Test-plan reconciliation is conditional workflow guidance within Jest and the existing implementation, QA, and review roles.

## Conclusion

Keep the procedure's plan-to-suite reconciliation, source-evidence reading, gap-focused test generation, and readable suite organization. The live Jest skill covers behavior-oriented tests, mocks, fixtures, and layered execution, but lacks an explicit workflow for repositories that use test plans and lacks configuration-derived import guidance. Add those concise Jest and role updates. Omit all fixed paths, module format, alias syntax, tooling mandates, line-count rule, and the instruction to leave errors unresolved.
