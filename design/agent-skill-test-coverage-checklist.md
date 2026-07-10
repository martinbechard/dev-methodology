# Agent, Skill, Technology, And Test Coverage Checklist

This page is generated from the canonical roles, bundled skill frontmatter, setup-time technology detection registry, declared evaluation cases, and verified evidence receipts. Regenerate it with scripts/build-support-checklist.py.

## Status Meaning

- [x] Structural means the item exists in the canonical catalog and is covered by repository validation or generation checks.
- Declared means an evaluation case names the item. Declaration does not prove invocation or behavior.
- Manual means a human-observed run exists without a complete machine-verifiable invocation and skill-read receipt.
- [x] Verified behavior requires captured agent identity, concrete model, skill content digests, skill-read tool evidence, deterministic assertions, and an independent verdict.
- [ ] Verified behavior means that proof is absent.
- A passing structural check is not a substitute for a behavior evaluation.

## Summary

- [x] 22 canonical agents are defined and generate through the supported native role adapters.
- [x] 72 bundled skills pass catalog and Agent Skill validation.
- [x] 2 agents and 10 skills are named in current evaluation cases.
- [ ] 0 agents and 0 skills have independently verified behavior evidence under the current proof contract.
- TypeScript implementation, Java and Spring Boot implementation, SQL behavior, and TypeScript code review have useful manual observations that must be rerun with truthful receipts.

## Harness Support

| Harness | Structural | Manual run | Verified behavior | Coverage |
| --- | --- | --- | --- | --- |
| Generic Agent Skills | [x] | [ ] | [ ] | Installer behavior is unit-tested; no native role format or captured behavior evidence. |
| Codex | [x] | [x] | [ ] | Native generation and manual runs exist; current evidence lacks machine-verifiable load and invocation receipts. |
| Claude Code | [x] | [ ] | [ ] | Skill installation and native role generation are tested; no captured behavior evidence. |
| Gemini CLI | [x] | [ ] | [ ] | Skill installation behavior is unit-tested; native role generation and behavior are not covered. |
| JetBrains Junie CLI | [x] | [ ] | [ ] | Destination and dry-run installation behavior are unit-tested; native role generation and behavior are not covered. |

## Technology Detection Registry

| Skill | Kind | Label | Capabilities | Declared cases | Verified behavior |
| --- | --- | --- | --- | --- | --- |
| api-routes | technology | Application route handlers | http-api | None | [ ] None |
| clerk-auth | technology | Clerk identity integration | identity-provider | None | [ ] None |
| electron-main | technology | Electron main process | desktop-main-runtime | None | [ ] None |
| electron-preload | technology | Electron preload boundary | desktop-preload-boundary | None | [ ] None |
| fastapi | technology | FastAPI | web-application-framework | None | [ ] None |
| harness-implementation | domain | Agent harness implementation | agent-harness-runtime | None | [ ] None |
| java-coding | technology | Java | language-coding | spring-boot-order-cancellation | [ ] None |
| jest | technology | Jest | test-framework | None | [ ] None |
| langgraph | technology | LangGraph | workflow-runtime | None | [ ] None |
| local-model-integration | domain | Local model integration | local-model-runtime | None | [ ] None |
| nextjs-app-router | technology | Next.js App Router | web-application-framework | None | [ ] None |
| node-cli | technology | Node command line application | command-line-runtime | None | [ ] None |
| plan-engine-implementation | domain | Plan engine implementation | planning-runtime | None | [ ] None |
| playwright | technology | Playwright | end-to-end-framework | None | [ ] None |
| postgres-drizzle | technology | PostgreSQL with Drizzle | persistence-framework | None | [ ] None |
| python-coding | technology | Python | language-coding | None | [ ] None |
| react-server-components | technology | React Server Components | server-user-interface | None | [ ] None |
| react-vite-renderer | technology | React renderer with Vite | client-user-interface | None | [ ] None |
| spring-boot | technology | Spring Boot | application-framework | spring-boot-order-cancellation | [ ] None |
| sql-coding | technology | SQL | query-language | spring-boot-order-cancellation | [ ] None |
| tailwind-design-system | technology | Tailwind design system | styling-system | None | [ ] None |
| tool-runtime-implementation | domain | Tool runtime implementation | tool-runtime | None | [ ] None |
| typescript-coding | technology | TypeScript | language-coding | typescript-order-pricing, typescript-code-review | [ ] None |
| typescript-esm | technology | TypeScript ECMAScript modules | module-system | typescript-order-pricing, typescript-code-review | [ ] None |
| typescript-strict | technology | Strict TypeScript | strict-type-system | typescript-order-pricing, typescript-code-review | [ ] None |
| vitest | technology | Vitest | test-framework | None | [ ] None |

