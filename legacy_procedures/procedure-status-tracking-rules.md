# Procedure: Status Tracking File Creation and Management

## 1. Purpose and Scope

- **RULE:** This document defines the process for creating and managing project status tracking files (e.g., refactoring-plan-status.md).
  - **BECAUSE:** To provide a clear, sequential, and trackable plan for executing development or refactoring tasks, especially when guided by an AI assistant.
    - **BECAUSE:** A structured plan ensures work is performed in the intended order, preventing out-of-sequence changes that could cause regressions or unnecessary complexity.
    - **BECAUSE:** Explicit status tracking allows both the user and the AI to know exactly what has been completed and what the next step is, reducing confusion and rework.
- **RULE:** The status file serves as the primary guide for the AI assistant's workflow execution for the tasks it covers.
  - **BECAUSE:** It centralizes the plan and progress, acting as a shared understanding of the work sequence and state.

## 2. File Naming and Format

- **RULE:** Status tracking files **MUST** be created in Markdown (.md) format.
  - **BECAUSE:** Markdown is readable, universally supported, and allows for easy integration of structure (headings, lists, links) and status indicators (checkboxes).
- **RULE:** Name status files descriptively, often related to the project phase or feature, ending with -status.md.
  - **EXAMPLE:** refactoring-plan-status.md, feature-x-implementation-status.md.
  - **BECAUSE:** Creates a consistent and predictable naming convention for locating status documents.

## 3. Structure and Content

- **RULE:** Structure the plan using logical **Phases** indicated by top-level headings (#, ##).
  - **EXAMPLE:** ## Phase 3: Unit Test Failure Remediation
  - **BECAUSE:** Groups related sequences of tasks, providing high-level structure to the plan.
- **RULE:** Each Phase or major Task group **SHOULD** include a brief Reason: or Note: explaining the context or goal of that section.
  - **BECAUSE:** Provides context for why the subsequent tasks are necessary.
- **RULE:** Define major work items as numbered **Tasks** (e.g., 1., 2.). Tasks often correspond to a specific module, component, test file, or significant refactoring goal.
  - **EXAMPLE:** 1. ⬜ Failing unit test for module [QuoteProcessor](/test/services/workflow/QuoteTradeWorkflow/QuoteProcessor.test.ts)
  - **BECAUSE:** Breaks down the overall plan into manageable, high-level objectives.
- **RULE:** Break down Tasks into specific, actionable **Subtasks** using bullet points (- or \*) indented under the parent Task.
  - **BECAUSE:** Provides the granular, step-by-step instructions needed for execution and precise status tracking.
- **RULE:** Subtasks **MUST** be written using clear, imperative language describing a single, verifiable action.
  - **EXAMPLE:** ⬜ UpdateQuoteTradeWorkflowinstantiation..., ⬜ Run failing tests..., ⬜ Verify file exists...
  - **BECAUSE:** Ensures instructions are unambiguous and progress can be clearly determined upon completion of the action. Avoid vague subtasks like "Fix issues".
- **RULE:** Link relevant files, designs, or definitions using Markdown links ([display text](path/or/link)) or wiki-links ([[path/to/file.md]]) within Tasks or Subtasks where appropriate. Reference [[design/definitions.md]] when discussing specific Classes/Interfaces/Types.
  - **BECAUSE:** Provides direct access to necessary context or artifacts referenced in the plan.
- **RULE:** If the main status tracking file exceeds approximately 200 lines, it **SHOULD** be refactored for better manageability by extracting large tasks into subplan files.
  - **Refactoring Steps:**
    1.  Identify Tasks within the main file that have a large number of Subtasks (e.g., more than 5-7).
    2.  Create a dedicated sub-directory if one doesn't exist (e.g., adjacent to the main status file, named [main-status-file-name]-subplans/).
    3.  For each identified large Task:
        - Create a new Markdown file within the sub-directory, named descriptively based on the Task (e.g., task-module-xyz-status.md).
        - Move the original Task heading (including its number and description) and all its associated Subtasks from the main status file into this new subplan file.
        - Ensure the subplan file follows the standard status tracking format defined in this procedure.
        - In the main status file, replace the moved Task and its Subtasks with a single placeholder line that includes the original Task number/description and a link to the subplan file. The placeholder **SHOULD** retain a primary status checkbox reflecting the overall status of the subplan (marked ✅ only when all subtasks in the linked file are complete).
          - **EXAMPLE:** 3. ⬜ Task for Module XYZ (See Subplan: [[path/to/subplans/task-module-xyz-status.md]])
  - **BECAUSE:** Prevents the main status file from becoming excessively long, improving readability, navigation, and maintainability.
    - **BECAUSE:** Large files hinder quick scanning and increase cognitive load when trying to find specific tasks or overall progress.
    - **BECAUSE:** Breaking complex tasks into subplans allows focused work on those tasks without the distraction of unrelated items in the main file.
    - **BECAUSE:** Smaller files can reduce the scope of merge conflicts in version control systems.

## 4. Status Indicators

- **RULE:** Every actionable Subtask **MUST** start with a status indicator checkbox. Tasks that link to subplans will also have a primary checkbox reflecting the overall subplan status.
  - **BECAUSE:** This is the primary mechanism for tracking granular and high-level progress.
- **RULE:** Use the following standard status indicators:
  - ⬜: **Pending** - The subtask (or linked subplan) has not yet been started or completed.
  - ▶️: **Actively Working On** - The AI is currently executing this specific subtask. Only one subtask should have this status at any given time within a plan/subplan.
  - ⏳: **In Progress** - Work has started on the linked subplan but is not yet complete. (Use only for main plan tasks linking to subplans).
  - ✅: **Completed** - The subtask (or all tasks in the linked subplan) has been successfully executed and verified.
  - N/A: **Not Applicable** - The subtask was determined to be unnecessary or irrelevant during execution (e.g., a conditional step whose condition was not met). Requires explanation if not obvious.
  - MISSING: **Blocked/Design Missing** - Used (as per refactoring-plan-gemini.md) when progress is blocked due to a missing prerequisite, typically a design document.
  - **BECAUSE:** Provides a clear, consistent visual language for the state of each specific step or major task group.
- **RULE:** The primary checkbox for a Task linking to a subplan (e.g., 3. ⬜ Task... (See Subplan: [[...]])) **SHOULD** only be marked ✅ when all actionable subtasks within the linked subplan file are marked ✅. It **SHOULD** be marked ⏳ when work on the subplan has started but is not yet complete.
  - **BECAUSE:** Provides an accurate summary status in the main plan file.

## 5. Updating the Status

- **RULE:** The status file (main or subplan) **MUST** be updated **immediately** before and after a Subtask is attempted.
  - **BECAUSE:** Ensures the status file accurately reflects the real-time progress and current focus of the work.
- **RULE:** The update process **MUST** follow the mandatory procedure defined in refactoring-plan-gemini.md (Section: Mandatory Status Check & Update):
  1.  **Before Execution:** Read the current relevant \*-status.md file. Apply a diff changing the pending (⬜) Subtask's indicator to actively working on (▶️). Wait for confirmation.
  2.  **Execute Action:** Perform the action described in the Subtask (e.g., use a tool, run a command).
  3.  **After Execution:** Read the relevant \*-status.md file again. Apply a diff changing the actively working on (▶️) Subtask's indicator to the final state (✅, N/A, or back to ⬜ if failed/retrying). Wait for confirmation before proceeding to identify the next pending (⬜) Subtask.
  - **BECAUSE:** This explicit read-diff-confirm process ensures atomic and accurate updates, preventing race conditions or missed updates, which is critical for AI-driven execution. It clearly shows which task is being attempted.
- **RULE:** When starting the first subtask of a subplan, or completing the last subtask of a subplan, the corresponding Task's status indicator in the **main** plan file **MUST** also be updated (⬜ -> ⏳ or ⏳ -> ✅). This requires a separate read/write operation on the main plan file immediately following the subplan file update (specifically, after the subtask's status changes to ▶️ for the first task, or after it changes to ✅ for the last task).
  - **BECAUSE:** Keeps the high-level summary status in the main plan synchronized with the detailed progress in the subplan.
