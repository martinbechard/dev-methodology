---
name: detect-technology-skills
description: Detect specialized technology and domain skills from source-backed folder scopes during Project Agent Setup. Use when creating or updating PROJECT.yaml and unconditional AGENTS.md folder skill loadouts, or when technology boundaries change.
metadata:
  category: development-practice
---

# Detect Technology Skills

Run technology detection during project setup, not during ordinary coding, review, verification, or diagnosis.

## Workflow

1. Inventory project tiers, ownership boundaries, manifests, source roots, and tests.
2. Choose representative folders that do not combine unrelated sibling technologies.
3. Run scripts/detect.py once for those scopes.
4. Review source evidence, missing required skills, exclusive conflicts, and explicit no-variant results.
5. Record accepted loadouts and source evidence in PROJECT.yaml.
6. Generate root or nested AGENTS.md sections with unconditional folder skill-loading instructions.
7. Verify every listed skill is installed.
8. Rerun only when project setup or technology boundaries change.

## Command

```bash
python3 [detector-skill]/scripts/detect.py --project-root [root] --scope [folder]
```

Repeat the scope option for separately analyzed folders. Keep each returned loadout separate.

## Evidence Model

- Each detection definition explicitly names the skill selected by its activation rule.
- Activation uses an anyOf root. Each branch may be one evidence predicate or an allOf clause whose predicates must all match.
- FileMatch binds a path glob and allowed extensions to the same file. Use it when a broad path name must not be satisfied by documentation or configuration files.
- OwningDependency and manifestFile read only the nearest owning project boundary.
- SourceImport parses supported source code so comments and string examples do not count as imports.
- The detector records the concrete matches from every satisfied branch as source evidence.

Example:

```yaml
skill: fastapi
activation:
  anyOf:
    - allOf:
        - fileExtension: .py
        - owningDependency: fastapi
    - sourceImport:
        module: fastapi
        extensions:
          - .py
```

## Boundaries

- Detect only technology and domain skills with machine-readable detection metadata.
- Do not use agent role, task wording, prompt keywords, read confirmations, or optional local commands as inputs.
- Do not add generic fixed-role skills to detector metadata.
- Stop setup when a detected required skill is unavailable or equal-priority exclusive matches conflict.
- Preserve explicit no-variant results instead of inventing support.
- Require one complete activation branch before selecting its named skill.
- Treat the bundled detector script as a generated mirror of the repository source script.
