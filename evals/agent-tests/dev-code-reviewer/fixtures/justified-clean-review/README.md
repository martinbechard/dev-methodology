# Justified Clean Review Fixture

This synthetic read-only change implements a bounded retry-delay contract. The source has focused success and failure tests and no seeded defect. Reviewers should use the same evidence process as a defect-bearing review and return no actionable findings when the evidence supports that result.

Run the fixture checks:

```bash
python3 -m unittest test_retry_policy.py
```
