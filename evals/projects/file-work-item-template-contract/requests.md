# Candidate File Work Items

## Authorized Design With Technical Uncertainty

The user requested an analysis of the import parser design. Create backlog/analysis-backlog/design-parser-boundary.md with Status: Ready. The existing parser boundary is an agent-resolvable Open Question. It is not a user-action gate.

## Context-Only Source Evidence

The only supplied evidence is: See the conversation above. Reject this candidate and do not create backlog/feature-backlog/context-only-request.md.

## Genuine User-Owned Authority

External release publication requires an authority grant that only the user can provide. Create backlog/user-action-required/publish-release.md with Status: User Action Required, Type: Feature, one exact question, the reason user input is required, known options and tradeoffs, Resolution: Pending, and an unattended-work boundary.

## Explicit Holding

The user deferred the dashboard work until the next planning cycle. Create backlog/holding/deferred-dashboard.md with Status: Holding, the deferral authority, and the resumption condition. Do not invent a user question.

## Related Series

The user requested two independently runnable import phases. Create backlog/feature-backlog/import-series/index.md and backlog/feature-backlog/import-series/phase-one.md. The index must link the child, and the child must record Series: backlog/feature-backlog/import-series/index.md.

## Governed Definition Approval

An earlier governed candidate named only skills and omitted exact canonical paths and user-message provenance. Reject that candidate and record GOVERNED-MANIFEST-REJECTED.

Create backlog/feature-backlog/governed-definition-update.md from this exact approval record.

Governed canonical sources:

- skills/create-file-work-item/SKILL.md
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/role-schema.yaml
- agents/model-profiles.yaml
- adapters/codex/model-profiles.yaml
- skills/create-file-work-item/agents/openai.yaml
- adapters/codex/skills/codex-harness-directives/SKILL.md
- adapters/codex/skills/codex-harness-directives/agents/openai.yaml

Allowed dependent artifacts:

- design/generated/skill-definitions.js
- scripts/test_bundle_content.py

Resolution evidence:

- Answer: Approved.
- User wording: approved
- Date: 2026-07-21
- Provenance: user-message:thread-123/message-456

The candidate change also names skills/unapproved/SKILL.md. Reject that path because it is outside the approved governed and dependent manifests.

The supplied checker-approval.yaml claims approval for every skill under skills. Treat it as derived operational evidence only. It cannot create or widen approval.
