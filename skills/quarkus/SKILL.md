---
name: quarkus
description: Implement, refactor, diagnose, or review Quarkus applications using version-aware rules for Arc CDI, configuration, REST execution, transactions, security, observability, build-time behavior, and native executables.
metadata:
  category: stack-and-domain
---

# Quarkus

Combine with Quarkus Design when the task chooses application boundaries, execution models, transaction ownership, extension strategy, or deployment form. Load Quarkus Persistence and Quarkus Testing when their concern-specific evidence applies.

## Framework Baseline

- Read the owning build for the Quarkus platform, Java release, extensions, REST stack, persistence stack, test support, and packaging targets before selecting APIs.
- Distinguish build-time-fixed configuration from runtime-overridable configuration. A runtime override cannot change behavior already fixed during augmentation.
- Identify whether each affected path is blocking, reactive, or virtual-thread based and keep blocking work off event-loop threads.

## Coding Guidance

- Use Arc CDI scopes and interception deliberately. Prefer constructor injection or package-private injection points when reflection-free native execution matters.
- Bind related configuration through the established typed configuration model, validate required settings, and keep secrets outside source and diagnostic output.
- Validate transport input, preserve the established error contract, and keep request, messaging, scheduling, and persistence execution models compatible.
- Define transaction boundaries on intercepted CDI methods and match blocking JTA or reactive transaction behavior to the selected persistence stack.
- Preserve Quarkus security, health, metrics, tracing, and logging facilities instead of replacing extension-provided behavior without evidence.
- Verify JVM startup and the packaged deployment form; add native build and integration evidence when reflection, resources, proxies, serialization, or native delivery is material.

Read [Quarkus Coding Guidelines](references/coding-guidelines-quarkus.md) when implementation or review needs detailed framework rules.

## Review Evidence

Read references/review-checklist-quarkus.md during code review. Use Code Review Evidence to extract and synthesize the results. Combine with Java and Application Security when applicable.
