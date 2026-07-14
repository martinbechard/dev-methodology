# Legacy Procedure Migration Report: Design Review Feedback Guidelines

## Source And Scope

- Source: [design-review-feedback-guidelines.md](../design-review-feedback-guidelines.md)
- Scope: How to assess an existing design-review artifact and express feedback as inline TODO comments, then decide whether that review is acceptable or needs rework.
- Current model: artifact-specific review skills and review-structured produce an evidence-backed completed checklist followed by severity-ordered findings. The artifact-review-agent performs that read-only review and returns findings and corrections.

## Worth Keeping

The durable value is not the TODO syntax. Keep the underlying feedback discipline:

1. Establish the review target and all authoritative inputs before assessing it.
2. Validate each claimed problem against those inputs; challenge unsupported, vague, contradictory, or unscoped claims.
3. Make feedback precise, evidence-linked, and explicit about both the requested correction and why it matters.
4. Scale severity to the affected user or operational impact, rather than treating every defect as equally important.
5. Separate a problem in the reviewed design from a problem in the review evidence itself.
6. Close a review with a clear pass, findings requiring correction, or a genuine evidence gap.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| Locate the review artifact and corresponding design, then read the design before judging the review | review-structured; artifact-review-agent | Partial | Keep. review-structured requires the target and input artifacts, but does not require reading authoritative inputs before inspecting an existing review artifact. Add that ordering for review-of-review work. |
| Test every stated finding for contradiction, vagueness, or error against the design | review-structured | Partial | Keep as a conditional review-of-review step. Current directive-coverage and unsupported-assertion checks cover target claims, but do not explicitly validate pre-existing review findings. |
| Give special attention to critical findings and assess relevance for intended users | review-structured; artifact-review-agent | Partial | Keep the user-impact test. Findings already have severity, but neither the skill nor the role asks the reviewer to ground severity in actor, user, or operational consequence. |
| Make feedback specific, action-led, scoped, and justified | review-structured; artifact-review-agent | Partial | Keep, translated into finding fields rather than TODO prose. Current target, synopsis, and BECAUSE fields provide part of this, but an explicit correction field and concrete-action rule are absent. |
| Cite governing standards or source documents | review-structured; documentation-page-verifier | Partial | Keep. Both skills require sources or evidence, but review-structured's findings format does not require a cited authority when a correction depends on one. |
| Distinguish fix, documentation, proposal, investigation, and deferral | review-structured; development-orchestrator | Missing | Keep as a small classification field in review findings. A deferral should name the receiving backlog or decision artifact; it should not become an untracked TODO. |
| Use TODO2 and TODO3 to maintain a reply thread | No destination | Obsolete | Omit. Numbered inline conversations are replaced by completed checklists, finding identifiers, revised artifacts, and a new review pass. |
| Put TODOs immediately beside the reviewed prose | review-structured | Obsolete | Omit the placement rule. The new system deliberately separates the durable audit trail and findings from the source artifact. Preserve precise target locations instead. |
| Ask for clarification when the review finding itself is unclear or unverifiable | review-structured | Partial | Keep. The question status supports ambiguity, but the workflow should say that a questionable existing finding is a defect in the review artifact, distinct from a defect in the design. |
| Approve a sound review or request rework, then update a project status document | artifact-review-agent; development-orchestrator | Partial | Keep only the evidence-based disposition. The named approval note, status-file name, and AI revision loop are project-specific and should not enter a portable skill. Coordination of tracked follow-up belongs to the orchestrator or the target project's backlog practice. |

## Obsolete Or Project-Specific Guidance To Omit

- The TODO, TODO2, and TODO3 comment protocol and the requirement to insert comments inline.
- The legacy filename pairing convention using ComponentName-design-review.md and ComponentName-design.md. Current skills use artifact-name.review-checklist-[review-target].md and artifact-name.review-findings.md, while inputs are selected from actual authority.
- The retail-trader example. Preserve actor-impact reasoning, not this product audience.
- The named status document refactoring-plan-status.md, named approval note, and instruction that an AI assistant will revise the review. These are local workflow choices.
- The recursion of repeatedly commenting on a review document. Re-run the relevant checklist after corrections instead.

## Precise Suggested Additions

No new skill or agent is warranted. Make the following small additions to the existing generic review path:

1. In review-structured, after Required inputs, add a conditional subsection titled Reviewing an Existing Review Artifact:

   > When the target is a prior review or findings artifact, read the reviewed artifact and its authoritative inputs before evaluating the prior findings. For each prior finding, verify its target reference, evidence, severity, and stated consequence. Record an unsupported, contradictory, vague, or unscoped prior finding as a finding about the review artifact itself.

2. In review-structured, under Extract findings, add required fields after TARGET:

   > CORRECTION: an imperative, bounded action that resolves the finding, or a named investigation or deferral destination when a direct correction is not yet justified.
   > AUTHORITY: the applicable source, directive, standard, or checklist evidence when the correction depends on one.

3. In review-structured, add one finding-quality rule:

   > Set severity from the consequence for the affected actor, user, operator, system, or delivery decision. Do not elevate a finding solely because its wording sounds urgent.

4. In references/review-checklist-structured.md, add conditional questions:

   - When reviewing prior findings, does each finding cite the reviewed artifact and authoritative evidence?
   - When reviewing prior findings, are unclear, contradictory, or unsupported findings recorded as review-artifact defects?
   - Does every reported finding state a bounded correction, investigation, or tracked deferral destination?
   - Is the reported severity justified by actor, user, operational, or delivery impact?

5. Do not add these requirements to every artifact-specific checklist immediately. They belong in the generic base checklist, which all structured reviews load; artifact-specific checklists can inherit them without duplicating feedback-writing policy.

## Conclusion

Migrate the evidence-first feedback principles into review-structured and its base checklist. Retire inline TODO conversations, legacy filename conventions, and project status-file mechanics. The existing artifact-review-agent remains the correct role; development-orchestrator can own any project-specific disposition or tracked follow-up. The highest-value gap is a required, explicit correction and authority for each finding, with severity tied to real impact.
