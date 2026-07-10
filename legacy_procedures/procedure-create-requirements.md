# Procedure: Creating Requirements Documents

## 1. Purpose and Scope

**RULE:** This document defines the process for creating new building block specification documents using the standardized template.
  **BECAUSE:** Ensures consistency, clarity, and completeness across all building block specification documents.
    **BECAUSE:** Consistent specifications facilitate better understanding and implementation by developers.
      **BECAUSE:** Well-structured requirements lead to more accurate and efficient implementations.

**RULE:** This procedure applies to all building block specifications created during the project lifecycle.
  **BECAUSE:** Maintains a unified approach to documenting requirements throughout the project.

## 2. Preparation

**RULE:** Identify the specific building block or component that needs specification.
  **BECAUSE:** Clear identification ensures focus and prevents scope creep in the specification.

**RULE:** Gather all relevant source materials and discussions related to the building block.
  **BECAUSE:** Comprehensive input ensures the specification accurately reflects stakeholder needs and project requirements.
    **BECAUSE:** Missing information leads to incomplete or incorrect specifications.

**RULE:** Use the template file located at `templates/building-block-specification-template.md` as the starting point.
  **BECAUSE:** The template ensures structural consistency across all building block specifications.
    **BECAUSE:** Consistency makes specifications easier to read, compare, and implement.

## 3. Document Structure and Content Guidelines

**RULE:** Name the document according to the pattern: `[Building Block Name] Specification.md`
  **BECAUSE:** Consistent naming improves document discoverability and organization.

**RULE:** Fill out all required sections in the template, replacing placeholders with appropriate information.
  **BECAUSE:** Complete documentation ensures all aspects of the building block are properly specified.

**RULE:** Stick to the essentials and respect the requested limits; when limits are not specified, don't exceed 5-7 bullet points per section.
  **BECAUSE:** Concise documentation is more understandable for both humans and LLMs.
    **BECAUSE:** More detailed specifications will be created from this initial document.
    **BECAUSE:** Test-Driven Development will be used to finalize the implementation design.

**RULE:** Explain by example where possible, but don't create excessive code examples.
  **BECAUSE:** Examples clarify requirements but too much code can cause confusion in the future.
    **BECAUSE:** The focus is on functional and technical requirements, not implementation details.

**RULE:** Do not include interfaces, classes, or code implementations in the specification.
  **BECAUSE:** We will be developing using Test-Driven Development, so implementation details belong in the design and code, not the requirements.
    **BECAUSE:** Including implementation details prematurely can constrain the design process.

**RULE:** Use clear, simple language rather than overly technical or verbose descriptions.
  **BECAUSE:** Simple language improves understanding and reduces misinterpretation.
    **BECAUSE:** Requirements should be accessible to all stakeholders, not just technical team members.

## 4. Section-Specific Guidelines

### Building Block Name

**RULE:** Provide a clear, descriptive name that reflects the component's primary purpose.
  **BECAUSE:** The name establishes identity and helps team members quickly understand the component's role.

### Purpose

**RULE:** Describe the core purpose in 1-2 concise sentences.
  **BECAUSE:** A brief, focused purpose statement provides immediate clarity about the component's role.
    **BECAUSE:** This sets the context for all other sections of the specification.

### Core Responsibilities

**RULE:** List 3-7 primary responsibilities that define what the building block does.
  **BECAUSE:** Clear responsibilities define the scope and boundaries of the component.
    **BECAUSE:** This prevents feature creep and helps maintain the Single Responsibility Principle.

**RULE:** Express responsibilities as action statements (e.g., "Store and organize prompts" rather than "Prompt storage").
  **BECAUSE:** Action-oriented descriptions clarify what the component actively does.
    **BECAUSE:** This makes responsibilities more concrete and testable.

### Interfaces

**RULE:** Clearly define all inputs the component receives or consumes.
  **BECAUSE:** Well-defined inputs establish what the component needs to function properly.

**RULE:** Clearly define all outputs the component produces or provides.
  **BECAUSE:** Well-defined outputs establish what other components can expect from this one.

**RULE:** List all dependencies on other components.
  **BECAUSE:** Documented dependencies clarify integration points and potential coupling.
    **BECAUSE:** This helps in planning implementation order and identifying potential risks.

### Key Behaviors

**RULE:** Describe 3-5 key behaviors focusing on how the component acts in different scenarios.
  **BECAUSE:** Behavioral descriptions provide insight into the component's runtime characteristics.
    **BECAUSE:** This helps implementers understand the expected functionality beyond static properties.

