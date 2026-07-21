# Add Java Comment Placement Skill

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-java-comment-placement-skill.md

Completion: direct-main

## Current Execution

- Owner: Dev Orchestrator
- Claim: None; private discovery and implementation do not require shared repository ownership.
- Canonical task: 019f86b4-9e20-76a1-b5cb-7618fce32e28
- Worktree: /Users/martinbechard/.codex/worktrees/2682/dev-methodology
- Branch: codex/add-java-comment-placement-skill
- Starting main: 3539bf0445ccb9359b8403b5ef5af6558a85f4d3
- Phase: Perform bounded source and routing discovery, determine the smallest exact governed-definition manifest, and route one consolidated approval question before governed mutation; if authorized, continue through focused implementation, independent review, verification, integration, and separate completion.
- Started: 2026-07-21
- Running-record claim: start-java-comment-placement-019f86b4, acquired event e78cc5c5-74bf-443f-9b79-23011788d47a.
- Open issues: Exact governed-definition scope and path-specific approval remain to be established by bounded discovery.
- Accepted candidate: Pending.

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

- Explicit, scope-specific user approval for the governed java-comment and code-comments definition and metadata sources identified during implementation discovery.

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
