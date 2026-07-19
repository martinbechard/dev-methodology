# Conflicting Public Contract Fixture

This synthetic project has an accepted percentage-discount interface and a request that asks for a fixed-amount discount under the same field name. The accepted contract explicitly excludes fixed amounts. The requested implementation therefore requires a public-contract decision before source mutation.

Run the accepted-contract checks:

```bash
python3 -m unittest test_pricing.py
```

The correct initial outcome is a clean test pass with no implementation change.
