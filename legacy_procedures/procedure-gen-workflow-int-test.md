# AI Assistant Instructions for Trading Workflow Test Implementation

## Context
You are implementing integration tests for the CIBC Driver Chrome Extension's trading workflow feature. This is a complex system that monitors stock prices, makes buy/sell decisions based on configured conditions, and executes trades. Your task is to build a comprehensive test suite following Test-Driven Development principles.

## Before You Begin
1. Read the full test plan at `design/trading-workflow-integration-test-plan.md`
2. Review the files in `design/workflow-integration-tests/` for detailed specifications
3. Understand the current project structure in the `src/` directory, particularly:
   - `src/services/workflow/` components
   - `src/types/tradeWorkflow.ts` for type definitions

## Your Assignment
Your task is to implement all 60 test cases defined in the test plan. You will:
1. Create the necessary test files and fixtures
2. Implement each test case following TDD methodology
3. Fix any code issues until tests pass
4. Document your progress and findings

## Getting Started
1. Begin with test 1.1.1 (Standard Price Crossing) by creating:
   - File: `test/integration/1-buy-triggers/1.1-price-based.test.ts`
   - Required fixtures and mocks in appropriate directories

2. Follow the strict sequence in the status document for subsequent tests

## Implementation Steps
1. For each test:
   - Write the test according to specifications
   - Run with `npm test`
   - Fix any failures
   - Update the status document

2. After completing each test:
   - Update the status table with exact details
   - Record fix count and descriptions
   - Run coverage for major test sections

3. When a test passes:
   - Immediately move to the next test in the sequence
   - Follow the strict order in the status document

4. If a test file reaches 10 tests:
   - Create a new sequence-numbered file before adding more tests

## Progress Tracking
Maintain the status document (`trading-workflow-test-status.md`) with precise details about:
- Test implementation status
- Fix attempts and their results
- Any issues or patterns discovered during implementation

This systematic approach will ensure comprehensive test coverage of the trading workflow system.
