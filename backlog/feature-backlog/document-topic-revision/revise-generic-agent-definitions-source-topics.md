# Revise the Generic Agent Definitions Source Document Topics

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/document-topic-revision/revise-generic-agent-definitions-source-topics.md

Completion: direct-main

Series: backlog/feature-backlog/document-topic-revision/index.md

## Summary

Analyze and revise design/generic-agent-definitions-source.html so conceptual sources, schemas, model profiles, generation, adapter output, and ownership boundaries are organized as explicit topics.

## Context

The page explains the canonical conceptual-agent source model and its generated runtime adapters. Topic structure must prevent generated formats, source schemas, and model-profile mappings from being conflated.

## Source Evidence

Direct user request in task 019fa9bf-1e81-7a70-87e5-a747ce97318f on 2026-07-28 to create one work item for each document to revise it after integrating the document-topic agent and skills.

## Requirements

- Produce a fresh source-grounded scored topic outline for design/generic-agent-definitions-source.html.
- Distinguish conceptual definition semantics, schema constraints, model profiles, generators, adapter mappings, and generated-mirror ownership.
- Revise compound or misplaced topics without changing the underlying generation contract.
- Preserve all supported runtime formats, source paths, examples, links, identifiers, and accessibility behavior.
- Ensure every generated-output statement names its canonical owner.

## Acceptance Criteria

- The page clearly separates canonical inputs from generated outputs.
- Model-profile and adapter relationships are complete and correctly scoped.
- No generated mirror is presented as an independent source.
- All source-backed examples and runtime distinctions survive revision.

## Dependencies

backlog/feature-backlog/document-topic-revision/incorporate-document-topic-agent-and-skills.md

## Verification

- Run agent-schema, model-profile, generation-freshness, and focused page-content tests.
- Run link, markup, accessibility, and git diff checks.
- Obtain independent editorial and generated-ownership review.

## Open Questions

None.
