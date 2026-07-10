# Procedure:  Document New Design
## 1. Purpose and Scope

- **RULE:** This document outlines the standard procedure for creating a design document for a **new** module or significant feature **before** implementation begins.
  - **BECAUSE:** It ensures that requirements, responsibilities, interactions, and key decisions are thought through and documented upfront.
    - **BECAUSE:** A clear design specification guides implementation, facilitates communication, enables effective reviews, and reduces ambiguity.
      - **BECAUSE:** Planning the design before coding leads to more robust, maintainable, and well-integrated solutions, minimizing costly rework later.

- **RULE:** This procedure applies whenever a new, non-trivial module, class, or distinct functional component is being introduced to the project.
  - **BECAUSE:** It establishes a consistent approach for specifying new pieces of the system architecture.

## 2. Preparation and Pre-computation

- **RULE:** Before starting the design document, **MUST** understand the requirements and goals for the new module.
  - **BECAUSE:** The design must directly address the problem or need it's intended to solve.

- **RULE:** **MUST** check existing design documents in `design/modules/` and the central registry [[definitions.md]] for any existing components (classes, types, interfaces) that might be reusable or related.
  - **BECAUSE:** Avoiding duplication and leveraging existing components promotes consistency and efficiency, as mandated by [[procedure-coding-rules.md]].

- **RULE:** **MUST** determine a proposed, unique name for the new module (e.g., `OrderProcessor`, `AuthService`). This name **SHOULD** follow the PascalCase convention if the primary export will be a class or component (as per [[procedure-coding-rules.md]]).
  - **BECAUSE:** A clear name is needed for the design document itself and for referencing the future module.

- **RULE:** **MUST** identify the proposed location (directory path) for the new module's code within the project structure (e.g., `src/services/`, `src/utils/`). This path **MUST** align with the organizational rules in [[procedure-coding-rules.md]].
  - **BECAUSE:** Defining the location upfront helps ensure the module fits logically within the existing architecture and aids in planning imports/dependencies.

## 3. Document Creation

- **RULE:** Create a new design document file named `<ProposedModuleName>-design.md` (e.g., `OrderProcessor-design.md`).
  - **BECAUSE:** This follows a consistent naming convention, linking the design directly to the component it specifies.

- **RULE:** Place the new design document in the `design/modules/` directory.
  - **BECAUSE:** This is the designated location for module-specific design documentation as per [[procedure-coding-rules.md]].

- **RULE:** If a preliminary or outdated design document for this module exists, its contents **SHOULD** be reviewed for relevance but the new document should be created fresh following this procedure unless updating the existing one is more appropriate. Consult with the user/mentor if unsure.
  - **BECAUSE:** Ensures the design process starts with current requirements and avoids carrying over outdated assumptions.

## 4. Required Sections

*Fill out the following sections in the newly created design document. Use the `BECAUSE` chain format extensively to justify decisions and explain reasoning.*

### 1. Basic Information

-   **Proposed Path**: The intended full path to the primary file of the module, formatted as a Markdown link (e.g., `[[/src/services/OrderProcessor.ts]]`).
    -   **BECAUSE:** Clearly identifies the intended location within the project structure and provides a navigable link.
-   **Responsibilities**: List the primary responsibilities this module **will** have (one clear statement per responsibility).
    -   **BECAUSE:** Defines the scope and purpose of the module upfront.
-   **Anticipated Structure**: If the module is expected to be complex or large (potentially >300 lines eventually), outline a potential logical separation into multiple files or sub-components. Note if specific classes or types might reside in separate files within the module's directory.
    -   **BECAUSE:** Encourages thinking about modularity and cohesion early in the design phase.

### 2. Intended Callers / Consumers

-   List the other modules, functions, or parts of the system that **will** call or use this new module. Each caller **MUST** be linked to its corresponding design document using the `[[path/to/caller-design.md]]` format.
    -   **BECAUSE:** Clearly identifies the components that depend on this new module and provides easy navigation to their designs.
-   For each intended caller, explain **WHY** it needs this module using the `BECAUSE` chain format.
    -   Example: "`UserController` [[/design/modules/UserController-design.md]] will call this module BECAUSE it needs to process the submitted order BECAUSE the controller orchestrates user requests."
-   Include conceptual examples of how the module is expected to be invoked.
    -   **BECAUSE:** Clarifies the module's role in the broader system and its primary interaction points.

### 3. Dependencies

-   **FORMAT:** Dependencies **MUST** be listed using Markdown list items (`-` or `*`), with the dependency name enclosed in backticks, followed by a link to its defining design document, and optionally a description/justification. Example: `-   \`DependencyName\` [[path/to/defining-design.md]]: Justification...`
-   List the other modules, functions, external libraries, or services that this new module **will** depend on. Reference specific classes/interfaces/types from [[definitions.md]] if relying on existing components.
-   **RULE:** The dependency list **MUST** explicitly identify each imported function, class, interface, or type by name and include a link to the design document where that specific entity is defined (using `[[path/to/defining-design.md]]`).
    -   **BECAUSE:** This ensures that the design explicitly acknowledges all external contracts and definitions it relies upon.
    -   **BECAUSE:** Linking to the defining design document makes it easy for reviewers and implementers to verify the dependency's contract and intended usage.
    -   **BECAUSE:** It helps identify potential coupling issues or missing dependencies early in the design phase.
