---
name: create-document-outline
description: Infer a complete topic hierarchy from a document and evaluate and justify parent containment and sibling sequence.
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

## Preserve Author-Signaled Topic Boundaries

Before regrouping the material, make a topic map from the title and meaningful
section and subsection headings.

Use that map as the editorial baseline:

- use the document title as the root when it already names the complete
  subject; expand or replace it only when it is ambiguous or fails to contain
  a major topic;
- represent substantial introductory material before the first named section
  as Overview or Subject Overview unless the document supplies a more accurate
  heading;
- keep a meaningful section as a distinct outline topic by default;
- preserve sections that play different editorial roles, such as defining
  terms, explaining a problem, describing a structure, giving operating
  guidance, or presenting evidence;
- do not merge separately headed topics solely because they share a broad
  theme;
- do not demote a meaningful section into a detail when it advances the
  document at the same editorial level as its neighbors;
- allow a broad container section to split into several sibling topics when
  its substantial subsections cover different editorial purposes;
- group adjacent subsections only when one natural topic name fully describes
  them together.

Every meaningful heading must remain recognizable in the final outline,
whether it appears directly or beneath a clearly corresponding parent. Record
and justify every merge, promotion, or split that changes an author-signaled
boundary.

For every section containing three or more substantive blocks, map the
editorial role of each block before accepting the section as one undivided
group. When adjacent block clusters answer different stable reader questions,
represent those roles as intermediate topics. Keep the original heading as
their parent only when its ordinary meaning contains every role; otherwise,
split or promote the roles while preserving the heading's subject in their
names or rationale.

Preserving a topic does not require preserving its original heading depth. When
a broad container cannot contain several substantial subsections, promote
those subsections, then rebalance the resulting siblings:

1. Compare the breadth of every sibling topic at the new level.
2. Identify adjacent promoted topics that are materially narrower than the
   established section topics around them.
3. When one natural umbrella fully contains an adjacent run, add that umbrella
   at the broader level and retain the original promoted headings beneath it.
4. Keep an independently broad promoted topic as its own sibling.
5. Recheck containment, sequence, and heading recognizability after
   rebalancing.

Do not leave several narrow procedure, example, integration, or evidence
subsections beside broad subject sections merely because all were promoted
from the same container. Do not group them unless the parent is a genuine
umbrella rather than a concatenation of their labels.

## Inventory The Topics

1. Create exactly one one-line working summary for each substantive paragraph,
   list item, table row, callout, or equivalent content block.
2. Record a source identifier with every working summary for traceability.
3. Use this block-summary inventory as the coverage ledger. Do not omit a
   block because its material resembles a neighboring block.
4. Preserve distinct subjects, definitions, parts, types, properties,
   behaviors, relationships, constraints, processes, and other meaningful
   matters the document covers.
5. Merge duplicate wording only when it expresses the same topic.
6. Keep similarly named topics separate when the document gives them
   different meanings or roles.

The topic inventory is working evidence. It is not automatically the final
outline.

## Preserve Useful Topic Granularity

Start from the one-line block summaries in the inventory. A substantive block
contributes one final leaf by default. Refine that default only when it would
hide a real topic boundary inside the block.

Split a source block when:

- it changes subject or editorial function;
- it states rules or responsibilities that apply independently;
- it explicitly enumerates named parts, stages, or lifecycle states;
- it contrasts alternatives or separates a general rule from an exception;
- one part could move to a different parent without changing the other parts.

Keep one leaf when the sentences elaborate the same subject and claim through
reasons, parameters, cases, consequences, examples, command variants, or
inseparable qualifications. Express those details in the topic text after an
em dash when they are needed for completeness.

Do not merge distinct requirements, exceptions, stages, responsibilities,
relationships, or consequences merely because they concern the same subject
or answer the same broad reader question. A detail deserves its own leaf when
omitting it would conceal a separately meaningful point the author makes.

Normally derive no more than three sibling leaves directly from one prose
block. More are justified only when the author explicitly enumerates
independently named items, stages, rules, or comparison cases. A table row
normally remains one topic whose text summarizes its relevant cells.

