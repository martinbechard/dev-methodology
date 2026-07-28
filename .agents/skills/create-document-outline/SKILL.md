---
name: create-document-outline
description: Infer a document's conceptual topic hierarchy with traceable source coverage and parent-child alignment scores.
metadata:
  category: documentation-methodology
---

# Create Document Outline

Create a traceable conceptual outline that explains what the document's subject
is, including its parts, properties, behavior, and supporting details.

Do not turn the outline into a hierarchy of sentences about the page. Source
summaries are working evidence for inferring the conceptual hierarchy; they are
not automatically displayed as outline topics.

## Inputs

- The document to outline.
- Any user-specified content boundary or exclusions.
- The requested output format, when one is specified.

## Identify Content Blocks

1. Identify the meaningful content blocks in document order.
2. Include paragraphs, list items, table rows, callouts, and other prose-bearing
   structures that contribute to the document.
3. Give every examined block a stable source identifier.
4. Classify each block as one of:
   - subject content that explains the document's concepts;
   - document framing that states the page's purpose, scope, or organization;
   - interface or structural text;
   - boilerplate.
5. Exclude navigation, interactive controls, generated status messages,
   repeated chrome, and boilerplate unless they are part of the requested
   subject.

Do not reduce a structured document to paragraph elements when lists, tables,
or other structures carry substantive content.

## Create The Coverage Ledger

1. Create a one-line summary for every subject-content block.
2. Preserve the block's subject, principal claim, and important constraint.
3. Record how each framing block informs the document's subject or scope instead
   of automatically turning it into an outline node.
4. Record why every interface, structural, or boilerplate block is excluded.

The ledger preserves source coverage. The outline presents the inferred
conceptual model. Keep those responsibilities separate.

## Infer The Document Subject

1. Use the title, headings, introduction, framing statements, recurring
   concepts, and substantive content to identify what the document explains.
2. Express the root as a subject or concept, normally with a noun phrase.
3. State what the subject is before describing what it does.
4. Include the subject's intended scope when that distinguishes it from a
   merely generic label.
5. Reject a root that is only:
   - a list of actions performed by the subject;
   - a sentence saying what the page explains;
   - a concatenation of section headings;
   - a summary of the document-writing activity.

For example, prefer a root shaped like:

Agentic configuration — the project-level arrangement of agents, skills,
instructions, workflow choices, and runtime files used to guide coding agents.

Do not substitute:

The page explains how coding-agent runtimes use generated files.

The first form identifies the subject and its scope. The second is document
framing that should inform the root rather than appear beneath it.

## Build The Conceptual Hierarchy

1. Ask what definitions, parts, properties, behaviors, relationships, or
   constraints the document attributes to the root subject.
2. Group the coverage-ledger summaries by those conceptual aspects.
3. Name every group as a concept or aspect of its parent, normally with a noun
   phrase.
4. Recursively group each aspect into narrower concepts until the remaining
   details no longer benefit from another conceptual level.
5. Preserve source order where it does not weaken the conceptual model.
6. Permit one conceptual group to draw on non-adjacent source blocks when the
   document discusses the same aspect in several places.
7. Keep source identifiers attached to the lowest applicable topic for
   traceability.

Every child should answer at least one of these questions:

- What is this parent?
- What is part of this parent?
- What property or behavior belongs to this parent?
- What constraint, relationship, or example explains this parent?

Do not add a child merely because a source sentence can be summarized.

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
7. Continue until the meaningful conceptual details appear as leaf nodes.

Every displayed topic begins with an alignment prefix. Alignment scores measure
conceptual parent-child coherence, not lexical similarity, source coverage, or
the percentage of the parent covered by one child. Sibling scores do not need
to sum to 100%.

## Evaluate Alignment

Judge whether the child is a direct and useful specialization of its parent:

- 95 to 100%: direct specialization with no meaningful topic drift.
- 80 to 94%: clear contribution with a narrower or supporting scope.
- 60 to 79%: partial fit, secondary relevance, or an overly broad label.
- Below 60%: weak grouping; regroup or relabel before accepting the outline.

Base each score on whether the child is genuinely a definition, part, property,
behavior, relationship, constraint, or example of the parent. Do not award a
high score merely because the child repeats words from the parent or supports a
sentence used to summarize it.

Do not use false numerical precision to conceal uncertainty. Prefer scores in
five-point increments unless a more exact distinction is supported.

## Verify The Outline

Confirm that:

- the root identifies what the document's subject is and the scope in which the
  document explains it;
- the root does not merely list what the subject does;
- page-purpose statements inform the root but do not appear as content topics
  unless the document itself is the subject;
- every subject-content block maps to at least one outline topic;
- every framing or excluded block has a recorded disposition;
- every displayed child is conceptually part of or explanatory of its parent;
- each parent accurately describes all of its children;
- no child falls below 60% alignment;
- important constraints survive summarization.

## Output

Return:

1. the content boundary and exclusions;
2. the top-down nested outline with alignment prefixes;
3. the source-coverage ledger or a coverage summary;
4. the disposition of document-framing statements;
5. any low-confidence grouping or coverage concern.
