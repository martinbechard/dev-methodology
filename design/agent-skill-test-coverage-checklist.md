# Agent, Skill, Technology, And Test Coverage Checklist

This page is generated from the live conceptual agent and skill inventories, all six evaluation catalogs, executable fixture checks, sandbox declarations, Judge calibration records, and classified evidence receipts. Regenerate it with scripts/build-support-checklist.py.

## Status Meaning

- Structural means the current agent or skill source exists and passes repository catalog checks.
- Probe-declared and scenario-declared mean the current source has an explicit evaluation declaration. Declaration is not execution.
- For agents, case-backed scenarios report exactly which declared scenarios have cases. Full fixture-backed status requires every declared scenario to be backed.
- For skills, a positive case alone does not prove activation precision or causal skill contribution. Full probe coverage additionally requires a negative-activation case and executable target-present, target-omitted, and wrong-skill controls over frozen input.
- Executable fixture means every case required for the corresponding full coverage claim has a project, task, and verification command.
- A workflow pack may have partial case coverage without having an end-to-end fixture for every declared phase, agent, and handoff.
- Model Judge calibration promotion is disabled pending per-sample provenance. Diagnostic records cannot create calibrated status; Deterministic-Judge-only declarations show not-required.
- Executed means a version-two receipt has a structurally complete harness capture. It does not imply a Judge pass or security containment.
- Judge-passed means the required Deterministic Judge and Model Judge checks passed. Model Judge calibration is reported separately and may remain pending.
- Security-contained means a governed external runner established filesystem, process, network, and resource containment. The local tier does not make this claim.
- Stale-by-digest means a prior execution no longer matches current agent, skill, model, or Judge artifacts.
- Legacy verified fields remain for data compatibility only; primary reporting uses Executed, Judge-passed, Security-contained, and Stale-by-digest.
- Catalog coverageStatus values never create execution or evidence claims.

## Summary

- [x] 26 conceptual agents and 87 bundled skills have structural coverage.
- [x] 26 agents are scenario-declared and 87 skills are probe-declared.
- [x] 52 agent scenarios and 5 workflow packs are declared.
- 5 workflow packs have associated cases; 5 are partial and 0 have end-to-end fixture coverage.
- 7 cases are fixture-backed and 7 fixtures are structurally executable before harness readiness is considered.
- 7 cases can run locally through Codex and 7 can run locally through Junie.
- 7 cases use the ordinary local tier; 0 explicitly high-risk cases require the externally-contained tier.
- 6 agents have at least one case-backed scenario; 6 are partial and 0 have all declared scenarios backed.
- 17 skills have positive-case support, 0 have negative-activation cases, 0 have executable paired controls, and 0 satisfy the full probe contract.
- 0 agents and 0 skills have executable full fixtures.
- 0 agents and 0 skills have calibrated Model Judge status.
- 26 agents and 66 skills have pending Model Judge status.
- 0 agents and 21 skills use Deterministic Judges only and do not require Model Judge calibration.
- 0 agents and 0 skills have classified executions.
- 0 agents and 0 skills have Judge-passed evidence.
- 0 agents and 0 skills have security-contained evidence.
- 0 agents and 0 skills have stale-by-digest evidence.
- Positive-case-only skill evidence: 0 executed, 0 Judge-passed, 0 security-contained, and 0 stale; these do not promote full-probe status.

## Evaluation Harness And Sandbox Support

Evaluation execution support is limited to Codex and Junie. Ordinary synthetic cases run locally in disposable workspaces with controlled harness state, timeouts, cleanup, isolated evidence, and mutation audits. External containment is reserved for explicitly high-risk cases. Workspace isolation and tool configuration do not create a security-containment claim.

