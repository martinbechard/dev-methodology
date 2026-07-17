# Agent Suite Rollout Plan

This is the ongoing tracker for creating and executing one behavioral test suite per conceptual agent. No remaining step is active until explicitly started.

## Goal

- **GOAL: GOAL-1** Complete the agent-owned evaluation catalog in end-user value order
  - **SYNOPSIS:** Each conceptual agent receives a compact suite derived from its canonical definition, with hardcoded project agents, project skills, scenarios, evidence, and independent judging.
  - **STATUS:** 4 of 26 suites partially complete; 22 not started.

## How To Complete One Agent Step

Every numbered agent step follows the same procedure.

1. Read the canonical role and generated adapter.
2. Create or refresh the agent folder with suite.yaml, scenarios.yaml, agents/supervisor.toml, agents/judge.toml, and one suite-specific skill.
3. Define a compact scenario set covering representative success, a material boundary, and a dependency or recovery path when the role has one.
4. Reuse an existing synthetic fixture where possible; add one only when current fixtures cannot expose the behavior.
5. Add deterministic gates and structural regression coverage.
6. Run the scenarios through the hardcoded supervisor, target agent, and independent Judge.
7. Record verdicts, timing, evidence, cleanup, and commit, then mark the step done.

A suite is done only when its initial scenarios are executable and have governed results. A suite scaffold or one representative PASS is partial progress.

## Tracking Rules

- Status values are todo, in progress, partial, done, blocked, or deferred.
- When work starts, record Owner and Started At in UTC.
- When work ends, record Finished At, Actual Elapsed, Evidence, and Commit.
- Historical elapsed time stays unknown when no start time was recorded.
- Up to four supervisor steps in the same batch may run concurrently.
- Each supervisor uses exactly one child at a time. The normal ceiling is nine active agents; one declared nested dependency may temporarily raise it to ten.
- Complete the current batch and its review gate before starting the next batch.

## Completed Foundation

- [x] Common protocol and agent-first strategy — commit ad8c45f051aa46db86731422af5eb35f7293ba63.
- [x] Shared supervision, scenario-design, and evidence-judging skills — commit ad8c45f051aa46db86731422af5eb35f7293ba63.
- [x] Codex identity hardening and representative first-batch runs — commit efe7bb773f2db7730629113808f0b80c33c89383.
- [x] First review corrections and structural regression coverage — commit 2bf41a7e0584d6c3443139cd996599ee984a02c5.
- [x] Retained first-batch result — evals/agent-tests/results/2026-07-17-codex-agent-suites.md.

Historical elapsed time for this foundation is unknown. Git timestamps are completion checkpoints, not active-work duration.

## Batch 1: Finish Existing Suites

These suites have definitions and one representative PASS each, but their initial scenario sets are not complete.

- [ ] **TASK: STEP-01** Dev Coder
  - **STATUS:** partial
  - **REMAINING:** Execute the Spring scenario and implement the blocked-authority scenario.
  - **EVIDENCE:** TypeScript representative PASS in the retained first-batch result.

- [ ] **TASK: STEP-02** Dev Code Reviewer
  - **STATUS:** partial
  - **REMAINING:** Implement and execute the justified-clean-review and incomplete-review-evidence scenarios.
  - **EVIDENCE:** Seeded TypeScript defects representative PASS in the retained first-batch result.

- [ ] **TASK: STEP-03** Dev Runtime Diagnostician
  - **STATUS:** partial
  - **REMAINING:** Implement and execute the retained-process-port and worker-stall scenarios.
  - **EVIDENCE:** Unavailable runtime dependency representative PASS in the retained first-batch result.

- [ ] **TASK: STEP-04** Project Bootstrapper
  - **STATUS:** partial
  - **REMAINING:** Formalize executable fixtures and governed results for all three catalog scenarios.
  - **EVIDENCE:** Valid-configuration representative PASS in the retained first-batch result.

## Gate A: Repeatable Execution

Complete this gate before Batch 2.

