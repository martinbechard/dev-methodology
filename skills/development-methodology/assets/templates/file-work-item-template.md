<!--
File path: skills/development-methodology/assets/templates/file-work-item-template.md
1-line summary: Template for one self-contained file-backed work item.
-->

# TODO Work Item Title

Status: TODO Ready, User Action Required, or Holding

Type: TODO Defect, Feature, Analysis, Investigation, or Holding

Provider: file

Provider Reference: TODO canonical repository-relative backlog path

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

> This section prevents work from starting or closing without accounting for prerequisite items. Coordinators and implementers use it during dispatch and status review to list canonical provider references or explicitly state that none exist.

TODO: List canonical provider references, or state None.

## Verification

> This section makes the evidence required for completion visible before delivery begins. Implementers and verifiers use it during planning and closeout to name the tests, builds, checks, reviews, or artifacts that must demonstrate the result.

- TODO: Name expected tests, builds, checks, reviews, or artifacts.

## Open Questions

> This section keeps agent-resolvable uncertainty visible without misclassifying it as a user-owned blocker. Implementers and designers use it during discovery and design to record technical questions and update them as evidence resolves them.

TODO: Record agent-resolvable technical uncertainty for discovery, design, review, or verification. State None when no technical questions remain. Open Questions do not by themselves make an authorized item non-dispatchable.

<!-- OPTIONAL: User Action Required. Keep this section only when one concrete user-owned answer blocks the next safe step. Remove this comment and the entire section otherwise. -->

## User Action Required

> This optional section separates a genuine user-owned blocker from technical uncertainty, preventing unsafe assumptions while allowing bounded discovery to continue. Coordinators and implementers use it only when one concrete answer is required for the next safe step, and record the question, rationale, options, resolution, and unattended boundary in its subsections.

<!-- OPTIONAL: Governed definition pre-answer evidence. Keep these subsections only when governed definitions are expected to change. Remove this comment and both subsections otherwise. -->

### Governed Canonical Sources

> This subsection makes definition-change approval exact enough to enforce and audit. Definition maintainers use it before asking for approval to list every governed canonical file that discovery shows must change.

- TODO: List each exact repository-relative governed source path that discovery found necessary. Do not use directories, wildcards, or artifact categories.

### Allowed Dependent Artifacts

> This subsection bounds noncanonical effects of an approved definition change, preventing approval from expanding implicitly. Definition maintainers and reviewers use it with governed-source approval to list supported generated mirrors and any separately permitted dependent files.

- TODO: List supported generated mirrors and each separately allowed non-governed dependent path. State None when approval covers only the governed sources.

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

Pending. After the answer, record the exact answer, user wording, date, and user-message provenance. For governed definitions, preserve the approved Governed Canonical Sources and Allowed Dependent Artifacts above; do not infer broader scope from the answer.

### Unattended Work Boundary

> This subsection protects the unresolved decision while preserving safe progress elsewhere. Coordinators and implementers use it to state which mutations must wait and which read-only discovery may continue before resolution.

TODO: State what work must not proceed before resolution and what read-only discovery may continue.

<!-- OPTIONAL: Notes. Remove this comment and the entire section when no edge cases, examples, or non-goals add useful context. -->

## Notes

> This optional section preserves useful context that does not belong in the requirements or acceptance contract. Implementers and reviewers use it only when edge cases, examples, or non-goals materially help implementation or review, and record that context without expanding the requirements.

TODO: Record useful edge cases, examples, or non-goals.