| Harness | Profile | Implementation | Workspace isolation | Containment status |
| --- | --- | --- | --- | --- |
| codex | codex-permission-profile-git-write | local-tier-implemented | native-policy-plus-copy-on-write-declared | containment-unverified |
| codex | codex-read-only | partial | native-policy-plus-copy-on-write-declared | containment-unverified |
| codex | codex-workspace-write | partial | native-policy-plus-copy-on-write-declared | containment-unverified |
| junie | junie-read-only | local-tier-implemented | disposable-workspace-plus-mutation-audit | containment-unverified |
| junie | junie-workspace-write | local-tier-implemented | disposable-workspace-plus-mutation-audit | containment-unverified |

## Agent Checklist

| Agent | Profile | Structural | Scenario-declared | Case-backed scenarios | All scenarios backed | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dev-artifact-reviewer | advanced | [x] | [x] dev-artifact-reviewer-boundary, dev-artifact-reviewer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-backlog-steward | default | [x] | [x] dev-backlog-steward-boundary, dev-backlog-steward-happy | [x] dev-backlog-steward-boundary | [ ] none | [ ] none | pending | none | none | none | none |
| dev-browser-operator | advanced | [x] | [x] dev-browser-operator-boundary, dev-browser-operator-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-code-reviewer | advanced | [x] | [x] dev-code-reviewer-boundary, dev-code-reviewer-happy | [x] dev-code-reviewer-happy | [ ] none | [ ] none | pending | none | none | none | none |
| dev-coder | advanced | [x] | [x] dev-coder-boundary, dev-coder-happy | [x] dev-coder-happy | [ ] none | [ ] none | pending | none | none | none | none |
| dev-documentation-writer | default | [x] | [x] dev-documentation-writer-boundary, dev-documentation-writer-happy | [x] dev-documentation-writer-happy | [ ] none | [ ] none | pending | none | none | none | none |
| dev-merge-coordinator | advanced | [x] | [x] dev-merge-coordinator-boundary, dev-merge-coordinator-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-orchestrator | advanced-long | [x] | [x] dev-orchestrator-boundary, dev-orchestrator-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-prompt-reviewer | advanced | [x] | [x] dev-prompt-reviewer-boundary, dev-prompt-reviewer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-runtime-diagnostician | advanced | [x] | [x] dev-runtime-diagnostician-boundary, dev-runtime-diagnostician-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-security-reviewer | advanced | [x] | [x] dev-security-reviewer-boundary, dev-security-reviewer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-ux-specialist | default | [x] | [x] dev-ux-specialist-boundary, dev-ux-specialist-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| dev-verifier | advanced | [x] | [x] dev-verifier-boundary, dev-verifier-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| methodology-artifact-reviewer | advanced | [x] | [x] methodology-artifact-reviewer-boundary, methodology-artifact-reviewer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| methodology-maintainer | advanced | [x] | [x] methodology-maintainer-boundary, methodology-maintainer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| project-bootstrapper | advanced-long | [x] | [x] project-bootstrapper-boundary, project-bootstrapper-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| project-configurator | default | [x] | [x] project-configurator-boundary, project-configurator-happy | [x] project-configurator-happy | [ ] none | [ ] none | pending | none | none | none | none |
| project-organiser | default | [x] | [x] project-organiser-boundary, project-organiser-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-architect | advanced | [x] | [x] wiki-architect-boundary, wiki-architect-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-artifact-reviewer | advanced | [x] | [x] wiki-artifact-reviewer-boundary, wiki-artifact-reviewer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-ingester | default | [x] | [x] wiki-ingester-boundary, wiki-ingester-happy | [x] wiki-ingester-happy | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-query-responder | default | [x] | [x] wiki-query-responder-boundary, wiki-query-responder-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-researcher | default | [x] | [x] wiki-researcher-boundary, wiki-researcher-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-source-collector | simple | [x] | [x] wiki-source-collector-boundary, wiki-source-collector-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-topic-verifier | advanced | [x] | [x] wiki-topic-verifier-boundary, wiki-topic-verifier-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |
| wiki-writer | default | [x] | [x] wiki-writer-boundary, wiki-writer-happy | [ ] none | [ ] none | [ ] none | pending | none | none | none | none |

