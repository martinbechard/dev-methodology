---
name: dev-orchestrator-suite-contract
description: Share the canonical Dev Orchestrator evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Orchestrator Suite Contract

Evaluate bounded coordination through the canonical owners. Require committed clean handoffs, fresh independent reviews, verification only after review gates, deliberate integration only for multiple contributions, and post-integration review before complete verification. Apply resource coordination independently: agent-claim requires non-overlapping claims and clean release evidence, while none requires zero claim calls and zero claim evidence. Fixed dependencies are Dev Coder, Dev Code Reviewer, Dev Verifier, Dev Merge Coordinator, and Dev Backlog Steward. The dependency-routing scenario additionally selects Dev Documentation Writer and Dev Artifact Reviewer without changing the canonical role definition.

For dependency-routing, require this exact dependency order: Dev Coder candidate, fresh Dev Code Reviewer, Dev Documentation Writer, fresh Dev Artifact Reviewer, Dev Verifier, Dev Merge Coordinator, fresh post-integration Dev Code Reviewer, fresh post-integration Dev Artifact Reviewer, final Dev Verifier, effective Commit skill application, and Dev Backlog Steward only after Commit returns READY. The Commit skill returns the prepared handoff; it does not dispatch the manager. AWAITING_REVIEW preserves the same delivery identity with zero Persistence calls. After Commit READY, Dev Orchestrator dispatches Dev Backlog Steward exactly once and verifies the selected manager's recorded closure. Provider none instead requires verified task-local COMPLETED finalization and zero steward calls. Use one nested dependency at a time. Require structured receipts for source, documentation, integration, Commit disposition, and Persistence closeout. Each receipt names its lane, role, commit, review, and verification. It also names claim release evidence only when resource coordination selects agent-claim. Prose summaries do not replace receipts.

Keep bounded-correction and terminal-status-integrity behavior unchanged. Stop after two failed corrections for one finding. Preserve AWAITING_REVIEW without Persistence closeout, resume the same Commit delivery identity through corrections and merge, and require Commit READY before Dev Backlog Steward. READY requires the final delivered commit, provider closeout when selected, and clean released enabled resource ownership. Judge routing, dependency order, ownership separation, evidence continuity, and terminal integrity.
