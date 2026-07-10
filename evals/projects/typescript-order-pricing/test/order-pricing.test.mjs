import assert from "node:assert/strict";
import test from "node:test";

import { quoteOrder } from "../dist/order-pricing.js";

test("quotes the subtotal for valid order lines", () => {
  assert.deepEqual(
    quoteOrder([
      { quantity: 2, unitPriceCents: 250 },
      { quantity: 1, unitPriceCents: 125 },
    ]),
    { subtotalCents: 625, totalCents: 625 },
  );
});

test("quotes an empty order as zero", () => {
  assert.deepEqual(quoteOrder([]), { subtotalCents: 0, totalCents: 0 });
});
