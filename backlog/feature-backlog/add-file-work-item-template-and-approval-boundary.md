# Add File Work Item Template And Approval Boundary

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-file-work-item-template-and-approval-boundary.md

Completion: direct-main

## User Action Required

### Question For The User

Do you approve changing exactly skills/create-file-work-item/SKILL.md and skills/development-methodology/SKILL.md, together with their supported generated skill mirrors and directly related non-governed file-work-item template, template-catalog documentation, generated template data, and focused tests, to implement this work item?

### Why User Input Is Required

Bounded read-only discovery by canonical task 019f85c8-628f-75c3-87b6-65a140c3dd20 established these two governed skill definitions as the smallest coherent source scope. Repository policy requires exact path-specific approval before either definition is mutated.

### Options And Tradeoffs

- Approve the exact two-skill scope: implement the reusable template and approval boundary coherently with its distribution owner.
- Narrow the scope by naming allowed paths: preserve the remaining requirements as unresolved follow-up work.
- Defer: move the item to Holding without creating implementation artifacts.

### Resolution

- Answer: Approved.
- User wording: "approved".
- Date: 2026-07-21.
- Provenance: direct user response in parent backlog-coordination task 019f77f4-c4bd-7c91-b197-c987a7beb838 to the exact two-skill question recorded above.
- Approved governed scope: skills/create-file-work-item/SKILL.md and skills/development-methodology/SKILL.md.
- Approved dependent scope: only their supported generated mirrors and the directly related non-governed file-work-item template, template-catalog documentation, generated template data, and focused tests.
- Exclusions: no other governed definition unless separately approved.
- Disposition: Ready for a fresh canonical Dev Orchestrator task.

### Unattended Work Boundary

Implementation is authorized only within the exact resolved scope above. Preserve the read-only decision that removable HTML comments provide template guidance and that exact approval scope plus user-message provenance remain durably recorded in the work-item body, with any checker YAML treated as derived operational evidence.

### Discovery Evidence

- Canonical discovery task: 019f85c8-628f-75c3-87b6-65a140c3dd20.
- Worktree: /Users/martinbechard/.codex/worktrees/b295/dev-methodology, clean at starting main 2624b5b25ba6e5548051d7b9953933b1e57b3f87.
- UAR routing claim: route-file-work-item-template-approval, acquired event b1fb319c-060d-41e3-80b3-f24d830f17b0.

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Provide a reusable file-backed work-item template and make create-file-work-item explicitly distinguish ordinary Open Questions from genuine user-owned approval gates, including governed-definition changes.

## Context

The earlier coordination item used Open Decisions and asked whether the user authorized a design-only precursor. The user found that framing confusing because technical design questions should be resolved by agents and the requested design analysis was already authorized.

The user-reviewed dialogue on 2026-07-21 selected Open Questions as the consistent heading and identified a reusable template as the right place to standardize the document shape. Repository policy separately requires exact, scope-specific approval before mutating governed agent or skill definitions.

## Source Evidence

- The user rejected the context-free sentence in the earlier draft and asked which writing, review, and backlog skills apply to work-item creation.
- On 2026-07-21, the user agreed that ordinary technical questions belong under Open Questions and stated that the governed-definition boundary should be represented in a skill and template.
- On 2026-07-21, the user explicitly requested creation of work items based on the completed conversations.

## Requirements

- Add a reusable template for file-backed work items using the required provider fields and standard sections.
- Use Open Questions for unresolved technical matters; do not label them Open Decisions merely because a choice remains.
- State that agents resolve ordinary technical questions through discovery, design, review, and verification.
- Use Question for the User only for a genuine user-owned decision, authority grant, value judgment, risk acceptance, or user-held information.
- Make create-file-work-item state the governed-definition approval boundary.
- When governed definitions are expected to change, require source discovery to produce an exact canonical-path manifest before requesting approval.
- Prohibit vague questions such as asking permission to continue designing when design is already requested.
- Keep change-control manifests out of Design Principles; treat them as approval evidence.
- Define how the template handles sections that are not applicable without encouraging empty boilerplate.
- Update validation, examples, documentation, and focused regression tests.
- Obtain exact, scope-specific approval before changing create-file-work-item or any other governed skill definition.

## Acceptance Criteria

- A newly created file-backed item is understandable without its originating conversation.
- The template contains the canonical provider metadata, Summary, Context, Requirements, Acceptance Criteria, Dependencies, Verification, Notes, and an appropriate Open Questions location.
- User Action Required fields appear only when a concrete user-owned answer blocks the next safe step.
- Technical questions do not make an otherwise authorized item non-dispatchable.
- Governed-definition work records the exact approval scope before mutation without treating that manifest as part of the design.
- Focused tests reject vague, context-dependent source evidence and invalid user-action classification.

## Dependencies

None.

## Verification

- Compare the template against create-file-work-item and manage-file-work-items required fields and transitions.
- Exercise Ready, User Action Required, Holding, and related-series examples.
- Test Open Questions and exact governed-definition approval behavior.
- Use structured-artifact review and documentation-page verification on the template and skill wording.
- Run focused bundle tests, Git diff validation, and independent methodology review.

## Open Questions

None. Bounded discovery selected removable optional-section comments and durable approval scope plus user-message provenance in the item body; checker-compatible YAML is derived operational evidence rather than the authority record.

## Notes

- The project-wiki shared-page contract also uses Open Questions, reinforcing the repository-wide vocabulary without making the wiki template authoritative for backlog items.
