# Missing Configuration Multi-Contribution Fixture

This synthetic project begins without PROJECT.yaml, AGENTS.md, documentation, or a wiki. It has two source responsibilities and green source tests. The bootstrap workflow must configure the project first, create independently reviewed non-wiki and wiki contributions, integrate the accepted commits in dependency order, repeat review after integration, and run final verification.

Inspect the initial state:

```bash
python3 validate_fixture.py initial
```

The initial command succeeds only when all intended setup artifacts are absent. Check the completed state after configuration and documentation work:

```bash
python3 validate_fixture.py final
```

Run the source tests:

```bash
python3 -m unittest discover -s tests
```
