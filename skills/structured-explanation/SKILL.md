---
type: Skill
name: structured-explanation
description: |
  Use this skill when you need to explain reasoning in a structured way using
  QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER items. Use it to
  break a question into smaller questions, ground each answer in concrete
  facts, separate guesses from knowns, and keep the final answer easy to
  inspect.
version: 0.1.0
---

# Structured Explanation

Write structured markdown that explains an answer through nested questions and
supporting statements.

## When To Use

Use this skill when you need to:

- explain why code behaves a certain way
- trace the cause of a bug or design issue
- answer a technical question with explicit support
- separate known facts from guesses
- show what is still unknown

## Core Model

The format has six item types:

- `QUERY`
- `SUB-QUERY`
- `FACT`
- `HYPOTHESIS`
- `UNKNOWN`
- `ANSWER`

Use them in this order of thought:

1. State the main `QUERY`
2. Break it into `SUB-QUERY` items when needed
3. Support each sub-query with `FACT`, `HYPOTHESIS`, and `UNKNOWN` items
4. Close each sub-query with an `ANSWER`
5. End with an `ANSWER` to the main query

When the explanation needs to describe concrete system elements, use the
`structured-design` skill for that part of the explanation. Use it only when
the system elements are part of the explanation, not by default.

## Item Meanings

- `QUERY`
  - the top-level question being answered
- `SUB-QUERY`
  - one smaller question that helps answer the parent query
- `FACT`
  - something directly supported by code, files, logs, or other inputs
- `HYPOTHESIS`
  - a plausible explanation that is not yet proven
- `UNKNOWN`
  - a gap that is still unresolved
- `ANSWER`
  - the current best answer to the parent query or sub-query

## Structured-Design Interop

If the explanation needs to describe system structure, workflow, files,
modules, rules, or prompts, use the `structured-design` skill and its item
types such as:

- `ENTITY`
- `MODULE`
- `PROCESS`
- `FILE`
- `RULE`
- `PROMPT-MODULE`
- `PROMPT-PAIR`

Use them only as supporting structure inside a `SUB-QUERY` or `ANSWER`.

Do not replace the explanation model with a pure design document.

The rule is:

- use `QUERY` and `SUB-QUERY` to drive the explanation
- use `FACT`, `HYPOTHESIS`, and `UNKNOWN` to classify support
- use `ANSWER` to close reasoning
- use `structured-design` items only when the explanation needs to name or
  organize real system elements

## Required Discipline

- Use plain English, short sentences, and simple words.
- Keep the structure tight. Do not add extra item types.
- Make `FACT` items concrete. Cite files, logs, commands, or observed behavior.
- Do not present a `HYPOTHESIS` as if it were a `FACT`.
- Use `UNKNOWN` when the evidence is missing or incomplete.
- Each `ANSWER` must follow from the items directly under its parent query.
- If a point does not help answer a query, leave it out.
- Prefer one clear `SUB-QUERY` over a mixed paragraph.
- Use markdown by default.
- If you use `structured-design` items, keep them subordinate to the
  explanation structure.
- Do not let `ENTITY`, `MODULE`, `PROCESS`, or `RULE` displace the main
  `QUERY` / `SUB-QUERY` / `ANSWER` flow.

## Formatting

Write each item like this:

```markdown
**QUERY: Q-1**
- **SYNOPSIS:** Main question.

**SUB-QUERY: SQ-1**
- **SYNOPSIS:** Smaller question.

**FACT: F-1**
- **SYNOPSIS:** Supported statement.
- **FILE:** [runner.py](/path/to/runner.py:10)

**HYPOTHESIS: H-1**
- **SYNOPSIS:** Plausible but unproven explanation.

**UNKNOWN: U-1**
- **SYNOPSIS:** Missing information.

**ANSWER: A-1**
- **SYNOPSIS:** Best current answer.
```

## IDs

- Use stable IDs when review or cross-reference matters.
- Good defaults:
  - `Q-1`
  - `SQ-1`
  - `F-1`
  - `H-1`
  - `U-1`
  - `A-1`

## Good Output Shape

A good explanation should:

- start from a clear top-level query
- use sub-queries only when they help
- separate evidence from conjecture
- make unresolved gaps explicit
- end with a direct answer
- use `structured-design` items only where system structure needs to be named
  explicitly

## Do Not

- Do not use `CLAUSE` for sub-questions.
- Do not hide uncertainty inside a `FACT`.
- Do not collapse the whole explanation into prose paragraphs.
- Do not add conclusions that are not supported by the listed facts.
- Do not turn the whole explanation into a design doc unless the user asked
  for design rather than explanation.
