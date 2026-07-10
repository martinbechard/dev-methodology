# Procedure: Unit and Integration Testing Rules

This document details the procedures and rules for writing, running, and debugging unit and integration tests, based on refactoring-plan-gemini.md and code-review-checklist.md. Rigorous testing using Test-Driven Development (TDD) is mandatory.

## 1. Test-Driven Development (TDD) Process

- **RULE:** All code modifications (new features, bug fixes, refactoring) **MUST** strictly follow the **TDD cycle**:

  1.  **Update Design/Plan & Verify Alignment:**

      - Ensure the relevant design document reflects the intended change. Consult the design document referenced in the implementation file's header (// Design: [[...]]). Use [[definitions.md]] to confirm the link between the definition and its design doc/canonical path.

      - Update the design if necessary (with user permission if creating new documents).

      - Create/update the test plan based on the design, following [[procedure-unit-test-plan-from-design.md]].

      - **Check Definitions:** Explicitly check [[definitions.md]] for any relevant existing Classes, Interfaces, or Types that should be used or imported. Note their canonical paths.

      - **Consult/Update Module Design:** The `design/modules/` directory is the primary reference for module designs. Before implementing changes, consult the relevant design document (usually linked via header comment or [[definitions.md]]). If code changes are made, the design document **MUST** be updated accordingly. If code seems incorrect or incomplete, use the design document to understand or reconstitute the intended logic.

        - **BECAUSE:** Ensures design documentation remains the source of truth and stays synchronized with implementation.

      - **Handle Missing/Incorrect Design:** Follow rules in procedure-coding-rules.md (Section 10 / Design Adherence). Prioritize the design/definitions.md unless clarification is sought and granted. **PENALTY:** $5000 penalty applies if definitions.md/design is not consulted before proposing changes due to code/test mismatches.

      - **BECAUSE:** Ensures work is driven by the agreed-upon specification registered in design docs and definitions.md, preventing architectural drift and leveraging existing definitions.

  2.  **Add Failing Test (Red):**

      -   **Check Target Test File Size and Structure:**
          -   **RULE:** Before adding the new test (`it` block) to a target test file (e.g., `module.test.ts` or `module/logic.test.ts`):
              -   Check the current line count of the target test file.
              -   **IF** the line count **exceeds 250 lines** **AND** the file is not already part of a split suite (i.e., not inside a dedicated test directory like `test/module/`):
                  -   **THEN** the entire test suite **MUST** be refactored *before* adding the new test:
                      1.  Create a dedicated directory named after the test suite (e.g., `test/module/`).
                      2.  Move the existing large test file into this directory.
                      3.  Split the tests within the moved file into multiple, logically named files within the new directory (e.g., `initialization.test.ts`, `parsing.test.ts`) based on `describe` blocks or functional areas.
                      4.  Ensure all necessary setup (`beforeEach`, mocks) is correctly placed or shared.
                      5.  Add the *new* test case to the appropriate *newly created* logical file within the directory.
              -   **ELSE** (the target test file *is* already within a dedicated directory but has exceeded 250 lines):
                  -   **THEN** a *new logical test file* **MUST** be created within the *existing* directory (e.g., `parsing_part2.test.ts` or a name reflecting the new tests).
                  -   Add the new test case (`it` block) to this *newly created file*. (Further refactoring of the original >250 line file within the directory is encouraged but not mandated by this specific step).
          -   **ELSE** (target test file is 250 lines or less):
              -   Add the new test case (`it` block) to the target test file.
          -   **BECAUSE:** This explicitly integrates the test suite splitting requirement from `procedure-coding-rules.md` into the TDD workflow using a **deterministic** line count trigger (250 lines) that applies consistently to *all* test files.
          -   **BECAUSE:** It promotes the organized structure of logical files within dedicated directories and prevents individual files within those directories from becoming excessively large by mandating the creation of new files when the limit is hit.
          -   **BECAUSE:** Addressing file size *before* adding the next test prevents files from growing unmanageably during incremental development.

      - Write **one** specific test case (using the `<ModulePrefix>-<AreaPrefix>-<SeqNum>` naming convention) for the desired change based on the test plan.

      - **Import correctly:** Use [[definitions.md]] to determine the correct import path for any required definitions as per procedure-coding-rules.md Section 2.

      - The test **MUST** fail initially (either compilation error or runtime failure).

      - Run _only_ this test (`pnpm run test <file> -t "<Test-ID>"`) to verify it fails.

      - **BECAUSE:** Writing the test first clarifies requirements. Using definitions.md ensures correct imports. Verifying failure confirms the test setup and validity.

  3.  **Minimal Implementation (Green):**

      - Write _only_ the absolute minimum code required in the implementation file (.ts) to make the _current_ failing test pass.

      - **Check/Update Definitions:** If implementation requires a _new_ reusable Class/Interface/Type, follow procedure-coding-rules.md Section 4: check [[definitions.md]], create it in the canonical path if needed, and **update [[definitions.md]] immediately**. Import the new definition correctly.

      - If the test requires adding a new function/method not covered by the verified design (Step 1), **STOP** and go back to Step 1 to get design clarification/update and potentially update [[definitions.md]].

      - **BECAUSE:** Focuses effort, simplifies debugging, ensures implementation follows design, and keeps definitions.md synchronized with code structure.

  4.  **Verify Pass (Verify Green):**

      - Run the _same single test_ again (`pnpm run test <file> -t "<Test-ID>"`) using the correct syntax. Confirm it passes.

      - Run the _full test suite_ for the module (`pnpm run test <file>`) to ensure no regressions.

      - If needed, debug the minimal code using `trace.log` etc.

      - **BECAUSE:** Confirms the minimal code works and didn't break related functionality.

  5.  **Review:**

      - Perform code review using code-review-checklist.md. Update `<module>-code-review.md`.

      - **BECAUSE:** Provides human check for quality beyond automated tests.

  6.  **Refactor:**

      - Apply review findings _to the current cycle's code only_. Improve clarity, remove duplication, etc.

      - If extracting functions with TDD, ensure any new types/interfaces created are added to [[definitions.md]] if they are reusable/exported.

      - **BECAUSE:** Improves design of verified working code systematically. Keeps definitions.md current during refactoring.

  7.  **Verify Refactor:**

      - Run the _full test suite_ for the module (`pnpm run test <file>`) again. Ensure all tests pass.

      - **BECAUSE:** Guarantees refactoring didn't introduce regressions.

  8.  **Repeat:** Go back to Step 2 for the next test case.

  9.  **Final Module Check & Status Update:**

      - Run the _entire_ test suite for the module one last time (`pnpm run test <name of suite>`).

      - Update status in refactoring-plan-status.md.

      - **Dependency Check:** Use `search_files` to find dependent files potentially affected by interface changes (identifiable via [[definitions.md]]). Plan updates for dependents.

      - **BECAUSE:** Final confirmation, progress tracking, identifies subsequent work needed due to interface changes registered in definitions.md.

