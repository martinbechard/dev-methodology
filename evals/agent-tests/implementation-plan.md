# Implementation Plan: Agent-Owned Evaluation Suites

## 1. Tracking Summary

This file is the program tracker for moving behavioral evaluation from exhaustive skill-by-skill coverage to compact suites derived from canonical conceptual agent definitions.

Plan status: active, with further implementation intentionally not started.

Source snapshot: repository state at f705fe3ada0d940967d38b5aa41ee88efb33d371 on 2026-07-17.

| Work area | Status | Progress | Next action |
|---|---|---:|---|
| Agent-first strategy and common protocol | Done | 100% | Keep aligned as suites evolve |
| Shared suite project skills | Done | 100% | Reuse; change only from observed cross-suite needs |
| First four suite definitions | Done | 4 of 4 | Close their remaining scenario and execution gaps |
| First four representative Codex runs | Done | 4 of 4 | Convert all retained evidence to the repeatable runner contract |
| Remaining scenarios for the first four suites | Todo | 0 of 8 planned scenarios | Implement after explicit authorization |
| Repeatable four-supervisor execution | Todo | 0% | Implement after first-suite gap review |
| Timing capture | Todo | 0% | Add to execution and result records before broad rollout |
| Remaining conceptual agent suites | Todo | 0 of 22 | Add in the priority order below |

Historical task durations are unknown because start times and per-task elapsed times were not recorded. Git commit times are preserved as completion checkpoints, but the interval between commits is not treated as active work time.

## 2. Goal Hierarchy

This section fixes the outcome and the dependency-ordered chunks of work.

- **GOAL: GOAL-1** Maintain one high-value behavioral evaluation suite for every conceptual agent
  - **SYNOPSIS:** Each suite derives a small scenario set from the complete canonical agent definition and evaluates observable agent behavior rather than attempting one test per assigned skill.
  - **BECAUSE:** Agent-level outcomes give end users more useful confidence at a sustainable evaluation cost.
  - **SUBGOAL: SUBG-1** Establish the common suite contract
    - **STATUS:** done
    - **BECAUSE:** Every suite needs the same orchestration, evidence, judging, privacy, mutation, and concurrency rules.
  - **SUBGOAL: SUBG-2** Prove the strategy on the highest-value agents
    - **STATUS:** partially done
    - **BECAUSE:** The first four suites demonstrate coding, review, diagnosis, and project setup before the catalog expands.
  - **SUBGOAL: SUBG-3** Make execution repeatable and measurable
    - **STATUS:** todo
    - **BECAUSE:** Scaling to every agent requires governed automation, durable receipts, and elapsed-time evidence rather than manual reconstruction.
  - **SUBGOAL: SUBG-4** Expand the suite catalog in value-ordered batches
    - **STATUS:** todo
    - **BECAUSE:** A bounded rollout delivers useful coverage before lower-value or narrower agents consume evaluation effort.
  - **SUBGOAL: SUBG-5** Operate the suites as a maintained verification system
    - **STATUS:** todo
    - **BECAUSE:** Definition, adapter, fixture, rubric, and skill changes can make prior evidence stale.

## 3. Completed Work

Only work supported by current repository artifacts, result evidence, or Git history is marked done.

- **TASK: DONE-1** Replace exhaustive skill-first planning with agent-owned suites
  - **STATUS:** done
  - **SYNOPSIS:** The evaluation documentation now makes agent-owned suites the primary planning and orchestration unit while retaining skill probes as targeted diagnostic controls.
  - **PRODUCES:** evals/README.md, evals/agent-tests/README.md, and aligned root README guidance.
  - **COMPLETED:** 2026-07-16 23:44:10 America/Toronto at commit ad8c45f051aa46db86731422af5eb35f7293ba63.
  - **ELAPSED:** unknown; no task start time was recorded.

