# Project Configuration Routing Evaluation

Inspect the repository evidence and create exactly one PROJECT.yaml at the repository root. Then create root AGENTS.md plus the nested AGENTS.md files justified by the configuration.

PROJECT.yaml must record the project family, selected conceptual agent definitions, complete fixed and conditional skill metadata, representative folder evidence, technology skill loadouts, runtime availability, validation commands, nested guidance decisions, and the most-specific-pattern-wins rule. Use only project-relative evidence paths.

The API, web application, and automation folders have distinct runtime responsibilities. Do not infer a technology from a dependency that is not pertinent to a folder's source responsibility. Record NO_VARIANT with general model training when no pertinent specialized skill exists. Do not create nested PROJECT.yaml files or copy generic claim procedures into project guidance.

Use only the skills listed in available-skills.txt. Keep the evidence files unchanged. Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections.

Use the configured deterministic operations for runtime skill availability, technology detection, claims, YAML validation, and Markdown link verification. Use a documented fallback only when the corresponding operation is unavailable, not when it returns a valid structured outcome.

Load the project template only through one skill_resource_load call for development-methodology and assets/templates/project-template.yaml. Do not read that resource from the filesystem. Run technology detection once with the scopes services/api, apps/web, and automation in that order.

Acquire one claim with claim id, agent, task, and root task id all set to project-configuration-routing except that agent is project-configurator. Claim exactly PROJECT.yaml, AGENTS.md, services/api/AGENTS.md, apps/web/AGENTS.md, automation/AGENTS.md, and eval-result.md, in that order, with scope reason evaluation output ownership. Omit other optional claim inputs. Validate only PROJECT.yaml with verify_yaml. Validate AGENTS.md, services/api/AGENTS.md, apps/web/AGENTS.md, automation/AGENTS.md, and eval-result.md, in that order, with one verify_markdown_links call. Commit the outputs, then release the same claim without no-change mode.
