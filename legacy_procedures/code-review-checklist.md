# Code Review Checklist

## Instructions

- Review each code file against the checklist criteria
- For each area, look for the specified evidence in the code
- Rate each item on a scale: ✅ Good, ⚠️ Needs Improvement, ❌ Problematic, N/A Not Applicable
- Provide specific code examples or file/line references to support your assessment
- Document any recommendations for improvement
- Focus on patterns rather than isolated instances
- Place your answers and findings directly inline with the relevant questions or evidence points.

## 1. File Naming and Organization

### Evidence to Look For

- [ ] **File Header:** Every `.ts` implementation file starts with a header comment referencing the primary design document (`// Design: [[path/to/design.md]]`).
- [ ] **Design Alignment:** File name and location match the `Design Code Path` in `[[definitions.md]]` (if applicable).
- [ ] **Naming Convention:** Files containing a class or interface are named with the same PascalCase as the class/interface (e.g., `StatusManager.ts` for class `StatusManager`).
- [ ] **Utility Naming:** Utility files or modules with multiple exports use lowercase or camelCase (e.g., `index.ts`, `errorHandler.ts`).
- [ ] **Directory Structure:** Files are placed in the correct standard directory (`src`, `test`, `design`, etc.). Unit tests mirror the `src` structure within `test`. Related files (types, helpers) are co-located with the main module file.
- [ ] Inconsistent file naming conventions across related components.
- [ ] Illogical file organization or structure (deviating from standards).
- [ ] Files with unclear or misleading names.

### Questions to Answer

- Does every implementation file have a `// Design: ...` header?
- Do file names and locations align with `definitions.md`?
- Do file names match the classes or interfaces they contain (PascalCase)?
- Is the standard directory structure followed (`src`, `test`, co-location)?
- Is naming convention consistent across the codebase?
- Are there any duplicate or redundant files?
- **Verification:** Has the code been verified against the design document referenced in the header and `definitions.md`?

## 2. Imports and Dependencies

### Evidence to Look For

- [ ] **Import Source:** Imports for definitions listed in `[[definitions.md]]` use the canonical `Design Code Path` as the target.
- [ ] **Alias vs. Relative:** Project aliases (`@/`, `@test/`) used for cross-module imports; relative paths (`./`, `../`) used for intra-module imports.
- [ ] **No Extension:** Import paths do not include `.ts` or `.js` extensions.
- [ ] Unused imports.
- [ ] Inconsistent import organization (e.g., external, alias, relative order not followed).
- [ ] Circular dependencies.

### Questions to Answer

- Do imports target the canonical paths defined in `definitions.md`?
- Are alias and relative paths used correctly according to project conventions?
- Are there unnecessary imports?
- Are imports organized logically (external, alias, relative)?
- Have circular dependencies been avoided?

## 3. Duplicate Code

### Evidence to Look For

- [ ] Nearly identical blocks of code
- [ ] Similar algorithms reimplemented in multiple places
- [ ] Repeated validation or error handling logic
- [ ] Copy-pasted sections with minor variations
- [ ] Abstractions created to reduce duplication maintain or improve clarity and correctness.

### Questions to Answer

- Is there repeated code that should be extracted into reusable functions?
- Are there similar algorithms reimplemented in multiple places?
- Is there repeated validation or error handling logic?
- If abstractions were used to reduce duplication, do they maintain or improve clarity and correctness?

## 4. Long Methods/Classes

### Evidence to Look For

- [ ] Methods longer than 30-40 lines
- [ ] Classes longer than 300 lines
- [ ] Functions/constructors with > 2 parameters use a single parameter object type (e.g., `<FunctionName>Params` or `<ClassName>Options`).
- [ ] Methods with multiple levels of abstraction
- [ ] Classes with unrelated fields or methods

### Questions to Answer

- Are there methods or classes that are too large?
- Are there methods addressing multiple concerns? (Consider extracting internal logic into private helpers first).
- Do functions/constructors with > 2 parameters use parameter objects?
- Are classes violating the Single Responsibility Principle?

## 5. Inappropriate Coupling

### Evidence to Look For

- [ ] Direct access to another class's private fields
- [ ] Multiple dependencies between classes
- [ ] Classes that know too much about each other's implementation
- [ ] Lack of interface abstraction between components

### Questions to Answer

- Are there classes that depend too much on implementation details of other classes?
- Is there tight coupling between classes?
- Are interfaces used appropriately to decouple components?

## 6. Feature Envy

### Evidence to Look For

- [ ] Methods that use more methods/properties from another class than their own
- [ ] Methods that would make more sense if moved to another class
- [ ] Excessive getters/setters used by external classes

### Questions to Answer

- Are there methods that use features of other classes excessively?
- Should certain methods be moved to other classes?
- Is functionality implemented in the appropriate class?

## 7. Primitive Obsession

### Evidence to Look For

