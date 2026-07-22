---
name: dev-orchestrator-suite-contract
description: Share the canonical Dev Orchestrator evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Orchestrator Suite Contract

Evaluate bounded coordination through the canonical owners. Require non-overlapping claims, committed clean handoffs, fresh independent reviews, verification only after review gates, deliberate integration only for multiple contributions, and post-integration review before complete verification. Fixed dependencies are Dev Coder, Dev Code Reviewer, Dev Verifier, Dev Merge Coordinator, and Dev Backlog Steward. The dependency-routing scenario additionally selects Dev Documentation Writer and Dev Artifact Reviewer without changing the canonical role definition.

For dependency-routing, require this exact dependency order: Dev Coder candidate, fresh Dev Code Reviewer, Dev Documentation Writer, fresh Dev Artifact Reviewer, Dev Verifier, Dev Merge Coordinator, fresh post-integration Dev Code Reviewer, fresh post-integration Dev Artifact Reviewer, final Dev Verifier, effective Commit skill application, and Dev Backlog Steward only after Commit returns READY. Use one nested dependency at a time. Require structured receipts for source, documentation, integration, Commit disposition, and Persistence closeout. Each receipt names its lane, role, commit, review, verification, and claim release evidence. Prose summaries do not replace receipts.

Keep bounded-correction and terminal-status-integrity behavior unchanged. Stop after two failed corrections for one finding. Preserve AWAITING_REVIEW without Persistence closeout, resume the same Commit delivery identity through corrections and merge, and require Commit READY before Dev Backlog Steward. READY requires the final delivered commit, provider closeout when selected, and clean released claims. Judge routing, dependency order, ownership separation, evidence continuity, and terminal integrity.