## Bundled Skill Checklist

### Wiki and knowledge skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code-project-wiki | [x] | [x] probe-code-project-wiki | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki | [x] | [x] probe-project-wiki | [x] wiki-raw-ingest | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-create | [x] | [x] probe-project-wiki-create | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-query | [x] | [x] probe-project-wiki-query | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-research | [x] | [x] probe-project-wiki-research | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-review | [x] | [x] probe-project-wiki-review | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-topic-verify | [x] | [x] probe-project-wiki-topic-verify | [x] wiki-raw-ingest | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| project-wiki-topic-write | [x] | [x] probe-project-wiki-topic-write | [x] wiki-raw-ingest | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

### Documentation methodology skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent-role-authoring | [x] | [x] probe-agent-role-authoring | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-project-configuration | [x] | [x] probe-create-project-configuration | [x] project-configuration-routing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| development-methodology | [x] | [x] probe-development-methodology | [x] documentation-functional-spec, project-configuration-routing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| documentation-bootstrap | [x] | [x] probe-documentation-bootstrap | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| documentation-page-verify | [x] | [x] probe-documentation-page-verify | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| documentation-reverse-engineer | [x] | [x] probe-documentation-reverse-engineer | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| maintain-methodology-documentation | [x] | [x] probe-maintain-methodology-documentation | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| name-methodology-artifacts | [x] | [x] probe-name-methodology-artifacts | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| skill-authoring | [x] | [x] probe-skill-authoring | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

### Artifact creation skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| create-architecture | [x] | [x] probe-create-architecture | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-functional-spec | [x] | [x] probe-create-functional-spec | [x] documentation-functional-spec | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-high-level-design | [x] | [x] probe-create-high-level-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-module-design | [x] | [x] probe-create-module-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-unit-test-plan | [x] | [x] probe-create-unit-test-plan | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

### Artifact review skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| review-architecture | [x] | [x] probe-review-architecture | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| review-functional-spec | [x] | [x] probe-review-functional-spec | [x] documentation-functional-spec | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| review-high-level-design | [x] | [x] probe-review-high-level-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| review-module-design | [x] | [x] probe-review-module-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| review-structured-artifact | [x] | [x] probe-review-structured-artifact | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| review-unit-test-plan | [x] | [x] probe-review-unit-test-plan | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

### Development practice skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent-claim | [x] | [x] probe-agent-claim | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| agent-work-merge | [x] | [x] probe-agent-work-merge | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| application-security | [x] | [x] probe-application-security | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| ast-grep | [x] | [x] probe-ast-grep | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| careful-coding | [x] | [x] probe-careful-coding | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| code-comments | [x] | [x] probe-code-comments | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| code-discovery | [x] | [x] probe-code-discovery | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| code-execution-tracing | [x] | [x] probe-code-execution-tracing | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| code-review-evidence | [x] | [x] probe-code-review-evidence | [x] typescript-code-review | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| create-backlog | [x] | [x] probe-create-backlog | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| detect-technology-skills | [x] | [x] probe-detect-technology-skills | [x] project-configuration-routing | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| end-to-end-verification | [x] | [x] probe-end-to-end-verification | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| fix-explanation | [x] | [x] probe-fix-explanation | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| manage-backlog | [x] | [x] probe-manage-backlog | [x] backlog-lifecycle | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| organise-project-files | [x] | [x] probe-organise-project-files | [x] project-configuration-routing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| prompt-contracts | [x] | [x] probe-prompt-contracts | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| root-cause-analysis | [x] | [x] probe-root-cause-analysis | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| runtime-evidence-collection | [x] | [x] probe-runtime-evidence-collection | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| structured-design | [x] | [x] probe-structured-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| structured-explanation | [x] | [x] probe-structured-explanation | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| test-driven-development | [x] | [x] probe-test-driven-development | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| test-strategy | [x] | [x] probe-test-strategy | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| user-experience-review | [x] | [x] probe-user-experience-review | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

