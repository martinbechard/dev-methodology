---
name: route-technology-skills
description: Resolve specialized skills for a role and file scope from project bindings and machine-readable activation evidence. Use before coding, code review, verification, diagnosis, security review, user-experience review, prompt review, or source-backed technical documentation when the applicable specialized guidance must be selected and its availability verified.
metadata:
  category: development-practice
---

# Route Technology Skills

Resolve specialized guidance from repository facts instead of prompt keywords.

## Workflow

1. Read the root and nearest AGENTS.md plus AGENTS-PLAN.yaml when present.
2. Identify the role and the exact files or folders in scope.
3. Run scripts/resolve.py with the role, project root, and scope paths.
4. Treat project bindings as required only when they include activation evidence; block stale bindings that contradict live scoped evidence.
5. Read every resolved SKILL.md completely before acting.
6. Record the routing receipt in the work evidence, including resolved, unavailable, conflicting, and unmatched capabilities.
7. Stop when a required project-bound skill is unavailable. Do not silently replace it with model knowledge.
8. When no bundled variant exists, use the generic role guidance and label specialized guidance as unavailable rather than claiming it was loaded.

During project setup, populate source-backed skill_loadouts and folder_routing in AGENTS-PLAN.yaml, then run scripts/render_agents_routing.py to produce the operational AGENTS.md routing section.

## Command

```bash
python3 [router-skill]/scripts/resolve.py --project-root [root] --role [role] --scope [path] --format markdown
```

Repeat --scope for multi-file or multi-tier work. Pass --agents-plan when the plan is not at the project root.

```bash
python3 [router-skill]/scripts/render_agents_routing.py --agents-plan AGENTS-PLAN.yaml
```

## Routing Receipt

Report:

- Role and scope paths.
- Project bindings that applied.
- Repository evidence that activated each specialized skill.
- Skill source path, availability, and content digest.
- Confirmation that each resolved SKILL.md was read.
- Missing required skills and conflicts.
- Capabilities without a bundled specialized variant.

The resolver proves deterministic selection and file availability. A harness or evaluation must use tool-call evidence to prove that the agent actually read the selected files.

## Boundaries

- Do not use prompt wording as the primary activation signal.
- Treat prompt keywords as advisory discovery hints only; they never select a skill.
- Do not load every registered skill as a precaution.
- Do not treat a skill mentioned in a prompt or result as proof that it loaded.
- Do not mark a routing failure as a successful fallback.
- Keep project-specific bindings in AGENTS-PLAN.yaml and AGENTS.md. Keep reusable activation rules with their owning specialized skills.
