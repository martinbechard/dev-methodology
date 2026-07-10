# Procedure: Creating Procedure Rules Documents

## 1. Purpose and Scope

- **RULE:** This document defines the process for creating new procedure documents (like procedure-coding-rules.md, procedure-testing-rules.md).
  - **BECAUSE:** Ensures consistency, clarity, justification, and maintainability across all procedural documentation within the project.
    - **BECAUSE:** Consistent procedures reduce ambiguity and learning time for developers (or LLMs) using them.
      - **BECAUSE:** Clear, well-justified rules are easier to understand, follow, and agree upon, leading to better adherence and code quality.

## 2. Source Identification and Rule Extraction

- **RULE:** Clearly identify the source documents or primary inputs from which the procedure rules are derived (e.g., refactoring-plan-gemini.md, specific design documents, meeting notes, user requests).
  - **BECAUSE:** Provides context and traceability for the rules, allowing verification against the original intent.
    - **BECAUSE:** Understanding the source helps interpret the rules correctly if ambiguity arises later.
- **RULE:** Extract specific principles, constraints, commands, best practices, or explicit instructions from the source materials to form the basis of the rules.
  - **BECAUSE:** Ensures the procedure accurately reflects the requirements and decisions captured in the source documents.
    - **BECAUSE:** Avoids inventing rules not grounded in project decisions or established practices.

## 3. Rule Formulation

- **RULE:** Formulate rules using clear, direct, and imperative language.
  - **BECAUSE:** Reduces ambiguity and clearly states the required action or constraint.
- **RULE:** Use standard requirement keywords consistently:
  - MUST / MUST NOT: Indicate absolute requirements or prohibitions.
  - SHOULD / SHOULD NOT: Indicate strong recommendations where exceptions might exist but need justification.
  - MAY: Indicate optional actions or permissions.
  - **BECAUSE:** These keywords have well-understood meanings (RFC 2119) and clearly convey the level of obligation for each rule.
- **RULE:** Each rule **MUST** focus on a single, specific action, constraint, or principle.
  - **BECAUSE:** Keeps rules granular and easy to understand, test (if applicable), and reference.
    - **BECAUSE:** Avoids combining multiple unrelated requirements into one complex rule.
- **RULE:** Start each rule statement explicitly with the RULE: keyword.
  - **BECAUSE:** Clearly delineates rules from explanatory text or justifications, improving readability and scannability.

## 4. Justification (BECAUSE Clauses)

- **RULE:** Every RULE: **MUST** be followed by at least one BECAUSE: clause explaining the primary reason for the rule.
  - **BECAUSE:** Justification promotes understanding and buy-in, moving beyond arbitrary instructions to reasoned guidelines.
    - **BECAUSE:** Explaining the 'why' helps developers apply the rule correctly in different contexts and understand its importance.
- **RULE:** Apply the "5 Whys" technique (or similar drill-down reasoning) to add nested BECAUSE: clauses, explaining the reasoning behind the parent BECAUSE: or RULE:.
  - **BECAUSE:** Deeper justification clarifies the fundamental principles or consequences driving the rule, providing richer context.
    - **BECAUSE:** This helps ensure the rule is well-founded and addresses the root cause or core benefit.
- **RULE:** Stop adding nested BECAUSE: clauses when the explanation becomes fundamental, self-evident within the project context, references an established external principle (e.g., SRP, OCP), or cannot be broken down further meaningfully.
  - **BECAUSE:** Avoids excessive or circular justifications, keeping the explanation concise and focused on practical reasoning.
- **RULE:** Ensure each BECAUSE: clause directly explains or supports its immediate parent (RULE: or preceding BECAUSE:).
  - **BECAUSE:** Maintains a clear logical chain of reasoning from the rule to its underlying justifications.
- **RULE:** Parallel BECAUSE: clauses at the same indentation level are acceptable if they provide distinct, independent justifications for the same parent rule or reason.
  - **BECAUSE:** Some rules have multiple benefits or address several concerns simultaneously.

## 5. Structure and Formatting

- **RULE:** Procedure documents **MUST** be created in Markdown (.md) format.
  - **BECAUSE:** Markdown is widely supported, easy to read/write, and integrates well with version control and many documentation tools.
- **RULE:** Use clear headings (#, ##, ###) to structure the document into logical sections and sub-sections.
  - **BECAUSE:** Improves navigation and allows readers to quickly find relevant sections.
- **RULE:** Number sections and rules sequentially for easy referencing.
  - **BECAUSE:** Allows specific rules or sections to be referred to unambiguously (e.g., "See rule 4.2").
- **RULE:** Name procedure files using the pattern procedure-<topic>-rules.md (e.g., procedure-coding-rules.md).
  - **BECAUSE:** Creates a consistent and predictable naming convention for locating procedure documents.
- **RULE:** Use consistent formatting for keywords:

  - RULE: (Bold)
  - BECAUSE: (Bold, indented under the clause it explains)
  - EXAMPLE: (Bold, indented, used to provide concrete illustrations)
  - FORMAT: (Bold, indented, used to specify syntax or layout)
  - PENALTY: (Bold, indented, used for externally defined consequences from source docs)
  - **BECAUSE:** Consistent formatting enhances readability and makes the document structure immediately apparent.

- **RULE:** Nested `BECAUSE:` clauses **MUST** use ASCII line characters (`├──`, `│`, `└──`) to visually represent the tree structure and logical hierarchy of justifications, following the 5 Whys principle.
  - **FORMAT:**
    ```
    RULE: Top-level rule statement.
    ├── BECAUSE: First-level reason 1.
    │   └── BECAUSE: Second-level reason branching from reason 1.
    ├── BECAUSE: First-level reason 2.
    └── BECAUSE: Last first-level reason.
        └── BECAUSE: Second-level reason branching from the last reason.
    ```
  - **BECAUSE:** This specific format makes the logical flow and relationship between justifications exceptionally clear and easy to follow.
    - **BECAUSE:** Visual hierarchy aids comprehension, especially for complex reasoning chains.
    - **BECAUSE:** It standardizes the presentation of the 5 Whys analysis within the documentation.
- **RULE:** Include specific, relevant EXAMPLE: blocks where they significantly clarify a rule's application.
  - **BECAUSE:** Concrete examples are often easier to understand than abstract descriptions alone.
- **RULE:** Use [[path/to/other/document.md]] syntax for cross-references to other documents within the project repository.
  - **BECAUSE:** Creates navigable links (in supporting tools) and clearly indicates dependencies on other documentation.

## 6. Refinement and Review

- **RULE:** After drafting a procedure document, review it against the rules defined in this document (procedure-procedure-creation-rules.md).
  - **BECAUSE:** Ensures the new procedure itself adheres to the established meta-procedure for consistency (dogfooding).
- **RULE:** Seek review and feedback from the intended audience or stakeholders (e.g., the user requesting the procedure, developers who will use it).
  - **BECAUSE:** Feedback helps identify ambiguities, missing rules, incorrect assumptions, or areas needing better justification from the user's perspective.
- **RULE:** Iterate on the procedure document based on feedback until it is clear, comprehensive, accurate, and agreed upon.
  - **BECAUSE:** Ensures the final procedure is effective and serves its intended purpose for the project.