-   For each dependency, explain **WHY** this module needs it using the `BECAUSE` chain format.
    -   Example: "This module will depend on `DatabaseService` [[design/modules/DatabaseService-design.md]] BECAUSE it needs to persist order data BECAUSE storing orders is a core responsibility."
-   Note any significant external systems (e.g., third-party APIs) it will interact with.
    -   **BECAUSE:** Identifies external coupling and helps assess potential integration challenges.

### 4. Context Diagrams

-   **Module Context Diagram**: Create a diagram (e.g., flowchart, sequence diagram fragment) showing the proposed module, its intended callers, and its key dependencies.
    -   Label interactions with proposed function/method names and the primary data being exchanged.
    -   Use clear, distinct names for diagrams to avoid conflicts.
    -   **BECAUSE:** Provides a visual overview of the module's immediate ecosystem and interactions.
-   **(Optional but Recommended) Function Context Diagrams**: For key proposed public functions/methods, create simple diagrams illustrating their expected inputs, outputs, and interactions with dependencies, including potential error paths.
    -   **BECAUSE:** Helps visualize the flow of control and data for critical operations.

### 5. Invariant Rules

-   List critical requirements or constraints that the implemented module **MUST** always obey. Use the format:
    -   **RULE:** [Statement of the rule]
    -   **WHY:** [Chain of reasoning using BECAUSE]
    -   Example: "**RULE:** Order IDs generated must be unique across the system. **WHY:** Duplicate IDs would make tracking specific orders impossible BECAUSE the ID is the primary key."
-   Categorize rules if helpful (e.g., Security, Performance, Data Integrity, Business Logic).
    -   **BECAUSE:** Defines the non-negotiable constraints and quality attributes for the implementation.

### 6. Design Decisions

-   Document key choices made during the design process using the format:
    -   **Decision:** [Statement of the chosen approach]
    -   **Alternatives Considered:** [List other options briefly]
    -   **Rationale:** [Explain **WHY** this choice was made, using `BECAUSE` chains, referencing requirements or constraints]
    -   **Assumptions:** [List underlying assumptions that, if changed, might invalidate this decision]
-   Include significant trade-offs considered (e.g., performance vs. simplicity).
    -   **BECAUSE:** Records the reasoning behind the chosen architecture, aiding future understanding and maintenance.

### 7. Proposed Classes, Interfaces, and Types

-   Define the key data structures and contracts the module will expose or use internally.
-   For each proposed `class`, `interface`, or `type`:
    -   **Name**: The proposed name (following conventions in [[procedure-coding-rules.md]]).
    -   **Purpose**: A brief description of what it represents or does.
    -   **Properties/Data Members**: List intended members with their proposed types (use existing types from [[definitions.md]] where applicable) and brief descriptions.
    -   **Methods (for classes)**: List the proposed public methods with their intended signatures (parameters, return types). Implementation details go in Section 8.
    -   **Notes**: Mention any relevant design patterns intended (e.g., Factory, Singleton).
    -   **BECAUSE:** Specifies the intended public API and internal structure, providing a blueprint for implementation.

### 8. Proposed Functions / Methods

-   List the key functions or class methods (especially public ones) the module will contain. Organize them logically (e.g., top-down flow, by responsibility).
-   For each significant function/method:
    -   **Purpose**: Brief description of what it does and **WHY** it's needed.
    -   **Signature**: Proposed parameters (consider using parameter objects for >2 params as per [[procedure-coding-rules.md]]), return type, and potential exceptions/error types it might throw (aligning with [[/design/error-strategy.md]]).
    -   **High-Level Logic / Pseudo-code**: Outline the intended steps using structured language (e.g., following [[pseudo-code-rules]]). Focus on the core logic, key decisions, and interactions with dependencies. Use `BECAUSE` chains to explain critical logic steps.
        ```
        PROCEDURE processOrder(orderData)
          VALIDATE orderData against OrderSchema BECAUSE invalid data must be rejected early
          IF validation fails THEN
            THROW InvalidOrderError BECAUSE processing cannot continue
          END IF
          CALCULATE orderTotal based on items and pricing rules BECAUSE accuracy is required
          CALL DatabaseService.saveOrder(processedOrder) BECAUSE the order must be persisted
          RETURN orderId BECAUSE the caller needs confirmation
        END PROCEDURE
        ```
    -   **Error Handling**: Briefly describe how errors identified within this function will be handled (e.g., logged, thrown, returned).
    -   **BECAUSE:** Details the intended behavior and implementation strategy for the core logic of the module.

### 9. Processing Rules (If Applicable)

-   For modules implementing complex workflows, state machines, or intricate business logic:
    -   Document states and transitions (visual diagram recommended).
    -   Define conditions for state changes.
    -   Explain the processing logic associated with each state or step, using `BECAUSE` chains for rationale.
    -   **BECAUSE:** Clearly specifies the behavior for complex, stateful processes.

