---
name: detect-technology-skills
description: Detect specialized technology and domain skills from source-backed folder scopes during Project Agent Setup. Use when creating or updating PROJECT.yaml and unconditional AGENTS.md folder skillsets, or when technology boundaries change.
metadata:
  category: development-practice
---

# Detect Technology Skills

Run technology detection during project setup, not during ordinary coding, review, verification, or diagnosis.

## Workflow

1. Inventory project tiers, ownership boundaries, manifests, source roots, and tests.
2. Choose representative folders that do not combine unrelated sibling technologies.
3. Run the detect_technology_skills MCP tool once for those scopes when available; otherwise run the loaded scripts/detect.py fallback once.
4. Review source evidence, missing required skills, exclusive conflicts, and explicit no-variant results. Reject a candidate when its evidence proves only that a dependency exists in an owning manifest but not that the analyzed folder owns the behavior or verification workflow covered by that skill.
5. Record accepted skillsets and source evidence in PROJECT.yaml.
6. Compare every detected candidate with the technology skills actually exposed by the target runtime, not only with skills present in the methodology source tree.
7. Generate root or nested AGENTS.md sections with unconditional folder skill-loading instructions.
8. Verify every listed skill is installed and exposed to the agents that will work in that folder.
9. Rerun only when project setup, technology boundaries, or the runtime's available-skill catalog changes.

## Operation Selection

Use detect_technology_skills when mcp-agent-ops is available. Pass the absolute project root and the representative project-relative scopes. The server supplies its configured technology registry and complete active skill catalog, so do not reconstruct repeated available-skill arguments for the MCP call.

READY, BLOCKED, and explicit NO_VARIANT loadouts are valid detection results. Do not reinterpret BLOCKED or NO_VARIANT as a transport failure and do not retry them through the script. Use the fallback only when the MCP tool is absent or the server cannot initialize or connect before request dispatch. Never bypass a path, root, authorization, input-policy, or other structured rejection through the script.

## Fallback Command

```bash
python3 [detector-skill]/scripts/detect.py \
  --project-root [root] \
  --scope [folder] \
  --available-skill [runtime-exposed-skill-id]
```

Repeat the scope option for separately analyzed folders and repeat the available-skill option for the complete technology-skill catalog exposed by the target runtime. Keep each returned skillset separate. Use the skills-root option only when that directory is the target runtime's actual installed-skill catalog; do not rely on the methodology source-tree default as proof of runtime availability. The fallback remains authoritative when MCP is unavailable before dispatch, but it is not a second opinion on a valid MCP result or policy rejection.

## Evidence Model

- Each detection definition explicitly names the skill selected by its activation rule.
- Activation uses an anyOf root. Each branch may be one evidence predicate or an allOf clause whose predicates must all match.
- FileMatch binds a path glob and allowed extensions to the same file. Use it when a broad path name must not be satisfied by documentation or configuration files.
- OwningDependency and manifestFile read only the nearest owning project boundary.
- OwningContentPattern reads only files beside the nearest owning manifest. Use it for project-root markers that must not be satisfied by nested documentation or examples.
- SourceImport parses supported source code so comments and string examples do not count as imports.
- The detector records the concrete matches from every satisfied branch as source evidence.
- An owning-manifest match is candidate evidence, not automatic proof that every nested folder uses the matched technology. Confirm pertinence from that folder's source, configuration, test runner, or runtime responsibility before accepting the skill.

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
- Do not route a skill merely because it is installed, exposed, or detected. It must be pertinent to the folder's source-backed responsibility.
- Do not use the selected conceptual agent definition, task wording, prompt keywords, read confirmations, or optional local commands as inputs.
- Do not add generic definition-owned skills to detector metadata.
- Stop setup when a detected required skill is unavailable or equal-priority exclusive matches conflict.
- Preserve explicit no-variant results instead of inventing support. When no pertinent specialized skill exists for a source-backed scope, record `NO_VARIANT` and route that scope to general model training; do not skip the scope and do not report it as blocked.
- Distinguish `NO_VARIANT` from a detected required-but-unavailable skill. The former uses general model training; the latter remains `BLOCKED` until the required skill is available.
- Require one complete activation branch before selecting its named skill.
- Treat the bundled detector script as a generated mirror of the repository source script.
