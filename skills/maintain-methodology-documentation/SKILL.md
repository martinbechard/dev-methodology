---
name: maintain-methodology-documentation
description: Maintain the dev-methodology skill catalog, conceptual agent definitions, generated runtime adapters, generated HTML data, README, design pages, installers, and regression tests. Use when adding, renaming, deleting, or materially changing a distributed skill, conceptual agent definition, adapter, documentation category, or methodology design page.
metadata:
  category: documentation-methodology
---

# Maintain Methodology Documentation

Keep source files, generated outputs, documentation, installers, and tests aligned in one change.

## Workflow

1. Apply the project instructions already in context, then read README.md, the affected source skills and detection metadata, conceptual agent definition sources, source model profiles, adapter model mappings, and relevant design pages. Use agent-role-authoring whenever a conceptual definition or its schema changes.
2. Update sources under skills, technology detection metadata, agents/roles, and design/skill-categories.yaml before changing derived artifacts.
3. Run the metadata synchronizer after skill name or description changes.
4. Run the technology detection generator after specialized activation metadata changes.
5. Run the documentation generator after any skill, category, or conceptual agent definition change.
6. Inspect generated Codex, Claude Code, Gemini CLI, and Junie CLI native agent definitions and confirm that unconditional core skills are inlined by default, absent from native skills properties in that mode, and still available through native loading when inline-core-skills is false. Confirm request-specific skills retain human-readable conditions, every skill ID resolves to a bundled skill, and every model profile resolves through each supported adapter.
7. Update hand-authored policy in README.md and the design HTML pages when the operating model changes.
8. Run stale-output checks, repository regression tests, Agent Skill validation, and git diff checks.
9. Keep maintenance repository-local. Do not populate user-home skill or agent folders to validate or use the bundle.

## Deterministic Operations

When mcp-agent-ops is available, prefer skill_validate for changed skill packages, verify_yaml for changed YAML, and verify_markdown_links for Markdown link checks. These operations supplement the generators, repository regression suites, and git diff gate; they do not replace them.

Treat structured findings as valid failed gates. Fall back to the commands below only when the corresponding MCP tool is absent or the server cannot initialize or connect before request dispatch. Do not rerun a valid failed result through the fallback to seek a different outcome, and never bypass a path, root, authorization, input-policy, or other structured rejection.

After an explicitly requested deployment changes a configured installed skill root, call skill_refresh so a long-running server atomically publishes the new catalog revision. Source-only maintenance does not refresh a user installation.

## Commands

```bash
python3 scripts/openai_metadata.py skills
python3 scripts/build-technology-detection.py
python3 scripts/build-technology-detection.py --check
python3 scripts/build-skill-docs.py
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 scripts/validate-agent-skills.py skills
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
git diff --check
```

## Boundaries

- Treat skills, conceptual agent definition files, and the category catalog as sources.
- Treat detection.yaml beside each specialized technology or domain skill as the setup-time activation source and the generated registry as derived output.
- Keep conceptual agent definition skillsets generic. Skill entries without conditions are definition-owned core skills and are statically appended to generated agent instructions by default. Skill entries with conditions are request-specific and generate judgment-based dynamic loading instructions. Project Agent Setup detects technology and domain variants once, records unconditional folder skillsets in PROJECT.yaml, and statically embeds them in AGENTS.md by default.
- Keep concise single-phase agent instructions as strings. Use the structured instruction mapping defined by the conceptual agent definition schema when an agent has state branches, delegation, review loops, failure handling, or several completion criteria.
- Require every conceptual agent definition to declare repositoryMutation as required, conditional, or never. The generator validates that definitions requiring mutation load agent-claim as a definition-owned skill, conditional definitions load it conditionally, and read-only definitions do not load it.
- Keep generic claim behavior in agent-claim and conceptual agent definitions. PROJECT.yaml and AGENTS.md may contain source-backed project-specific coordination overrides, but must not reproduce the generic procedure.
- Treat agents/model-profiles.yaml as the semantic model source and adapters/[runtime]/model-profiles.yaml as runtime-owned model mappings. Keep provider model identifiers out of conceptual agent definitions.
- Treat design/generated and generated/adapters as derived outputs; regenerate them instead of editing them manually.
- Keep every conceptual agent definition skill entry to a real bundled skill ID.
- Keep customer-independent source and generated adapters free of customer material.
- Preserve stable skill and conceptual agent definition names unless the requested change explicitly includes a rename and reference sweep.
- Require explicit caller-supplied destinations for any separately requested deployment. Do not use deployment as a maintenance verification step.
- Do not silently replace customized customer installations. Use discrepancy analysis between the old generic, installed customer, and new generic definitions before updating them.
