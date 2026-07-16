# Add Retry Policy

Status: Claimed

Type: Feature

## Summary

Add bounded retries for transient delivery failures.

## Context

The runner claim identifies eval-run-17. The durable result record is missing.

## Requirements

- Retry transient failures at most twice.
- Do not retry permanent validation failures.
- Record the terminal delivery outcome.

## Acceptance Criteria

- Focused tests cover transient success, retry exhaustion, and permanent failure.
- The delivery result identifies the committed change and verification outcome.

## Dependencies

None.

## Verification

Run the focused delivery tests and record their exit status.
