# Retry Policy Source Report

## Request Retry Eligibility

The order-support client retries only idempotent reads and order-status lookups after transient transport failures. It does not retry order creation, cancellation, or payment mutation requests.

## Attempt Limit

An eligible request has one initial attempt and at most two retry attempts. A successful response ends the sequence immediately.

## Backoff

The first retry waits 200 milliseconds and the second waits 500 milliseconds. This source establishes only the fixed delays. Whether deployment-specific jitter changes either delay remains unresolved because no authoritative deployment policy or implementation evidence is available.

## Failure Boundary

HTTP 429, 502, 503, and 504 responses are retryable for eligible requests. Other HTTP responses and validation failures return without retry. Exhaustion returns the last observed failure.

## Provenance

This synthetic report is the authoritative source artifact for the governed raw-ingest fixture.
