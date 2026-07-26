# User Action Required Queue

## Purpose

This directory contains backlog work whose next safe step requires a decision, approval, authority grant, value judgment, or information that belongs to the user.

Items here are visible but not dispatchable. An agent reading this queue asks the exact recorded question and does not claim or implement the underlying work until the user answers.

The Coordinator selects this state and the provider records it before the responsible agent presents the request. The request starts with one plain-language question. It explains why the user owns the answer, gives evidence-backed options or an illustrative example when helpful, states each practical consequence, and names exactly what unattended work stops.

Example:

> Do you approve publishing this accepted release to production? Production publication requires your authority. Approve means the release is published; defer means production remains unchanged. No publication may run while this question is pending, but read-only release-note review may continue.

## Item Contract

Each item keeps its underlying work Type and uses Status: User Action Required. It contains the normal backlog sections plus:

- User Action Required.
- Question for the User.
- Why User Input Is Required.
- Options and Tradeoffs when choices are known.
- Resolution, initially Pending.
- Unattended Work Boundary.

## Lifecycle

- An approved or answered item moves to its typed active backlog folder with Status: Ready and the user decision preserved as authority evidence before any separate claim or Running transition.
- A deferred item moves to backlog/holding.
- A rejected or abandoned item moves to the matching failed-backlog type when the user clearly ends the work.
- A partially answered item stays here with a narrower question.

README.md is queue guidance and is not a backlog item.

## Boundary

Ordinary technical dependencies, missing tools, implementation failures, and synthetic evaluation boundaries do not belong here when an agent can investigate or correct them without inventing user authority.
