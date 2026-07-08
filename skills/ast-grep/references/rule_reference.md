# ast-grep Rule Reference

Use this reference when a structural search needs more than a simple pattern.

## Rule Types

Atomic rules match the current AST node:

- pattern matches code shape with metavariables.
- kind matches a tree-sitter node kind, such as call_expression or function_declaration.
- regex matches the text of the current node.
- nthChild matches a node by position among siblings.
- range matches by source location.

Relational rules match by AST relationship:

- inside requires the target node to be inside a matching ancestor.
- has requires the target node to contain a matching descendant.
- precedes requires the target node to appear before another matching node.
- follows requires the target node to appear after another matching node.

Composite rules combine other rules:

- all requires every sub-rule to match.
- any requires at least one sub-rule to match.
- not excludes a sub-rule.
- matches invokes a reusable utility rule by id.

At least one positive rule such as pattern or kind is needed. When metavariables from earlier matches matter, use all so rule order is explicit.

## Relational Rules

Use stopBy: end for deep searches unless a narrower boundary is intentional.

```yaml
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
    stopBy: end
```

Without stopBy: end, ast-grep may stop too early and miss nested matches.

Use field when only a specific child field should be searched:

```yaml
rule:
  kind: binary_expression
  has:
    field: operator
    pattern: $$OP
```

## Metavariables

$VAR captures one named AST node.

$$VAR captures one unnamed node, such as an operator or punctuation.

$$$VAR captures zero or more nodes. It is useful for argument lists, statement lists, JSX children, and function bodies.

$_ is a non-capturing metavariable. It can match different content each time and is useful when the value does not need to be reported or reused.

Metavariables must occupy a complete syntax node. Patterns such as obj.on$EVENT or "Hello $WORLD" do not work because the metavariable is embedded inside a larger token.

## Common Patterns

Find calls:

```yaml
rule:
  pattern: console.log($$$)
```

Find a function containing await:

```yaml
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
    stopBy: end
```

Find a call inside a method:

```yaml
rule:
  pattern: console.log($$$)
  inside:
    kind: method_definition
    stopBy: end
```

Find async functions using await without try-catch:

```yaml
rule:
  all:
    - kind: function_declaration
    - has:
        pattern: await $EXPR
        stopBy: end
    - not:
        has:
          pattern: try { $$$ } catch ($E) { $$$ }
          stopBy: end
```

Find alternatives:

```yaml
rule:
  any:
    - pattern: console.log($$$)
    - pattern: console.warn($$$)
    - pattern: console.error($$$)
```

## Debugging

If a rule does not match:

1. Replace the rule with the simplest pattern that might match.
2. Add one condition at a time.
3. Inspect the parsed query or target snippet.

```bash
ast-grep run --pattern 'function f() { return 1 }' --lang javascript --debug-query=cst
ast-grep run --pattern 'function $NAME($$$ARGS) { $$$BODY }' --lang javascript --debug-query=pattern
```

4. Check node kinds in the debug output.
5. Add stopBy: end to relational rules.
6. If shell quoting becomes noisy, move the rule into a temporary YAML file and run ast-grep scan with --rule.
