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
5. Leave every owning generator runnable in the originating change. When adding a conceptual
   role, add its suite index, suite, and scenario declaration before completion. When adding
   a distributed skill, record its supported probe disposition and update exact inventory
   assertions that consume the catalog. Do not defer originating inventory drift to a later
   work item.
6. Run the documentation generator after any skill, category, or conceptual agent definition change.
7. Inspect generated Codex, Claude Code, Gemini CLI, and Junie CLI native agent definitions and confirm that unconditional core skills use by-reference delivery by default and remain fixed while conditional skills retain their conditions. Confirm explicit inline generation embeds the same fixed core skill bodies, every skill ID resolves to a bundled skill, and every model profile resolves through each supported adapter.
8. Update hand-authored policy in README.md and the design HTML pages when the operating model changes.
9. Do not pack a sequence or enumeration into a long paragraph. Treat three or more distinct steps or items in one paragraph as a list-structure trigger. Introduce the group with a short sentence, use a numbered list for ordered steps and a bulleted list for unordered items, and keep one coherent step or item in each entry.
10. Run stale-output checks, repository regression tests, Agent Skill validation, and git diff checks.
11. Keep maintenance repository-local. Do not populate user-home skill or agent folders to validate or use the bundle.

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
- Keep conceptual agent definition skillsets generic and technology-agnostic. Skill entries without conditions are definition-owned core skills; by-reference delivery is the default and explicit inline remains supported. Skill entries with conditions remain request-specific. Project Agent Setup detects technology and domain variants once, obtains user confirmation, records folder skillsets in PROJECT.yaml, and references them from AGENTS.md by default.
- Keep concise single-phase agent instructions as strings. Use the structured instruction mapping defined by the conceptual agent definition schema when an agent has state branches, delegation, review loops, failure handling, or several completion criteria.
- Require every conceptual agent definition to declare repositoryMutation as required, conditional, or never. Treat it as a capability declaration independent from resource coordination, and reject direct loading of a project-selected resource-coordination implementation from conceptual role skills.
- Keep each resource-coordination procedure in its selected skill. PROJECT.yaml selects none or one implementation project-wide, and generated AGENTS.md references that implementation only when enabled without reproducing its procedure.
- Treat agents/model-profiles.yaml as the semantic model source and adapters/[runtime]/model-profiles.yaml as runtime-owned model mappings. Keep provider model identifiers out of conceptual agent definitions.
- Treat design/generated and generated/adapters as derived outputs; regenerate them instead of editing them manually.
- Keep every conceptual agent definition skill entry to a real bundled skill ID.
- Keep customer-independent source and generated adapters free of customer material.
- Preserve stable skill and conceptual agent definition names unless the requested change explicitly includes a rename and reference sweep.
- Require explicit caller-supplied destinations for any separately requested deployment. Do not use deployment as a maintenance verification step.
- Do not silently replace customized customer installations. Use discrepancy analysis between the old generic, installed customer, and new generic definitions before updating them.
