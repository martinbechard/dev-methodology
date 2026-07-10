# Procedure: Apply Refactoring Plan

## Overview

Follow the following steps to execute the previously defined plan.

## Guiding Principles for Changes

Adhere to the following principles when making any changes, especially when addressing errors or refactoring:

1.  **Prioritize Correctness & Type Safety:** Always aim for correct, type-safe code, following [[procedure-coding-rules.md]]. Avoid `any` or type assertions (`as`) as shortcuts.

2.  **Root Cause Analysis:** Before applying fixes, analyze errors using [[procedure-root-cause-analysis.md]] and document the analysis in <thinking>.

3.  **Targeted & Incremental Changes:** Address one logical issue per step. Verify outcomes before proceeding.

4.  **Transparency:** Clearly explain the reasoning for code changes in <thinking> blocks.

## Current Phase: Design Review and Refactoring

### Design Document Management

- **RULE:** Do not create new design documents without explicit user permission. Update existing ones as needed.

  - **BECAUSE:** Prevents specification proliferation and keeps design changes tracked centrally.

- **RULE:** Ensure every `.ts` implementation file references its primary design document in the header (// Design: [[...]]) and that this aligns with the entry in [[definitions.md]], as per [[procedure-coding-rules.md]], section 0.

### Approach: Design Review

1.  **Documentation Review:** Review all component design documents against [[design-review-checklist.md]].

2.  **Standards Alignment:** Ensure designs align with [[/design/Object-Instantiation-Design-Directives.md]] and [[/design/error-strategy.md]]. Reference these in reviews.

3.  **Review Process:**

    - Create `<filename>-review.md` for each design review.

    - Focus on concrete evidence and actionable recommendations.

    - Address user TODOs within the review file, preserving the TODO comment.

    - Once approved, update the design document based _only_ on clarifications/corrections.

    - Create tasks in the Status File for design updates and subsequent implementation/testing work, following [[procedure-status-tracking-rules.md]].

### Approach: Refactoring Implementation and Testing

- **Status Tracking:**

  - **RULE:** All work **MUST** follow the task sequence in

  - **RULE:** Status updates **MUST** be performed immediately after task completion using the mandatory read-diff-confirm process.

  - (Refer to [[procedure-status-tracking-rules.md]] for details on format and updates.)

- **Development Process:**

  - **RULE:** All code modifications (features, fixes, refactoring) **MUST** strictly follow the **TDD cycle** defined in [[procedure-TDD-rules.md]], section 1.

  - **RULE:** All coding (implementation, refactoring) **MUST** adhere to [[procedure-coding-rules.md]], including referencing [[definitions.md]] for imports and managing new definitions.

  - **RULE:** All test creation and mocking **MUST** adhere to [[procedure-mocking-rules.md]].

  - **RULE:** Creation of status tracking plans **MUST** adhere to [[procedure-status-tracking-rules.md]].

  - **RULE:** Creation of new procedures **MUST** adhere to [[procedure-create-procedure]].

- **Design and Definition Handling:**

  - **RULE:** Handle discrepancies between code/tests and design/[[definitions.md]] by prioritizing the design/[[definitions.md]] reference, as detailed in [[procedure-TDD-rules.md]] (TDD Step 1) and [[procedure-coding-rules.md]]. Ask for clarification if ambiguous.

  - **PENALTY:** $5000 penalty applies each time design/[[definitions.md]] is not consulted before proposing changes based on code/test mismatches.

  - **RULE:** Handle missing design documents (verify existence, update status, create stubs if needed) as per [[procedure-TDD-rules.md]] (TDD Step 1) and [[procedure-coding-rules.md]] (Section 10).

  - **RULE:** Before creating _any_ new Class, Interface, or Type, check [[definitions.md]]. If it exists, import from its canonical path. If not, create it and **immediately update [[definitions.md]]** as per [[procedure-coding-rules.md]].

- **Testing and Debugging:**

  - **RULE:** All testing activities (unit, integration, debugging) **MUST** follow [[procedure-TDD-rules.md]]. This covers the TDD cycle, test naming, structure, setup, execution, assertions, and debugging strategies (including trace log analysis, troubleshooting hierarchy, backtracing, loop detection).

  - **RULE:** Mocking strategy (unit vs. integration, justifying integration mocks, avoiding mocks for spying only, handling complex mocks, and forbidden mocks like `Tracer` and fake timers) **MUST** follow [[procedure-mocking-rules.md]].

  - **RULE:** Debugging Strategy: Use `trace.log` as primary tool, follow analysis and logging practices (including variable names), adhere to Troubleshooting Hierarchy, prioritize code issues, verify saves, avoid infrastructure assumptions, use backtracing, detect loops via logs. (See [[procedure-TDD-rules.md]] and [[procedure-coding-rules.md]] for details).

  - **RULE:** Root Cause Analysis **MUST** use [[procedure-root-cause-analysis.md]].

  - **RULE:** **Three Strikes Rule:** If attempts to fix errors (e.g., test failures, type errors) for a specific component or test file fail three consecutive times, the AI **MUST** stop attempting fixes and instead proceed to delete the problematic code and/or test file(s). Following deletion, the AI **MUST** restart the development process for that component using strict TDD, starting with writing a failing test based on the original design/requirements.
    - **BECAUSE:** LLMs often excel at generating correct code from scratch using TDD, and repeated failed fix attempts indicate a potentially deeper issue best resolved by a clean implementation OR the changes required might be minor enough that a fresh TDD cycle is efficient.

- **`Tracer` Utility:**

  - **RULE:** **NEVER** mock `Tracer`. Its real logging is essential for LLM context and loop detection. Refer to usage rules in [[procedure-mocking-rules.md]] and [[procedure-TDD-rules.md]].

  - **PENALTY:** $10,000 penalty applies each time `Tracer` is mocked.

  - **RULE:** Do not explicitly initialize `Tracer` in test setup; rely on environment variables.

- **Process Improvement Principle:** Whenever a generic source or pattern of error is identified, propose and incorporate specific preventative measures or clarifications into this plan or related procedure documents.

## Future Enhancements

During review, future improvements may be identified. Document them in: design/future-improvements.md.