**RULE:** Focus on behaviors that are essential to the component's core purpose.
  **BECAUSE:** Essential behaviors highlight the most important aspects that must be implemented correctly.

### Implementation Considerations

**RULE:** Include only important technical notes or constraints specific to this component.
  **BECAUSE:** These provide critical context for implementation decisions.
    **BECAUSE:** This section helps bridge requirements and design.

**RULE:** Do not include routine architecture standards or practices that apply to all components.
  **BECAUSE:** Standard practices belong in separate documentation to avoid repetition.
    **BECAUSE:** Focus should remain on unique considerations for this specific component.

### C4 Model Diagrams

**RULE:** Include all four required C4 diagrams (Context, Container, Component, and Dynamic).
  **BECAUSE:** These diagrams provide visual representations of the component from different perspectives.
    **BECAUSE:** Visual models improve understanding of complex relationships and interactions.

**RULE:** Customize the diagram templates already present in the template file to accurately reflect the specific building block.
  **BECAUSE:** Generic diagrams don't provide valuable insights for implementation.
    **BECAUSE:** Accurate diagrams serve as important design documentation.

**RULE:** Use the existing diagram examples in the template as a starting point rather than creating diagrams from scratch.
  **BECAUSE:** The template includes properly formatted mermaid diagram examples for all four C4 diagram types.
    **BECAUSE:** Maintaining consistent diagram structure improves readability across specifications.

**RULE:** Ensure diagrams are consistent with the textual descriptions in other sections.
  **BECAUSE:** Inconsistencies between text and diagrams create confusion and implementation errors.

### Nice to Have

**RULE:** Include only features that were actually discussed but deemed non-essential.
  **BECAUSE:** This maintains a clear distinction between requirements and potential enhancements.
    **BECAUSE:** This provides context for future extension without blurring current requirements.

### Undiscussed Suggestions

**RULE:** Only include suggestions that are directly relevant to the building block's purpose.
  **BECAUSE:** Relevant suggestions provide value for future consideration.
    **BECAUSE:** Suggestions that diverge from the core purpose can dilute focus.

**RULE:** Limit this section to no more than 5 items.
  **BECAUSE:** Too many suggestions can overwhelm and detract from the core requirements.

## 5. Review and Refinement

**RULE:** Review the completed specification for clarity, completeness, and consistency.
  **BECAUSE:** Self-review helps identify gaps or inconsistencies before sharing with others.
    **BECAUSE:** High-quality specifications lead to higher-quality implementations.

**RULE:** Ensure the specification captures functional and technical requirements, as well as the intended usage in the big picture.
  **BECAUSE:** Context about how the component fits into the overall system is crucial for proper implementation.

**RULE:** Check that all diagrams accurately reflect the textual descriptions.
  **BECAUSE:** Alignment between diagrams and text prevents misunderstandings during implementation.

**RULE:** Seek feedback from stakeholders and revise as needed before finalizing.
  **BECAUSE:** Stakeholder validation ensures the specification meets actual needs.
    **BECAUSE:** Early feedback reduces the cost of changes later in the development process.

## 6. Example Sections

### Example Purpose Section

**EXAMPLE:**
```markdown
## Purpose
Manages storage, retrieval, versioning, and customization of prompts used throughout the system, providing a centralized prompt repository with specialized support for decision-making prompts.
```

### Example Core Responsibilities Section

**EXAMPLE:**
```markdown
## Core Responsibilities
- Store and organize prompts in structured repositories
- Support versioning and change tracking for prompts
- Provide prompt retrieval by ID, category, or purpose
- Enable customization of prompts at organization/department levels
- Validate prompt structures and parameters
```

### Example Interfaces Section

**EXAMPLE:**
```markdown
## Interfaces
- **Inputs**:
  - Prompt creation and update requests
  - Prompt retrieval requests (by ID, purpose, etc.)
  - Customization specifications

- **Outputs**:
  - Formatted prompts ready for use
  - Prompt metadata and version information
  - Validation results

- **Dependencies**:
  - Unix-like Storage System
  - Document Retriever
```

### C4 Model Diagrams Note

**RULE:** For C4 Model diagrams, use the examples in the template file as a starting point and customize them to accurately represent your specific building block.
  **BECAUSE:** The template already contains correctly formatted mermaid diagrams for all four required C4 diagram types.
    **BECAUSE:** It's easier to modify existing diagrams than to create new ones from scratch while maintaining proper C4 notation.

**EXAMPLE:**
```
See the template file for complete diagram examples. All four diagram types (Context, Container, Component, and Dynamic) must be included and customized to reflect your specific building block.
```