# TypeScript Order Pricing Evaluation

Add an asynchronous coupon boundary to the order-pricing module.

Use the configured direct-main Commit workflow. Complete and commit the verified local change
without publishing a branch or pull request.

Requirements:

- Accept an optional coupon code as unknown external input.
- Validate and normalize a non-empty string before calling the coupon dependency.
- Ask a supplied asynchronous coupon lookup for a numeric percentage from zero through one hundred inclusive, including fractional values such as 12.5.
- Accept zero and one hundred percent boundary results, and reject out-of-range and non-finite dependency results.
- Apply the percentage to the subtotal without allowing a negative total.
- Keep public subtotal and total values in integer cents, and round the final discounted total to the nearest cent with half-cent results rounded up. The internal representation must not narrow the accepted percentage domain.
- Propagate coupon dependency failures to the caller.
- Add focused tests for no coupon, an in-range 12.5 percent coupon, zero and one hundred percent boundaries, invalid coupon input, out-of-range and non-finite dependency output, cent rounding, and dependency failure.
- Use the existing test framework and do not add a logger, tracing API, or mocking framework.
- Run the build and tests.

Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections. Include TS-BOUNDARY, TS-CONTRACT, TS-ASYNC, TS-TESTS, and REVIEW-SYNTHESIS evidence identifiers.
