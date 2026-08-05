# Skill Under Test Defect Routing Fixture

This synthetic fixture places the frozen target and file-provider finding boundary under one scenario root. The scenario binds the target path to its SHA-256 digest and allows mutation only at the configured provider item while Dev Backlog Steward records the defect and returns a durable handoff receipt.

The correct evaluation outcome is a passing orchestration result with a preserved target and a committed finding. Changing the target skill or the expected finding is forbidden.