- **TASK: DONE-2** Define the common root protocol
  - **STATUS:** done
  - **SYNOPSIS:** The protocol defines source authority, suite structure, supervisor and Judge responsibilities, finding disposition, mutation and claim rules, evidence, terminal statuses, and cleanup.
  - **PRODUCES:** evals/agent-tests/AGENTS.md.
  - **VALIDATES:** At most four concurrent supervisors, exactly one active child per supervisor, a normal ceiling of nine active agents, and a temporary ceiling of ten for one declared nested dependency.
  - **COMPLETED:** 2026-07-16 23:44:10 America/Toronto at commit ad8c45f051aa46db86731422af5eb35f7293ba63.
  - **ELAPSED:** unknown; no task start time was recorded.

- **TASK: DONE-3** Create shared project skills for cross-suite behavior
  - **STATUS:** done
  - **SYNOPSIS:** Three shared project skills govern suite supervision, scenario design, and independent evidence judging.
  - **PRODUCES:** evals/agent-tests/skills/agent-suite-supervision, evals/agent-tests/skills/agent-scenario-design, and evals/agent-tests/skills/agent-evidence-judging.
  - **COMPLETED:** 2026-07-16 23:44:10 America/Toronto at commit ad8c45f051aa46db86731422af5eb35f7293ba63.
  - **ELAPSED:** unknown; no task start time was recorded.

- **TASK: DONE-4** Create the first four value-ordered agent suites
  - **STATUS:** done
  - **SYNOPSIS:** Dev Coder, Dev Code Reviewer, Dev Runtime Diagnostician, and Project Bootstrapper each have a suite folder, suite manifest, authoritative scenario catalog, hardcoded supervisor, hardcoded read-only Judge, and suite-specific contract skill.
  - **PRODUCES:** Four direct child suite folders under evals/agent-tests and their entries in evals/agent-tests/suite-index.yaml.
  - **COMPLETED:** 2026-07-16 23:44:10 America/Toronto at commit ad8c45f051aa46db86731422af5eb35f7293ba63.
  - **ELAPSED:** unknown; no task start time was recorded.

- **TASK: DONE-5** Add structural regression coverage for the suite contract
  - **STATUS:** done
  - **SYNOPSIS:** Bundle tests verify suite order, directory shape, role and adapter references, project-agent names, project-skill packages, scenario count, dependency alignment, concurrency limits, identity requirements, and common protocol phrases.
  - **PRODUCES:** Agent-owned suite checks in scripts/test_bundle_content.py.
  - **COMPLETED:** Initial coverage landed on 2026-07-16 23:44:10 America/Toronto and was hardened through 2026-07-17 15:31:47 America/Toronto.
  - **ELAPSED:** unknown; no per-change start times were recorded.

- **TASK: DONE-6** Harden Codex custom-agent execution and identity evidence
  - **STATUS:** done
  - **SYNOPSIS:** Codex project-agent names are underscore-safe, agent identity requires retained custom-agent and developer-instruction evidence, applicable conditional skills must be staged before target execution, and mutation fixtures must permit declared worktree and Git metadata access.
  - **PRODUCES:** Updated common and suite contracts plus the runtime-dependency fixture.
  - **COMPLETED:** 2026-07-17 01:00:29 America/Toronto at commit efe7bb773f2db7730629113808f0b80c33c89383.
  - **ELAPSED:** unknown; the 1 hour 16 minute interval from the previous commit is only a checkpoint interval.

- **TASK: DONE-7** Execute and independently judge one representative Codex scenario for each first-priority suite
  - **STATUS:** done
  - **SYNOPSIS:** The retained result reports PASS for Dev Coder, Dev Code Reviewer, Dev Runtime Diagnostician, and Project Bootstrapper with verified target and Judge identities.
  - **PRODUCES:** evals/agent-tests/results/2026-07-17-codex-agent-suites.md.
  - **COMPLETED:** 2026-07-17 01:00:29 America/Toronto at commit efe7bb773f2db7730629113808f0b80c33c89383.
  - **ELAPSED:** unknown; individual run durations were not retained in the summary.

