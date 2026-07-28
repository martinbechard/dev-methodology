---
name: create-document-outline
description: Infer a complete topic hierarchy from a document and evaluate parent containment and sibling sequence.
metadata:
  category: documentation-methodology
---

# Create Document Outline

Create an outline that represents the topics the document covers and the
relationships among them.

Work like a text editor reconstructing the author's topical organization.
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
   topics the author intended to distinguish.
3. Distinguish subject matter from navigation, interface controls, repeated
   chrome, generated status text, and boilerplate.
4. Treat statements about the page's purpose or organization as editorial
   framing. Use them to understand the subject, but do not automatically turn
   them into subject-matter topics.

Do not discard a meaningful section merely because its content uses a
different structure, such as a glossary list or comparison table.

## Inventory The Topics

1. Identify the topics expressed by each substantive content block.
2. Record a concise working summary and source identifier for traceability.
3. Preserve distinct subjects, definitions, parts, types, properties,
   behaviors, relationships, constraints, processes, examples, and other
   meaningful matters the document covers.
4. Merge duplicate wording only when it expresses the same topic.
5. Keep similarly named topics separate when the document gives them
   different meanings or roles.

The topic inventory is working evidence. It is not automatically the final
outline.

## Group Topics Editorially

Begin with the most detailed topics and repeatedly group them one level at a
time.

For each grouping pass:

1. Place topics together when the document presents them as parts or aspects
   of the same broader idea.
2. Use an existing heading as the parent when it accurately names the complete
   group.
3. Otherwise, write a parent topic at one natural level of abstraction above
   its children.
4. Prefer a clear topic name over a sentence about what the document says.
5. Preserve the document's order unless a different grouping is necessary to
   represent an explicit topical relationship.
6. Allow one group to use non-adjacent source material when the document
   returns to the same topic later.
7. Repeat until one root topic encompasses the complete document.

Do not force unrelated topics together simply to reduce the number of
groups. Add another sibling group when that is the more faithful editorial
choice.

## Reconcile Every Grouping Level

After each grouping pass, compare the new parent topics with every topic from
the preceding level.

Confirm that:

- every preceding topic belongs to a parent;
- no distinct topic disappeared during abstraction;
- each parent genuinely includes all of its children;
- no parent contains a qualifier that excludes one of its children;
- sibling topics are reasonably comparable in abstraction and scope;
- a child is not attached merely because it shares vocabulary with its parent;
- the set of parent topics represents the complete set of child topics.

If a topic is missing, restore it before continuing upward. If a parent does
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
concatenates headings, or excludes a major child topic.

## Build The Nested View

1. Start with the root topic.
2. Insert the next-lower grouping level beneath it.
3. Recursively insert each remaining level until the useful detailed topics
   appear.
4. Keep source identifiers on the lowest applicable topics when traceability is
   requested.
5. Mark the root topic with:

   [100% alignment | root]

6. For the first child in any group, convert its parent-containment score to a
   percentage of 2 and prefix the topic with:

   [100% alignment | parent 2/2]

7. For every later child in that group, prefix the topic with its parent
   containment score and preceding-sibling sequence score. Add the scores,
   convert the total to a percentage of 4, and prefix the topic with:

   [100% alignment | parent 2/2 | sequence 2/2]

Use the actual percentage and component values in each prefix. The sequence
score always compares the current topic with its immediately preceding sibling
in the same group, not with the preceding topic elsewhere in the outline.

## Evaluate Topic Placement

### Parent Containment

Score how well the current topic is contained within its parent topic:

- 0 points: the topic is not contained in the parent.
- 1 point: the topic is partially contained in the parent.
- 2 points: the topic is completely contained in the parent.

### Sibling Sequence

When the current topic has a preceding sibling in the same group, score how
logical it is for the current topic to follow that sibling:

- 0 points: the topic does not follow logically.
- 1 point: the topic follows somewhat logically.
- 2 points: the topic follows fully logically.

The first child has no sequence score, so its total is the parent-containment
score out of 2. Every later child combines both dimensions for a total out of
4.

Convert the total to a percentage for the displayed alignment result:

- First child: parent-containment score divided by 2.
- Later child: combined parent-containment and sequence score divided by 4.

Keep the component scores visible beside the percentage. An alignment
percentage must not conceal a zero or partial score in either dimension.

Revise a grouping when parent containment is 0. Reorder, regroup, or explain an
editorial discontinuity when sibling sequence is 0. Treat any score of 1 as an
explicit point for editorial review.

Score only after completing the grouping-level reconciliation. A strong score
cannot compensate for a missing topic or an incomplete parent.

## Verify The Outline

Confirm that:

- the document's meaningful sections are recognizable in the topic
  inventory;
- every substantive topic survives through each grouping level;
- every parent encompasses the complete meaning of its children;
- the root encompasses every immediate child;
- editorial framing has informed the outline without becoming accidental
  subject matter;
- every non-root topic has the required parent-containment score;
- every topic after the first sibling has the required sequence score;
- zero and partial component scores are revised or explicitly explained;
- exclusions and unresolved editorial judgments are stated.

## Output

Return:

1. the content boundary and exclusions;
2. the top-down topic outline with placement-score prefixes;
3. a concise topic-coverage summary;
4. any unresolved grouping or interpretation concern.
