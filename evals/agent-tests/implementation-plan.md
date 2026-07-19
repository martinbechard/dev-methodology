# Agent Suite Rollout Plan

This tracker records the completed rollout of one governed behavioral test suite per conceptual agent.

## Goal

- **GOAL: GOAL-1** Complete the agent-owned evaluation catalog in end-user value order
  - **STATUS:** done — 26 of 26 suites complete; 78 of 78 scenarios executed.
  - **OUTCOME:** Every conceptual agent has a compact executable suite derived from its canonical definition, with hardcoded project agents, project skills, deterministic gates, retained evidence, and independent judging or an explicitly proved critical skip.
  - **EVIDENCE:** [Complete agent-suite execution report](results/2026-07-17-complete-agent-suites.md).

## Completion Standard

A suite is done when all of its initial scenarios are executable and have a governed terminal checkpoint. A PASS is not required when the scenario is designed to exercise a blocked authority boundary or when the run exposes a reproducible target defect. Bounded infrastructure failures are corrected and rerun. Unsuitable test contracts are failed and backlogged instead of allowing an unbounded recovery, and target defects are preserved as results and recorded in the backlog.

## Completed Foundation

- [x] Common protocol and agent-first strategy — commit ad8c45f051aa46db86731422af5eb35f7293ba63.
- [x] Shared supervision, scenario-design, and evidence-judging skills — commit ad8c45f051aa46db86731422af5eb35f7293ba63.
- [x] Codex identity hardening and representative first-batch runs — commit efe7bb773f2db7730629113808f0b80c33c89383.
- [x] First review corrections and structural regression coverage — commit 2bf41a7e0584d6c3443139cd996599ee984a02c5.
- [x] Repeatable bounded runner with retained checkpoints, identity audits, concurrency audits, cleanup recovery, runtime preflights, and partial-batch evidence.
- [x] Complete suite catalog, fixtures, target agents, independent Judges, and suite-specific contracts.

## Completed Suites

| Priority | Suite | Scenarios | Status |
| ---: | --- | ---: | --- |
| 1 | Dev Coder | 3 | done |
| 2 | Dev Code Reviewer | 3 | done |
| 3 | Dev Runtime Diagnostician | 3 | done |
| 4 | Project Bootstrapper | 3 | done |
| 5 | Dev Verifier | 3 | done |
| 6 | Dev Orchestrator | 3 | done |
| 7 | Project Configurator | 3 | done |
| 8 | Dev Security Reviewer | 3 | done |
| 9 | Dev Backlog Steward | 3 | done |
| 10 | Dev Merge Coordinator | 3 | done |
| 11 | Dev Documentation Writer | 3 | done |
| 12 | Wiki Ingester | 3 | done |
| 13 | Wiki Writer | 3 | done |
| 14 | Wiki Query Responder | 3 | done |
| 15 | Dev Artifact Reviewer | 3 | done |
| 16 | Dev Prompt Reviewer | 3 | done |
| 17 | Dev UX Specialist | 3 | done |
| 18 | Dev Browser Operator | 3 | done |
| 19 | Project Organiser | 3 | done |
| 20 | Wiki Architect | 3 | done |
| 21 | Wiki Topic Verifier | 3 | done |
| 22 | Wiki Artifact Reviewer | 3 | done |
| 23 | Wiki Researcher | 3 | done |
| 24 | Wiki Source Collector | 3 | done |
| 25 | Methodology Maintainer | 3 | done |
| 26 | Methodology Artifact Reviewer | 3 | done |

## Repeatable Execution Gate

- [x] Suite and scenario selection.
- [x] At most four concurrent supervisors.
- [x] Exactly one active child per supervisor.
- [x] Serialized temporary nested-agent allowance.
- [x] Staged custom-agent identity and instruction-binding audit.
- [x] Ordered target tool-call and nested-dependency audit.
- [x] Runtime capability preflight for offline Node, offline Maven, loopback, process, and browser cases.
- [x] Partial checkpoint retention after coordinator or batch failure.
- [x] Owned fixture, worktree, process, browser, claim, and credential cleanup.
- [x] UTC completion timestamps and monotonic elapsed time in retained summaries.

## Closeout

- **OWNER:** root.
- **STARTED AT:** 2026-07-17T22:27:47Z.
- **FINISHED AT:** 2026-07-18T18:57:23Z.
- **ACTUAL ELAPSED:** Recorded per parallel batch and recovery run in the complete execution report; suite elapsed times overlap because up to four supervisors ran concurrently.
- **EVIDENCE:** [Complete agent-suite execution report](results/2026-07-17-complete-agent-suites.md).
- **BACKLOG:** Reproducible target and skill corrections were recorded under [Agent Skill Lifecycle](../../backlog/feature-backlog/agent-skill-lifecycle/index.md). No distributed skill was corrected from inside its governed evaluation.
- **COMMIT:** Recorded by the repository commit containing this completed tracker and report.

## Final State

The rollout is complete. Future work is ordinary suite maintenance: preserve the catalog-to-role mapping, add scenarios when behavior changes, keep infrastructure corrections separate from target findings, and execute the affected suites before shipping those changes.
