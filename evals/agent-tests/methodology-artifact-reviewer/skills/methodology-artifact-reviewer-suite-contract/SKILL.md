---
name: methodology-artifact-reviewer-suite-contract
description: Share the canonical Methodology Artifact Reviewer evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Methodology Artifact Reviewer Suite Contract

Evaluate the target as a source-backed independent reviewer of methodology catalog changes.

## Required Contract

- Extract source, generated adapter, documentation, naming, dependency, regression, and command evidence before synthesis.
- Treat skills and conceptual roles as sources and generated adapters and generated documentation as derived outputs.
- Check harness boundaries, portability, concise skills, structured role behavior, stable names, and explicit dependencies.
- Verify that every source change has aligned catalog, adapter, documentation, and regression coverage.
- Complete and save the existing structured-review checklist before writing findings or returning a verdict.
- Validate every applicable existing checklist question and source-defined completion field before returning GOOD or NEEDS_CORRECTION.
- Use existing checklist questions unchanged. Do not add, redesign, expand, or rewrite them.
- For every NEEDS_CORRECTION finding, identify the existing checklist question and include authority, evidence, correction, and impact.
- Lead with severity-ordered actionable findings and separate required corrections, optional improvements, missing evidence, and residual risk.
- Treat the candidate as read-only while allowing only authorized checklist and findings artifact writes.
- Bind the exact canonical checklist and retained completed checklist with SHA-256, and accept checklist-completeness only from the repository validator.
- Protect the candidate with the runner-owned baseline inventory. Permit only the declared checklist and findings output paths, retain their exact bytes, and restore the baseline before verdict.

## Failure Conditions

- Accept source-to-adapter or catalog drift.
- Recommend direct generated-output edits instead of source correction and regeneration.
- Miss a missing regression expectation or claim verification from absent command evidence.
- Manufacture a finding for an aligned change.
- Return GOOD or NEEDS_CORRECTION when the saved checklist is missing or incomplete.
- Return a NEEDS_CORRECTION finding that omits its existing checklist question, authority, evidence, correction, or impact.
- Add, redesign, expand, or rewrite an existing checklist question.
- Modify the candidate methodology change.
- Accept a missing, incomplete, reordered, rewritten, or duplicated saved checklist record, an unauthorized candidate change, or a retained-output byte mismatch.

## Semantic Dimensions

Judge evidence extraction, source authority, saved-checklist validity, checklist-to-finding traceability, finding-field completeness, drift detection, catalog completeness, regression analysis, correction quality, uncertainty discipline, and read-only compliance.