## Canonical Agent Checklist

| Agent | Profile | Structural | Declared cases | Verified behavior | Verified evidence |
| --- | --- | --- | --- | --- | --- |
| artifact-review-agent | advanced | [x] | None | [ ] | None |
| backlog-steward | default | [x] | None | [ ] | None |
| code-review-agent | advanced | [x] | typescript-code-review | [ ] | None |
| coding-agent | advanced | [x] | typescript-order-pricing, spring-boot-order-cancellation | [ ] | None |
| development-orchestrator | advanced-long | [x] | None | [ ] | None |
| documentation-writer | default | [x] | None | [ ] | None |
| e2e-browser-agent | advanced | [x] | None | [ ] | None |
| merge-coordinator | advanced | [x] | None | [ ] | None |
| methodology-artifact-reviewer | advanced | [x] | None | [ ] | None |
| methodology-maintainer | advanced | [x] | None | [ ] | None |
| project-agent-setup-agent | default | [x] | None | [ ] | None |
| project-bootstrap-agent | advanced-long | [x] | None | [ ] | None |
| project-organiser | default | [x] | None | [ ] | None |
| prompt-contract-reviewer | advanced | [x] | None | [ ] | None |
| public-source-collector | simple | [x] | None | [ ] | None |
| qa-and-verification-agent | advanced | [x] | None | [ ] | None |
| runtime-diagnostician | advanced | [x] | None | [ ] | None |
| security-reviewer | advanced | [x] | None | [ ] | None |
| shared-install-verifier | default | [x] | None | [ ] | None |
| ux-designer-or-reviewer | default | [x] | None | [ ] | None |
| wiki-ingest-agent | default | [x] | None | [ ] | None |
| wiki-query-agent | default | [x] | None | [ ] | None |

## Bundled Skill Checklist

### Wiki and knowledge skills

- [x] code-project-wiki — structural; declared: none; verified behavior: [ ] none
- [x] project-wiki — structural; declared: none; verified behavior: [ ] none
- [x] project-wiki-query — structural; declared: none; verified behavior: [ ] none
- [x] project-wiki-research — structural; declared: none; verified behavior: [ ] none
- [x] project-wiki-topic-verifier — structural; declared: none; verified behavior: [ ] none
- [x] project-wiki-topic-writer — structural; declared: none; verified behavior: [ ] none

### Documentation methodology skills

- [x] create-agents-plan — structural; declared: none; verified behavior: [ ] none
- [x] development-methodology — structural; declared: none; verified behavior: [ ] none
- [x] documentation-bootstrap — structural; declared: none; verified behavior: [ ] none
- [x] documentation-page-verifier — structural; declared: none; verified behavior: [ ] none
- [x] documentation-reverse-engineering — structural; declared: none; verified behavior: [ ] none
- [x] maintain-methodology-documentation — structural; declared: none; verified behavior: [ ] none

### Artifact creation skills

- [x] create-architecture — structural; declared: none; verified behavior: [ ] none
- [x] create-functional-spec — structural; declared: none; verified behavior: [ ] none
- [x] create-high-level-design — structural; declared: none; verified behavior: [ ] none
- [x] create-module-design — structural; declared: none; verified behavior: [ ] none
- [x] create-project-wiki — structural; declared: none; verified behavior: [ ] none
- [x] create-unit-test-plan — structural; declared: none; verified behavior: [ ] none

### Artifact review skills

- [x] review-architecture — structural; declared: none; verified behavior: [ ] none
- [x] review-functional-spec — structural; declared: none; verified behavior: [ ] none
- [x] review-high-level-design — structural; declared: none; verified behavior: [ ] none
- [x] review-module-design — structural; declared: none; verified behavior: [ ] none
- [x] review-project-wiki — structural; declared: none; verified behavior: [ ] none
- [x] review-structured — structural; declared: typescript-code-review; verified behavior: [ ] none
- [x] review-unit-test-plan — structural; declared: none; verified behavior: [ ] none

### Development practice skills

