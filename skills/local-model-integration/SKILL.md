---
type: Skill
name: local-model-integration
description: Use when coding, reviewing, or testing local model integration, model downloads, MLX serving, cache paths, runtime startup, resource limits, logs, or local versus remote model routing.
---

# Local Model Integration

Use this application-domain pack for product code that manages local model files, local inference servers, runtime selection, and model routing.

## Routing

- Load with Coding Agent for model registry, download, cache, server lifecycle, local runtime configuration, and model selection changes.
- Load Runtime Diagnostician only for long-running setup failures, logs, resource exhaustion, or exclusive local runtime resources.
- Combine with Electron Main or Node CLI when local runtime control happens from desktop or command line code.

## Guidance

- Keep model metadata, downloaded artifacts, runtime state, and user-visible status distinct.
- Make interrupted downloads, resume behavior, and cache paths inspectable.
- Treat local resource failures as operational states with clear logs.
- Keep local and remote model routing explicit.

## Verification

- Run focused tests for model selection, download state, runtime paths, and error mapping.
- Smoke-test local runtime setup when resources are available.
- Report resource-blocked checks without pretending they passed.
