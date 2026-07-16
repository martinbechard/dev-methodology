# Order HTTP Contract

## Read Order

GET /orders/{orderId} returns the authenticated customer's order projection. A service agent can read the projection only through the service-agent authority described by the runtime identity context. The supplied evidence does not identify paging because this operation addresses one order.

## List Cancellation Reasons

GET /cancellation-reasons returns active reason codes and labels sorted by label. Customers receive only the customer-visible reasons. Service agents receive both customer-visible and service-only reasons.

## Cancel Order

POST /orders/{orderId}/cancel accepts a required reasonCode. Ownership is enforced for customers. Service-agent authority permits an on-behalf-of cancellation. Success returns status 200 with the updated order projection. An unknown order returns 404, an invalid or unauthorized reason returns 400 or 403 as applicable, and a non-cancellable state returns 409.
