# UNIT TEST PLAN GENERATION PROCEDURE FROM A DESIGN

## Overview

When asked to generate unit test plans from a design, follow this procedure to create comprehensive test plans that cover all code paths and business rules.

The test plans should be placed in the `test` hierearchy according to the unit under test's location in the src hierarchy. This is also where the actual tests will be created.

The test plan should be called `<module name>.plan.md`

## Step-by-Step Process

### 1. MODULE ANALYSIS

For each module defined in the design document:

- Read the design and identify all **functionalities** (capabilities, behaviors) the module must provide.
- For each functionality, identify:
  - all aspects to be implemented by the current module with references to the relevant pseudocode
  - all aspects to be implemented by other modules which will need to be mocked
  - guiding examples for inputs
  - guiding examples for resulting outputs and state changes
  - optional behavior dependent on input values
  - optional behavior dependent on state
- Recognize that these functionalities are implemented via specific **code functions/methods** within the module, containing the relevant **code paths** (pseudocode).
- The TDD methodology will help us build the full function progressively as we add tests one at a time and add the minimal code to support them.

### 2. TEST SCENARIOS CREATION

For each identified **code path** (within the code functions implementing a functionality):

- Create a detailed test scenario that includes:
  - **Synopsis**: A clear, descriptive name for the test.
  - **Purpose**: What specific aspect of the overall **functionality** is being tested by targeting this code path.
  - **Code Path**: If there are multiple optional behaviors, explain which one is being tested and how it is being activated
  - **Input Values**: Concrete input values to use for the test.
  - **Mock Values**: Specific values for all mocked dependencies.
  - **Expected Behavior**: Detailed description of expected behavior.
  - **Expected Output**: Specific expected return values or state changes.
  - **Assertions**: List of specific assertions that should be made.

### 3. MOCK REQUIREMENTS DEFINITION

For each test scenario:

- Identify all external dependencies that need to be mocked.
- For each mock:
  - Define the specific function or method to mock.
  - Specify expected input values for the mock function.
  - Define return values or side effects for each mock function.
  - Note any verification requirements (calls, parameters, etc.).
- IMPORTANT: Never mock any methods of the Tracer class such as Tracer.log.
- Ignore the tracer.js external dependency for mocking purposes.

### 4. Control Flow Decisions

- Test scenarios must validate if statements and other control flow decisions
  - For conditional behaviors, make sure to test both cases where the condition is true and the one where it is false
  - If there are multiple clauses, determine the critical input values to cause each clause to be true or false and what combination that will demonstrate the conditions are properly evaluated

### 5. UI Notification and Integration

- Test scenarios should mock UI elements and integrations of other components and APIs

#### Persistence and Recovery

If this module involves persistence:

- Test scenarios for:
  - Saving configurations.
  - Restoring from storage.
  - Handling of persistence failures.

### 6. EDGE CASES AND ERROR HANDLING

Ensure test scenarios explicitly cover:

- Null/undefined input parameters.
- Empty collections or data structures.
- Boundary conditions (minimum/maximum values).
- Invalid input values
- Error conditions and exception handling.
- Race conditions or timing issues.
- Network failures and API errors.
- Storage failures.

### 7. OUTPUT FORMAT

Present the test plan as a structured document with:

- Module name and description.
- List of functionalities to be tested.
- Mock requirements section.
- Detailed test scenarios.
- Coverage map showing which lines of pseudo-code from the design document are covered by which tests.

IMPORTANT: DO NOT embed javascript test code in the test plan

Always justify using the 5 WHYs approach :

- Add BECAUSE after each significant choice or declaration
- Chain up to 5 BECAUSE statements for complex operations
- Each BECAUSE should add new information and be added on a separate line
- Indent BECAUSE if it supports the previous line
- Keep BECAUSE in the same column as the previous line if it's independent and supports a line before that

Example:
Test input validation
BECAUSE we must check format of inputs
BECAUSE invalid input breaks processing

Test context creation
BECAUSE we track processing state
BECAUSE state affects decisions
BECAUSE we may need to backtrack
BECAUSE in case of error, we need to get back to a stable state B
ECAUSE we won't be able to do anything if we aren't in a stable state

Test with limit = 1
BECAUSE it's the simplest legal value
BECAUSE it generates a single loop
BECAUSE the loop is controlled by `limit`

## REMEMBER

- Every pseudo-code path (within the code functions implementing the functionalities) must be covered by at least one test scenario.
- Business rules must be explicitly verified.
- Mock requirements must be clearly defined.
- Test scenarios must be concrete with specific input and expected output values.
- Always follow object-oriented testing best practices, including proper setup, execution, and verification.
