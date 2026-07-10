# Agent, Skill, Technology, And Test Coverage Checklist

This page is generated from the canonical roles, bundled skill frontmatter, technology classification, and evaluation cases. Regenerate it with scripts/build-support-checklist.py.

## Status Meaning

- [x] Structural means the item exists in the canonical catalog and is covered by repository validation or generation checks.
- [x] Live behavior means the item participated in a recorded live agent evaluation.
- [ ] Live behavior means no dedicated live evaluation currently proves that item.
- A passing structural check is not a substitute for a behavior evaluation.

## Summary

- [x] 22 canonical agents are defined and generate through the supported native role adapters.
- [x] 63 bundled skills pass catalog and Agent Skill validation.
- [x] 2 agents have direct live behavior evidence.
- [x] 10 skills have direct live behavior evidence.
- [x] TypeScript implementation, Java and Spring Boot implementation, SQL behavior, and TypeScript code review have live evaluation evidence.
- [ ] The remaining agents, skills, technologies, and harnesses need dedicated behavior evaluations as marked below.

## Harness Support

| Harness | Structural | Live behavior | Coverage |
| --- | --- | --- | --- |
| Generic Agent Skills | [x] | [ ] | Installer behavior is unit-tested; no native role format or live harness run. |
| Codex | [x] | [x] | Skill installation, native role generation, semantic model resolution, and live evaluations passed. |
| Claude Code | [x] | [ ] | Skill installation and native role generation are tested; no live behavior evaluation yet. |
| Gemini CLI | [x] | [ ] | Skill installation behavior is unit-tested; native role generation and live behavior are not covered. |
| JetBrains Junie CLI | [x] | [ ] | Destination and dry-run installation behavior are unit-tested; native role generation and live behavior are not covered. |

## Supported Technology Skills

| Technology | Skills | Structural | Direct live coverage |
| --- | --- | --- | --- |
| TypeScript and Node.js | typescript-coding, typescript-strict, typescript-esm, node-cli, jest, vitest | [x] | typescript-coding: typescript-order-pricing, typescript-code-review; typescript-strict: typescript-order-pricing, typescript-code-review; typescript-esm: typescript-order-pricing, typescript-code-review |
| Java and Spring Boot | java-coding, spring-boot | [x] | java-coding: spring-boot-order-cancellation; spring-boot: spring-boot-order-cancellation |
| SQL and PostgreSQL | sql-coding, postgres-drizzle | [x] | sql-coding: spring-boot-order-cancellation |
| React, Next.js, Vite, and Tailwind | nextjs-app-router, react-server-components, react-vite-renderer, tailwind-design-system | [x] | None |
| Electron | electron-main, electron-preload | [x] | None |
| Browser automation | playwright | [x] | None |
| HTTP APIs and authentication | api-routes, clerk-auth | [x] | None |
| Agent and model runtimes | harness-implementation, langgraph, local-model-integration, plan-engine-implementation, tool-runtime-implementation | [x] | None |

## Canonical Agent Checklist

| Agent | Profile | Structural | Live behavior | Evaluation evidence |
| --- | --- | --- | --- | --- |
| artifact-review-agent | advanced | [x] | [ ] | None |
| backlog-steward | default | [x] | [ ] | None |
| code-review-agent | advanced | [x] | [x] | typescript-code-review |
| coding-agent | advanced | [x] | [x] | typescript-order-pricing, spring-boot-order-cancellation |
| development-orchestrator | advanced-long | [x] | [ ] | None |
| documentation-writer | default | [x] | [ ] | None |
| e2e-browser-agent | advanced | [x] | [ ] | None |
| merge-coordinator | advanced | [x] | [ ] | None |
| methodology-artifact-reviewer | advanced | [x] | [ ] | None |
| methodology-maintainer | advanced | [x] | [ ] | None |
| project-agent-setup-agent | default | [x] | [ ] | None |
| project-bootstrap-agent | advanced-long | [x] | [ ] | None |
| project-organiser | default | [x] | [ ] | None |
| prompt-contract-reviewer | advanced | [x] | [ ] | None |
| public-source-collector | simple | [x] | [ ] | None |
| qa-and-verification-agent | advanced | [x] | [ ] | None |
| runtime-diagnostician | advanced | [x] | [ ] | None |
| security-reviewer | advanced | [x] | [ ] | None |
| shared-install-verifier | default | [x] | [ ] | None |
| ux-designer-or-reviewer | default | [x] | [ ] | None |
| wiki-ingest-agent | default | [x] | [ ] | None |
| wiki-query-agent | default | [x] | [ ] | None |