- [x] agent-claim — structural; declared: none; verified behavior: [ ] none
- [x] agent-work-merge — structural; declared: none; verified behavior: [ ] none
- [x] application-security — structural; declared: none; verified behavior: [ ] none
- [x] ast-grep — structural; declared: none; verified behavior: [ ] none
- [x] careful-coding — structural; declared: typescript-order-pricing, spring-boot-order-cancellation, typescript-code-review; verified behavior: [ ] none
- [x] code-discovery — structural; declared: none; verified behavior: [ ] none
- [x] code-execution-tracing — structural; declared: none; verified behavior: [ ] none
- [x] code-review-evidence — structural; declared: typescript-order-pricing, spring-boot-order-cancellation, typescript-code-review; verified behavior: [ ] none
- [x] create-backlog — structural; declared: none; verified behavior: [ ] none
- [x] detect-technology-skills — structural; declared: none; verified behavior: [ ] none
- [x] end-to-end-verification — structural; declared: none; verified behavior: [ ] none
- [x] fix-explanation — structural; declared: none; verified behavior: [ ] none
- [x] manage-backlog — structural; declared: none; verified behavior: [ ] none
- [x] prompt-contracts — structural; declared: none; verified behavior: [ ] none
- [x] root-cause-analysis — structural; declared: none; verified behavior: [ ] none
- [x] runtime-evidence-collection — structural; declared: none; verified behavior: [ ] none
- [x] structured-design — structural; declared: none; verified behavior: [ ] none
- [x] structured-explanation — structural; declared: none; verified behavior: [ ] none
- [x] test-driven-development — structural; declared: typescript-order-pricing, spring-boot-order-cancellation; verified behavior: [ ] none
- [x] test-strategy — structural; declared: none; verified behavior: [ ] none
- [x] user-experience-review — structural; declared: none; verified behavior: [ ] none

### Stack and domain skills

- [x] api-routes — structural; declared: none; verified behavior: [ ] none
- [x] clerk-auth — structural; declared: none; verified behavior: [ ] none
- [x] electron-main — structural; declared: none; verified behavior: [ ] none
- [x] electron-preload — structural; declared: none; verified behavior: [ ] none
- [x] fastapi — structural; declared: none; verified behavior: [ ] none
- [x] harness-implementation — structural; declared: none; verified behavior: [ ] none
- [x] java-coding — structural; declared: spring-boot-order-cancellation; verified behavior: [ ] none
- [x] jest — structural; declared: none; verified behavior: [ ] none
- [x] langgraph — structural; declared: none; verified behavior: [ ] none
- [x] local-model-integration — structural; declared: none; verified behavior: [ ] none
- [x] nextjs-app-router — structural; declared: none; verified behavior: [ ] none
- [x] node-cli — structural; declared: none; verified behavior: [ ] none
- [x] plan-engine-implementation — structural; declared: none; verified behavior: [ ] none
- [x] playwright — structural; declared: none; verified behavior: [ ] none
- [x] postgres-drizzle — structural; declared: none; verified behavior: [ ] none
- [x] python-coding — structural; declared: none; verified behavior: [ ] none
- [x] react-server-components — structural; declared: none; verified behavior: [ ] none
- [x] react-vite-renderer — structural; declared: none; verified behavior: [ ] none
- [x] spring-boot — structural; declared: spring-boot-order-cancellation; verified behavior: [ ] none
- [x] sql-coding — structural; declared: spring-boot-order-cancellation; verified behavior: [ ] none
- [x] tailwind-design-system — structural; declared: none; verified behavior: [ ] none
- [x] tool-runtime-implementation — structural; declared: none; verified behavior: [ ] none
- [x] typescript-coding — structural; declared: typescript-order-pricing, typescript-code-review; verified behavior: [ ] none
- [x] typescript-esm — structural; declared: typescript-order-pricing, typescript-code-review; verified behavior: [ ] none
- [x] typescript-strict — structural; declared: typescript-order-pricing, typescript-code-review; verified behavior: [ ] none
- [x] vitest — structural; declared: none; verified behavior: [ ] none

## Manual Evaluation Observations Requiring Receipt-Based Reruns

- [ ] TypeScript order pricing produced eight passing tests and a build, but lacks a machine-verifiable agent and skill-read receipt.
- [ ] Spring Boot order cancellation produced ten passing tests and useful boundary evidence, but lacks a machine-verifiable agent and skill-read receipt.
- [ ] TypeScript code review truthfully found all seeded defects in a read-only run, but lacks a complete captured invocation and skill-read receipt.
- [ ] Staged model execution remains unverified until separate evidence-extraction and synthesis invocations are captured.

## Repository Verification Layers

- [x] Agent Skill format validation for every bundled skill.
- [x] Canonical role schema, skill reference, model profile, and adapter completeness tests.
- [x] Codex TOML and Claude Code Markdown native role generation checks.
- [x] Generic, Codex, Gemini CLI, Claude Code, and Junie CLI installer behavior tests.
- [x] Generated documentation and agent-skill hierarchy freshness checks.
- [x] Shared installation refresh exercised for Agents, Codex, and Claude destinations.
- [x] Evaluation fixture runner verifies expected project behavior, including intentionally failing review fixtures.
- [ ] Agent and skill attribution remains unchecked until a valid evidence receipt is supplied.
