---
name: code-review-evidence
description: Use when reviewing source changes by loading applicable coding and stack skills, completing their evidence checklists, and synthesizing findings from cited evidence. Use for code review, diff review, regression review, or delegated low-cost evidence extraction.
metadata:
  category: development-practice
---

# Code Review Evidence

Keep review knowledge with the skills that create the code. This skill owns the review protocol, not one universal catalog of language, framework, tier, or database rules.

## Inputs

- The requested review scope and changed files.
- Project guidance and intended behavior.
- Applicable generic, language, framework, tier, persistence, and test skills.
- Tests, build output, and runtime evidence relevant to the change.

## Workflow

1. Inventory the changed files and select the same coding and stack skills that should have governed their implementation.
2. Load references/review-checklist-code-evidence.md plus each selected skill's review checklist.
3. Extract evidence before writing findings. A lower-cost model may perform this stage when the harness supports staged model profiles.
4. Record each checklist item as supported, contradicted, unknown, or not applicable. Cite the smallest useful file, symbol, location, command, or test result.
5. Treat extracted evidence as observations, not final judgment. Preserve uncertainty and conflicts.
6. Use the synthesis model to reconcile the evidence, assess impact, and produce findings, passes, open questions, and residual risk.

## Evidence Packet

For every applicable question record:

- Checklist and question identifier.
- Status: supported, contradicted, unknown, or not applicable.
- File, symbol, and tight location.
- Test or command evidence when relevant.
- Short factual observation.
- Confidence and missing evidence.

## Synthesis Rules

- Derive findings from contradicted or materially unknown checklist items.
- Cite the evidence packet and source location for every finding.
- Rank by user, correctness, security, data, operability, or maintainability impact.
- Do not elevate personal style preferences into findings.
- Do not mark a rule satisfied because no defect was found; require positive evidence where the checklist calls for it.
- Keep language and framework details in their owning skills and checklists.
