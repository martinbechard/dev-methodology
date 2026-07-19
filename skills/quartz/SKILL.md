---
name: quartz
description: Use when implementing, reviewing, testing, or diagnosing Quartz Scheduler jobs, triggers, calendars, persistence, clustering, recovery, or scheduler lifecycle behavior.
metadata:
  category: stack-and-domain
---

# Quartz Scheduler

Combine with Java and with SQL when JDBC job storage, schema ownership, locking, or database operations are in scope. Apply the applicable testing guidance when scheduler behavior changes. Apply Application Security when scheduler controls are remotely exposed, job inputs are untrusted, JobDataMap data is sensitive, or protected side effects are involved. Apply Spring Boot or Quarkus guidance only when the owning application uses that integration; this skill owns Quartz behavior rather than framework configuration conventions.

## Job And Schedule Contracts

- Give each JobDetail and Trigger a stable JobKey or TriggerKey and define who creates, replaces, pauses, resumes, unschedules, and deletes it. Preserve durable-job and orphan-trigger behavior intentionally.
- Keep work inputs in JobDataMap small and compatibility-safe. Prefer primitive values and strings for durable stores, consume the merged execution-context map when trigger values should override job values, and treat stored key or type changes as persisted-data migrations.
- Choose SimpleTrigger, CronTrigger, and registered calendars from the required time semantics. Record the cron expression, timezone, start and end bounds, exclusions, and daylight-saving behavior; test real transition dates when a local wall-clock schedule matters.
- Select an explicit misfire instruction for every consequential trigger. Verify the chosen fire-now, skip, reschedule, or ignore behavior against the deployed Quartz version and account for backlog bursts after downtime.

## Execution And Side Effects

- Decide concurrency per JobKey. Use DisallowConcurrentExecution only when executions for the same JobDetail must not overlap, and do not infer exclusion across different JobKeys or external workers.
- Treat trigger acquisition, retries, scheduler failover, recovery requests, manual refires, and process failure as sources of duplicate or partial execution. Quartz scheduling does not make external side effects exactly once.
- Assign ownership for retry count, delay, backoff, terminal failure, and operator replay. Make side effects idempotent with durable operation keys, state transitions, constraints, or equivalent application-owned evidence.
- Use JobExecutionException refire or unschedule controls only from a bounded, documented failure policy. Preserve interruption and cancellation semantics for long-running work and keep listeners concise so they do not stall scheduler threads.
- Combine PersistJobDataAfterExecution with DisallowConcurrentExecution when mutable job data is persisted across executions. Prefer an application-owned durable state model when correctness depends on more than small scheduler metadata.

## Storage, Clustering, And Recovery

- Choose RAMJobStore only when losing schedules and execution state on process exit is acceptable. For JDBCJobStore, select JobStoreTX or JobStoreCMT from transaction ownership and use the official schema for the exact Quartz and database version.
- Never write Quartz scheduling rows directly. Treat table prefix, delegate, datasource, connection capacity, transaction isolation, lock behavior, schema migration, backup, and restore as one database operational contract.
- Enable clustering only for scheduler instances that share the same JDBC job store and scheduler identity. Require unique instance identifiers, synchronized clocks, compatible configuration and code, database availability, and observed check-in and failover behavior.
- Set request-recovery only for jobs that can distinguish recovery execution and safely repeat after an interrupted node. Define which in-flight work is recovered, which ordinary failures are retried elsewhere, and how duplicate or partially completed side effects are reconciled.
- Size and verify the misfire threshold, cluster check-in interval, batch acquisition, worker threads, and datasource pool from measured workload and failure-recovery objectives rather than copying defaults.

## Lifecycle And Verification

- Make scheduler construction, registration, start, standby, graceful shutdown, and application termination ownership explicit. Decide whether shutdown waits for running jobs and prove that redeploy does not duplicate registration or abandon required work.
- Observe scheduler, trigger, and job identity; scheduled, actual, previous, and next fire times; misfires; execution duration and outcome; refires; recovery mode; queue depth; thread-pool saturation; datastore latency; and cluster membership without logging secrets or sensitive JobDataMap values.
- Test job and trigger identity, calendar and timezone calculations, selected misfire behavior, same-key concurrency, duplicate delivery, retry exhaustion, partial failure, restart persistence, recovery, and shutdown at the narrowest real scheduler boundary.
- For JDBC clustering, use the production database engine and at least two scheduler instances for failover and exclusion evidence. Record observed firings and persisted state rather than accepting configuration presence as proof.

## Version Authority

Ground version-sensitive behavior in the [Quartz documentation for the deployed release](https://www.quartz-scheduler.org/documentation/) and its matching API documentation. Confirm exact misfire instructions, configuration defaults, supported database delegate and schema, and integration compatibility before implementation or rollout.