### Stack and domain skills

| Skill | Structural | Probe-declared | Positive case | Negative case | Paired controls | Full probe | Executable full fixture | Judge calibration | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent-harness | [x] | [x] probe-agent-harness | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| api-routes | [x] | [x] probe-api-routes | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| clerk-auth | [x] | [x] probe-clerk-auth | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| electron-main | [x] | [x] probe-electron-main | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| electron-preload | [x] | [x] probe-electron-preload | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| fastapi | [x] | [x] probe-fastapi | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| java | [x] | [x] probe-java | [x] spring-boot-order-cancellation | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| java-design | [x] | [x] probe-java-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| jest | [x] | [x] probe-jest | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| jhipster-domain-modeling | [x] | [x] probe-jhipster-domain-modeling | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| jhipster-persistence | [x] | [x] probe-jhipster-persistence | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| jhipster-project | [x] | [x] probe-jhipster-project | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| jhipster-security | [x] | [x] probe-jhipster-security | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| jhipster-testing | [x] | [x] probe-jhipster-testing | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| langgraph | [x] | [x] probe-langgraph | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| liquibase | [x] | [x] probe-liquibase | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| local-model-integration | [x] | [x] probe-local-model-integration | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | not-required | none | none | none | none |
| nextjs-app-router | [x] | [x] probe-nextjs-app-router | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| node-cli | [x] | [x] probe-node-cli | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| plan-engine | [x] | [x] probe-plan-engine | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| playwright | [x] | [x] probe-playwright | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| postgres-drizzle | [x] | [x] probe-postgres-drizzle | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| python | [x] | [x] probe-python | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| react-server-components | [x] | [x] probe-react-server-components | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| react-vite-renderer | [x] | [x] probe-react-vite-renderer | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| spring-boot | [x] | [x] probe-spring-boot | [x] spring-boot-order-cancellation | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| spring-boot-design | [x] | [x] probe-spring-boot-design | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| spring-boot-testing | [x] | [x] probe-spring-boot-testing | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| spring-data-jpa | [x] | [x] probe-spring-data-jpa | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| sql | [x] | [x] probe-sql | [x] spring-boot-order-cancellation | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| tailwind-design-system | [x] | [x] probe-tailwind-design-system | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| tool-runtime | [x] | [x] probe-tool-runtime | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| typescript | [x] | [x] probe-typescript | [x] typescript-code-review, typescript-order-pricing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| typescript-esm | [x] | [x] probe-typescript-esm | [x] typescript-code-review, typescript-order-pricing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| typescript-strict | [x] | [x] probe-typescript-strict | [x] typescript-code-review, typescript-order-pricing | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |
| vitest | [x] | [x] probe-vitest | [ ] none | [ ] none | [ ] | [ ] none | [ ] none | pending | none | none | none | none |

## Technology Detection Registry

