---
name: java-comment
description: Place required Java file-level comment information in package or top-level type Javadoc without duplicating standalone headers. Use whenever Java source is created, materially changed, or reviewed together with the generic code-comments contract.
metadata:
  category: stack-and-domain
---

# Java Comment

Apply code-comments for the required information and public-contract content. This skill refines only where Java file-level information belongs and how it is expressed.

## Placement Contract

- Do not begin a Java source file with a standalone header comment solely to carry the generic file-level information.
- In package-info.java, put the information in the package documentation Javadoc immediately before the package declaration.
- In an ordinary packaged source file, keep the package declaration and imports in their valid Java positions, then put the information in the Javadoc for the first top-level class, interface, enum, record, or annotation type.
- In a source file without a package declaration, put the information in the Javadoc for the first top-level class, interface, enum, record, or annotation type.
- Do not add a separate standalone header when package or top-level type Javadoc carries the information.
- Keep the Javadoc valid. Preserve annotations, modifiers, package declarations, imports, and type declarations in the order required by Java and the project formatter.

## Required Information

Preserve every field required by code-comments:

- The exact Copyright statement supplied by the applicable project instructions.
- The truthful AI attribution required by the project or the generic fallback wording.
- A one-sentence Responsibility summary for the file.
- The applicable Design document path when one exists.
- The applicable Test plan path when one exists.

Do not invent a Design or Test plan reference. Omit that field when no governing document exists and applies. Preserve established project labels when they differ, but do not omit the underlying information.

## package-info.java

Use package Javadoc as the file-level information carrier:

```java
/**
 * [exact project copyright statement]
 * AI attribution: Generated with AI assistance.
 * Responsibility: Defines the public contract and shared conventions for the order package.
 * Design: docs/design/order-package.md
 * Test plan: docs/test-plans/order-package.md
 */
package com.example.orders;
```

## Ordinary Packaged Type

For an ordinary packaged source file, attach the information to the first top-level type rather than placing a standalone block before the package declaration:

```java
package com.example.orders;

/**
 * [exact project copyright statement]
 * AI attribution: Modified with AI assistance.
 * Responsibility: Coordinates validated order submission for application callers.
 * Design: docs/design/order-submission.md
 * Test plan: docs/test-plans/order-submission.md
 *
 * <p>Callers create the service with an order gateway and submit validated orders.</p>
 */
public final class OrderService {
}
```

## Top-Level Type Without A Package Declaration

When no package declaration exists, the first top-level type Javadoc is also the first file content:

```java
/**
 * [exact project copyright statement]
 * AI attribution: Generated with AI assistance.
 * Responsibility: Starts the command-line order import workflow.
 * Design: docs/design/order-import.md
 * Test plan: docs/test-plans/order-import.md
 */
public final class OrderImport {
}
```

## Duplicate And Incomplete Forms

The following shape is not acceptable: a standalone header duplicates metadata already present in the type Javadoc.

```java
/* [copyright, AI attribution, responsibility, design, and test-plan metadata] */
package com.example.orders;

/**
 * [the same copyright, AI attribution, responsibility, design, and test-plan metadata]
 */
public final class OrderService {}
```

Moving the information is also not permission to discard it. A package or type Javadoc that omits the applicable copyright, AI attribution, responsibility, design, or test-plan information is incomplete under code-comments.

## Review Evidence

Read references/review-checklist-java-comment.md during Java comment review. Apply it together with the code-comments checklist so placement and information completeness are verified separately.
