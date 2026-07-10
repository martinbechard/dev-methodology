---
name: code-comments
description: Write and review comments in source code, tests, scripts, migrations, and other executable code artifacts, including mandatory file headers and public API documentation. Use when creating or changing code artifacts, documenting public functions or constructs, or reviewing whether comments and implementation agree.
metadata:
  category: development-practice
---

# Code Comments

Treat comments as part of the code contract. Keep them concise, structured, and synchronized with behavior.

## Scope

- Apply this skill to human-maintained source code, test code, executable scripts, and executable schema or migration code.
- Do not require code headers in configuration, documentation, data, lock, manifest, or other non-code files, even when their format permits comments.
- For generated code, update the generator or template rather than hand-editing generated output. Follow the repository's generated-file policy.
- Preserve required interpreter directives, encoding declarations, and other syntax that must precede a comment header.

## Structured Comment Writing

Before writing or materially revising a non-trivial header or public-construct comment block, load structured-explanation.

- Use its discipline to identify the question being answered, concrete facts, unresolved uncertainty, and the direct answer.
- Translate that reasoning into concise language-native comment prose.
- Do not copy QUERY, FACT, UNKNOWN, or ANSWER labels into code unless the repository explicitly requires them.
- Leave out background that does not help a maintainer use, change, or review the code.

## Mandatory Code Artifact Header

Every human-maintained code artifact created or materially changed must have a language-appropriate header near the beginning of the file. Include:

- The exact copyright statement defined by the applicable root, nearest, or global AGENTS.md. Do not invent a holder, address, or year when the instruction is absent or ambiguous.
- An accurate AI attribution. Use the repository's wording when defined. Otherwise use AI attribution: Generated with AI assistance. for a new AI-authored file and AI attribution: Modified with AI assistance. for an existing human-origin file changed by AI. Preserve an existing generated-with-AI attribution on later changes.
- A one-sentence summary of the file's responsibility.
- A durable path to the governing design document when one exists and applies.
- A durable path to the governing test plan when one exists and applies.

Do not add a witty remark. Do not fabricate design or test-plan references. Update the summary and references when the file's responsibility or authority changes.

## Public Construct Documentation

Precede every public or exported construct with the language's standard documentation comment form. This includes public functions, methods, classes, interfaces, types, enums, modules, constants, and other constructs that callers are expected to use.

For a public function or method, document:

- Why the function exists and the responsibility it owns.
- Its intended callers or usage when that is not evident from the public boundary.
- Each parameter's meaning and valid values, including relevant ranges, units, defaults, sentinel values, nullability, or allowed combinations that the type alone does not express.
- The returned result and meaningful result variants when applicable.
- Observable side effects, mutations, I/O, state transitions, callbacks, emitted events, or external calls.
- Failures, thrown errors, cancellation, retry, concurrency, or lifecycle behavior that callers must handle.

For other public constructs, document why the construct exists, its intended usage, its invariants or valid states, and any lifecycle or ownership constraints. Do not merely restate the declaration or duplicate type information that is already explicit.

## Local Rationale Comments

- Explain why: rationale, business rules, invariants, constraints, compatibility requirements, and non-obvious workarounds.
- Prefer names, types, and direct control flow that make routine behavior understandable without commentary.
- Comment complex algorithms only where the reasoning or constraint is not evident from the implementation.
- Keep routine tests self-explanatory through names and arrangement. Comment non-obvious timing, setup, assertions, or domain constraints.
- Explain why a non-obvious integration boundary is mocked or replaced.
- Keep suppression comments narrow. Name the suppressed rule, the reason, the scope, and the condition for removal when it is temporary.
- Use TODO or FIXME comments only when repository policy permits them and the comment names a concrete action plus durable tracking or ownership. Do not use them as an untracked backlog.
- Remove commented-out code. Use version control for history.

## Change Workflow

1. Read the root and nearest AGENTS.md, the applicable language or framework skills, and any governing design or test plan.
2. Decide whether each changed file is a code artifact and determine its language-native header and documentation syntax.
3. Load structured-explanation before writing non-trivial header or public-construct comment blocks.
4. Add or update the header, public documentation, and local rationale together with the behavior change.
5. Verify parameter handling, side effects, errors, callers, tests, and implementation behavior against the documented intent.
6. Remove or correct comments made false, redundant, or obsolete by the current change without rewriting unrelated commentary.

When implementation and comments conflict, identify the authoritative intent from project guidance, design, tests, and callers. Do not silently rewrite the comment to excuse incorrect code or change code merely to preserve an obsolete comment.

## Review Evidence

Read references/review-checklist-code-comments.md during code review. Treat public documentation as a claimed contract and verify the implementation against it. Report missing or contradictory comments when they create correctness, usage, compliance, or maintainability risk rather than as style-only findings.