- **TASK: DONE-8** Address first review findings in the suite infrastructure
  - **STATUS:** done
  - **SYNOPSIS:** The common contract now keeps one authoritative scenarios.yaml per suite, separates test-infrastructure correction from target-product findings, requires backlog routing for subject findings, and uses a steady-state result name.
  - **COMPLETED:** 2026-07-17 15:31:47 America/Toronto at commit 2bf41a7e0584d6c3443139cd996599ee984a02c5.
  - **ELAPSED:** unknown; the 14 hour 31 minute interval from the previous commit is only a checkpoint interval.

- **TASK: DONE-9** Establish this implementation tracker
  - **STATUS:** done
  - **SYNOPSIS:** This file records completed evidence, remaining dependencies, rollout order, status rules, and future timing fields without starting further suite work.
  - **COMPLETED:** 2026-07-17.
  - **ELAPSED:** not recorded.

## 4. Current Coverage And Gaps

This section distinguishes suite structure, executable fixture readiness, and retained live results.

| Suite | Definition | Scenario catalog | Fixture or case readiness | Retained representative run | Remaining scenario work |
|---|---|---:|---:|---:|---:|
| Dev Coder | Done | 3 scenarios | 2 fixture-backed, 1 planned | 1 PASS | Execute Spring path; build blocked-authority path |
| Dev Code Reviewer | Done | 3 scenarios | 1 fixture-backed, 2 planned | 1 PASS | Build clean-review and incomplete-evidence paths |
| Dev Runtime Diagnostician | Done | 3 scenarios | 1 executable, 2 planned | 1 PASS with expected blocked target outcome | Build retained-port and worker-stall paths |
| Project Bootstrapper | Done | 3 scenarios | 3 planned in the catalog | 1 PASS from a governed disposable run | Formalize executable fixtures for all three paths |

- **GAP: GAP-1** Eight scenarios remain marked planned
  - **SYNOPSIS:** One Dev Coder, two Dev Code Reviewer, two Dev Runtime Diagnostician, and three Project Bootstrapper scenarios do not name executable cases.
  - **BECAUSE:** Scenario declarations alone do not establish executable or Judge-passed coverage.

- **GAP: GAP-2** One fixture-backed Dev Coder scenario has no retained result in the current suite summary
  - **SYNOPSIS:** The Spring boundary-change scenario points to an existing executable case, but the retained report covers the TypeScript scenario only.
  - **BECAUSE:** Fixture readiness and executed evidence are separate claims.

- **GAP: GAP-3** Project Bootstrapper catalog status does not express the retained run state
  - **SYNOPSIS:** The valid-configuration scenario is still marked planned even though a governed disposable run is summarized as PASS.
  - **BECAUSE:** Catalog readiness, execution status, and result evidence should not appear contradictory.

- **GAP: GAP-4** Four-supervisor execution is a declared protocol rather than a demonstrated repeatable runner path
  - **SYNOPSIS:** The common contract and suite index define concurrency, while the existing evaluation runner states that selected cases execute serially.
  - **BECAUSE:** The requested operating model needs an executable coordinator and evidence that the limit is enforced.

- **GAP: GAP-5** Historical and per-run elapsed time is not available
  - **SYNOPSIS:** Current summaries retain evidence digests and outcomes but not start, finish, or elapsed fields for every supervisor, target, dependency, Judge, and suite.
  - **BECAUSE:** Git timestamps cannot distinguish active execution from waiting or unrelated work.

- **GAP: GAP-6** Twenty-two conceptual agents do not yet have agent-owned suite folders
  - **SYNOPSIS:** The canonical catalog contains twenty-six conceptual agents and four currently have suites.
  - **BECAUSE:** The target steady state is one suite folder per conceptual agent under test.

## 5. Dependencies And Execution Order

This section prevents broad suite creation before the shared execution path is stable.

- **PROCESS: PROC-1** Close the first-four evidence gaps
  - **STATUS:** todo
  - **DEPENDS-ON:** DONE-1 through DONE-8.
  - **PRODUCES:** Executable cases or explicit deferrals for the eight planned scenarios, one retained result for the existing Spring case, and reconciled catalog readiness labels.
  - **BECAUSE:** The first four suites should prove the complete lifecycle before their structure is copied broadly.

