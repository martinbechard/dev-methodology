import assert from "node:assert/strict";
import test from "node:test";

import { quoteWithCoupon } from "../dist/coupon-pricing.js";

test("applies a valid coupon", async () => {
  const provider = {
    async find() {
      return { percent: 20 };
    },
  };

  assert.equal(await quoteWithCoupon(1_000, "SAVE20", provider), 800);
});

test("propagates a provider failure", async () => {
  const provider = {
    async find() {
      throw new Error("coupon service unavailable");
    },
  };

  await assert.rejects(
    quoteWithCoupon(1_000, "SAVE20", provider),
    /coupon service unavailable/,
  );
});

test("rejects a percentage outside the valid range", async () => {
  const provider = {
    async find() {
      return { percent: 150 };
    },
  };

  await assert.rejects(
    quoteWithCoupon(1_000, "BROKEN", provider),
    /percentage/i,
  );
});
