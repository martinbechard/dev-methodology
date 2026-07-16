# Order Cancellation Requirements

An authenticated customer can cancel an order that the same customer owns while the order is Pending or Confirmed. A service agent can cancel an order on behalf of a customer after supplying a reason code.

A successful cancellation changes the order state to Cancelled, records the selected reason and initiating actor, and returns the updated order projection. A Shipped or Cancelled order cannot be cancelled and returns a conflict response without changing the order.

The interface disables cancellation while an order is outside the cancellable states. If the cancellation request fails, the current order remains visible and the interface presents the returned problem message.