### 1.1 Project Logging

- **RULE:** For each TDD task (implementing a feature, fixing a bug, refactoring), a corresponding Project Log file **MUST** be maintained alongside the status file.
    - **NAMING:** The log file **MUST** be named `<base_name>_log.md`, where `<base_name>` matches the corresponding status file (e.g., `feature-x_log.md` alongside `feature-x_status.md`).
    - **PROCESS:** This file is **APPEND-ONLY**. After completing *any* step in the TDD cycle (e.g., adding a test, implementing minimal code, refactoring, running tests), a new log entry **MUST** be appended.
    - **FORMAT:** Each log entry **MUST** follow the format:
        `YY-MM-DD HH:MM:SS - G - Step Description - [Attempt #N] - [Optional Info]`
        - **Timestamp:** `YY-MM-DD HH:MM:SS` (fixed length, padded, local time). Use the timestamp provided in the environment details.
        - **Glyph (G):**
            - `✅`: Step completed successfully (e.g., tests pass).
            - `❌`: Step failed (e.g., tests fail, error encountered). **MUST** be logged immediately after the failed attempt. Subsequent fix attempts for the *same* failed step **MUST** also be logged with `❌` and an incremented attempt counter until the step succeeds (`✅`).
            - `ℹ️`: Informational step (e.g., starting a phase, observation, describing a planned fix *before* attempting it).
            - `❓`: Asking a question or seeking clarification.
        - **Step Description:** Clear description of the TDD step attempted (e.g., "Add test IV-01", "Implement minimal code for IV-01", "Run tests for inputValidation.test.js", "Attempt fix for VL-11 assertion").
        - **Attempt Count:** (Optional, but **Required** for `❌` glyphs on retries) Include `[Attempt #N]` only if this is a retry of the *immediately preceding* failed step (N > 1).
        - **Optional Info:** (Optional) Brief relevant details. If `G` is `❌` due to test failures, this **MUST** include the number of failing tests (e.g., "5 tests failing"). It MAY also include the specific fix being attempted or the question asked if `G` is `❓`.
    - **STATUS FILE UPDATE:** The corresponding `<base_name>_status.md` file **MUST** only be updated when the *entire* TDD task is complete or significantly blocked/changed, summarizing the final state. The project log provides the detailed history.
    - **BECAUSE:** Provides a detailed, immutable audit trail of the development process, step-by-step.
    - **BECAUSE:** Separates the high-level status summary from the granular execution log, improving clarity for both.
    - **BECAUSE:** Explicitly logging failures and retries helps track effort and identify problematic steps.