An explicit lifecycle or state enumeration normally becomes a parent topic
with one child per named stage or state. A pair of alternative operating modes
normally becomes a parent with one child per mode. Keep an enumeration inside
one leaf only when the items are examples or parameter values rather than
topics the document distinguishes.

When a block splits:

1. Replace its working summary with the split topics when the summary merely
   restates them collectively.
2. Retain the summary as their parent only when it names a genuine umbrella
   that adds useful structure.
3. Do not keep both a generic block summary and equivalent child wording.

Apply the same test above the leaf level. When one headed section contains
several paragraph clusters with distinct editorial functions, introduce
separate sibling subtopics for those functions. Do not hide distinct reader
questions inside one broad convenience bucket.

After drafting, challenge every leaf and intermediate topic that uses several
coordinated phrases. Split it unless the combined phrase names one indivisible
topic. Then challenge every split: recombine clause fragments that have no
meaningful identity apart from the same claim.

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

Apply a primary-relationship test when a topic participates in more than one
process or domain:

1. Ask what the topic itself is or does, using its heading and substantive
   body as the strongest evidence.
2. Distinguish that enduring subject or function from an incidental mechanism
   that creates, installs, delivers, invokes, or verifies it.
3. Place the topic under the parent that answers its primary subject or
   function. Keep the incidental mechanism as detail or a cross-relationship,
   not as the grouping reason.
4. When the document gives both relationships equal weight, prefer the parent
   that makes the sibling set more coherent and complete.

Do not force unrelated topics together simply to reduce the number of
groups. Add another sibling group when that is the more faithful editorial
choice.

Reject a synthetic catch-all parent when it merely:

- joins several child labels with and or commas;
- uses a vague label such as general material, foundations, operations, or
  other material without a document-supported meaning;
- hides children that perform different editorial roles;
- exists only to reduce the number of topics at the next level.

A useful parent names a real umbrella topic and clarifies why its children
belong together.

Apply a mandatory coordinate-parent test to every new parent whose name joins
topics with and, or, commas, slashes, or similar coordination:

1. Separate the proposed parent into its coordinate parts.
2. Decide whether the complete phrase names a document-supported editorial
   domain, stage, responsibility, or reader question shared by all children.
3. If the parts merely reproduce separate child labels and do not add a shared
   relationship, the label is a bundle of sibling topics rather than an
   umbrella.
4. Split those parts into separate sibling parents and keep their applicable
   children beneath them.
5. Retain the parent when the coordinated phrase is an established topic or a
   coherent editorial umbrella whose ordinary meaning fully contains every
   child. Different children may emphasize different aspects of that umbrella;
   they need not each instantiate every coordinate word.

Never accept a coordinated label merely because it is broad enough to mention
everything beneath it.

## Reconcile Every Grouping Level

After each grouping pass, compare the new parent topics with every topic from
the preceding level.

Confirm that:

- every preceding topic belongs to a parent;
- no distinct topic disappeared during abstraction;
- each parent genuinely includes all of its children;
- no parent contains a qualifier that excludes one of its children;
- sibling topics are reasonably comparable in abstraction and scope;
- narrow promoted subsections have been rebalanced against broader sibling
  sections;
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
   percentage of 2. Add a concise justification that answers why the topic is
   included in that parent, and prefix the topic with:

   [100% alignment | parent 2/2 — why: {parent-containment justification}]

7. For every later child in that group, prefix the topic with its parent
   containment score and preceding-sibling sequence score. Add a concise
   justification after each component that answers why the topic is included
   in the parent and why it follows the immediately preceding sibling. Add the
   scores, convert the total to a percentage of 4, and prefix the topic with:

   [100% alignment | parent 2/2 — why: {parent-containment justification} | sequence 2/2 — why: {preceding-sibling justification}]

Use the actual percentage, component values, and justifications in each
prefix. The sequence score and its justification always compare the current
topic with its immediately preceding sibling in the same group, not with the
preceding topic elsewhere in the outline.

## Evaluate Topic Placement

### Parent Containment

Score how well the current topic is contained within its parent topic:

- 0 points: the topic is not contained in the parent.
- 1 point: the topic is partially contained in the parent.
- 2 points: the topic is completely contained in the parent.

Award 2 points only when the ordinary meaning of the parent fully includes the
child without relying on a vague or synthetic catch-all interpretation. A
child that extends beyond the parent receives at most 1 point.

