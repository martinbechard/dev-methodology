# Add Java Comment Placement Skill

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/add-java-comment-placement-skill.md

Completion: direct-main

## Current Execution

- Owner: Unowned
- Claim: None
- Canonical task: 019f77f4-c4bd-7c91-b197-c987a7beb838
- Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/java-validation-contract-20260722
- Branch: codex/java-comment-validation-contract-20260722
- Starting main: 6ffacb7dd9de75d351761577dff7d18ec9b36609; correction baseline: preserved recovery tip 90333e05922e712d1d4172ea067e52ae330eac13.
- Phase: Completed after accepted line-oriented validation, independent review and verification, direct-main integration, and focused post-main checks.
- Started: 2026-07-21; resumed with a fresh owner on 2026-07-22.
- Open issues: None. Structured skill_validate remained unavailable for linked worktrees because configured roots reject them; the repository-native validator passed on the primary checkout before and after integration.
- Accepted candidate: 9e4cf541d33146150ed2ba6ff0fd9f30bd911d5e on codex/java-comment-validation-contract-20260722, cumulatively preserving the approved Java feature and the accepted validation contract.

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

## Resumption Evidence

- Preserved pre-attempt state: main commit 4a4a6195231fa9cbe351627bf0c42fa586e07b6c, work-item blob a82d72cd1c38592506d4ecfe40164b9348e116c5, Status Blocked, Owner Unowned, Claim None.
- Resumption authority: On 2026-07-22, the user directed the parent task to carry out the recorded sequential recovery plan.
- Blocker reconciliation: The fresh recovery owner accepted the exact evaluator-only correction scope. The original exhausted task remains stopped; its blocker, evidence, candidate, and acceptance criteria are preserved above.
- Lifecycle transition: Blocked moved through Ready only for the serialized acquisition attempt, then to Running after the new exclusive claim succeeded.
- New ownership: java-comment-recovery-20260722, branch codex/java-comment-placement-recovery-20260722, worktree /Users/martinbechard/dev/dev-methodology/.worktrees/java-comment-recovery-20260722, baseline current main 4a4a6195231fa9cbe351627bf0c42fa586e07b6c.
- Recovery acceptance: Reject bare labels, blank sections, duplicate or malformed required headings, and missing affected-path or verification-result fields; accept complete evidence; then obtain fresh independent review and verification of the cumulative candidate.
- Running transition claim: resume-java-comment-backlog-20260722 acquired event 019b310d-6068-4f79-adbd-43aa7a9f77ac and releases immediately after this one-file commit.

## Second Recovery Blocked Handoff

- Preserved cumulative recovery: 55e49f1 replayed the approved Java feature candidate; cd13193 added real heading and scoped-field validation; dde1c4d rejected fenced pseudo-headings, malformed ATX headings, Windows paths, and URI paths; 90333e0 rejected HTML comments, comment-only values, and ordinary raw HTML tag blocks.
- Passing focused evidence: the Java bundle/evaluator contract test and Java technology-detection test passed; both changed skills and metadata validated; technology detection, skill documentation, hierarchy, and support-checklist freshness checks passed; Python compilation, Git diff, clean-worktree, and governed-byte identity checks passed. The three governed source blobs remain byte-identical to approved candidate 02cc7215.
- Decisive final review finding: standard Markdown raw-HTML forms beginning with CDATA, processing instructions, or an end-of-line tag opener such as `<pre` still hide all six pseudo-sections while validate_evidence returns no errors.
- Why execution stopped: the same hidden-Markdown-content acceptance criterion remained open after correction commits dde1c4d and 90333e0. Repository policy prohibits a third correction attempt in the same bounded loop.
- Exact unblock condition: start a fresh correction owner from 90333e0; replace the partial raw-text recognizer with one complete Markdown block model, or a fully enumerated CommonMark-compatible block parser, that excludes every fenced and raw-HTML block form before recognizing headings and fields. Add exact-diagnostic regressions for comments, CDATA, processing instructions, declarations, ordinary tag blocks including split-line openers, fenced blocks, malformed ATX headings, comment-only values, and non-repository paths. Then obtain fresh independent review and focused verification of the cumulative candidate.
- Preserved branch/worktree: codex/java-comment-placement-recovery-20260722 at 90333e05922e712d1d4172ea067e52ae330eac13 in /Users/martinbechard/dev/dev-methodology/.worktrees/java-comment-recovery-20260722; clean and intentionally retained for a fresh dispatch.
- Recovery implementation claim: java-comment-recovery-20260722 acquired event 27a73910-4a76-4c3b-84cb-8a1e9ef81656, heartbeat event 8609ac3a-4496-411d-ae49-772f01d72a1f, and released cleanly at event 74ec7ae4-b577-4ea3-9437-95f486b220e8.
- Backlog blocker transaction: block-java-comment-recovery-20260722 acquired event c0a060f4-fa7d-45e8-8d5c-677b11e0e678 and releases immediately after this one-file commit.

