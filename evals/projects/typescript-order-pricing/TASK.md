# TypeScript Order Pricing Evaluation

Add an asynchronous coupon boundary to the order-pricing module.

Requirements:

- Accept an optional coupon code as unknown external input.
- Validate and normalize a non-empty string before calling the coupon dependency.
- Ask a supplied asynchronous coupon lookup for a percentage from zero through one hundred.
- Reject invalid dependency results.
- Apply the percentage to the subtotal without allowing a negative total.
- Preserve exact cents using integer arithmetic and document the rounding rule through tests.
- Add focused tests for no coupon, valid coupon, invalid input, invalid dependency output, and dependency failure.
- Use the existing test framework and do not add a logger, tracing API, or mocking framework.
- Run the build and tests.

Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections. Include TS-BOUNDARY, TS-CONTRACT, TS-ASYNC, TS-TESTS, and REVIEW-SYNTHESIS evidence identifiers.