- **PROCESS: PROC-2** Implement repeatable bounded orchestration and timing
  - **STATUS:** todo
  - **DEPENDS-ON:** PROC-1.
  - **PRODUCES:** A coordinator path that schedules no more than four supervisors, enforces one child per supervisor, preserves the exceptional nested-agent rule, and records timing fields.
  - **BECAUSE:** Repeatable measurement and concurrency enforcement are prerequisites for cost-controlled expansion.

- **PROCESS: PROC-3** Add the next four highest-value suites
  - **STATUS:** todo
  - **DEPENDS-ON:** PROC-2.
  - **PRODUCES:** Dev Verifier, Dev Orchestrator, Project Configurator, and Dev Security Reviewer suites.
  - **BECAUSE:** These roles protect final acceptance, coordinate multi-agent work, establish project routing, and address high-impact security risk.

- **PROCESS: PROC-4** Add the remaining suites in batches of at most four
  - **STATUS:** todo
  - **DEPENDS-ON:** A stable result from the preceding batch.
  - **PRODUCES:** Suite definitions, representative scenarios, fixtures, governed execution evidence, and maintenance ownership for the remaining conceptual agents.
  - **BECAUSE:** Small batches limit duplicated infrastructure mistakes and keep result review manageable.

- **PROCESS: PROC-5** Add recurring freshness and regression operation
  - **STATUS:** todo
  - **DEPENDS-ON:** PROC-2 and at least one completed expansion batch.
  - **PRODUCES:** Digest-driven stale classification, scheduled structural validation, selected live runs, cost and duration reporting, and finding handoff.
  - **BECAUSE:** Agent and skill definitions continue to change after their suites first pass.

## 6. Work Breakdown

These tasks are planned only. None of them is authorized or started by the creation of this file.

### 6.1 Stabilize Existing Suites

- **TASK: TASK-10** Reconcile scenario readiness and execution terminology
  - **STATUS:** todo
  - **SYNOPSIS:** Define and validate distinct values for planned, fixture-ready, executable, executed, and retained-result states.
  - **VALIDATES:** The Project Bootstrapper representative result can be understood without treating a planned catalog entry as executable proof.
  - **ESTIMATE:** small.

- **TASK: TASK-11** Make the eight planned first-four scenarios executable or explicitly deferred
  - **STATUS:** todo
  - **SYNOPSIS:** Reuse current synthetic projects where they expose the required behavior and add a new fixture only where no current fixture can do so.
  - **VALIDATES:** Each non-deferred scenario resolves to one frozen executable case and deterministic Judge plan.
  - **ESTIMATE:** large; fixture needs differ by scenario.

- **TASK: TASK-12** Execute the existing Spring Dev Coder scenario
  - **STATUS:** todo
  - **SYNOPSIS:** Run and judge the fixture-backed Spring boundary-change scenario through the same identity and evidence gates as the retained TypeScript run.
  - **VALIDATES:** A second representative technology path without creating a technology-exhaustive matrix.
  - **ESTIMATE:** medium.

- **TASK: TASK-13** Normalize retained suite results to the current evidence-receipt contract
  - **STATUS:** todo
  - **SYNOPSIS:** Ensure each retained result binds the suite, scenario, role digest, adapter digest, project-agent identity, staged skills, deterministic gates, Judge evidence, cleanup, and terminal status.
  - **VALIDATES:** The standard result validator can classify each retained run without narrative inference.
  - **ESTIMATE:** medium.

### 6.2 Automate Execution And Timing

- **TASK: TASK-20** Define the root coordinator execution contract
  - **STATUS:** todo
  - **SYNOPSIS:** Hardcode suite selection, four-supervisor capacity, failure isolation, result ordering, cancellation, cleanup, and exceptional nested-agent behavior.
  - **VALIDATES:** No execution path can exceed the declared concurrency ceilings.
  - **ESTIMATE:** medium.

