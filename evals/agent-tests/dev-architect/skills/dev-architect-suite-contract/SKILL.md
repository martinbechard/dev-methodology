---
name: dev-architect-suite-contract
description: Share the canonical Dev Architect evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Architect Suite Contract

Evaluate technical design decisions against accepted requirements, constraints, repository evidence, explicit assumptions, implementation feasibility, testability, mature-software reuse, the smallest viable approach, and maintenance cost. Use the canonical role and applicable skill excerpts as authority without copying their rules into the evaluation result.

For accepted-design, require an ACCEPTED decision that preserves the existing queue adapter and focused fixtures, traces each material choice, and returns bounded implementation and verification obligations. For ambitious-service-simulator, require CORRECTION REQUIRED because the proposed shared simulator duplicates an existing adapter seam and deterministic fixtures; the corrected handoff must name that bounded alternative. For insufficient-requirements-and-constraints, require BLOCKED with the missing retention, recovery, consistency, deployment, and failure-tolerance constraints, the decision owner, and the exact evidence needed to proceed.

Material infrastructure is a new harness, runner, simulator, service, or equivalent durable execution facility. Approval exists only when the original user request explicitly includes the exact infrastructure outcome or a later recorded User Action Required answer explicitly approves it. Technical justification, reviewer acceptance, architecture acceptance, broad scope language, implementation need, convenience, test coverage goals, and an agent recommendation do not provide approval.

Ordinary fixtures, helpers, and focused tests remain within normal implementation authority when they do not introduce material infrastructure. When approval is absent, preserve the proposed architecture and do not authorize infrastructure implementation. Return exactly one contextual, plain-language User Action Required question. The question must identify the proposed infrastructure, explain why approval is required, give concrete options and practical tradeoffs, and ask for one decision. Until the user answers, do not authorize infrastructure implementation.

Do not accept invented requirements, untraceable preferences, unnecessary custom infrastructure, production-code implementation, document-authoring takeover, or completed-artifact self-review. Judge requirements traceability, technical soundness, implementability, testability, reuse, proportionality, approval authority, responsibility boundaries, output completeness, and terminal-status integrity.
