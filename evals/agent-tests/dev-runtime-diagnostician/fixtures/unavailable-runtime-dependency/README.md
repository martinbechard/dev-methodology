# Synthetic Runtime Dependency Fixture

This disposable fixture represents an application with a healthy local boundary and a configured storage health endpoint. The test command verifies the local boundary. The application command attempts the configured storage request and emits its observed outcome.

Run the local test:

```bash
python3 -m unittest test_app.py
```

Run the application boundary:

```bash
python3 app.py
```