For every parent-containment score, answer:

Why is this topic included in this parent?

Use one concise causal clause that names the semantic relationship. For
example, identify the topic as a type, part, stage, property, rule, example, or
other aspect of the parent. Match the justification to the score:

- 2 points: explain why the complete topic falls within the parent's ordinary
  meaning.
- 1 point: explain both the aspect that fits and the aspect that extends beyond
  or only partly fits the parent.
- 0 points: explain the subject or scope mismatch that prevents containment.

Do not use circular explanations such as it belongs here because it is related
to the parent.

### Sibling Sequence

When the current topic has a preceding sibling in the same group, score how
logical it is for the current topic to follow that sibling:

- 0 points: the topic does not follow logically.
- 1 point: the topic follows somewhat logically.
- 2 points: the topic follows fully logically.

Award 2 points only when the order expresses a clear progression, comparison,
dependency, chronology, or other editorial relationship. Mere adjacency or
preservation of source order receives at most 1 point.

A repeated parallel series under one comparison schema has complete parent
containment but only 1 point for sequence unless the items themselves have an
ordered scale, chronology, dependency, or progression. A stable catalog order
alone does not make one parallel case follow logically from another.

For every sibling-sequence score, answer:

Why is this topic a logical successor to the immediately preceding sibling?

Use one concise causal clause that names the transition between the two
topics. Match the justification to the score:

- 2 points: identify the progression, dependency, chronology, narrowing,
  contrast, or other strong transition that makes this successor logical.
- 1 point: explain the limited connection, such as a parallel alternative,
  loose comparison, or source-order adjacency without an intrinsic
  progression.
- 0 points: explain why no meaningful editorial transition connects the
  siblings.

Do not justify sequence by saying only that the document presents the topics
in that order.

The first child has no sequence score, so its total is the parent-containment
score out of 2. Every later child combines both dimensions for a total out of
4.

Convert the total to a percentage for the displayed alignment result:

- First child: parent-containment score divided by 2.
- Later child: combined parent-containment and sequence score divided by 4.

Keep the component scores visible beside the percentage. An alignment
percentage must not conceal a zero or partial score in either dimension.
Keep each component's why clause visible beside that component. The aggregate
percentage does not replace either explanation.

Revise a grouping when parent containment is 0. Reorder, regroup, or explain an
editorial discontinuity when sibling sequence is 0. Treat any score of 1 as an
explicit point for editorial review.

Score only after completing the grouping-level reconciliation. A strong score
cannot compensate for a missing topic or an incomplete parent.

After scoring, perform a skeptical editorial pass:

- challenge every 2-point component by checking whether its why clause names a
  complete semantic relationship;
- challenge every 1-point or 0-point component by checking whether its why
  clause states the exact limitation or mismatch;
- reduce the score when the relationship depends only on shared words,
  adjacency, or an invented umbrella;
- revise the grouping when several high scores depend on the same vague parent;
- prefer correcting the outline over defending a generous score.

## Verify The Outline

Confirm that:

- the document's meaningful sections are recognizable in the topic
  inventory;
- every author-signaled topic boundary is preserved or its merge, promotion,
  or split is justified;
- every substantive topic survives through each grouping level;
- compound source blocks and broad paragraph clusters have been split wherever
  they contain independently useful topics;
- every parent encompasses the complete meaning of its children;
- the root encompasses every immediate child;
- no accepted parent is a synthetic catch-all;
- every coordinated parent passes the coordinate-parent test;
- editorial framing has informed the outline without becoming accidental
  subject matter;
- every non-root topic has the required parent-containment score;
- every parent-containment score has a concise explanation of why the topic is
  included in that parent;
- every topic after the first sibling has the required sequence score;
- every sequence score has a concise explanation of why the topic is or is not
  a logical successor to the immediately preceding sibling;
- zero and partial component scores are revised or explicitly explained;
- exclusions and unresolved editorial judgments are stated.

## Output

Return:

1. the content boundary and exclusions;
2. the top-down topic outline with placement-score prefixes and a why clause
   for every constituent score;
3. a concise topic-coverage summary;
4. any unresolved grouping or interpretation concern.
