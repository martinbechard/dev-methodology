---
name: maintain-methodology-documentation
description: Maintain the dev-methodology skill catalog, agent roles, generated runtime adapters, generated HTML data, README, design pages, installers, and regression tests. Use when adding, renaming, deleting, or materially changing a distributed skill, role, adapter, documentation category, or methodology design page.
metadata:
  category: documentation-methodology
---

# Maintain Methodology Documentation

Keep source files, generated outputs, documentation, installers, and tests aligned in one change.

## Workflow

1. Apply the project instructions already in context, then read README.md, the affected source skills and detection metadata, source role files, source model profiles, adapter model mappings, and relevant design pages. Use agent-role-authoring whenever a role or role schema changes.
2. Update sources under skills, technology detection metadata, agents/roles, and design/skill-categories.yaml before changing derived artifacts.
3. Run the metadata synchronizer after skill name or description changes.
4. Run the technology detection generator after specialized activation metadata changes.
5. Run the documentation generator after any skill, category, or role change.
6. Inspect generated Codex and Claude agent definitions and confirm that roles distinguish generic fixed skills from request-specific skills with human-readable conditions, every skill ID resolves to a bundled skill, and every model profile resolves through each supported adapter.
7. Update hand-authored policy in README.md and the design HTML pages when the operating model changes.
8. Run stale-output checks, repository regression tests, Agent Skill validation, and git diff checks.
9. Keep maintenance repository-local. Do not populate user-home skill or agent folders to validate or use the bundle.

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

- Treat skills, role files, and the category catalog as sources.
- Treat detection.yaml beside each specialized technology or domain skill as the setup-time activation source and the generated registry as derived output.
- Keep role skillsets generic. Skill entries without conditions are fixed role skills. Skill entries with conditions are request-specific and generate judgment-based loading instructions. Project Agent Setup detects technology and domain variants once and records unconditional folder skillsets in PROJECT.yaml and AGENTS.md.
- Keep concise single-phase role instructions as strings. Use the structured instruction mapping defined by the role schema when a role has state branches, delegation, review loops, failure handling, or several completion criteria.
- Require every role to declare repositoryMutation as required, conditional, or never. The role generator validates that required roles load agent-claim as a fixed skill, conditional roles load it conditionally, and read-only roles do not load it.
- Keep generic claim behavior in agent-claim and roles. PROJECT.yaml and AGENTS.md may contain source-backed project-specific coordination overrides, but must not reproduce the generic procedure.
- Treat agents/model-profiles.yaml as the semantic model source and adapters/[runtime]/model-profiles.yaml as runtime-owned model mappings. Keep provider model identifiers out of roles.
- Treat design/generated and generated/adapters as derived outputs; regenerate them instead of editing them manually.
- Keep every role skill entry to a real bundled skill ID.
- Keep customer-independent source and generated adapters free of customer material.
- Preserve stable skill and role names unless the requested change explicitly includes a rename and reference sweep.
- Require explicit caller-supplied destinations for any separately requested deployment. Do not use deployment as a maintenance verification step.
- Do not silently replace customized customer installations. Use discrepancy analysis between the old generic, installed customer, and new generic definitions before updating them.
