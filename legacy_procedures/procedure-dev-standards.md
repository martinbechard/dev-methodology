# Procedure: Development Standards

- **RULE (For AI Assistants):** In order to do development effectively, recursively read all other procedures and standards mentioned in this document when first processing it for a task.
  - **BECAUSE:** This ensures the AI has the full context of all relevant development practices before proceeding with the task.
    - **BECAUSE:** Having complete context reduces errors and ensures adherence to all project standards.

## 1. Purpose and Scope

- **RULE:** This document outlines the core development standards and procedures to be followed in this project.
  - **BECAUSE:** It serves as a central reference point for developers (human or AI) to understand the expected practices for coding, testing, planning, and tracking work.
    - **BECAUSE:** Consistent adherence to these standards ensures code quality, maintainability, and efficient collaboration.
      - **BECAUSE:** High-quality, maintainable code reduces bugs, lowers development costs, and facilitates future enhancements.

- **NOTE (For AI Assistants):** When you use the `read_file` tool to consult this or any other procedure/design document, the user can see which file you are reading. Use this tool judiciously to gather necessary information.

## 2. Core Development Procedures

- **RULE:** Developers **MUST** follow the Test-Driven Development (TDD) approach as defined in [[/procedure-TDD-rules.md]].

  - **BECAUSE:** TDD ensures that code is written with testability in mind and that functionality meets requirements through verifiable tests.
    - **BECAUSE:** Writing tests first helps clarify requirements and design before implementation begins.
      - **BECAUSE:** A comprehensive test suite provides a safety net for refactoring and adding new features.

- **RULE:** Mocking of dependencies for testing **MUST** follow the guidelines specified in [[/procedure-mocking-rules.md]].
  - **BECAUSE:** Consistent mocking practices ensure tests are reliable, maintainable, and accurately reflect component interactions.
    - **BECAUSE:** Proper mocking isolates the unit under test and controls external factors.
      - **BECAUSE:** Reliable tests increase confidence in code changes and reduce debugging time.

- **RULE:** All code **MUST** adhere to the coding standards specified in [[/procedure-coding-rules.md]].

  - **BECAUSE:** Consistent coding standards improve code readability and maintainability across the project.
    - **BECAUSE:** Readability reduces the cognitive load required to understand the code, making reviews and debugging easier.
      - **BECAUSE:** Maintainability ensures the codebase can be effectively modified or extended over time.

- **RULE:** All proposed code changes (implementations, fixes, refactoring) **MUST** be justified by explaining the intended effect and why the change is desirable and robust, ensuring alignment with documented requirements and design.

  - **BECAUSE:** This promotes thoughtful development and ensures changes are purposeful and well-considered.
    - **BECAUSE:** Justification helps reviewers understand the rationale and verify that the change correctly addresses the problem or requirement without introducing unintended consequences.
      - **BECAUSE:** It encourages developers to think critically about the robustness and alignment of their solutions before implementation.

- **RULE:** Development **MUST** utilize the technologies and libraries defined in [[/procedure-technical-stack-rules.md]].

  - **BECAUSE:** Adhering to the defined technical stack ensures consistency and leverages approved tools.
    - **BECAUSE:** It simplifies dependency management, build processes, and developer onboarding.
      - **BECAUSE:** Using a common set of tools facilitates collaboration and knowledge sharing.

- **RULE:** When creating a new design based on requirements (i.e., before code exists), the process outlined in [[/procedure-document-new-design.md]] **MUST** be followed.
  - **BECAUSE:** This ensures a structured approach to translating requirements into a well-defined design document.
    - **BECAUSE:** A clear design process helps identify potential issues and ambiguities early.

- **RULE:** Unit test plans **MUST** be created based on design specifications following the procedure outlined in [[/procedure-unit-test-plan-from-design.md]].

  - **BECAUSE:** This ensures that unit tests systematically cover the requirements and design intentions before coding begins, aligning with the TDD approach.
    - **BECAUSE:** A test plan derived from the design provides a clear roadmap for test implementation and ensures critical paths and edge cases are considered early.
      - **BECAUSE:** Verifying against the design helps catch potential design flaws or ambiguities before they are implemented in code.

