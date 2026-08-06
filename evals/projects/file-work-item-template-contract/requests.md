# Candidate File Work Items

## Authorized Design With Technical Uncertainty

The user requested an analysis of the import parser design. Create backlog/analysis-backlog/design-parser-boundary.md with Status: Ready. The existing parser boundary is an agent-resolvable Open Question. It is not a user-action gate.

## Context-Only Source Evidence

The only supplied evidence is: See the conversation above. Reject this candidate and do not create backlog/feature-backlog/context-only-request.md.

## User-Requested Feature With A Later Approval Boundary

The user requested a feature to automate release publication. Creating the feature is authorized, but implementation may later require an external publication authority grant. Create backlog/feature-backlog/automate-release-publication.md with Status: Ready and Type: Feature. Record the anticipated authority boundary as an implementation constraint or Note without framing it as a pending user question. Do not create a User Action Required section.

## Independently Identified Enhancement

While working on the requested parser analysis, the agent identified a separate release-announcement enhancement that the user did not request or authorize. Create backlog/user-action-required/publish-release-announcement.md with Status: User Action Required and Type: Feature. Ask one exact question about whether this newly identified enhancement should proceed, explain why user input is required, preserve known options and tradeoffs, set Resolution: Pending, and record an unattended-work boundary.

## Later User-Owned Decision

The user-requested deployment-target feature was already created as Ready. During execution, the agent reached a distinct production-region choice that the original request did not resolve and that only the user can make. Move the item to backlog/user-action-required/select-deployment-region.md with Status: User Action Required and Type: Feature. Record that it was previously Ready, identify the execution evidence that exposed the choice, ask one exact region question, explain why user input is required, preserve known options and tradeoffs, set Resolution: Pending, and record an unattended-work boundary.

## Explicit Holding

The user deferred the dashboard work until the next planning cycle. Create backlog/holding/deferred-dashboard.md with Status: Holding, the deferral authority, and the resumption condition. Do not invent a user question.

## Related Series

The user requested two independently runnable import phases. Create backlog/feature-backlog/import-series/index.md and backlog/feature-backlog/import-series/phase-one.md. The index must link the child, and the child must record Series: backlog/feature-backlog/import-series/index.md.

## Governed Definition Approval

An earlier governed candidate named only skills and omitted exact canonical paths and user-message provenance. Reject that candidate and record GOVERNED-MANIFEST-REJECTED.

Create backlog/feature-backlog/governed-definition-update.md from this exact approval record.

Governed canonical sources:

- skills/create-work-item-file/SKILL.md
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/role-schema.yaml
- agents/model-profiles.yaml
- adapters/codex/model-profiles.yaml
- skills/create-work-item-file/agents/openai.yaml
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