## Bundled Skill Checklist

### Wiki and knowledge skills

- [x] code-project-wiki — structural; [ ] Live behavior: no dedicated evaluation
- [x] project-wiki — structural; [ ] Live behavior: no dedicated evaluation
- [x] project-wiki-query — structural; [ ] Live behavior: no dedicated evaluation
- [x] project-wiki-research — structural; [ ] Live behavior: no dedicated evaluation
- [x] project-wiki-topic-verifier — structural; [ ] Live behavior: no dedicated evaluation
- [x] project-wiki-topic-writer — structural; [ ] Live behavior: no dedicated evaluation

### Documentation methodology skills

- [x] create-agents-plan — structural; [ ] Live behavior: no dedicated evaluation
- [x] development-methodology — structural; [ ] Live behavior: no dedicated evaluation
- [x] documentation-bootstrap — structural; [ ] Live behavior: no dedicated evaluation
- [x] documentation-page-verifier — structural; [ ] Live behavior: no dedicated evaluation
- [x] documentation-reverse-engineering — structural; [ ] Live behavior: no dedicated evaluation
- [x] maintain-methodology-documentation — structural; [ ] Live behavior: no dedicated evaluation

### Artifact creation skills

- [x] create-architecture — structural; [ ] Live behavior: no dedicated evaluation
- [x] create-functional-spec — structural; [ ] Live behavior: no dedicated evaluation
- [x] create-high-level-design — structural; [ ] Live behavior: no dedicated evaluation
- [x] create-module-design — structural; [ ] Live behavior: no dedicated evaluation
- [x] create-project-wiki — structural; [ ] Live behavior: no dedicated evaluation
- [x] create-unit-test-plan — structural; [ ] Live behavior: no dedicated evaluation

### Artifact review skills

- [x] review-architecture — structural; [ ] Live behavior: no dedicated evaluation
- [x] review-functional-spec — structural; [ ] Live behavior: no dedicated evaluation
- [x] review-high-level-design — structural; [ ] Live behavior: no dedicated evaluation
- [x] review-module-design — structural; [ ] Live behavior: no dedicated evaluation
- [x] review-project-wiki — structural; [ ] Live behavior: no dedicated evaluation
- [x] review-structured — structural; [x] Live behavior: typescript-code-review
- [x] review-unit-test-plan — structural; [ ] Live behavior: no dedicated evaluation

### Development practice skills

- [x] agent-claim — structural; [ ] Live behavior: no dedicated evaluation
- [x] agent-work-merge — structural; [ ] Live behavior: no dedicated evaluation
- [x] ast-grep — structural; [ ] Live behavior: no dedicated evaluation
- [x] careful-coding — structural; [x] Live behavior: typescript-order-pricing, spring-boot-order-cancellation, typescript-code-review
- [x] code-execution-tracing — structural; [ ] Live behavior: no dedicated evaluation
- [x] code-review-evidence — structural; [x] Live behavior: typescript-order-pricing, spring-boot-order-cancellation, typescript-code-review
- [x] create-backlog — structural; [ ] Live behavior: no dedicated evaluation
- [x] fix-explanation — structural; [ ] Live behavior: no dedicated evaluation
- [x] manage-backlog — structural; [ ] Live behavior: no dedicated evaluation
- [x] root-cause-analysis — structural; [ ] Live behavior: no dedicated evaluation
- [x] runtime-evidence-collection — structural; [ ] Live behavior: no dedicated evaluation
- [x] structured-design — structural; [ ] Live behavior: no dedicated evaluation
- [x] structured-explanation — structural; [ ] Live behavior: no dedicated evaluation
- [x] test-driven-development — structural; [x] Live behavior: typescript-order-pricing, spring-boot-order-cancellation

