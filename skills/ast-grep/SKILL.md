---
type: Skill
name: ast-grep
description: Use when the agent needs structure-aware code search, AST pattern matching, syntax-aware refactor discovery, codemod planning, or rule authoring with ast-grep. Trigger for requests such as finding async functions without error handling, locating React components using a hook, finding calls inside specific constructs, searching for functions with too many parameters, or any code query where plain text search is too imprecise.
---

# ast-grep

Use ast-grep for syntax-aware code search and rule development. It matches code by parsed structure instead of raw text, so it is useful when a query depends on language constructs, nesting, arguments, function bodies, JSX, classes, imports, or control flow shape.

## Tool Roles

- Use ast-grep for structural code search and AST-aware matching.
- Use rg for fast plain-text search, file discovery, and simple literal or regex queries when it is available.
- Use grep only as a portability fallback when rg is unavailable.
- Do not replace rg with ast-grep for simple text search. Do not replace ast-grep with rg or grep when syntax and nesting matter.

Before using ast-grep in a new environment, verify the CLI is available:

```bash
ast-grep --version
```

If it is missing, tell the user it must be installed first. Common install options are:

```bash
brew install ast-grep
npm install -g @ast-grep/cli
cargo install ast-grep
```

## Workflow

1. Clarify the structural target.
   Identify the language, the construct to match, and any required context or exclusions. If the request is ambiguous and the wrong rule could mislead the user, ask a focused question.

2. Start with the smallest matching pattern.
   For simple code shapes, test ast-grep run with a pattern and language:

```bash
ast-grep run --pattern 'console.log($$$)' --lang javascript .
```

3. Use rule mode for relationships or logic.
   Use ast-grep scan with inline rules or a temporary rule file when the query needs inside, has, not, all, any, precedes, follows, or utility rules.

```bash
ast-grep scan --inline-rules 'id: console-in-class
language: javascript
rule:
  pattern: console.log($$$)
  inside:
    kind: method_definition
    stopBy: end' .
```

4. Test the rule on a tiny example before running it across the repository.
   Use standard input for quick checks:

```bash
echo 'class A { m() { console.log("x") } }' | ast-grep scan --inline-rules 'id: test
language: javascript
rule:
  pattern: console.log($$$)
  inside:
    kind: method_definition
    stopBy: end' --stdin
```

5. Debug failed rules structurally.
   Inspect how ast-grep parses the pattern or target snippet:

```bash
ast-grep run --pattern 'class A { m() { console.log("x") } }' --lang javascript --debug-query=cst
ast-grep run --pattern 'console.log($$$)' --lang javascript --debug-query=pattern
```

6. Run broadly only after the small example works.
   Prefer scoped paths when possible. Add JSON output when downstream processing or precise summaries are needed:

```bash
ast-grep scan --rule /tmp/find-pattern.yml --json src
```

## Rule Guidance

- Prefer pattern for direct single-node matches.
- Prefer kind plus has or inside for nested structural requirements.
- Add stopBy: end to relational rules unless there is a specific reason not to.
- Use all, any, and not for composite logic.
- Use $$$ for zero or more nodes, such as variable arguments or statements.
- When shell quoting is fragile, use single-quoted inline rules or a temporary YAML rule file.
- For complex syntax, read references/rule_reference.md before writing the final rule.

## Result Reporting

Report matches with file paths and line numbers. Include the rule or pattern when it helps the user verify the search. If no matches are found, say whether the rule was tested on an example and whether the absence of matches is likely meaningful or may reflect a rule limitation.