- **RULE:** Design reviews **MUST** be conducted following the process outlined in [[/procedure-design-review.md]].

  - **BECAUSE:** This ensures designs are thoroughly evaluated against project standards and best practices before implementation.
    - **BECAUSE:** A consistent review process improves design quality and catches potential issues early.

- **RULE:** Task planning and status tracking **MUST** follow the procedures defined in [[/procedure-status-tracking-rules.md]].

  - **BECAUSE:** Consistent status tracking provides visibility into project progress and helps manage dependencies and timelines effectively.
    - **BECAUSE:** Clear task planning ensures that work is well-defined and aligned with project goals.
      - **BECAUSE:** Effective tracking facilitates communication within the team and allows for timely identification and mitigation of potential roadblocks.

- **RULE:** New procedures **MUST** be created following the guidelines in [[/procedure-procedure-creation-rules.md]].
  - **BECAUSE:** This ensures consistency in how procedures are defined, documented, and structured.
    - **BECAUSE:** Standardized procedures are easier to understand, follow, and maintain across the project.
      - **BECAUSE:** It promotes clarity and reduces ambiguity in process documentation.


- **RULE:** When linking between markdown files within this project, links **MUST** use a forward slash `/` to denote the project root, followed by the specific folder names and the filename (e.g., `[[/design/architecture/Architecture-Overview.md]]`). Relative paths (e.g., `../../procedure-code-review.md`, `./local-file.md`) **MUST NOT** be used.
- **EXAMPLE (Correct):** `[[/procedure-coding-rules.md]]`, `[[/design/architecture/Architecture-Overview.md]]`
- **EXAMPLE (Incorrect):** `[[../../procedure-coding-rules.md]]`, `[[./procedure-coding-rules.md]]`
- **BECAUSE:** Absolute paths from the project root ensure links remain valid regardless of the file's location or future directory restructuring.
  - **BECAUSE:** This improves maintainability and reduces broken links as the project evolves.
    - **BECAUSE:** Consistent linking simplifies navigation and understanding of the documentation structure.

- **RULE:** To find the definition file for a specific type, interface, or class within the `src` directory, use the `grep` command with appropriate flags. Check `[[definitions.md]]` first for the canonical path.
  - **EXAMPLE (Type):** `grep -rFn --include='*.ts' "type MyType" src` (Primarily search in `src/types/`)
  - **EXAMPLE (Interface):** `grep -rFn --include='*.ts' "interface MyInterface" src` (Primarily search in `src/interfaces/`)
  - **EXAMPLE (Class):** `grep -rFn --include='*.ts' "class MyClass" src` (Search within module folders in `src/`)
  - **BECAUSE:** Provides a standard command-line method for locating definitions quickly within the TypeScript source files, considering the structure defined in the Coding Rules.
    - **BECAUSE:** Using specific keywords (`type`, `interface`, `class`) and the exact name increases search accuracy.
      - **BECAUSE:** Efficient code navigation is essential for understanding dependencies and implementing changes correctly.

## 3. Review and Updates

- **RULE:** This document **SHOULD** be reviewed periodically and updated as development practices evolve.
  - **BECAUSE:** Keeping the standards document current ensures it remains a relevant and accurate guide for the team.
    - **BECAUSE:** Project needs and best practices can change over time.

## 4. AI Assistant Interaction Confirmation

- **RULE (For AI Assistants):** Upon completing the reading and internal processing of *this specific document* (`procedure-dev-standards.md`) as part of fulfilling a user request, you **MUST** explicitly state the following: "I have come to the end of the dev standards and I have read the following documents:" followed by a list of *all* documents (including this one) read using the `read_file` tool during the execution of the current task.
  - **BECAUSE:** This provides explicit confirmation to the user that the core standards have been processed and acknowledges the context gathered from supporting documents for the current operation.
    - **BECAUSE:** Transparency about the information processed helps the user verify the AI's understanding and context.

--- END OF FILE procedure-dev-standards.md ---