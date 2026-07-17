---
name: dev-prompt-reviewer-suite-contract
description: Share the canonical Dev Prompt Reviewer evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Dev Prompt Reviewer Suite Contract

Evaluate the target as an end-to-end model-facing contract reviewer rather than a prompt copy editor.

## Required Contract

- Trace instructions, state, tools, outputs, retries, cancellation, fallback, authority, and protected-data boundaries together.
- Ground each finding in the supplied prompt or runtime evidence.
- Keep verified behavior, contradictions, assumptions, missing evidence, and residual risk distinct.
- Identify repeated-side-effect and schema-promise risks at the boundary that owns the correction.
- Map material promises and failure modes to executable evaluation coverage.
- Return prompt contract findings, schema and tool-call risks, and evaluation gaps.

## Failure Conditions

- Review wording in isolation from runtime behavior.
- Infer provider semantics or tool authority absent from evidence.
- Miss a material duplicate-side-effect or protected-data boundary.
- Manufacture a finding for an aligned contract.
- Modify a read-only fixture or claim verification without trace evidence.

## Semantic Dimensions

Judge contract traceability, safety-boundary accuracy, schema analysis, uncertainty discipline, evaluation-gap quality, and output completeness.
