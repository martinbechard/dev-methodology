# Project Configuration Routing Evaluation

Inspect the repository evidence and create exactly one PROJECT.yaml at the repository root. Then create root AGENTS.md plus the nested AGENTS.md files justified by the configuration.

PROJECT.yaml must record the project family, selected conceptual agent definitions, complete fixed and conditional skill metadata, representative folder evidence, technology skill loadouts, runtime availability, validation commands, nested guidance decisions, and the most-specific-pattern-wins rule. Use only project-relative evidence paths.

The API, web application, and automation folders have distinct runtime responsibilities. Do not infer a technology from a dependency that is not pertinent to a folder's source responsibility. Record NO_VARIANT with general model training when no pertinent specialized skill exists. Do not create nested PROJECT.yaml files or copy generic claim procedures into project guidance.

Use only the skills listed in available-skills.txt. Keep the evidence files unchanged. Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections.

Use the configured deterministic operations for runtime skill availability, technology detection, claims, YAML validation, and Markdown link verification. Use a documented fallback only when the corresponding operation is unavailable, not when it returns a valid structured outcome.

List runtime skill availability exactly once. The skill-authoring and maintain-methodology-documentation instructions are deliberately absent from the harness-preloaded context. Load both together with exactly one skill_load call, in that order, and do not read either package from the filesystem.

Load the project template only through one skill_resource_load call for development-methodology and assets/templates/project-template.yaml. Do not read that resource from the filesystem. Then validate the complete staged MCP skill root with exactly one skill_validate call. Pass the absolute current-workspace path ending in .eval-context/mcp-agent-ops/skills. Refresh the catalog with exactly one skill_refresh call after validation. Finally, run technology detection once with the scopes services/api, apps/web, and automation in that order. Do not repeat any of these operations.

Acquire one claim with claim id, agent, task, and root task id all set to project-configuration-routing except that agent is project-configurator. Claim exactly PROJECT.yaml, AGENTS.md, services/api/AGENTS.md, apps/web/AGENTS.md, automation/AGENTS.md, and eval-result.md, in that order, with scope reason evaluation output ownership. Omit other optional claim inputs. Read claim status exactly once after acquisition. Extend the same claim exactly once with mcp-operation-evidence.md, then refresh its heartbeat exactly once. Create mcp-operation-evidence.md with the six evidence labels MCP-SKILL-LOAD, MCP-SKILL-VALIDATION, MCP-SKILL-REFRESH, MCP-CLAIM-STATUS, MCP-CLAIM-EXTENSION, and MCP-CLAIM-HEARTBEAT. Validate only PROJECT.yaml with verify_yaml. Validate AGENTS.md, services/api/AGENTS.md, apps/web/AGENTS.md, automation/AGENTS.md, eval-result.md, and mcp-operation-evidence.md, in that order, with one verify_markdown_links call. Commit all outputs, then release the same claim without no-change mode.
