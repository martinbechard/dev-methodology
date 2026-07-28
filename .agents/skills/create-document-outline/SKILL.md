---
name: create-document-outline
description: Create a recursively grouped document outline with source coverage and parent-child alignment scores.
metadata:
  category: documentation-methodology
---

# Create Document Outline

Create a traceable outline by summarizing document content, grouping adjacent
summaries, and expanding the resulting hierarchy from its root.

## Inputs

- The document to outline.
- Any user-specified content boundary or exclusions.
- The requested output format, when one is specified.

## Identify Content Blocks

1. Identify the meaningful content blocks in document order.
2. Include paragraphs, list items, table rows, callouts, and other prose-bearing
   structures that contribute to the document.
3. Exclude navigation, interactive controls, generated status messages,
   repeated chrome, and boilerplate unless they are part of the requested
   content.
4. Give every included block a stable source identifier.

Do not reduce a structured document to paragraph elements when lists, tables,
or other structures carry substantive content.

## Summarize And Group

1. Create a one-line summary for every content block.
2. Preserve the block's subject, principal claim, and important constraint.
3. Group adjacent summaries that share a coherent topic.
4. Give every group a one-line topic summary and retain its ordered children.
5. Repeat the adjacent grouping operation until one topic represents the whole
   document.

Keep groups adjacent so the outline preserves the document's reasoning and
sequence. Do not combine distant material solely because it uses similar
terms.

## Build The Nested View

1. Start with the single whole-document topic.
2. Assign the root topic 100% alignment because it represents the complete
   document.
3. Insert the topics from the next-lower grouping level beneath the root in
   source order.
4. Before inserting each child, evaluate how coherently its topic fits its
   parent topic.
5. Prefix the child topic text with its score in this exact form:

   [x% alignment]

6. Recursively insert the next-lower grouping level beneath each child.
7. Continue until the content-block summaries appear as the leaf nodes.

Every displayed topic, including each leaf summary, begins with an alignment
prefix. Alignment scores measure thematic parent-child coherence, not the
percentage of the parent covered by one child. Sibling scores do not need to
sum to 100%.

## Evaluate Alignment

Judge whether the child is a direct and useful specialization of its parent:

- 95 to 100%: direct specialization with no meaningful topic drift.
- 80 to 94%: clear contribution with a narrower or supporting scope.
- 60 to 79%: partial fit, secondary relevance, or an overly broad label.
- Below 60%: weak grouping; regroup or relabel before accepting the outline.

Base each score on the topic text and the source blocks represented beneath it.
Do not use false numerical precision to conceal uncertainty. Prefer scores in
five-point increments unless a more exact distinction is supported.

## Verify The Outline

Confirm that:

- every included source block appears exactly once as a leaf;
- every leaf descends through each grouping level to the root;
- sibling order matches source order;
- each parent accurately describes all of its children;
- no child falls below 60% alignment;
- exclusions are stated;
- important constraints survive summarization.

## Output

Return:

1. the content boundary and exclusions;
2. the top-down nested outline with alignment prefixes;
3. any low-confidence grouping or coverage concern;
4. the count of included source blocks and leaf nodes.
