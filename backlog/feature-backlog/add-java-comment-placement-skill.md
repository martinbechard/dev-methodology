# Add Java Comment Placement Skill

Status: Blocked

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-java-comment-placement-skill.md

Completion: direct-main

## Current Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f8781-917c-7933-9c76-d7e3305df9b3
- Worktree: /Users/martinbechard/.codex/worktrees/e56a/dev-methodology
- Branch: codex/add-java-comment-placement-skill
- Starting main: 92a2009c70657860d6182b234e8a64da31ca40ed
- Phase: Blocked after the bounded correction loop exhausted the evaluator output-contract criterion; no integration or completion transaction started.
- Started: 2026-07-21.
- Open issues: The Java evaluation verifier accepts an eval-result.md containing only the six bare required labels. It does not require real Markdown headings or non-empty affected-path and verification-result content under each heading.
- Accepted candidate: 02cc7215edce2782875998c3074a2a84ce5e441e, preserved as one clean feature commit on codex/add-java-comment-placement-skill atop main 3f262f6c3e8f997a8038edf42ffbd49df7b44bc4. The candidate is not independently verified and is not accepted for integration.

## Blocked Handoff

- Blocker: Independent Dev Verifier demonstrated that evals/projects/java-comment-placement/verify.py checks only substring presence for six evidence labels. A result containing only those labels returns exit 0 even though TASK.md requires an affected path and verification result under every heading.
- Decisive evidence: HEADINGS_ONLY_EXIT=0 with empty stdout and stderr; verifier implementation lines 235-247 conflict with TASK.md line 18.
- Why execution stopped: The same evaluator and oracle acceptance boundary remained open after two correction attempts. The bounded correction loop prohibits a third blind correction or a weakened verification gate.
- Preserved work: candidate 02cc7215edce2782875998c3074a2a84ce5e441e on codex/add-java-comment-placement-skill. Earlier focused skill, metadata, detection, catalog, generator, diff, and clean-status checks passed, but they do not override the verifier failure.
- Next action owner: A fresh Dev Orchestrator task with a new correction owner; the exhausted canonical task must not resume implementation.
- Unblock condition: Parse actual Markdown headings, require non-empty affected-path and verification-result content under every required heading, add a bare-label rejection regression, add a complete-evidence acceptance regression, and obtain fresh independent review and verification of the cumulative candidate.
- Permitted resumption: After a fresh owner accepts the item through the normal Blocked to Ready to newly claimed Running transition. Do not integrate 02cc721 directly and do not infer ownership from this authorization.
- Scope authority: The existing exact approval for skills/code-comments/SKILL.md, skills/java-comment/SKILL.md, and skills/java-comment/agents/openai.yaml remains valid. The required evaluator-only correction is within the already approved directly related non-governed tests and evaluations scope; no additional governed-definition approval is required.
- Released implementation claims: add-java-comment-placement-019f8781 release event 9ef2efdc-0752-4d99-9d4e-ba30a9459909; java-comment-correction-019f8781 release event cf590329-30e7-4ac7-8e14-51e207084891; java-comment-final-correction-019f8781 release event 7432a914-02ac-4a04-8151-886638933d4a.
- Backlog transition claim: block-java-comment-verifier-019f8781 acquired event fe03cd38-5a84-4d81-aca4-911ab1c7905b and releases immediately after this one-file commit.

## User Action Required

### Question For The User

Do you approve creating or changing exactly these three governed definition paths for the Java comment-placement item?

1. skills/code-comments/SKILL.md
2. skills/java-comment/SKILL.md
3. skills/java-comment/agents/openai.yaml

This approval also permits only their supported generated mirrors and directly related non-governed detection metadata, review checklists, tests and evaluations, README, and design documentation. No other governed definition is authorized.

### Why User Input Is Required

The work item requires two distributed skill definitions and one skill metadata definition. Repository policy requires explicit path-specific approval before any of those governed sources can be created or changed.

### Options And Tradeoffs

- Approve the exact three-path scope: implement the requested Java placement refinement and its supported dependent surfaces.
- Narrow the scope by naming allowed paths: preserve excluded behavior as blocked follow-up work.
- Defer: retain the completed discovery without implementation.

### Resolution

- Answer: Approved.
- User wording: "ok".
- Date: 2026-07-21.
- Provenance: direct user response in parent backlog-coordination task 019f77f4-c4bd-7c91-b197-c987a7beb838 to the Java comment-placement approval item and exact three-path question previously presented.
- Approved governed scope: skills/code-comments/SKILL.md, skills/java-comment/SKILL.md, and skills/java-comment/agents/openai.yaml.
- Approved dependent scope: only their supported generated mirrors and directly related non-governed detection metadata, review checklists, tests and evaluations, README, and design documentation.
- Exclusions: no other governed definition; in particular, no change to skills/java/SKILL.md or skills/java/agents/openai.yaml.
- Disposition: Ready for a fresh canonical Dev Orchestrator task.

### Unattended Work Boundary

Implementation is authorized only within the exact resolved scope above. Preserve the evidence-backed selection through java-comment detection metadata and do not change the existing java skill definitions.

### Discovery Evidence

- Discovery task: 019f86b4-9e20-76a1-b5cb-7618fce32e28.
- Exact governed manifest: skills/code-comments/SKILL.md, skills/java-comment/SKILL.md, and skills/java-comment/agents/openai.yaml.
- No change is required to skills/java/SKILL.md or skills/java/agents/openai.yaml.
- Java selection is owned by ordinary skills/java-comment/detection.yaml using .java activation, parallel to the existing Java detection metadata.
- code-comments remains definition-owned by Dev Coder and Dev Code Reviewer; java-comment is setup-detected for Java folder scopes so both contracts apply.
- Directly related ordinary scope: the two review checklists, detection metadata, focused detection/bundle/evaluation coverage, README, relevant design documentation, and generated technology registry/detector outputs.
- Supported mirrors must be regenerated from approved skill sources; generated files must not be hand-edited.
- UAR routing claim: route-java-comment-approval-019f86b4, acquired event 18214d2e-c045-4a60-b25f-808da470d053.

