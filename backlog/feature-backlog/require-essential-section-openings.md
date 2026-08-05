# Require Essential Section Openings

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/require-essential-section-openings.md

Completion: direct-main

## Summary

Technical-document sections must begin by defining the essence of their topic. A section must establish what the topic is and why it matters before it enumerates properties or details.

## Context

Section openings shape the reader's understanding of all details that follow. The current technical-writing guidance permits a section to begin with an enumeration, which can leave the topic undefined and make the section harder to understand.

## Source Evidence

The direct user request in the current Codex task on 2026-08-04 states: "when writing documents, I noticed that the beginning of each section is critical but not often well written. Don't start enumerating various properties, you need to define the essence of the topic first. This needs to be part of the writing skill"

This request explicitly authorizes the writing-skill change recorded in Governed Definition Approval.

## Requirements

- Add a section-opening rule to the canonical STE technical-writing skill.
- Require the opening of each section to define the essence of the topic before it lists properties, components, examples, or other details.
- Keep artifact-specific skills responsible for required document structure.
- Add focused regression coverage for the new writing rule.
- Regenerate only supported skill-definition mirrors affected by the canonical change.

## Acceptance Criteria

- The writing skill says what a section opening must establish before enumeration begins.
- The rule applies to technical-document prose without changing artifact-specific section requirements.
- A focused test detects removal of the new rule.
- Canonical and generated skill-definition content is consistent.
- Focused validation and whitespace checks pass.

## Dependencies

None.

## Verification

- Run the focused STE technical-writing contract tests.
- Run the supported skill-definition regeneration and freshness checks.
- Run documentation validation for the changed Markdown source.
- Run Git whitespace validation for the intended changes.
- Obtain an independent review of the completed change.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/ste-technical-writing/SKILL.md

### Allowed Dependent Artifacts

- scripts/test_ste_technical_writing.py
- generated/adapters/**
- design/generated/skill-definitions.js

### Approval Resolution

Approved at creation from the direct user message in the current Codex task on 2026-08-04: "when writing documents, I noticed that the beginning of each section is critical but not often well written. Don't start enumerating various properties, you need to define the essence of the topic first. This needs to be part of the writing skill"

Approval is limited to skills/ste-technical-writing/SKILL.md and its supported dependent artifacts listed above. It does not authorize changes to another skill definition, an agent definition, a schema, model input, or unrelated metadata.
