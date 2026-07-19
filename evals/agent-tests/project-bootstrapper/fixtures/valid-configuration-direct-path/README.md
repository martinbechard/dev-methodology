# Valid Configuration Direct Path Fixture

This synthetic project already has valid routing, accepted configuration review evidence, a green source test, and a coverage manifest. Only the mapped module document remains. The bootstrap workflow should reuse the configuration, produce one independently accepted contribution, skip merge coordination, and verify the final direct commit.

Check the initial state:

```bash
python3 validate_fixture.py initial
```

Check the completed state after the module document exists and its manifest status is accepted:

```bash
python3 validate_fixture.py final
```

Run the source test:

```bash
python3 -m unittest test_inventory.py
```
