# UNIT TEST PLAN GENERATION PROCEDURE FOR EXISTING CODE

## Overview

When asked to generate unit test plans from existing code, follow this procedure to create comprehensive test plans that cover all code paths and business rules.

The test plans should be placed in the `test` hierearchy according to the unit under test's location in the src hierarchy. This is also where the actual tests will be created.

The test plan should be called `<module name>.plan.md`

## Step-by-Step Process

### 1. MODULE ANALYSIS

For each module to test:

- Open the source file and identify all functions, methods, and business logic.
- For each function or method, document:

  - Name, input parameters (with types), and return type.
  - All conditional statements with exact conditions.
  - All loops with iteration patterns and expected behavior.
  - All external dependencies and function calls.
  - All business rules implemented within the function.

- Verify the rules against the design documents and document any discrepancies, if any.
  For each discrepancy, propose a solution.
  If there are discrepancies, let the user know and wait for approval on how to deal with them.

### 2. CODE PATH IDENTIFICATION

For each function or method:

- Identify all possible code paths through the function.
- Specifically focus on:
  - Path variations through different conditional branches (if/else).
  - Path variations through loop iterations.
  - Path variations based on input parameter values.
  - Path variations based on external dependencies' return values.
  - Error handling and exception paths.
- Document each path with the specific lines of code it covers.
- Ensure every line of code is covered by at least one path.

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

### 4. TEST SCENARIOS CREATION

For each identified code path:

- Create a detailed test scenario that includes:
  - **Synopsis**: A clear, descriptive name for the test.
  - **Purpose**: What aspect of the function is being tested.
  - **Code Path**: Which specific path through the code is being exercised.
  - **Input Values**: Concrete input values to use for the test.
  - **Mock Values**: Specific values for all mocked dependencies.
  - **Expected Behavior**: Detailed description of expected function behavior.
  - **Expected Output**: Specific expected return values or state changes.
  - **Assertions**: List of specific assertions that should be made.

### 5. SPECIAL CONSIDERATIONS FOR TRADING COMPONENTS

For Quote Watch and Trading Workflow components:

#### Price and Velocity Calculations

- Test scenarios must cover:
  - Velocity calculations with various price change patterns.
  - Sliding window behavior for price change tracking.
  - Handling of insufficient history for velocity calculations.
  - Separate bid, ask, and last price velocity calculations.

#### Trading Decisions

- Test scenarios must verify:
  - Entry conditions with various price and velocity combinations.
  - Exit conditions including take profit, stop loss, and velocity thresholds.
  - Take profit mode activation and behavior.
  - Buy/sell limit adjustments for order execution.
  - All possible combinations of condition satisfaction.

#### UI Notification and Integration

- Test scenarios should cover:
  - Quote watch line creation and updates.
  - Trading status display and updates.
  - Notification management and rendering.
  - Error handling and display.

#### Persistence and Recovery

- Test scenarios for:
  - Saving workflow configurations.
  - Restoring watches and workflows from storage.
  - Handling of persistence failures.
  - State maintenance across initialization cycles.

### 6. EDGE CASES AND ERROR HANDLING

Ensure test scenarios explicitly cover:

- Null/undefined input parameters.
- Empty collections or data structures.
- Boundary conditions (minimum/maximum values).
- Error conditions and exception handling.
- Race conditions or timing issues.
- Network failures and API errors.
- Storage failures.

### 7. OUTPUT FORMAT

Present the test plan as a structured document with:

- Module name and description.
- List of functions to be tested.
- Mock requirements section.
- Detailed test scenarios for each code path.
- Coverage map showing which lines of code are covered by which tests.

IMPORTANT: DO NOT embed javascript test code in the test plan

### EXAMPLE TEST SCENARIO FORMAT

````
## Test Scenario: Calculate Price Velocity With Sufficient History

### Synopsis
Calculate price velocity when there is sufficient price history.

### Purpose
Verify that velocity calculations correctly sum price differences when 6 entries are available.

### Code Path
1. Check for existence of price changes array (line 42)
2. Verify sufficient history exists (line 45)
3. Sum price differences (lines 48-52)
4. Return calculated velocities (line 55)

### Input Values
- symbol: "TQQQ"
- priceChanges: Array of 6 entries with known differences

### Mock Values
- No external dependencies to mock

### Expected Behavior
- The function should sum all price differences in the sliding window.
- Separate velocities should be calculated for last, bid, and ask prices.

### Expected Output
```typescript
{
  velocity: 12.5,      // Sum of all last price differences
  bidVelocity: 10.2,   // Sum of all bid price differences
  askVelocity: 14.8    // Sum of all ask price differences
}
```

### Assertions

- Assert velocity equals 12.5
- Assert bidVelocity equals 10.2
- Assert askVelocity equals 14.8

````

## REMEMBER

- Every code path must be covered by at least one test.
- Business rules must be explicitly verified.
- Mock requirements must be clearly defined.
- Test scenarios must be concrete with specific input and expected output values.
- Always follow object-oriented testing best practices, including proper setup, execution, and verification.

```

```