| Skill | Kind | Label | Probe-declared | Positive case | Full probe fixture | Executed | Judge-passed | Security-contained | Stale-by-digest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| agent-harness | domain | Agent harness | [x] | [ ] | [ ] | none | none | none | none |
| api-routes | technology | Application route handlers | [x] | [ ] | [ ] | none | none | none | none |
| clerk-auth | technology | Clerk identity integration | [x] | [ ] | [ ] | none | none | none | none |
| electron-main | technology | Electron main process | [x] | [ ] | [ ] | none | none | none | none |
| electron-preload | technology | Electron preload boundary | [x] | [ ] | [ ] | none | none | none | none |
| fastapi | technology | FastAPI | [x] | [ ] | [ ] | none | none | none | none |
| java | technology | Java | [x] | [x] | [ ] | none | none | none | none |
| java-design | technology | Java Design | [x] | [ ] | [ ] | none | none | none | none |
| jest | technology | Jest | [x] | [ ] | [ ] | none | none | none | none |
| jhipster-domain-modeling | domain | JHipster Domain Modeling | [x] | [ ] | [ ] | none | none | none | none |
| jhipster-persistence | domain | JHipster Persistence | [x] | [ ] | [ ] | none | none | none | none |
| jhipster-project | technology | JHipster Project | [x] | [ ] | [ ] | none | none | none | none |
| jhipster-security | domain | JHipster Security | [x] | [ ] | [ ] | none | none | none | none |
| jhipster-testing | domain | JHipster Testing | [x] | [ ] | [ ] | none | none | none | none |
| langgraph | technology | LangGraph | [x] | [ ] | [ ] | none | none | none | none |
| liquibase | technology | Liquibase | [x] | [ ] | [ ] | none | none | none | none |
| local-model-integration | domain | Local model integration | [x] | [ ] | [ ] | none | none | none | none |
| nextjs-app-router | technology | Next.js App Router | [x] | [ ] | [ ] | none | none | none | none |
| node-cli | technology | Node command line application | [x] | [ ] | [ ] | none | none | none | none |
| plan-engine | domain | Plan engine | [x] | [ ] | [ ] | none | none | none | none |
| playwright | technology | Playwright | [x] | [ ] | [ ] | none | none | none | none |
| postgres-drizzle | technology | PostgreSQL with Drizzle | [x] | [ ] | [ ] | none | none | none | none |
| python | technology | Python | [x] | [ ] | [ ] | none | none | none | none |
| react-server-components | technology | React Server Components | [x] | [ ] | [ ] | none | none | none | none |
| react-vite-renderer | technology | React renderer with Vite | [x] | [ ] | [ ] | none | none | none | none |
| spring-boot | technology | Spring Boot | [x] | [x] | [ ] | none | none | none | none |
| spring-boot-design | technology | Spring Boot Design | [x] | [ ] | [ ] | none | none | none | none |
| spring-boot-testing | technology | Spring Boot Testing | [x] | [ ] | [ ] | none | none | none | none |
| spring-data-jpa | technology | Spring Data JPA | [x] | [ ] | [ ] | none | none | none | none |
| sql | technology | SQL | [x] | [x] | [ ] | none | none | none | none |
| tailwind-design-system | technology | Tailwind design system | [x] | [ ] | [ ] | none | none | none | none |
| tool-runtime | domain | Tool runtime | [x] | [ ] | [ ] | none | none | none | none |
| typescript | technology | TypeScript | [x] | [x] | [ ] | none | none | none | none |
| typescript-esm | technology | TypeScript ECMAScript modules | [x] | [x] | [ ] | none | none | none | none |
| typescript-strict | technology | Strict TypeScript | [x] | [x] | [ ] | none | none | none | none |
| vitest | technology | Vitest | [x] | [ ] | [ ] | none | none | none | none |

## Judge Calibration

- Calibration policy status: pending.
- Calibrated Model Judge rubrics: none.
- Pending Model Judge rubrics: artifact-contract, diagnosis-quality, review-quality, security-quality, source-faithfulness, ux-quality, workflow-quality.
- Judge outcome and calibration are separate: a raw Model Judge pass does not become calibrated until the governed calibration policy is enabled and satisfied.

## Repository Verification Layers

- [x] Every live skill has exactly one probe declaration.
- [x] Every live conceptual agent has exactly one scenario declaration with at least one scenario.
- [x] Evaluation catalog references, fixture paths, Judge plans, harnesses, workflow links, and sandbox profiles are validated.
- [x] Codex and Junie are the only supported evaluation harnesses.
- [x] Executed, Judge-passed, security-contained, calibration, and stale claims are classified independently by the evaluation runner.
- [x] Explorer data carries the same conservative coverage snapshot.
