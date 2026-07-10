---
name: maintain-methodology-documentation
description: Maintain the dev-methodology skill catalog, canonical agent roles, generated runtime adapters, generated HTML data, README, design pages, installers, and regression tests. Use when adding, renaming, deleting, or materially changing a distributed skill, canonical role, adapter, documentation category, or methodology design page.
metadata:
  category: documentation-methodology
---

# Maintain Methodology Documentation

Keep canonical sources, generated outputs, documentation, installers, and tests aligned in one change.

## Workflow

1. Read AGENTS.md, README.md, the affected source skills and routing metadata, canonical role files, canonical model profiles, adapter model mappings, and relevant design pages.
2. Update canonical sources under skills, skill routing metadata, agents/roles, and design/skill-categories.yaml before changing derived artifacts.
3. Run the metadata synchronizer after skill name or description changes.
4. Run the skill routing generator after activation metadata or generic role loadouts change.
5. Run the documentation generator after any skill, category, or canonical role change.
6. Inspect generated Codex and Claude agent definitions and confirm that canonical roles contain only generic fixed skills, every canonical skill ID resolves to a bundled skill, and every canonical model profile resolves through each supported adapter.
7. Update hand-authored policy in README.md and the design HTML pages when the operating model changes.
8. Run stale-output checks, repository regression tests, Agent Skill validation, and git diff checks.
9. Refresh shared skill installs only after source validation passes.

## Commands

```bash
python3 scripts/openai_metadata.py skills
python3 scripts/build-skill-routing.py
python3 scripts/build-skill-routing.py --check
python3 scripts/build-skill-docs.py
python3 scripts/build-skill-docs.py --check
python3 scripts/build-agent-skill-hierarchy.py --check
python3 scripts/build-support-checklist.py --check
python3 scripts/validate-agent-skills.py skills
python3 -m unittest discover scripts
PYTHONPATH=skills/project-wiki/scripts python3 -m unittest discover skills/project-wiki/scripts
python3 scripts/refresh-shared-skills.py
git diff --check
```

## Boundaries

- Treat skills, canonical role files, and the category catalog as sources.
- Treat routing.yaml beside each routed skill as the activation source and the generated registry as derived output.
- Keep canonical role loadouts generic. Resolve technology, framework, domain, and optional tool variants through route-technology-skills.
- Treat agents/model-profiles.yaml as the semantic model source and adapters/[runtime]/model-profiles.yaml as runtime-owned model mappings. Keep provider model identifiers out of canonical roles.
- Treat design/generated and generated/adapters as derived outputs; regenerate them instead of editing them manually.
- Keep every canonical role skill entry to a real bundled skill ID.
- Keep customer-independent source and generated adapters free of customer material.
- Preserve stable skill and role names unless the requested change explicitly includes a rename and reference sweep.
- Do not silently replace customized customer installations. Use discrepancy analysis between the old generic, installed customer, and new generic definitions before updating them.