- **RULE:** Only update a status to ✅ upon **successful** completion and verification (e.g., tests passing, command executed without error). Do not update if an attempt failed; revert to ⬜ or use a specific failure indicator if defined.
  - **BECAUSE:** The ✅ mark signifies successful completion, not just an attempt.
- **RULE:** If new tasks or regressions are identified (e.g., after a "Run all tests" subtask), add them to the relevant status file (main or subplan) as new ⬜ Tasks or Subtasks in the appropriate sequence or phase, potentially marking them as **NEW:**.
  - **BECAUSE:** Keeps the status file comprehensive and ensures all required work, including newly discovered items, is tracked and executed.

## 6. Sequencing and Dependencies

- **RULE:** Subtasks within a Task (or subplan file), and Tasks within a Phase, **MUST** generally be executed in the order they appear in the file.
  - **BECAUSE:** The sequence usually reflects logical dependencies or a specific workflow (like the TDD cycle).
- **RULE:** Explicitly note any critical sequencing constraints or dependencies within the plan.
  - **EXAMPLE:** **Note:** This phase should only begin after all unit tests in Phase 3 are passing. or DO NOT attempt to fix other items out of order...
  - **BECAUSE:** Highlights critical workflow rules or dependencies that must be respected.
- **RULE:** Incorporate verification steps (like "Run specific test", "Run all tests", "Verify design alignment") as explicit ⬜ Subtasks at the appropriate points in the sequence.
  - **BECAUSE:** Ensures that verification is part of the tracked workflow and not skipped.

## 7. Review and Maintenance

- **RULE:** The initial status tracking plan **SHOULD** be reviewed for clarity, completeness, correctness of sequence, and actionability before starting execution. Consider if any tasks should be immediately extracted into subplans based on anticipated complexity.
  - **BECAUSE:** Ensures the plan is sound and understandable before work commences, reducing the chance of needing major corrections mid-execution. Proactive extraction can prevent the main file becoming unwieldy later.
- **RULE:** The status file(s) are living documents. Update them not only with status changes (▶️, ✅, etc.) but also with clarifications, newly identified tasks, or blocking notes (MISSING) as work progresses.
  - **BECAUSE:** The plan needs to adapt to discoveries made during implementation and testing to remain an accurate guide.
