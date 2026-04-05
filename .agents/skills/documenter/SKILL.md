---
name: documenter
description: Documentation skill for README, API docs, code comments, release docs, and AI-friendly project documentation.
---

# Documenter

This skill adds documentation-specific guidance.

## Priorities

- keep docs accurate, scannable, and current
- prefer examples over vague prose
- match README/docs to actual build, test, install, and release behavior
- keep Doxygen-facing docs API-focused and release-facing docs user-focused

## Core Workflow

1. Identify the audience: user, contributor, maintainer, or agent.
2. Read the current docs and the source of truth in code/build scripts.
3. Update only the sections affected by the change.
4. Keep structure compact: title, one-line purpose, quick start, key commands,
   important constraints.
5. If public headers change, update API comments immediately.

## README Rules

- answer what it is, how to build it, how to test it, and how to release it
- keep quick start runnable in minutes
- avoid stale feature claims and aspirational behavior presented as shipped

## Code Comment Rules

- comment why, contracts, and non-obvious behavior
- do not narrate obvious statements line by line
- keep public API comments complete enough for Doxygen/docs generation

## Project Docs Rules

- keep checklists actionable
- prefer concise tables and commands over long prose where possible
- keep agent-facing docs aligned with repo guidance and local skills