- [ ] **TASK: GATE-A** Make suite execution repeatable and measurable
  - **STATUS:** todo
  - **OUTCOME:** The evaluation runner accepts suite and scenario inputs, schedules at most four supervisors, enforces child limits, and records UTC timestamps plus monotonic elapsed seconds.
  - **VALIDATES:** One-suite execution, four-suite execution, fifth-supervisor queuing, the temporary tenth-agent exception, cleanup, and partial-batch failure retention.

## Batch 2: Core Delivery Control

- [ ] **TASK: STEP-05** Dev Verifier — cover final acceptance, failed verification, and incomplete evidence.
- [ ] **TASK: STEP-06** Dev Orchestrator — cover dependency routing, bounded delegation, and terminal status.
- [ ] **TASK: STEP-07** Project Configurator — cover valid reuse, technology routing, and invalid configuration.
- [ ] **TASK: STEP-08** Dev Security Reviewer — cover material findings, justified clean review, and missing authority.

## Batch 3: Work Completion And Durable Knowledge

- [ ] **TASK: STEP-09** Dev Backlog Steward — cover creation and claim, recovery, and blocked state transitions.
- [ ] **TASK: STEP-10** Dev Merge Coordinator — cover clean integration, conflict handling, and incomplete contribution evidence.
- [ ] **TASK: STEP-11** Dev Documentation Writer — cover routed authoring, source gaps, and verification correction.
- [ ] **TASK: STEP-12** Wiki Ingester — cover raw ingest, destination collision, and verifier failure.

## Batch 4: Knowledge And Contract Review

- [ ] **TASK: STEP-13** Wiki Writer — cover durable topic creation, maintenance, and insufficient sources.
- [ ] **TASK: STEP-14** Wiki Query Responder — cover supported answers, source conflict, and durable knowledge gaps.
- [ ] **TASK: STEP-15** Dev Artifact Reviewer — cover accepted artifacts, findings, and missing review authority.
- [ ] **TASK: STEP-16** Dev Prompt Reviewer — cover prompt defects, justified acceptance, and unverifiable contracts.

## Batch 5: Interactive And Structural Work

- [ ] **TASK: STEP-17** Dev UX Specialist — cover interaction quality, accessibility findings, and missing runtime evidence.
- [ ] **TASK: STEP-18** Dev Browser Operator — cover successful workflow, boundary failure, and owned cleanup.
- [ ] **TASK: STEP-19** Project Organiser — cover known placement, taxonomy extension, and ambiguous ownership.
- [ ] **TASK: STEP-20** Wiki Architect — cover initialization, restructuring, and unsafe boundary changes.

## Batch 6: Wiki Verification And Sources

- [ ] **TASK: STEP-21** Wiki Topic Verifier — cover accepted topic, correction findings, and stale source evidence.
- [ ] **TASK: STEP-22** Wiki Artifact Reviewer — cover accepted wiki artifact, structural findings, and missing authority.
- [ ] **TASK: STEP-23** Wiki Researcher — cover bounded research, excluded sources, and unresolved evidence gaps.
- [ ] **TASK: STEP-24** Wiki Source Collector — cover approved collection, exclusions, and blocked repository writes.

## Batch 7: Methodology Maintenance

- [ ] **TASK: STEP-25** Methodology Maintainer — cover coherent catalog change, generated drift, and blocked maintenance scope.
- [ ] **TASK: STEP-26** Methodology Artifact Reviewer — cover accepted change, catalog drift findings, and incomplete verification.

## Batch Closeout

After every batch:

1. Update each step status and timing fields.
2. Link the governed result and commit.
3. Run applicable catalog, bundle, generated-output, and Git hygiene checks.
4. Recheck canonical role inventory and suite priority.
5. Record defects through the configured backlog without fixing the subject under test from inside a governed run.
6. Start the next batch only after the current batch evidence is reviewed.

## Next Step

- **TASK: NEXT-1** Finish Batch 1
  - **STATUS:** waiting for authorization
  - **SYNOPSIS:** Start STEP-01 through STEP-04, with at most four supervisors, when implementation is explicitly authorized.
