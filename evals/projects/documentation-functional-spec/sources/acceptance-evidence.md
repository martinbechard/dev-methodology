# Acceptance Evidence

- Customer cancellation succeeds for an owned Pending order and records the customer as initiator.
- Customer cancellation is denied for another customer's order.
- Service-agent cancellation requires a reason code and records the service agent as initiator.
- Cancellation reason lookup filters service-only reasons from customer responses.
- Cancellation of a Shipped order returns 409 and leaves the state unchanged.
- Reading an unknown order and cancelling an unknown order both return 404.
- The supplied evidence does not identify a notification, background job, or external message emitted after cancellation.
