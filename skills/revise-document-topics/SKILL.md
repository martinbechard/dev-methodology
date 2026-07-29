---
name: revise-document-topics
description: Revise an explicitly authorized document from a scored topic analysis by repairing weak placement, grouping, sequence, and ownership without gaming alignment scores.
metadata:
  category: documentation-methodology
---

# Revise Document Topics

Revise a document's topical organization only when the caller explicitly
authorizes source mutation. Prefer a more truthful structure over a higher
percentage.

## Dependency

Load and apply [Analyze Document Topics](../analyze-document-topics/SKILL.md)
before this skill. Use its read-only topic, containment, sequence, granularity,
and scoring contracts as the baseline. Stop after analysis when revision
authority is absent.

## Inputs

- The source document.
- Its current scored topic outline.
- Explicit authority to revise the source document.
- Any linked documents that may own displaced material.
- Any stated content boundary or document-ownership map.
- Whether the caller requests a durable before-and-after topic-analysis
  artifact. Do not retain one by default.

## Establish The Audit Set

1. List every topic with a partial or zero parent-containment or sequence score.
2. Add every full-score topic whose justification depends on a vague parent,
   compound label, shared vocabulary, or unexplained source order.
3. Record each topic's current parent and, when applicable, its immediately
   preceding sibling.
4. Recheck coverage before moving anything. Never improve placement by dropping
   a difficult topic.

## Apply The Improvement Ladder

Test each audited topic in this order.

### 1. Reorder Within The Current Parent

Try a different sibling order only when it creates a real directed transition.
Recalculate the moved topic and every sibling whose predecessor changes.

Reject a reorder that merely transfers a partial score from one sibling to
another. Stable catalog order, alphabetical order, and source order do not
become progressions merely because they are consistent.

### 2. Move To An Existing Parent

Prefer the parent that contains the topic's primary subject or function. Do not
place a topic beneath an incidental mechanism that creates, installs, invokes,
or verifies it when another existing parent describes what the topic actually
is.

Confirm that:

- the entire child scope is a subset of the proposed parent;
- the new predecessor-to-child transition is stronger;
- the move does not leave the old group incomplete or create a duplicate;
- non-adjacent source material may join when it clearly has the same owner.

### 3. Split A Compound Topic

Split a topic when its clauses have different primary subjects or different
document owners. Merge each clause into an existing topic when that topic
already represents the subject. Do not retain the compound wording as a
duplicate parent or summary.

### 4. Add A Genuine Parent

Add a parent only when the document supports a stable type, stage, format,
responsibility, reader question, or other shared domain.

Reject:

- a one-child parent created only to remove a sequence score;
- a parent that concatenates its children's labels;
- a parent that groups topics only because they are adjacent;
- a parent whose ordinary meaning does not contain every child.

### 5. Reassess Document Ownership

Consider another document only after reorder, reparenting, splitting, and
genuine regrouping fail.

Move a topic when its primary subject is owned by another document and the
current document covers it only incidentally. Use headings, ownership
statements, navigation summaries, and substantive coverage as evidence.

When moving source content:

1. Move the explanation, not merely its outline label.
2. Preserve a concise linked boundary statement in the former document when
   readers still need routing.
3. Remove duplicated normative prose.
4. Preserve or update heading identifiers, navigation, table counts, and
   references.
5. Re-outline the affected groups in both documents.

Do not move one side of a comparison when doing so would destroy a meaningful
comparison owned by the current document.

## Preserve Honest Partial Scores

Keep a partial sequence score when sibling placement is correct but the topics
are parallel cases rather than successive stages. Common examples include:

- runtime or vendor rows under one comparison schema;
- two alternative operating modes;
- peer policy categories;
- catalog entries with no intrinsic order.

A partial score that precisely exposes parallelism is useful evidence, not a
defect. Do not invent chronology, dependency, or contrast to force 100%.

## Evaluate The Revision

For every proposal, report:

- topic;
- current parent and predecessor;
- proposed parent and predecessor;
- before and after component scores and percentages;
- why containment or succession improves;
- any new weakness introduced elsewhere;
- document-owner evidence when a move crosses documents.

Count proposals separately as:

- improved by reorder;
- improved by regrouping, splitting, or reparenting;
- honest partial scores that should remain;
- probable wrong-document topics.

## Verify

Confirm that:

- every source topic remains represented exactly once;
- full containment explanations prove subset relationships;
- full sequence explanations prove directed transitions;
- every changed predecessor relationship was rescored;
- no score improved only because a topic became the first child;
- no synthetic or one-child score-fixing parent was introduced;
- document moves follow primary ownership and leave useful linked boundaries;
- the revised outline is editorially clearer even when its aggregate score does
  not increase.

## Output

Return:

1. a prioritized improvement matrix;
2. the revised scored outline when revision is requested;
3. document-architecture recommendations separated from outline-only changes;
4. counts for reorder, regrouping or reparenting, honest partials, and probable
   wrong-document topics;
5. unresolved tradeoffs, including stable comparison order versus local
   sequence quality;
6. changed paths and verification evidence;
7. the durable before-and-after analysis artifact when the caller requested
   one, or an explicit statement that no durable artifact was retained.
