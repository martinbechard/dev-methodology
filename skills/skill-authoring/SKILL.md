---
name: skill-authoring
description: Create or review concise, portable Agent Skills with clear scope, progressive disclosure, harness-aware instruction boundaries, and verifiable workflows. Use when adding or materially changing a SKILL.md package, its references, scripts, assets, metadata, or methodology review rules for skills.
metadata:
  category: documentation-methodology
---

# Skill Authoring

Keep each skill focused on task-specific knowledge that the agent runtime does not already supply.

## Harness Boundary

- Treat applicable root and nested project instructions supplied by the harness as already loaded.
- Do not tell ordinary task agents to locate, open, read, reread, or follow AGENTS.md, CLAUDE.md, or equivalent harness-managed instruction files.
- Refer to applicable project instructions when policy precedence matters without adding a discovery or reading step.
- Inspect an instruction file explicitly only when the task creates, updates, validates, renders, or reviews that file as an artifact, or when the task investigates instruction-loading behavior.
- Read a task-relevant procedure or reference explicitly when the harness did not supply its contents and the skill needs that source to complete the work. Do not require blanket instruction-file scans.

## Authoring Workflow

1. Define the concrete task, trigger conditions, required inputs, outputs, and success evidence.
2. Separate task-specific expertise from harness behavior, project instructions, role behavior, and general model knowledge.
3. Remove setup steps that repeat automatically supplied context, permissions, tool descriptions, or runtime routing.
4. Keep the main workflow concise and move optional detail into directly referenced resources only when progressive disclosure reduces routine context.
5. Name every explicit dependency that the agent must load or execute because the harness does not provide it automatically.
6. Preserve legitimate instruction-file artifact work without presenting it as ordinary agent startup.
7. Validate the complete skill package and test any bundled scripts or deterministic workflows.

## Review Rules

Flag a skill when it:

- Directs an ordinary agent to rediscover or reread harness-loaded instruction files.
- Duplicates project policy, role behavior, tool instructions, or another skill instead of referencing the owning contract.
- Uses a blanket repository or instruction scan where task-specific evidence would suffice.
- Omits an explicit dependency that is not supplied automatically.
- Claims an instruction-file exception without actually creating, updating, validating, rendering, reviewing, or investigating that artifact.

Search the complete skill package for instruction-loading language before accepting it. Record the exact clause and whether it is redundant startup behavior, a legitimate artifact operation, or a required external dependency.

## Result

Return the skill changes or review findings, the harness-boundary decision, validation evidence, and any remaining dependency or portability risk.
