# Project Taxonomy

## Conventions

Filenames use lowercase kebab-case. Generated files must not be stored with hand-maintained source.

## Categories

### docs/operations/runbooks

- Purpose: Operational procedures for deployment and recovery.
- Signals: Human-maintained steps used by operators.
- Filename pattern: descriptive-name.md

### generated/client

- Purpose: Deterministic generated client source.
- Signals: Recreated by the client generator.
- Filename pattern: generator-owned

### test/fixtures

- Purpose: Stable synthetic inputs used by automated tests.
- Signals: Test-owned data that is not production output.
- Filename pattern: descriptive-name.ext

## Change Log

- 2026-07-01: Added operations runbooks for deployment procedures.
