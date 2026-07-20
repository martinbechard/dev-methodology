---
name: dev-artifact-reviewer-suite-contract
description: Share the canonical Dev Artifact Reviewer evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Artifact Reviewer Suite Contract

Evaluate finished non-wiki documentation through the generic structured-artifact checklist, the matching artifact-specific checklist when one applies, and the shared page verifier.

Complete the generic and specialized checklists as separate evidence artifacts before findings synthesis. For each checklist, preserve every canonical objective question exactly once and in source order. Use sequential Q001 headings, copy each Question line without rewriting it, and complete every field named by that checklist's Completion Format. Do not merge canonical questions into themes. Additional observations and concise synthesis may follow only after every applicable canonical record is complete.

The supervisor must run evals/agent-tests/dev-artifact-reviewer/checklist_contract.py with one repository-owned canonical and completed pair for each applicable checklist. Retain its JSON as the checklist-completeness evidence artifact. Pass that critical gate only when the command exits zero, every pair is independently valid, the reported counts match the current canonical sources, and the result binds repository-relative paths and SHA-256 digests for both the canonical sources and exact completed evidence artifacts. The supervisor and Judge must match each completed digest to the retained checklist artifact before using the result.

Require quoted source evidence, finding-first synthesis, an independent verifier assessment, prioritized actionable corrections, and read-only review authority unless saving review evidence was explicitly requested. Missing policy or specialized review authority limits the conclusion. Preserve the complete generic checklist, state the unavailable dimensions as an explicit blocker, and do not invent, rewrite, or substitute a specialized checklist. Judge checklist fit, evidence quality, source authority, finding priority, verifier integrity, and correction clarity.