- **TASK: TASK-21** Integrate agent-owned suites with the evaluation runner
  - **STATUS:** todo
  - **SYNOPSIS:** Make suite manifests and scenario catalogs executable inputs rather than relying on manually assembled runs.
  - **VALIDATES:** One command can run one suite and another can schedule a bounded set of suites.
  - **ESTIMATE:** large.

- **TASK: TASK-22** Capture task and agent elapsed time
  - **STATUS:** todo
  - **SYNOPSIS:** Record UTC start and finish timestamps plus monotonic elapsed seconds for coordinator, supervisor, target, dependency, deterministic-gate, Judge, and cleanup phases.
  - **PRODUCES:** Timing fields in machine-readable receipts and concise duration summaries in result reports.
  - **VALIDATES:** Parallel suite elapsed time is not incorrectly calculated as the sum of child durations.
  - **ESTIMATE:** medium.

- **TASK: TASK-23** Prove four-supervisor and nested-agent limits
  - **STATUS:** todo
  - **SYNOPSIS:** Add deterministic tests for four active supervisors, one child per supervisor, rejection or queuing of a fifth supervisor, and one allowed temporary tenth agent.
  - **VALIDATES:** Both normal and exceptional limits from the common protocol.
  - **ESTIMATE:** medium.

- **TASK: TASK-24** Add bounded cost and failure reporting
  - **STATUS:** todo
  - **SYNOPSIS:** Summarize tokens, tool calls, duration, retries, PASS, FAIL, BLOCKED, and STALE without merging those meanings.
  - **VALIDATES:** A partial batch failure preserves completed evidence and does not silently rerun successful paid work.
  - **ESTIMATE:** medium.

### 6.3 Add Agent Suites

- **TASK: TASK-30** Add Batch 2
  - **STATUS:** todo
  - **SYNOPSIS:** Add the first expansion batch after the runner and timing contract are proven.
  - **CONTAINS:** Dev Verifier, Dev Orchestrator, Project Configurator, and Dev Security Reviewer.
  - **BECAUSE:** These agents cover final acceptance, coordination, project routing, and material risk.

- **TASK: TASK-31** Add Batch 3
  - **STATUS:** todo
  - **SYNOPSIS:** Add work-state, integration, documentation, and wiki-ingest coverage.
  - **CONTAINS:** Dev Backlog Steward, Dev Merge Coordinator, Dev Documentation Writer, and Wiki Ingester.
  - **BECAUSE:** These agents cover recoverable work tracking, integration, durable documentation, and an existing fixture-backed wiki workflow.

- **TASK: TASK-32** Add Batch 4
  - **STATUS:** todo
  - **SYNOPSIS:** Add durable-knowledge and model-facing review coverage.
  - **CONTAINS:** Wiki Writer, Wiki Query Responder, Dev Artifact Reviewer, and Dev Prompt Reviewer.
  - **BECAUSE:** These agents create, answer from, and independently review durable knowledge and model-facing contracts.

- **TASK: TASK-33** Add Batch 5
  - **STATUS:** todo
  - **SYNOPSIS:** Add interactive, browser, placement, and wiki-structure coverage.
  - **CONTAINS:** Dev UX Specialist, Dev Browser Operator, Project Organiser, and Wiki Architect.
  - **BECAUSE:** These agents cover interactive quality, browser state, artifact placement, and wiki structure after the core runner is stable.

- **TASK: TASK-34** Add Batch 6
  - **STATUS:** todo
  - **SYNOPSIS:** Add independent wiki verification and bounded source-acquisition coverage.
  - **CONTAINS:** Wiki Topic Verifier, Wiki Artifact Reviewer, Wiki Researcher, and Wiki Source Collector.
  - **BECAUSE:** These agents complete independent wiki verification and the bounded source-to-raw workflow.

- **TASK: TASK-35** Add Batch 7
  - **STATUS:** todo
  - **SYNOPSIS:** Add the repository-specialized methodology maintenance and review coverage.
  - **CONTAINS:** Methodology Maintainer and Methodology Artifact Reviewer.
  - **BECAUSE:** Methodology-maintenance agents are important to this repository but are narrower for external end users than the earlier batches.

