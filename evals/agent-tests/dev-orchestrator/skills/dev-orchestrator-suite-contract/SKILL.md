---
name: dev-orchestrator-suite-contract
description: Share the canonical Dev Orchestrator evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Orchestrator Suite Contract

Evaluate bounded coordination through the canonical owners. Require non-overlapping claims, committed clean handoffs, fresh independent reviews, verification only after review gates, deliberate integration only for multiple contributions, and post-integration review before complete verification. Fixed dependencies are Dev Coder, Dev Code Reviewer, Dev Verifier, Dev Merge Coordinator, and Dev Backlog Steward. The dependency-routing scenario additionally selects Dev Documentation Writer and Dev Artifact Reviewer without changing the canonical role definition.

For dependency-routing, require this exact order: Dev Coder, fresh Dev Code Reviewer, Dev Documentation Writer, fresh Dev Artifact Reviewer, Dev Verifier, Dev Merge Coordinator, fresh post-integration Dev Code Reviewer, fresh post-integration Dev Artifact Reviewer, final Dev Verifier, and Dev Backlog Steward. Use one nested dependency at a time. Require structured receipts for source, documentation, integration, and closeout. Each receipt names its lane, role, commit, review, verification, and claim release evidence. Prose summaries do not replace receipts.

Keep bounded-correction and terminal-status-integrity behavior unchanged. Stop after two failed corrections for one finding. READY requires the final commit plus clean released claims. Judge routing, dependency order, ownership separation, evidence continuity, and terminal integrity.
