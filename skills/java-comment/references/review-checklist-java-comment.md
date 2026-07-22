# Java Comment Review Checklist

- Question: Is the selected metadata carrier valid Javadoc rather than a standalone file header added solely for generic information?
- Question: Does package-info.java put the file-level information in package documentation immediately before the package declaration?
- Question: Does every other Java source put the file-level information in the first top-level class, interface, enum, record, or annotation type Javadoc, including source without a package declaration?
- Question: Does the package documentation or first top-level type contain the exact copyright statement, truthful AI attribution, responsibility summary, and every applicable design or test-plan reference required by code-comments?
- Question: Is every required generic information field present exactly once without a duplicate standalone header?
- Question: Do package declarations, imports, annotations, modifiers, Javadoc, and type declarations remain syntactically valid and formatter-compatible?
- Question: Does the public type documentation still explain caller usage, invariants, lifecycle, ownership, and other applicable public-contract details rather than containing metadata alone?
