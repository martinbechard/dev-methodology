# Order Cancellation Source Report

## Current Behavior

An authenticated customer can cancel an owned order in Pending or Confirmed state. A service agent can cancel on behalf of a customer. Both paths require a valid reason code. Shipped and already-cancelled orders return a conflict and remain unchanged.

## Reason Visibility

Cancellation reasons have customer-visible and service-only visibility. The customer lookup excludes service-only reasons; the service-agent lookup includes both groups.

## Audit Event

A successful cancellation records an OrderCancelled audit event containing the order identifier, reason code, initiating actor type, and initiator identifier. The source does not establish an external notification or background job.

## Provenance

This synthetic report is the authoritative source artifact for the evaluation fixture.