### 6.4 Operate And Maintain

- **TASK: TASK-40** Add stale-by-digest checks to every suite run
  - **STATUS:** todo
  - **SYNOPSIS:** Compare canonical role, native adapter, suite, scenario, fixture, project-skill, and Judge-contract digests before accepting retained evidence.
  - **ESTIMATE:** medium.

- **TASK: TASK-41** Define the minimum recurring run set
  - **STATUS:** todo
  - **SYNOPSIS:** Run structural validation on every relevant change and select paid live scenarios by changed agent, skill, fixture, runner, or Judge impact.
  - **ESTIMATE:** medium.

- **TASK: TASK-42** Route findings without fixing the subject under test
  - **STATUS:** todo
  - **SYNOPSIS:** Preserve governed evidence, correct only authorized test infrastructure, and send product, role, skill, or generated-adapter findings through Dev Backlog Steward.
  - **ESTIMATE:** small after the runner exposes result hooks.

- **TASK: TASK-43** Review suite value and retire redundant scenarios
  - **STATUS:** todo
  - **SYNOPSIS:** Keep representative success, boundary, and dependency or recovery behavior while removing scenarios that only duplicate skill-level coverage.
  - **ESTIMATE:** recurring.

## 7. Agent Suite Rollout Register

This is the single ordered view of all canonical conceptual agents.

| Priority | Conceptual agent | Suite status | Execution status | Planned batch |
|---:|---|---|---|---:|
| 1 | Dev Coder | Defined | Representative PASS | Complete first-four gaps |
| 2 | Dev Code Reviewer | Defined | Representative PASS | Complete first-four gaps |
| 3 | Dev Runtime Diagnostician | Defined | Representative PASS | Complete first-four gaps |
| 4 | Project Bootstrapper | Defined | Representative PASS | Complete first-four gaps |
| 5 | Dev Verifier | Todo | Not run | 2 |
| 6 | Dev Orchestrator | Todo | Not run | 2 |
| 7 | Project Configurator | Todo | Not run | 2 |
| 8 | Dev Security Reviewer | Todo | Not run | 2 |
| 9 | Dev Backlog Steward | Todo | Not run | 3 |
| 10 | Dev Merge Coordinator | Todo | Not run | 3 |
| 11 | Dev Documentation Writer | Todo | Not run | 3 |
| 12 | Wiki Ingester | Todo | Not run | 3 |
| 13 | Wiki Writer | Todo | Not run | 4 |
| 14 | Wiki Query Responder | Todo | Not run | 4 |
| 15 | Dev Artifact Reviewer | Todo | Not run | 4 |
| 16 | Dev Prompt Reviewer | Todo | Not run | 4 |
| 17 | Dev UX Specialist | Todo | Not run | 5 |
| 18 | Dev Browser Operator | Todo | Not run | 5 |
| 19 | Project Organiser | Todo | Not run | 5 |
| 20 | Wiki Architect | Todo | Not run | 5 |
| 21 | Wiki Topic Verifier | Todo | Not run | 6 |
| 22 | Wiki Artifact Reviewer | Todo | Not run | 6 |
| 23 | Wiki Researcher | Todo | Not run | 6 |
| 24 | Wiki Source Collector | Todo | Not run | 6 |
| 25 | Methodology Maintainer | Todo | Not run | 7 |
| 26 | Methodology Artifact Reviewer | Todo | Not run | 7 |

The repository currently has twenty-six conceptual agent definitions: four defined suites and twenty-two remaining suite folders. Recheck the canonical role inventory before every batch so newly added, renamed, or retired agents are reflected without silently changing established priority IDs.

## 8. Tracking Protocol

This section defines how future work updates this file without overstating progress.

- **RULE: RULE-1** Update task status at task boundaries
  - **SYNOPSIS:** Set a task to in progress when implementation actually begins, then set it to done, blocked, or deferred only with evidence.
  - **BECAUSE:** A plan should distinguish intended work from active work and completed results.