- **RULE:** Focus on **one test case at a time**. If multiple tests fail, address only the _first_ listed failure by running it individually.

  - **BECAUSE:** Isolates the problem, simplifies debugging, provides a stable baseline.

### 1.2. Test Planning and Incremental Implementation

- **RULE:** When listing TDD implementation subtasks (e.g., "Add test for X", "Implement X") in a status plan, **MUST** include an attempt counter in parentheses `(0)` after the task description. Increment this counter each time an attempt is made to complete that specific subtask (e.g., running a test, writing implementation code).

  - **EXAMPLE:**
    - ⬜ Implement `QuoteWatchService` (TDD) - Test Plan: [[test/services/QuoteWatchService.plan.md]]
      - [▶️] Add test for `startWatching` (1)
      - [⬜] Implement `startWatching` in `QuoteWatchService.ts` (0)
      - [⬜] Add test for `setupTradeWorkflow` (0)
      - ... (etc.)
  - **BECAUSE:** Tracks the number of attempts for each step, providing visibility into areas causing difficulty and helping enforce rules like the "Three Strikes Rule".

- **RULE:** Before implementing a module or feature via TDD, **MUST** create a list of specific test cases (scenarios) to be implemented based on the design document and the procedure [[procedure-unit-test-plan-from-design.md]]. This list **SHOULD** be added to the relevant status tracking file (e.g., `*-status.md` or a dedicated test plan file like `test/services/MyService.plan.md` linked from the status file) as pending (⬜) subtasks under the main implementation task.

  - **EXAMPLE:**
    - ⬜ Implement `QuoteWatchService` (TDD) - Test Plan: [[test/services/QuoteWatchService.plan.md]] (0)
      - ⬜ Test Case: `QWS-INIT-01` - `initialize` should exist and not throw. (0)
      - ⬜ Test Case: `QWS-STATE-01` - `getWatchedSymbols` should return empty array initially. (0)
      - ⬜ Test Case: `QWS-WATCH-01` - `startWatching` should add symbol to internal list. (0)
      - ... (etc.)
  - **BECAUSE:** Planning tests upfront ensures comprehensive coverage based on requirements/design and provides a clear roadmap for implementation within the status file. Linking to a dedicated plan file keeps the main status file concise.

- **RULE:** Implement the planned test cases **strictly one at a time**, following the RED-GREEN-REFACTOR cycle for each individual test case before moving to the next pending (⬜) test case in the list.

  - **BECAUSE:** Adhering to the single-test TDD cycle prevents writing excessive implementation code before having a specific, failing test to guide it, reinforcing incremental development and focus.

- **RULE:** When writing a new failing test (RED step), consult the test plan for that specific test case to identify required dependencies. Only mock the dependencies absolutely necessary for _that specific test_ to compile and fail predictably (or pass, in the case of testing error handling). Do not add mocks for dependencies only needed by _future_ planned tests. Add necessary mocks incrementally as required by each new test case.
  - **BECAUSE:** This aligns mocking strategy with the incremental nature of TDD, ensuring mocks are added only when driven by a specific test requirement identified in the test plan, preventing over-mocking and keeping test setup focused.

## 2. Test Naming and Structure

- **RULE:** Each test case (`it(...)` block) **MUST** start with unique ID: `<ModulePrefix>-<AreaPrefix>-<SeqNum>`.

  - **EXAMPLE:** `it("SM-UPD-01: should update status to ACTIVE")`

  - **BECAUSE:** Provides unique, predictable, command-line-friendly identifier for precise targeting (`-t`).

- **RULE:** For complex integration tests, implement each distinct scenario in its **own separate test file**.

  - **BECAUSE:** Simplifies setup, improves isolation, aids debugging, keeps files focused.

## 3. Test Setup (`beforeEach`, `afterEach`)

- **RULE:** Call `Tracer.reset()` at the beginning of `beforeEach`.

  - **BECAUSE:** Ensures accurate, independent trace logs per test and prevents false `maxWrites` errors.

