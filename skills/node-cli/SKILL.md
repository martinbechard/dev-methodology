---
name: node-cli
description: Use when coding, reviewing, or testing Node.js command line interfaces, scripts, process arguments, filesystem operations, exit codes, logging, or local automation.
---

# Node CLI

Use this pack for local command line entrypoints and scripts that need predictable process behavior.

## Routing

- Load with Coding Agent for CLI entrypoints, command arguments, filesystem reads and writes, environment variables, and process exits.
- Load with Code Review Agent when scripts can modify files, spawn processes, or affect developer workflow.
- Combine with TypeScript ESM, project organizer, and test framework packs.

## Guidance

- Keep argument parsing explicit and report invalid input clearly.
- Use deterministic exit codes for success, user error, and execution failure.
- Avoid hidden writes and make dry-run behavior clear when available.
- Do not send private repository data to external services unless the caller explicitly authorizes it.

## Verification

- Run focused CLI tests or representative commands.
- Check failure behavior, not only the happy path.
- Run the project build after CLI import or packaging changes.