- [ ] **Definition Check:** Reusable types/interfaces/enums are checked against `[[definitions.md]]` before creation and added if new.
- [ ] Strings or numbers representing domain concepts (e.g., "ACTIVE" instead of a registered enum from `definitions.md`).
- [ ] Arrays or dictionaries instead of proper objects/types registered in `definitions.md`.
- [ ] Groups of primitives that are always used together (should be an interface/type registered in `definitions.md`).
- [ ] Primitive type checking scattered throughout code.
- [ ] Optional values handled correctly (members omitted where appropriate, meaningful defaults used with `??` only when necessary and justified).

### Questions to Answer

- Are reusable types/interfaces/enums checked against/added to `definitions.md`?
- Is the code using primitive types instead of domain-specific types/enums registered in `definitions.md`?
- Are groups of primitives encapsulated in types/interfaces registered in `definitions.md`?
- Are optional values handled correctly when passed or assigned?

## 8. Switch Statements / Conditionals

### Evidence to Look For

- [ ] Large switch statements or if/else chains
- [ ] The same type or property checked in multiple places
- [ ] Conditional logic that could be replaced with polymorphism
- [ ] Type checking followed by different behavior

### Questions to Answer

- Are there excessive switch/case or if/else chains?
- Is the same condition tested in multiple places?
- Could polymorphism be more appropriate?

## 9. Error Handling

### Evidence to Look For

- [ ] Adherence to the error handling strategy in `[[/design/error-strategy.md]]`.
- [ ] Empty `catch` blocks.
- [ ] Exceptions used for normal control flow.
- [ ] Unclear or non-informative error messages lacking context.
- [ ] Insufficient error logging/tracing via `Tracer`.
- [ ] `Tracer.log` calls missing variable names (e.g., `Tracer.log(\`Value: ${myVar}\`)`).

### Questions to Answer

- Does error handling follow the project's defined strategy?
- Are exceptions used only for exceptional conditions?
- Are errors logged effectively with context using `Tracer` (including variable names)?
- Are error messages clear and informative?

## 10. Comments

### Evidence to Look For

- [ ] Comments explaining _what_ code does (instead of _why_).
- [ ] Commented-out code blocks.
- [ ] Comments that contradict the code (outdated/inaccurate).
- [ ] Excessive comments where clearer code would suffice.
- [ ] Missing comments for complex algorithms, business rules, or rationale.
- [ ] Irrelevant development comments (`// TODO`, attributions, etc.).
- [ ] Non-standard or missing file comment at the beginning of file, as per procedure-coding-rules.md

### Questions to Answer

- Do comments primarily explain "why" (rationale, business rules)?
- Are comments accurate and up-to-date?
- Is commented-out code removed?
- Are complex parts adequately explained?
- Are temporary/irrelevant development comments removed?

## 11. Naming

### Evidence to Look For

- [ ] Cryptic or abbreviated names
- [ ] Inconsistent naming styles
- [ ] Names that don't reflect purpose
- [ ] Misleading names
- [ ] Too generic names (e.g., "data", "manager", "processor")

- [ ] Variables with similar names and meanings that could be easily confused (e.g., `orderCount` vs `orderCounts`)

### Questions to Answer

- Are names clear, consistent, and descriptive?
- Do names reflect purpose?
- Are naming conventions followed consistently?

## 12. Method/Class Cohesion

### Evidence to Look For

- [ ] **SRP Check:** Class responsibility aligns with its design document (referenced via `definitions.md`).
- [ ] Methods that perform multiple unrelated logical operations.
- [ ] Classes with fields used by only some methods.
- [ ] Methods with multiple levels of abstraction.
- [ ] Classes that change for multiple reasons (violating SRP).

### Questions to Answer

- Do methods perform a single logical operation?
- Do classes have a clear, focused responsibility aligned with their design doc?
- Are there methods or classes that should be split due to low cohesion?

## 13. Type Safety / Correctness

### Evidence to Look For

- [ ] Assignment of optional values to required parameters is justified by design and handled safely (e.g., with prior validation or meaningful defaults).
- [ ] Type assertions (`as any`, `as unknown as Type`) used appropriately and sparingly, with justification if complex.
- [ ] **Type Source:** Correct types used based on design documents, imported from the canonical path specified in `[[definitions.md]]`.

### Questions to Answer

- Is the code type-safe?
- Are optional/required type mismatches handled correctly?
- Are type assertions necessary and justified?
- Are types imported from their canonical locations as per `definitions.md`?

## 14. Testing

### Evidence to Look For

- [ ] Some state or its management rules not consistent with the design
- [ ] Some state in the design is not implemented consistently

### Questions to Answer

- Assuming the code is already algined with the current design, will applying the current changes continue to respect the current design.

## 15. Testing

### Evidence to Look For

- [ ] Logic extracted into new functions during refactoring is covered by specific unit tests created using TDD _before_ the original function was modified to call the new function.

### Questions to Answer

- If refactoring involved extracting functions, were those functions tested independently (ideally via TDD)?
