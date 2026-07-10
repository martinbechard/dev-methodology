# ROOT CAUSE ANALYSIS PROCEDURE FOR UNIT TESTS

When asked to perform a Root Cause Analysis, follow these steps:

1.  Create a numbered list of the problem facts that are available (Test suite, case, failure output, relevant config/input, expected outcome).
2.  Extract relevant failure snippets from the test execution output.
3.  Find the first failed unit test suite mentioned in the output.
4.  **Tracer Mock Verification:**
    -   READ the test file (`<test unit file name>`).
    -   SEARCH for the line `jest.mock("@/utils/tracer");`.
    -   **IF** the line is found:
        -   REMOVE the line `jest.mock("@/utils/tracer");` from the test file.
        -   RESTART the RCA process from Step 1 using the corrected file.
        -   DO NOT proceed further in the current RCA iteration.
    -   **ELSE (Tracer is not mocked):**
        -   CONTINUE to the next step.
5.  DELETE the content of the document called `<test unit file name>-rca.md` if it exists.
6.  SELECT one (1) test failure ONLY from the first failed suite.
7.  CREATE a Root Cause Analysis document (`<test unit file name>-rca.md`) with the following sections:
    7.1. **Problem Facts:** Write the numbered list from step 1.
    7.2. **Failure Output:** Write the relevant failure snippets from step 2.
    7.3. **Test Code (`it` block):** READ the test file (`<test unit file name>`). LOCATE the specific `it(...)` block for the FAILED test case. WRITE _only_ the code within that `it(...)` block (including the signature) to the RCA document.
    7.4. **Scenario Description:** READ the corresponding Scenario/Design document (`<module name>-scenarios.md` or similar). FIND the scenario for the FAILED test. WRITE the scenario description (Input, Config, Expectations) into the RCA.
    7.5. **Test Validity Evaluation:**
        -   Evaluate Input values: Do they match the scenario?
        -   Evaluate Mock values/setup: Does it match the scenario?
        -   Evaluate Assertions: Do they match the scenario's expectations?
        -   Determine overall test validity (VALID or INVALID) and WRITE the result and reasoning into the RCA.
8.  **IF** the Test Validity Evaluation is **INVALID**:
    -   CORRECT the test code to accurately reflect the test plan/scenario.
    -   REPEAT THE FULL RCA PROCESS FROM STEP 1 with the corrected test.
    -   DO NOT proceed to the CODE FIXING PROCESS.
9.  **ELSE IF** the Test Validity Evaluation is **VALID**:
    -   CONTINUE to the **CODE FIXING PROCESS** below.

---

**CODE FIXING PROCESS:** Add findings from each step to the RCA document.

1.  **External Description:** Look at the test output (Expected vs. Received, error messages) to describe the problem externally.
2.  **Read Trace Log:** READ the `<root>/trace.log`. FIND and WRITE the logs related **only** to the FAILED TEST execution to the RCA document. Include start/end line numbers if possible. Verify essential logs are present; if not, reconsider Tracer/mocking issues.
3.  **Perform Detailed Code Trace (Simulate Debugger):** (Incorporates `procedure-code-tracing.md`)
    3.1. Go through the code execution line-by-line, using the available trace logs as a guide. Start from the beginning of the test execution within the logs.
    3.2. Create a detailed, hierarchically numbered list (e.g., 3.1, 3.1.1) of what is happening at each significant step.
    3.3. For each step, include the file name and line number (`filename(line_number): description`).
    3.4. Provide detailed descriptions of what each line/block is doing, including relevant variable values and function calls observed or inferred from logs and code.
    3.5. Note function entries/exits, conditional statement outcomes, and loop iterations based on logs and code logic.
    3.6. Track significant variable declarations, assignments, or modifications relevant to the failure.
    3.7. Compare the actual execution flow (from logs/trace) with the expected flow based on the code logic and test scenario.
    3.8. Identify the specific point of divergence where the execution path or variable states differ from what is expected to produce the correct test outcome. WRITE this point of divergence clearly in the RCA.
4.  **Analyze for Infinite Loops (If `Max writes exceeded` error occurs):**
    4.1. Examine the `trace.log` (specifically the logs related to the failed test) for repeating sequences of log messages.
    4.2. Look for patterns where the indentation level (call stack depth) increases within the repeating sequence.
    4.3. Identify the specific function calls or code blocks involved in the repeating pattern.
    4.4. Determine the condition or state transition that is likely causing the loop to not terminate as expected. WRITE the analysis into the RCA.
5.  **Code Inspection at Divergence/Loop:** Look at the source code at the point of divergence (identified in step 3.8) or within the identified loop (step 4.3) for obvious logical failures. (Renumbered from 4)
6.  **Mock Interaction Check:** If divergence/loop involves calls to external/mocked functions, examine the mock implementation and the specific mock calls made (using `mock.calls` if necessary) to ensure correct behavior and return values. (Renumbered from 5)
7.  **Mock Setup Verification:** If using mocks, ensure the `jest.mock(...)` call precedes the relevant `import` statement in the test file. Verify mock setup values. (Renumbered from 6)
8.  **Previous Fix Attempts:** If applicable, list previous attempts to fix this specific failure at the same point of divergence/loop and analyze what each failure revealed. (Renumbered from 7)
9.  **Hypothesize Root Cause & Fix:** (Renumbered from 8)
    9.1. Create a list of up to 5 likely reasons explaining the divergence/loop.
    9.2. Identify the simplest explanation based on the trace and code analysis.
    9.3. Propose a specific code fix for the simplest explanation.
    9.4. Verify the proposed fix doesn't contradict previous findings (step 8).
    9.5. Verify the proposed fix aligns with relevant design documents (`design/...`).
    9.6. **Unit Test Verification (Integration Context):** IF fixing an integration test failure involves modifying `src/...` code, THEN plan to run corresponding unit tests (`test/.../<Module>.test.ts`) *after* applying the fix but *before* rerunning the integration test. (Renumbered from 8.3)
    9.7. **Design/Plan Verification (Unit Test Context):** IF RCA suggests modifying a *passing* unit test, THEN verify against design/plan docs first. (Renumbered from 8.4)
10. **Recommendation:** State the final recommended fix and WAIT for approval. (Renumbered from 9)
11. **Design Update (If Needed):** If the fix requires a design change, update the relevant design document and WAIT for approval. (Renumbered from 10)
12. **Apply Fix & Test:** Update the code with the approved fix. Run the corresponding unit tests (if applicable, see 9.6). Rerun the failed test suite. (Renumbered from 11)
13. **Repeat:** If tests still fail, REPEAT the RCA process from Step 1 (or Step 6 if only subsequent tests fail). (Renumbered from 12)