### 10. Proposed API Calls (If Applicable)

-   If the module will directly call external APIs:
    -   For each distinct API endpoint to be called:
        -   **Purpose**: Why is this API call needed?
        -   **Endpoint**: URL and HTTP Method (GET, POST, etc.).
        -   **Authentication/Headers**: Required headers or auth mechanisms.
        -   **Request Payload**: Structure and key parameters. Explain **WHY** data is mapped in a specific way if not obvious.
        -   **Expected Response Payload**: Structure and key data to be extracted. Note fields that will be ignored.
        -   **Error Handling**: How API errors (e.g., 4xx, 5xx, timeouts) will be handled.
    -   **BECAUSE:** Defines the contract and interaction pattern with external services.

### 11. Configuration Needs

-   Document any configuration parameters the module **will** require.
    -   **Parameter Name**: The proposed name for the configuration setting.
    -   **Purpose**: What does this parameter control?
    -   **Format/Type**: (e.g., string, number, boolean, environment variable, config file key).
    -   **Default Value (if any)**: The proposed default.
    -   **Validation Rules (if any)**: (e.g., must be positive integer, must be a valid URL).
    -   **BECAUSE:** Identifies necessary external configuration points for flexibility and environment adaptation.

### 12. Testing Strategy

-   Outline the proposed approach for testing this module.
    -   **Unit Tests**: Key scenarios, edge cases, and responsibilities to cover. List major dependencies that **will** need mocking.
    -   **Integration Tests (if applicable)**: Scenarios involving interaction with real dependencies (or high-fidelity mocks) that should be tested. Mention relevant integration test plans in `design/integration-test-plans/` if applicable.
    -   **Key Considerations**: Any specific challenges or areas requiring careful test design.
    -   **BECAUSE:** Ensures testability is considered from the beginning and guides the creation of effective tests.

## 5. Best Practices During Design

1.  **Clarity and Precision**: Use unambiguous language. Define terms if necessary.
2.  **Consistency**: Maintain consistent terminology and formatting throughout the document.
3.  **Rationale (BECAUSE)**: Justify significant decisions, rules, and logic steps using the `BECAUSE` chain format.
4.  **Visuals**: Use diagrams where they aid understanding (context, state transitions, complex flows).
5.  **Focus**: Keep the design focused on the module's responsibilities. Avoid over-designing or adding unnecessary complexity.
6.  **Reviewability**: Organize the document logically to facilitate review according to [[procedure-design-review.md]].
7.  **Single Responsibility Principle (SRP)**: Aim for modules and classes that have a single, well-defined purpose. If a module seems to have too many unrelated responsibilities, consider splitting the design.
8.  **Precision (New Rule)**: **RULE:** Statements **MUST** be precise and avoid vague language.
    -   **BECAUSE:** Ambiguity leads to misinterpretation during review and implementation.
        -   **BECAUSE:** Clear, specific statements ensure everyone understands the exact intent.
9.  **Source of Truth (New Rule)**: **RULE:** When referencing a canonical source (e.g., a constant from `stateVariableKeys.ts`, an interface from `definitions.md`), present it as the required definition, not merely an "example".
    -   **BECAUSE:** Using "example" implies potential variation, undermining the authority of the source of truth.
        -   **BECAUSE:** Clearly stating the required definition ensures consistency and correct implementation according to established standards.

## 6. Next Steps

-   **RULE:** After drafting the design document, **MUST** run the dependency verification script (`node scripts/verify_design_dependencies.js path/to/your-design.md`) and address any "Missing/Incorrect Dependencies" reported by ensuring the dependency is correctly listed in [[definitions.md]] and defined in its specified source file.
    -   **BECAUSE:** This proactively catches inconsistencies between the design's stated dependencies and the central registry/codebase before review.
    -   **BECAUSE:** Resolving these issues upfront streamlines the design review process.
-   **RULE:** Once the initial draft of the design document is complete and dependency verification passes, it **MUST** be submitted for review following the process outlined in [[procedure-design-review.md]].
    -   **BECAUSE:** Peer review helps identify flaws, inconsistencies, and areas for improvement before implementation effort is spent.
-   **RULE:** Feedback from the review **MUST** be addressed, potentially requiring updates to the design document.
    -   **BECAUSE:** Incorporating feedback improves the quality and robustness of the final design.
-   **RULE:** After the design is finalized and approved, relevant new Classes, Interfaces, Types, and their canonical paths **MUST** be added to [[definitions.md]].
    -   **BECAUSE:** This registers the newly designed components in the central registry, making them discoverable and establishing their authoritative location before implementation, as required by [[procedure-coding-rules.md]].
-   **RULE:** The approved design document becomes the primary specification for implementing the module. The implementation code **MUST** reference this design document in its file header (e.g., `// Design: [[design/modules/MyModule-design.md]]`).
    -   **BECAUSE:** Maintains the crucial link between specification and implementation.