Creation Claim: create-java-comment-skill-019f86a3

## Summary

Add a java-comment skill that places Java file-level comment information in the first package or top-level class documentation comment instead of starting the file with a standalone header comment. Clarify that the generic code-comments header guidance is appropriate for most languages but yields to a language-specific comment practice when one applies.

## Context

The generic code-comments skill currently requires a language-appropriate header near the beginning of every created or materially changed code artifact. For Java, starting a source file with a standalone header comment is considered poor practice in this project. Information normally carried by the generic header belongs in the first package documentation comment or, when there is no applicable package comment, in the first top-level class documentation comment.

The language-specific skill must refine placement without discarding the generic requirements for the exact project copyright statement, truthful AI-assistance attribution, a concise responsibility summary, and supported design or test-plan references. Java source must not receive both a standalone header and duplicated metadata in package or class documentation.

Applicable repository rules make distributed skill definitions and their metadata governed canonical sources. The implementation owner must identify the exact governed source scope and obtain explicit, scope-specific user approval before mutation. This backlog request authorizes creation of the work item; it does not by itself authorize immediate skill-definition changes.

## Source Evidence

- On 2026-07-21, the user stated that it is bad practice in Java to start a file with a comment and directed that information normally placed in a header comment go into the first package or class comment instead.
- In the same request, the user directed creation of a new java-comment skill and required the generic comment skill to state that header comments are appropriate for most languages unless language-specific practice says otherwise.
- Current source evidence is in skills/code-comments/SKILL.md, skills/code-comments/references/review-checklist-code-comments.md, and skills/java/SKILL.md.

## Requirements

- Add a distributed skill whose canonical identifier and directory are java-comment.
- Define Java-specific comment placement so a Java source file does not begin with a standalone header comment solely to carry generic file-header information.
- Put the information required by code-comments into the first package documentation comment when one applies; otherwise put it into the first top-level class or other applicable top-level type documentation comment.
- Preserve valid Java and Javadoc structure, including package-info.java and source files without package declarations.
- Keep copyright, truthful AI-assistance attribution, responsibility summary, and supported design or test-plan references aligned with the generic code-comments contract.
- Prevent duplicate header information when a package or top-level type documentation comment carries the file-level information.
- Update code-comments to state that its near-beginning standalone header form is appropriate for most languages and that a language-specific comment skill may override placement while preserving the required information.
- Update the code-comments review checklist so review verifies both the general default and language-specific placement overrides.
- Add Java-specific review guidance or a review checklist owned by java-comment that checks package-or-type placement, Javadoc validity, completeness, and absence of duplicated standalone headers.
- Define how java-comment is selected whenever Java source is in scope while retaining code-comments as the generic comment contract.
- Update required skill metadata, catalog entries, technology detection or folder-routing sources, evaluation probes and cases, bundle tests, generated mirrors, README content, and relevant design documentation from their canonical sources.
- Sweep canonical sources and generated outputs for contradictory guidance that always requires a standalone header at the beginning of Java files.
- Before changing any governed skill definition or metadata, run the supported definition-change check with an approval record citing explicit, exact user approval for the identified source scope.
- Do not hand-edit generated/adapters, design/generated/role-definitions.js, or design/generated/skill-definitions.js.

## Acceptance Criteria

- Java work loads java-comment together with code-comments through the repository-supported technology-selection mechanism.
- java-comment directs agents to place generic file-level comment information in the first package documentation comment or, when that is not applicable, in the first top-level class or type documentation comment.
- A conforming Java source file does not contain an additional standalone header that duplicates the package or type documentation.
- code-comments clearly identifies its standalone near-beginning header guidance as the default for most languages and defers placement to applicable language-specific comment guidance.
- The exact project copyright statement and all other required generic header information remain present in the Java-specific location.
- package-info.java, ordinary packaged classes, and Java source without a package declaration have explicit positive examples or focused fixtures.
- Negative coverage rejects a Java file with a duplicate standalone header and rejects removal of required information under the language-specific override.
- Source skill names, directories, Codex metadata, catalogs, generated mirrors, README inventory, design documentation, and evaluation coverage agree on the java-comment identifier and behavior.
- Exact governed-definition approval evidence exists for every changed canonical skill or metadata source.
- Focused validation, generator freshness checks, Git diff validation, and independent review pass before direct-main completion.

## Dependencies

None. The exact governed source scope is approved in the Resolution above.

## Verification

- Run the governed-definition pre-mutation check for each approved canonical source before editing it.
- Validate skills/java-comment/SKILL.md, its review guidance, and Codex metadata with the repository-native skill validators.
- Run focused bundle tests for skill packaging, catalog membership, metadata, Java selection, and coexistence with code-comments.
- Add and run focused evaluation probes covering package documentation, top-level type documentation, package-info.java, no-package source, duplicate-header rejection, and preservation of required information.
- Run applicable generator commands and freshness checks only for supported mirrors of the approved canonical sources.
- Run scripts/openai_metadata.py for affected skills after skill name or description changes.
- Run git diff --check.
- Obtain an independent review of the exact canonical source and generated diff.

## Notes

- The requested identifier is java-comment, not java-comments.
- This item changes comment placement for Java; it does not remove the generic information requirements.
- Follow the lowest repository verification tier supported by the final affected surfaces. Adding a governed skill plus supported generated mirrors is expected to require Tier 2 verification unless implementation evidence justifies a different tier.
