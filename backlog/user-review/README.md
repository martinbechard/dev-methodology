# User Review Queue

## Purpose

This directory contains backlog work whose next safe step requires a decision, approval, authority grant, value judgment, or information that belongs to the user.

Items here are visible but not dispatchable. An agent reading this queue asks the exact recorded question and does not claim or implement the underlying work until the user answers.

## Item Contract

Each item keeps its underlying work Type and uses Status: User Review. It contains the normal backlog sections plus:

- User Review Required.
- Question for the User.
- Why User Input Is Required.
- Options and Tradeoffs when choices are known.
- Resolution, initially Pending.
- Unattended Work Boundary.

## Lifecycle

- An approved or answered item moves to its typed active backlog folder with the user decision preserved as authority evidence.
- A deferred item moves to backlog/holding.
- A rejected or abandoned item moves to the matching failed-backlog type when the user clearly ends the work.
- A partially answered item stays here with a narrower question.

README.md is queue guidance and is not a backlog item.

## Boundary

Ordinary technical dependencies, missing tools, implementation failures, and synthetic evaluation boundaries do not belong here when an agent can investigate or correct them without inventing user authority.
