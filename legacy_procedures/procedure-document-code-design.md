# Module Design Documentation Procedure

This procedure outlines how to create comprehensive design documentation for code modules. Follow these steps for any module you want to document.

## Preparation
1. Read any existing design documents related to the module to document
2. Create a design document named `<module file name>-design.md` and place it in `design/modules`
3. Check if one already exists, and delete its content first if it does

## Required Sections

### 1. Basic Information
- **Path**: Full path to module within the project
- **Responsibilities**: List each responsibility of the module (one line each)
- **Module Structure**: If the module is large (>300 lines), suggest a logical separation into multiple files

### 2. Callers
- List what other modules/functions are calling this module
- For each caller, explain WHY using the BECAUSE chain format
  - Example: "ModuleA calls this BECAUSE it needs to validate user input BECAUSE..."
- Include typical calling patterns with code examples

### 3. Dependencies
- List what other modules/functions this module depends on
- For each dependency, explain WHY using the BECAUSE chain format
- Include any notable external libraries or services

### 4. Context Diagrams
- **Module Context Diagram**: Create a flow chart showing caller modules and dependency modules
  - Label each arrow with the function name and data being passed
  - Ensure diagram names don't create circular references (don't name the diagram the same as the module)
- **Function Context Diagrams**: For each important function, create a context diagram
  - Name each connection with format: `FunctionName (ModuleName.ts)`
  - Include indication of data types being passed and returned
  - Show error paths in addition to success paths

### 5. Invariant Rules
- List requirements that the module MUST obey using format:
  - Rule: [statement]
  - WHY: [chain of reasoning]
  - Example: "Rule: Transactions must be atomic. WHY: Partial updates would corrupt data integrity BECAUSE..."
- Categorize rules (security, performance, data integrity, etc.)

### 6. Design Decisions
- Document key design choices using format:
  - Decision: [statement]
  - Alternatives Considered: [list alternatives]
  - Rationale: [why this choice was made]
  - Assumptions: [underlying assumptions that, if changed, might invalidate this decision]
- Include trade-offs and compromises

### 7. Classes/Types
- For each class/interface/type:
  - Description and purpose
  - Data members with types and descriptions
  - For classes, list all member functions (implementation details go in section 8)
  - Notable design patterns used

### 8. Functions
- List functions top-down according to logical flow
- For each function:
  - **Purpose**: Brief description of what it does and why
  - **Signature**: Parameters, return type, and exceptions thrown
  - **Pseudo-code**: Following [[pseudo-code-rules]] format
  - **Error Cases**: How errors are handled, with error paths
  - **Processing Rules**: For complex logic, use a BECAUSE chain to explain reasoning
  - Example:
    ```
    PROCEDURE processData(input)
      VALIDATE input is not null BECAUSE null inputs cause system crashes
      IF input meets condition X THEN
        performActionA() BECAUSE business rule Y requires it when X is true
      ELSE
        performActionB() BECAUSE default handling is necessary
      END IF
    END PROCEDURE
    ```

### 9. Processing Rules (for State Machines/Workflows)
- For modules implementing workflows or state machines:
  - Document each state transition
  - Define entry and exit conditions
  - Explain processing logic for each state with BECAUSE chains
  - Include visual state diagram

### 10. API Calls
- For each API call made by the module:
  - URL to call
  - HTTP method (GET, POST, etc.)
  - Headers required
  - Request payload format and parameter mapping
    - Explain WHY for any non-obvious mappings
  - Response payload format and return data mapping
    - Indicate "Not used" for unused fields
  - Error handling for API failures
- Do not describe API calls invoked through another module

### 11. Configuration
- Document configuration options:
  - Format (environment variables, config files, etc.)
  - Default values
  - Validation rules
  - Effect of each configuration parameter

### 12. Testing Considerations
- Key test scenarios
- Mock dependencies needed
- Edge cases requiring special handling

## Best Practices

1. **Consistency**: Use consistent formatting throughout the document
2. **Examples**: Include code examples for complex sections
3. **Diagrams**: Use diagrams for complex relationships and flows
4. **Completeness**: Ensure all sections are filled out
5. **Modularity**: If a module is large, consider splitting the design document into logical sections
6. **Evolution**: Document how the design may evolve in the future
7. **Reviewability**: Organize content to make reviews efficient

## Template Example

```markdown
# Module: MyModule

## 1. Basic Information
- **Path**: src/services/MyModule.ts
- **Responsibilities**:
  - Validates user input
  - Processes business rules
  - ...

## 2. Callers
- **UserController** calls this module BECAUSE...
- ...

[continue with remaining sections]
```
