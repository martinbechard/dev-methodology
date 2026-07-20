# Quarkus Persistence Review Checklist

- Question: Is the blocking Hibernate ORM or Hibernate Reactive stack identified and used consistently?
- Question: Has stack-specific entity, repository, query, and transaction work been routed to the pertinent companion skill selected from owning evidence?
- Question: Are datasources, entity packages, persistence units, mappings, dialect settings, and constraints aligned with the migration-owned schema?
- Question: Are blocking and reactive execution and transaction models kept distinct throughout each workflow?
- Question: Is the migration system the production schema authority, with destructive automatic schema generation excluded from production?
- Question: Do tests use sufficient database and packaged-runtime fidelity to prove shared mappings, migrations, transaction boundaries, and database-specific behavior?
