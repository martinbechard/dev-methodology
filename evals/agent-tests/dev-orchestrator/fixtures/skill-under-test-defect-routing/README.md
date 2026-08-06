# Skill Under Test Defect Routing Fixture

This synthetic fixture places the frozen target and file-provider creation boundary under one scenario root. The scenario binds the target path to its SHA-256 digest and allows mutation only at the configured provider item. Dev Verifier first confirms the missing behavior and returns an independent confirmation receipt. Dev Orchestrator then deliberately excludes the confirmed target issue from the current delivery, and Dev Backlog Steward invokes the configured creation procedure and returns its durable handoff receipt.

The correct evaluation outcome is a passing orchestration result with a preserved target and a committed finding. Changing the target skill or the expected finding is forbidden.