### Stack and domain skills

- [x] api-routes — structural; [ ] Live behavior: no dedicated evaluation
- [x] clerk-auth — structural; [ ] Live behavior: no dedicated evaluation
- [x] electron-main — structural; [ ] Live behavior: no dedicated evaluation
- [x] electron-preload — structural; [ ] Live behavior: no dedicated evaluation
- [x] harness-implementation — structural; [ ] Live behavior: no dedicated evaluation
- [x] java-coding — structural; [x] Live behavior: spring-boot-order-cancellation
- [x] jest — structural; [ ] Live behavior: no dedicated evaluation
- [x] langgraph — structural; [ ] Live behavior: no dedicated evaluation
- [x] local-model-integration — structural; [ ] Live behavior: no dedicated evaluation
- [x] nextjs-app-router — structural; [ ] Live behavior: no dedicated evaluation
- [x] node-cli — structural; [ ] Live behavior: no dedicated evaluation
- [x] plan-engine-implementation — structural; [ ] Live behavior: no dedicated evaluation
- [x] playwright — structural; [ ] Live behavior: no dedicated evaluation
- [x] postgres-drizzle — structural; [ ] Live behavior: no dedicated evaluation
- [x] react-server-components — structural; [ ] Live behavior: no dedicated evaluation
- [x] react-vite-renderer — structural; [ ] Live behavior: no dedicated evaluation
- [x] spring-boot — structural; [x] Live behavior: spring-boot-order-cancellation
- [x] sql-coding — structural; [x] Live behavior: spring-boot-order-cancellation
- [x] tailwind-design-system — structural; [ ] Live behavior: no dedicated evaluation
- [x] tool-runtime-implementation — structural; [ ] Live behavior: no dedicated evaluation
- [x] typescript-coding — structural; [x] Live behavior: typescript-order-pricing, typescript-code-review
- [x] typescript-esm — structural; [x] Live behavior: typescript-order-pricing, typescript-code-review
- [x] typescript-strict — structural; [x] Live behavior: typescript-order-pricing, typescript-code-review
- [x] vitest — structural; [ ] Live behavior: no dedicated evaluation

## Recorded Live Evaluations

- [x] TypeScript order pricing: Coding Agent implementation, eight passing tests, build, coding checklist evidence, and review synthesis.
- [x] Spring Boot order cancellation: Coding Agent implementation, ten passing tests, HTTP, transaction, persisted-state, and conditional SQL evidence.
- [x] TypeScript code review: read-only Code Review Agent found the unawaited lookup, swallowed provider failure, and missing percentage validation in a deliberately defective change.
- [x] Codex model mapping: the live review exposed the rejected friendly alias and passed after generation switched to the concrete gpt-5.6-luna identifier.

## Repository Verification Layers

- [x] Agent Skill format validation for every bundled skill.
- [x] Canonical role schema, skill reference, model profile, and adapter completeness tests.
- [x] Codex TOML and Claude Code Markdown native role generation checks.
- [x] Generic, Codex, Gemini CLI, Claude Code, and Junie CLI installer behavior tests.
- [x] Generated documentation and agent-skill hierarchy freshness checks.
- [x] Shared installation refresh exercised for Agents, Codex, and Claude destinations.
- [x] Evaluation fixture runner verifies expected passing and intentionally failing behavior.