- **RULE:** Use `beforeEach` for common setup. Ensure imports for setup use canonical paths from [[definitions.md]].

  - **BECAUSE:** Reduces duplication, ensures consistent state, uses authoritative definitions.

- **RULE:** Use `afterEach` for cleanup (e.g., `jest.restoreAllMocks()`).

  - **BECAUSE:** Ensures test independence by cleaning up spies/mocks.

## 4. Running Tests

- **RULE:** Use correct `pnpm` command syntax:

  - Suite: `pnpm run test <filename>`

  - Single: `pnpm run test <filename> -t "<Test-ID>"` (No `--` before `-t`)

  - **BECAUSE:** Required for test runner arguments; targeting single tests is crucial for TDD.

- **RULE:** State attempt number when running single failing test during debugging.

  - **BECAUSE:** Tracks debugging efforts and enforces troubleshooting hierarchy.

## 5. Assertions and Verification

- **RULE:** Assertions (`expect(...)`) should be specific, testing one logical outcome per test case where possible.

  - **BECAUSE:** Provides clear failure messages, speeding up root cause identification.

- **RULE:** Verify mock interactions (`toHaveBeenCalledWith`, etc.) as appropriate.

  - **BECAUSE:** Tests outgoing commands/queries, ensuring correct collaboration with dependencies.

- **RULE:** Ensure tests align with requirements specified in the design document (linked via [[definitions.md]]) and test plan.

  - **BECAUSE:** Validates _intended_ functionality, not just accidentally implemented behavior.

- **RULE:** Test case code (`it` blocks) **MUST** include `Tracer.enter` at the beginning and `Tracer.exit` at the end.
  - **BECAUSE:** This provides clear entry and exit points in the trace logs for each test case, aiding in debugging and understanding test execution flow.
    - **BECAUSE:** Consistent tracing helps isolate issues within specific test executions.

## 6. Debugging and Troubleshooting

- **RULE:** **Root Cause Analysis (RCA):**: Whenever there is a test failure, execute procedure-root-cause-analysis.md