- **RULE: RULE-2** Record timestamps and elapsed time prospectively
  - **SYNOPSIS:** Every started task records Started At in UTC. Every terminal task records Finished At and Actual Elapsed. Automated runs also record monotonic duration seconds.
  - **BECAUSE:** Historical elapsed time cannot be reconstructed reliably from commit times.

- **RULE: RULE-3** Keep implementation status separate from evaluation verdict
  - **SYNOPSIS:** Implementation uses todo, in progress, done, blocked, or deferred. Governed suite runs use PASS, FAIL, BLOCKED, or STALE.
  - **BECAUSE:** A completed test implementation can legitimately produce a FAIL, BLOCKED, or STALE evaluation result.

- **RULE: RULE-4** Require evidence for done
  - **SYNOPSIS:** A done task names changed artifacts, verification commands, result receipts when applicable, completion timestamp, and commit.
  - **BECAUSE:** Narrative completion without durable evidence is not recoverable program state.

- **RULE: RULE-5** Preserve the no-work-started boundary of this plan task
  - **SYNOPSIS:** Creating this plan does not authorize TASK-10 or any later task.
  - **BECAUSE:** The user requested visibility and tracking before continuing implementation.

Future task tracking fields:

| Field | Required when |
|---|---|
| Status | Always |
| Owner | In progress or terminal |
| Started At | In progress or terminal |
| Finished At | Terminal |
| Actual Elapsed | Terminal; unknown only for historical work |
| Evidence | Done, blocked, or deferred |
| Commit | Done repository mutation |
| Next Action | Todo, in progress, or blocked |

## 9. Definition Of Good

This section defines completion for the program rather than for one run.

- **REQUIREMENT: REQ-1** Every suite is derived from its canonical agent definition
  - **SYNOPSIS:** Suite behavior traces back to the complete current role contract.
  - **VALIDATES:** Responsibility, decisions, skills, dependencies, mutation rules, outputs, failure handling, and terminal outcomes are traceable into the suite.

- **REQUIREMENT: REQ-2** Every suite uses hardcoded project agents and project skills
  - **SYNOPSIS:** The execution identities and shared methods are explicit suite inputs.
  - **VALIDATES:** The suite has a fixed supervisor, read-only Judge, target agent, shared skills, suite-specific skill, and allowed dependency list.

- **REQUIREMENT: REQ-3** Every live result proves runtime identity and governed evidence
  - **SYNOPSIS:** Retained evidence establishes which definitions actually ran and what they did.
  - **VALIDATES:** Task labels, child paths, and polished prose cannot substitute for custom-agent and loaded-instruction evidence.

- **REQUIREMENT: REQ-4** Concurrency remains bounded
  - **SYNOPSIS:** The coordinator and supervisors enforce the declared active-agent ceilings.
  - **VALIDATES:** Four supervisors maximum, one active child per supervisor, nine normal active agents, and one narrowly allowed temporary tenth agent.

- **REQUIREMENT: REQ-5** Test cost stays proportional to end-user value
  - **SYNOPSIS:** Scenario selection favors costly failures in end-user workflows over catalog-size coverage.
  - **VALIDATES:** Suites retain a compact success, boundary, and dependency or recovery set without creating one test per skill or technology.

- **REQUIREMENT: REQ-6** Results are measurable and maintainable
  - **SYNOPSIS:** Durable records expose the information needed to compare, refresh, and diagnose runs.
  - **VALIDATES:** Status, timing, cost, digests, cleanup, findings, and stale evidence are visible in durable records.

- **REQUIREMENT: REQ-7** Repository verification passes
  - **SYNOPSIS:** Each implementation batch closes with the repository's applicable deterministic checks.
  - **VALIDATES:** Relevant catalog validation, bundle regression tests, generated checks, and Git diff hygiene pass for every implementation batch.

## 10. Next Authorized Decision

- **TASK: NEXT-1** Review and approve or reorder the plan
  - **STATUS:** waiting for user direction
  - **SYNOPSIS:** The next implementation action would begin with TASK-10 only after explicit authorization.
  - **BECAUSE:** No remaining test-suite work should start as part of this planning request.
