---
name: create-document-outline
description: Infer a complete conceptual hierarchy from a document and evaluate the coherence of every parent-child grouping.
metadata:
  category: documentation-methodology
---

# Create Document Outline

Create an outline that represents the concepts the document explains and the
relationships among them.

Work like a text editor reconstructing the author's conceptual organization.
Do not merely shorten every sentence and stack the shortened sentences beneath
broader summaries.

## Inputs

- The document to outline.
- Any user-specified content boundary or exclusions.
- The requested output format, when one is specified.

## Read The Document Structure

1. Read the title, introduction, headings, paragraphs, lists, tables, callouts,
   and other substantive structures.
2. Treat headings and visible section organization as strong evidence of the
   concepts the author intended to distinguish.
3. Distinguish subject matter from navigation, interface controls, repeated
   chrome, generated status text, and boilerplate.
4. Treat statements about the page's purpose or organization as editorial
   framing. Use them to understand the subject, but do not automatically turn
   them into subject-matter topics.

Do not discard a meaningful section merely because its content uses a
different structure, such as a glossary list or comparison table.

## Inventory The Concepts

1. Identify the concepts expressed by each substantive content block.
2. Record a concise working summary and source identifier for traceability.
3. Preserve distinct definitions, parts, types, properties, behaviors,
   relationships, constraints, processes, and examples.
4. Merge duplicate wording only when it expresses the same concept.
5. Keep similarly named concepts separate when the document gives them
   different meanings or roles.

The concept inventory is working evidence. It is not automatically the final
outline.

## Group Concepts Editorially

Begin with the most detailed concepts and repeatedly group them one level at a
time.

For each grouping pass:

1. Place concepts together when the document presents them as parts or aspects
   of the same broader idea.
2. Use an existing heading as the parent when it accurately names the complete
   group.
3. Otherwise, write a parent topic at one natural level of abstraction above
   its children.
4. Prefer a clear concept name over a sentence about what the document says.
5. Preserve the document's order unless a different grouping is necessary to
   represent an explicit conceptual relationship.
6. Allow one group to use non-adjacent source material when the document
   returns to the same concept later.
7. Repeat until one root topic encompasses the complete document.

Do not force unrelated concepts together simply to reduce the number of
groups. Add another sibling group when that is the more faithful editorial
choice.

## Reconcile Every Grouping Level

After each grouping pass, compare the new parent topics with every concept from
the preceding level.

Confirm that:

- every preceding concept belongs to a parent;
- no distinct concept disappeared during abstraction;
- each parent genuinely includes all of its children;
- no parent contains a qualifier that excludes one of its children;
- sibling topics are reasonably comparable in abstraction and scope;
- a child is not attached merely because it shares vocabulary with its parent;
- the set of parent topics represents the complete set of child concepts.

If a concept is missing, restore it before continuing upward. If a parent does
not naturally encompass a child, rename the parent, move the child, or split
the group.

This reconciliation happens at every level, including the final comparison
between the root and its immediate children.

## Name The Root Topic

Name the root as the document's subject at the broadest useful level.

The root must:

- identify what the subject is;
- naturally encompass every immediate child;
- be specific enough to distinguish the document's actual subject;
- include important dimensions without becoming a list of section summaries.

Reject a root that only lists actions, repeats the page-purpose statement,
concatenates headings, or excludes a major child concept.

## Build The Nested View

1. Start with the root topic.
2. Insert the next-lower grouping level beneath it.
3. Recursively insert each remaining level until the useful detailed concepts
   appear.
4. Keep source identifiers on the lowest applicable topics when traceability is
   requested.
5. Prefix every topic with its parent-alignment score in this exact form:

   [x% alignment]

Assign the root 100% alignment because it represents the complete document.

## Evaluate Alignment

Score how naturally each child belongs beneath its parent:

- 95 to 100%: a direct definition, part, type, property, behavior,
  relationship, constraint, process, or example of the parent.
- 80 to 94%: a clear supporting aspect with a narrower or secondary
  relationship.
- 60 to 79%: a partial fit that may indicate an overly broad child or an
  incomplete parent label.
- Below 60%: an unacceptable grouping that must be revised.

Alignment measures conceptual coherence, not lexical similarity or the amount
of source text covered. Score only after completing the grouping-level
reconciliation. A high score cannot compensate for a missing concept or an
incomplete parent.

Prefer scores in five-point increments unless the evidence supports a finer
distinction.

## Verify The Outline

Confirm that:

- the document's meaningful sections are recognizable in the concept
  inventory;
- every substantive concept survives through each grouping level;
- every parent encompasses the complete meaning of its children;
- the root encompasses every immediate child;
- editorial framing has informed the outline without becoming accidental
  subject matter;
- no accepted child falls below 60% alignment;
- exclusions and unresolved editorial judgments are stated.

## Output

Return:

1. the content boundary and exclusions;
2. the top-down conceptual outline with alignment prefixes;
3. a concise concept-coverage summary;
4. any unresolved grouping or interpretation concern.
