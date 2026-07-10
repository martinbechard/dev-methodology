# PROCEDURE: CREATING INTEGRATION TESTS FOR TRADING WORKFLOW

Last Update: Wednesday, March 19, 2025

When asked to create or modify integration tests for the trading workflow system, follow these steps:

## INITIAL SETUP

1. REFERENCE DOCUMENTATION:

   - Begin by reviewing the main test plan at `design/testing/trading-workflow-integration-test-plan.md`
   - Consult the specific test specification files referenced in the test plan
   - Review necessary fixture and configuration files as needed

2. DIRECTORY STRUCTURE:

   - Verify if the specified test directories exist (e.g., `test/integration/1-buy-triggers/`)
   - Create these directories if they don't exist
   - Follow the exact directory structure specified in the test plan

3. IMPLEMENTATION APPROACH:
   - If the test file already exists, review and complete/modify it as needed
   - If the test file doesn't exist, create it following the specifications
   - Maintain consistency with existing test files and patterns

## IMPLEMENTATION DETAILS

1. FIXTURES AND HELPERS:

   - Implement necessary test fixtures first if they don't exist
   - Create helper functions as specified in the test helpers documentation
   - Implement price patterns as defined in the specifications

2. TEST STRUCTURE:

   - Follow Jest testing patterns with describe/it blocks
   - Organize tests hierarchically as specified in the test plan
   - Include appropriate setup/teardown for each test

3. MOCKING AND SIMULATION:
   - Use mocks as specified in the mock implementation documentation
   - Follow the guidelines for simulating time-based events
   - Ensure mock behavior accurately reflects real component behavior

## VALIDATION AND COMPLETION

1. VERIFICATION:

   - Ensure each test verifies the exact expectations listed in the specification
   - Add appropriate assertions for state validation
   - Include error handling and edge case testing

2. DOCUMENTATION:

   - Add JSDoc comments to explain test purpose and structure
   - Include comments explaining complex test scenarios or assertions

3. CODE QUALITY:
   - Follow project coding standards and patterns
   - Ensure tests are isolated and don't depend on state from other tests
   - Optimize for readability and maintainability

Remember to update this procedure document as new implementation patterns or requirements are identified during the review process.
