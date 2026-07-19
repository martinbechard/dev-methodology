# Inventory Normalization Fixture

This synthetic repository contains one implemented module and one success-path unit test. It intentionally has no module design.

The implementation also rejects a blank normalized location with ValueError. That branch is visible in source but has no automated test. Documentation must preserve that distinction.

The accepted source-test command is:

```bash
python3 -m unittest discover -s tests
```

Final fixture validation compares the produced module design with the canonical module design template supplied to the validator.