- **RULE:** **Primary Tool:** Use `trace.log`. Analyze _before_ code changes. Use explicit variable names in logs (Tracer.log(\`Var=\${val}\`)).

  - **BECAUSE:** Provides detailed execution flow crucial for LLM/developer diagnosis. Clear logging speeds up analysis.

- **RULE:** Follow **Troubleshooting Hierarchy (Revised v5):** Escalate analysis (Log -> RCA -> Tracing -> Ask) based on consecutive failures per file. This includes applying the "Three Strikes Rule" and "Reset Procedure" defined below.

  - **BECAUSE:** Structured, escalating approach for persistent failures, including specific recovery procedures.

- **RULE (Three Strikes - New Tests):** When building tests from scratch (e.g., for a new file) and the _same specific test case_ fails 3 times (tracked via the attempt counter in the status plan), **STOP** further attempts on that test.

  1. Use `ask_followup_question` to request user assistance.
  2. If user assistance is unavailable (e.g., user is offline), mark the specific test case sub-task and the parent implementation task as blocked (⏳) in the status plan, clearly stating the reason (3 strikes rule hit), and proceed to the next planned file or major task.

  - **BECAUSE:** Prevents wasting time on intractable issues without guidance and allows progress on other areas if blocked.

- **RULE (Reset Procedure - Existing Code):** If applying changes to _existing_ code and tests results in persistent compilation errors or test failures that cannot be resolved after multiple attempts (implicitly hitting the "3 strikes" threshold for the overall modification task):

  1. **Announce Reset:** State the intention to perform the reset procedure.
  2. **Delete Implementation:** Request deletion of the implementation file (`.ts`) being modified. **Verify deletion** using `list_files` before proceeding. **DO NOT** delete the test file (`.test.ts`).
  3. **Rename Old Test File:** Request renaming the existing test file by appending `.old` (e.g., `MyModule.test.ts` -> `MyModule.test.ts.old`). **Verify rename** using `list_files` before proceeding.
  4. **Create New Test File with First Test & TODOs:** Using `write_to_file`, create the test file with the original name (e.g., `MyModule.test.ts`). Include necessary imports, `describe`/`beforeEach`/`afterEach` setup, the _first_ relevant test case (`it(...)`) from the `.old` file, and TODO comments for subsequent tests (e.g., `// TODO: get test <Test-ID> from MyModule.test.ts.old`). Add a final comment: `// TODO: when all tests have been recreated, delete MyModule.test.ts.old`. **Verify creation** using `list_files`.
  5. **Rebuild Incrementally:** (State Check: Implementation file deleted, test file renamed to `.old`, new test file exists with only first test). Re-create the implementation file (`.ts`) from scratch, following the standard TDD cycle (Red-Green-Refactor) for the single active test in the new test file.
  6. **Add Tests Sequentially:** Once the first test passes, copy the _next_ relevant test case from the `.old` file into the new test file (replacing the corresponding TODO comment) and repeat the TDD cycle for it. Continue this process one test at a time.
  7. **Three Strikes during Rebuild:** If the "Three Strikes Rule" (3 failures on the _same test case_) is encountered during this rebuild process, follow the escalation steps defined in the "Three Strikes - New Tests" rule (ask user/block and move on).
  8. **Cleanup:** Once all tests from the `.old` file have been successfully added and pass in the new file, request deletion of the `.old` test file. **Verify deletion** using `list_files`.

  - **BECAUSE:** Provides a systematic way to recover from complex error states when modifying existing code by rebuilding incrementally from a clean slate, guided by individual tests. It incorporates the standard escalation path if individual tests prove problematic during the rebuild.

- **RULE:** If detailed step-by-step execution analysis is required, or when explicitly asked, **FOLLOW** the procedure outlined in [[procedure-code-tracing.md]].

  - **BECAUSE:** Provides a specific, structured method for deep code execution analysis when standard logging is insufficient.

- **RULE:** **Prioritize code issues.** Verify file saves (`read_file`) if fixes seem ineffective. Do not assume infrastructure problems. Check variable naming clarity.

  - **BECAUSE:** Focuses on most likely causes, avoids time sinks, ensures debugging is based on actual code. Renaming aids clarity.

- **RULE:** When a test fails, **NEVER** change implementation code without first verifying the intended behavior against the relevant design document (referenced via header/[[definitions.md]]) and the test plan [[procedure-unit-test-plan-from-design.md]].
  - **BECAUSE:** Ensures that code changes are driven by the specified design and requirements, not just by making a test pass potentially incorrectly.
    - **BECAUSE:** Prevents accidental introduction of logic errors or deviations from the intended architecture.
- **RULE:** If a test failure suggests a potential mismatch with a business rule or requirement documented in the design, **MUST** use `ask_followup_question` to consult the user before proposing or making changes to the implementation or design that alter the business rule.

  - **BECAUSE:** Business rules are core requirements and MUST NOT be changed without explicit user confirmation.
    - **BECAUSE:** Prevents wasted effort implementing incorrect assumptions about requirement changes.

- **RULE:** **Temporarily add more `Tracer.log` calls** (with IDs and variable names) if needed for granular detail. Remove after fixing.

  - **BECAUSE:** Allows focused debugging without permanent code clutter.

- **RULE:** Use **Backtracing** technique (log inputs before assignment) if trace log seems inconsistent with code.

  - **BECAUSE:** Systematically finds where values become incorrect.

- **RULE:** Detect **loops/recursion** via repeating logs with increasing indentation in `trace.log`.

  - **BECAUSE:** Systematic way to locate loops using trace data.

- **RULE:** If tests fail unexpectedly in ways that suggest a tooling or environment issue (e.g., tests not being discovered, persistent failures despite correct code, errors unrelated to code changes) after verifying file saves and basic syntax, **DO NOT** attempt commands like `jest --clearCache`. Instead, **MUST** use the `ask_followup_question` tool to ask the user for assistance in diagnosing potential IDE, cache, or environment problems.

  - **BECAUSE:** Clearing caches or modifying the environment can have unintended consequences or mask underlying issues. User intervention is required for these steps.

- **RULE:** **NEVER modify configuration files** (`jest.config.ts`, `tsconfig.json`) without user permission.

  - **BECAUSE:** Prevents unintended side effects and keeps configuration stable.

## 7. Test Maintenance and Verification

- **RULE:** Always run the corresponding unit test suite during the TDD cycle (Step 4/7) after modifying a module.

  - **BECAUSE:** Catches regressions early, ensures module integrity before further testing.

- **RULE:** After completing TDD for a module, check for dependents affected by interface changes (using [[definitions.md]] to identify interfaces) and plan updates (TDD Step 9).

  - **BECAUSE:** Ensures system consistency after contract changes.

- **RULE:** Perform code review on _integration_ test code (`test/integration/...`) using code-review-checklist.md.

  - **BECAUSE:** Integration tests are critical code requiring quality checks for reliability and maintainability.
