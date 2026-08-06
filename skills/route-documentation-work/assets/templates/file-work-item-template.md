<!--
File path: skills/route-documentation-work/assets/templates/file-work-item-template.md
1-line summary: Template for one self-contained file-backed work item.
-->

<!--
This template is only for ordinary file-backed work items. Future Ideas use the lightweight
record shape in manage-future-ideas and do not carry work-item lifecycle fields.
-->

# TODO Work Item Title

Status: TODO Ready, Blocked, User Action Required, or Holding

Type: TODO Defect, Feature, Analysis, Investigation, or Holding

Provider: file

Work Item ID: TODO immutable filename stem without .md

Completion: TODO direct-main, feature-branch, or UNSET

<!-- OPTIONAL: Series child metadata. Remove this comment and the Series line for a standalone item. -->

Series: TODO canonical repository-relative path to the related index.md

## Summary

> This section lets coordinators and implementers identify the promised outcome without reconstructing the whole request. Coordinators and implementers use it during triage, assignment, and closeout to state the durable result in one or two sentences.

TODO: State the durable outcome in one or two sentences.

## Context

> This section preserves the conditions and constraints that make the work necessary, so delivery does not depend on chat history. Implementers and reviewers use it during discovery and implementation to record current behavior, impact, constraints, and source references.

TODO: Record the current behavior, impact, constraints, and source references needed to understand this item without the originating conversation.

## Source Evidence

> This section makes the item's authority and origin auditable, preventing agents from treating an inferred request as approved work. Coordinators and reviewers use it during creation and review to record concrete wording and provenance that stand independently of conversation history.

TODO: Record the request, finding, or decision that authorizes creation. Include enough concrete wording and provenance to stand without chat context.

## Requirements

> This section translates the requested outcome into bounded obligations that implementation and review can evaluate consistently. Implementers and reviewers use it during planning and delivery to list the concrete behaviors or artifacts the item must provide.

- TODO: State concrete behavior or deliverables.

## Acceptance Criteria

> This section defines observable evidence of completion so closure is based on results rather than effort. Implementers, verifiers, and reviewers use it during implementation, verification, and review to list conditions that can be checked directly.

- TODO: State observable completion conditions.

## Dependencies

> This section prevents work from receiving Ready or closing without accounting for prerequisite items. Coordinators and implementers resolve each opaque Work Item ID before lifecycle assignment: no unmet hard prerequisite permits Ready; an unmet hard prerequisite requires Blocked and an exact unblock condition.

TODO: List Work Item IDs, or state None.

## Verification

> This section makes the evidence required for completion visible before delivery begins. Implementers and verifiers use it during planning and closeout to name the tests, builds, checks, reviews, or artifacts that must demonstrate the result.

- TODO: Name expected tests, builds, checks, reviews, or artifacts.

## Open Questions

> This section keeps agent-resolvable uncertainty visible without misclassifying it as a user-owned blocker. Implementers and designers use it during discovery and design to record technical questions and update them as evidence resolves them.

TODO: Record agent-resolvable technical uncertainty for discovery, design, review, or verification. State None when no technical questions remain. Open Questions do not by themselves make an authorized item non-dispatchable.

<!-- OPTIONAL: Governed Definition Approval. Keep this section when governed definitions are expected to change. Remove this comment and the entire section otherwise. -->

## Governed Definition Approval

> This optional section makes definition-change authority exact and auditable without manufacturing a second approval request for work the user already requested. Definition maintainers and reviewers use it to record the governed manifest, dependent effects, and the request or later answer that authorizes the scope.

### Governed Canonical Sources

> This subsection lists every governed canonical file in the approved scope. For a user-requested work item that creates or modifies named skills, resolve and record the exact named skill-definition paths approved by that request.

- TODO: List each exact repository-relative governed source path. Do not use directories, wildcards, or artifact categories.

### Allowed Dependent Artifacts

> This subsection bounds noncanonical effects of an approved definition change. List supported generated mirrors and any separately permitted non-governed dependent files without treating them as additional governed definitions.

- TODO: List supported generated mirrors and each separately allowed non-governed dependent path. State None when approval covers only the governed sources.

### Approval Resolution

> This subsection records why the exact governed manifest is authorized. When the user explicitly requested a work item to create or modify the named skills, record Approved at creation with the exact request wording, date, and user-message provenance. If an additional governed path is discovered later, keep the original manifest approved and record Pending only for the additional path until the user answers.

TODO: Record Approved at creation, Approved by later answer, or Pending for additional scope, with exact wording, date, provenance, and unchanged boundaries.

<!-- OPTIONAL: User Action Required. Keep this section only when one concrete user-owned answer blocks the next safe step. Remove this comment and the entire section otherwise. -->

## User Action Required

> This optional section separates a genuine user-owned blocker from technical uncertainty, preventing unsafe assumptions while allowing bounded discovery to continue. Coordinators and implementers use it only when one concrete answer is required for the next safe step, and record the question, rationale, options, resolution, and unattended boundary in its subsections.

### Question for the User

> This subsection focuses the blocker on the one decision only the user can make. Coordinators and implementers use it to ask a concrete question about authority, values, risk acceptance, or information the user uniquely holds.

TODO: Ask one concrete question about a user-owned decision, authority grant, value judgment, risk acceptance, or user-held information.

### Why User Input Is Required

> This subsection shows why proceeding would exceed agent authority or require an unsafe assumption. Coordinators and implementers use it before pausing affected work to explain the decision boundary that evidence and technical work cannot resolve.

TODO: Explain why agents cannot resolve this question safely.

### Options and Tradeoffs

> This optional subsection helps the user make an informed decision without having to rediscover feasible choices. Coordinators and implementers use it when meaningful alternatives are known to summarize each option's practical effects.

- TODO: List known options and their practical effects. Remove this subsection when no meaningful choice set is known.

### Resolution

> This subsection creates durable evidence of the answer so later agents can act within exactly the authority granted. Coordinators and implementers use it after the user responds to record the wording, date, provenance, and unchanged approval boundaries.

Pending. After the answer, record the exact answer, user wording, date, and user-message provenance. When this answer approves additional governed scope, update Governed Definition Approval above without broadening the originally approved manifest.

### Unattended Work Boundary

> This subsection protects the unresolved decision while preserving safe progress elsewhere. Coordinators and implementers use it to state which mutations must wait and which read-only discovery may continue before resolution.

TODO: State what work must not proceed before resolution and what read-only discovery may continue.

<!-- OPTIONAL: Notes. Remove this comment and the entire section when no edge cases, examples, or non-goals add useful context. -->

## Notes

> This optional section preserves useful context that does not belong in the requirements or acceptance contract. Implementers and reviewers use it only when edge cases, examples, or non-goals materially help implementation or review, and record that context without expanding the requirements.

TODO: Record useful edge cases, examples, or non-goals.
