---
name: mysql
description: Use when implementing, reviewing, testing, or diagnosing MySQL and InnoDB schemas, queries, transactions, indexes, locking, migrations, or production database behavior.
metadata:
  category: stack-and-domain
---

# MySQL

Combine with SQL and the applicable migration, framework, ORM, and testing skills. SQL owns vendor-neutral query correctness, parameterization, transaction ownership, constraints, and migration discipline. This skill owns MySQL and InnoDB consequences.

## Engine And Schema

- Confirm the deployed MySQL version, table storage engines, row formats, server SQL mode, and effective defaults before relying on engine behavior.
- Define an explicit, stable primary key for each InnoDB table. Account for the clustered key's effect on row locality and for primary-key columns stored in every secondary-index record; wide or mutable primary keys multiply storage and write cost.
- Choose secondary indexes from representative predicates, joins, ordering, grouping, and covering needs. Account for leftmost-prefix use, selectivity, clustered-key lookups, write amplification, and redundant indexes.
- Select character sets and collations from required Unicode coverage, equality, ordering, case and accent sensitivity, and cross-service compatibility. Keep related join and foreign-key columns compatible, and treat charset conversion as a data migration that can rebuild the table or change values.
- Align foreign-key column type, size, signedness, character set, collation, and leading index order. Make referential actions explicit and verify the indexes MySQL creates or reuses for enforcement.

## Transactions And Locking

- Verify the effective isolation level instead of assuming a deployment default. Distinguish consistent nonlocking reads from locking reads and current reads when reasoning about one transaction.
- Reason about locks from the indexes and ranges the statement scans, not only from rows ultimately returned. Under InnoDB, range access can acquire record, gap, or next-key locks, while a unique lookup can have a narrower lock footprint.
- Keep write transactions short, access shared tables and rows in a consistent order, and index locking predicates so they do not scan and lock unnecessary ranges.
- InnoDB rolls back a deadlock victim's transaction. A lock-wait timeout normally rolls back only the failed statement unless innodb_rollback_on_timeout is enabled; inspect the effective setting and explicitly roll back any still-active transaction before retrying the complete transaction. Retry only when the unit is safely repeatable, use bounded backoff, and preserve the original failure when retries are exhausted.
- Diagnose contention with transaction, lock, and lock-wait evidence from Performance Schema and InnoDB status together with the exact statements and transaction boundaries.

## Query Plans

- Capture EXPLAIN evidence with representative data and bound values before and after a consequential query or index change. Compare access method, chosen key, key parts, estimated rows, filters, join order, temporary work, sorting, and partition pruning where applicable.
- Use EXPLAIN ANALYZE only in a controlled environment where executing the statement and its workload is safe. Compare estimated and actual rows, loops, and timing rather than treating optimizer cost as elapsed time.
- Refresh or investigate table statistics when estimates are stale, but do not force an index or optimizer switch until measured evidence shows that the alternative is stable for relevant data distributions.

## DDL And Migrations

- Check the exact MySQL version and table characteristics for each ALTER operation. State an algorithm and lock clause when silent fallback to a table copy, rebuild, or stronger lock is unacceptable.
- Treat atomic DDL as crash-safe statement execution, not transactional DDL. Account for implicit commits, metadata-lock acquisition, long-running transactions, temporary space, redo and binary-log volume, and replica apply time.
- Plan foreign-key changes across both parent and child tables. Keep foreign-key checks enabled in ordinary operation; when a controlled migration disables them, validate existing data explicitly because re-enabling checks does not scan rows created while checks were disabled.
- Prefer expand-and-contract changes when application versions overlap. Define cancellation, retry, rollback or forward recovery, and the observation point that proves the migration completed safely.

## Production Verification

- Record server version, storage engines, table definitions, isolation, SQL mode, character-set and collation settings, and relevant binary-log or replication configuration from the target environment.
- Run representative correctness, concurrency, and plan checks against the production engine. Verify deadlock retry, constraint failure, connection charset, migration locking, and recovery behavior at the narrowest useful integration boundary.
- For replicated deployments, account for statement volume, replica lag, schema compatibility during rolling rollout, and read-after-write expectations. Verify every materially different topology rather than inferring replica behavior from a standalone instance.
- Report the statements and data shape tested, observed plans and locks, migration algorithm and lock behavior, server variables relied on, replica evidence, and remaining operational risk.

## Version Authority

Ground version-sensitive decisions in the [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/) and verify the corresponding official manual for the deployed server version before implementation or rollout.