## Validation Contract Resolution

- User direction: HTML is content, not evidence-heading syntax, and may be the correct verification content. It must not be rejected merely because it is HTML. Fenced code may also remain as content; it is ignored only while locating structural heading tokens.
- Definition of good: the evaluator owns a small line-oriented evidence format rather than a complete rendered-Markdown, CommonMark, or HTML interpretation. The six exact `## NAME` lines delimit records outside fenced code. Each record contains exactly one non-empty `Affected path:` value and one non-empty `Verification result:` value. Affected paths use repository-relative POSIX syntax. Verification results may contain arbitrary non-empty text, including HTML. HTML is neither parsed nor globally rejected.
- Required regression evidence: passing complete plain-text records; passing HTML verification content; passing unrelated HTML and fenced content without treating either as an error; rejection of bare labels, headings only, missing or blank fields, duplicate exact headings, malformed required heading tokens, headings found only inside fenced code, and non-repository affected paths.
- Scope: only evals/projects/java-comment-placement/TASK.md, evals/projects/java-comment-placement/verify.py, and scripts/test_bundle_content.py. No governed definition or generated mirror changes are authorized or required by this correction.
- Resumption claim: resume-java-validation-contract-20260722 acquired event 217dc06f-70f7-4e2f-b641-ec9f3912f232 and releases immediately after this one-file Running commit.
- Implementation claim: java-validation-contract-20260722 acquired event 3cec62d4-0ec1-4847-8f4f-7c316168cb0b on codex/java-comment-validation-contract-20260722 from preserved recovery tip 90333e05922e712d1d4172ea067e52ae330eac13.

## Delivery Evidence

- Final definition of good: six exact line-oriented Markdown record delimiters outside fenced code; exactly one non-empty affected path and verification result per record; repository-relative POSIX affected paths; arbitrary non-empty verification content including HTML; no HTML parsing or renderer emulation.
- Focused regressions: complete plain-text and HTML-bearing records pass; HTML wrappers and supplementary fenced examples pass; fenced-only records, bare labels, headings only, missing, blank, duplicate, or malformed headings and fields, and Windows, URI, NUL, or HTML affected paths fail with exact diagnostics.
- Independent review: ACCEPT on 168100b after the user-defined boundary correction; ACCEPT on 9e4cf54 after adding malformed wrong-label and missing-colon cases. No material findings remain.
- Independent verification: VERIFIED-WARN on 9e4cf54. All candidate checks passed; the warning is limited to the structured linked-worktree skill validator rejecting paths outside configured roots. No bypass was used.
- Verification: focused Java bundle/evaluator and Java technology-detection tests pass; Python compilation passes; repository-native skill and metadata validation passes; technology detection, skill documentation, hierarchy, and support-checklist freshness checks pass; Git diff, clean status, exact correction scope, and approved governed-byte identity pass.
- Direct-main integration: accepted cumulative content was replayed from current main and committed as 22c1925ce89b72847e04fc6f52258ed6849d94ea. All 36 integrated paths were byte-identical to accepted candidate 9e4cf54 before commit, and focused post-main verification passed.
- Integration claim: integrate-java-comment-20260722 acquired event cab79b5d-4f47-4f81-8304-7517b47e7da6 and released cleanly at event 0c320fb6-d0ac-4f3f-b8ab-d014485fdd4f.
- Validation correction claim: java-validation-contract-20260722 acquired event 3cec62d4-0ec1-4847-8f4f-7c316168cb0b and released cleanly at event cf44abd6-78d0-414f-8fa8-2e0a3defa9da.
- Terminal backlog claim: complete-java-comment-20260722 acquired event 875d4310-70f3-415a-9085-57f73d7c4e09 and releases immediately after the archive commit.
- Completed: 2026-07-22.

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
